"""Tests for the unit-cell packing Z estimator."""
from pathlib import Path

import pytest

from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.z_from_packing import (
    _filter_disorder,
    _expand_to_unit_cell,
    _count_components,
    _get_components,
    _z_from_components,
    _build_bond_graph,
    _z_sg_from_symmops,
    count_z,
    count_z_and_zprime,
    ZResult,
)


# ---------------------------------------------------------------------------
# Unit tests for disorder filtering
# ---------------------------------------------------------------------------

class TestFilterDisorder:
    def _make_atom(self, disorder_group) -> list:
        """Create a minimal fake atom record with the given disorder_group."""
        return ['C1', 'C', 0.1, 0.2, 0.3, disorder_group, 1.0, 0.02]

    def test_ordered_atom_is_kept(self):
        atoms = [self._make_atom(0)]
        assert len(_filter_disorder(atoms)) == 1

    def test_first_positive_disorder_component_is_kept(self):
        atoms = [self._make_atom(1)]
        assert len(_filter_disorder(atoms)) == 1

    def test_first_negative_disorder_component_is_kept(self):
        atoms = [self._make_atom(-1)]
        assert len(_filter_disorder(atoms)) == 1

    def test_second_positive_component_is_dropped(self):
        atoms = [self._make_atom(2)]
        assert len(_filter_disorder(atoms)) == 0

    def test_second_negative_component_is_dropped(self):
        atoms = [self._make_atom(-2)]
        assert len(_filter_disorder(atoms)) == 0

    def test_higher_disorder_groups_are_dropped(self):
        atoms = [self._make_atom(g) for g in (3, -3, 4, -4)]
        assert len(_filter_disorder(atoms)) == 0

    def test_mixed_disorder_keeps_only_allowed(self):
        """A disordered site with groups 0, 1, 2 should yield groups 0 and 1 only."""
        atoms = [self._make_atom(g) for g in (0, 1, 2)]
        filtered = _filter_disorder(atoms)
        assert len(filtered) == 2
        retained_groups = [int(a[5]) for a in filtered]
        assert 0 in retained_groups
        assert 1 in retained_groups
        assert 2 not in retained_groups

    def test_occupancy_sum_rationale(self):
        """Confirm that keeping groups {0,1,-1} retains one representative per site
        when a 0.6/0.4 disorder is present (groups 1 and 2)."""
        site_a = self._make_atom(1)
        site_a[6] = 0.6  # occ
        site_b = self._make_atom(2)
        site_b[6] = 0.4  # occ — should be dropped
        ordered = self._make_atom(0)
        filtered = _filter_disorder([site_a, site_b, ordered])
        assert len(filtered) == 2


# ---------------------------------------------------------------------------
# Unit tests for BFS component counting
# ---------------------------------------------------------------------------

class TestCountComponents:
    def test_single_node(self):
        adj = {0: set()}
        assert _count_components(adj) == 1

    def test_two_connected_nodes(self):
        adj = {0: {1}, 1: {0}}
        assert _count_components(adj) == 1

    def test_two_disconnected_nodes(self):
        adj = {0: set(), 1: set()}
        assert _count_components(adj) == 2

    def test_three_components(self):
        adj = {0: {1}, 1: {0}, 2: {3}, 3: {2}, 4: set()}
        assert _count_components(adj) == 3

    def test_chain(self):
        adj = {0: {1}, 1: {0, 2}, 2: {1, 3}, 3: {2}}
        assert _count_components(adj) == 1


class TestZFromComponents:
    """Tests for the GCD-by-composition Z derivation."""

    def test_single_molecule(self):
        # One molecule = one component; GCD(1) = 1.
        assert _z_from_components([['C', 'H', 'O']]) == 1

    def test_two_copies_same_formula(self):
        # Z=2 structure: 2 components with identical composition.
        assert _z_from_components([['C', 'O'], ['C', 'O']]) == 2

    def test_salt_four_copies(self):
        # Tetracycline HCl: 4 organic + 4 Cl  →  GCD(4, 4) = 4.
        org = ['C'] * 22 + ['H'] * 25 + ['N'] * 2 + ['O'] * 8
        components = [org] * 4 + [['Cl']] * 4
        assert _z_from_components(components) == 4

    def test_cocrystal_two_species(self):
        # 1:1 co-crystal, Z=2: two copies of each species → GCD(2, 2) = 2.
        a = ['C', 'C', 'O']
        b = ['N', 'H']
        assert _z_from_components([a, a, b, b]) == 2

    def test_empty_returns_one(self):
        assert _z_from_components([]) == 1


# ---------------------------------------------------------------------------
# Integration tests against real CIF files
# ---------------------------------------------------------------------------

def _load(relative_path: str) -> CifContainer:
    return CifContainer(Path(relative_path))


class TestCountZRealStructures:
    def test_triclinic_z2_ml7(self):
        """DK_ML7-66 — P -1, Z=2, single organic molecule, no disorder."""
        cif = _load('test-data/DK_ML7-66-final.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 2

    def test_monoclinic_z2_sucrose(self):
        """DK_Zucker2 — P 1 21 1 (sucrose), Z=2, single molecule, no disorder."""
        cif = _load('test-data/DK_Zucker2_0m-finalcif.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 2

    def test_triclinic_z2_ntd106c(self):
        """ntd106c — P -1, Z=2, single neutral organic molecule."""
        cif = _load('test-data/ntd106c-P-1-final.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 2

    def test_twin_structure_z2(self):
        """twin1/DK_ML7-66 — P -1, Z=2 (same molecule, twin dataset)."""
        cif = _load('tests/examples/twin1/DK_ML7-66-final.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 2

    def test_multicomponent_salt_gives_correct_z(self):
        """multi.cif — tetracycline hydrochloride (P 21 21 21), Z=4.

        The Cl⁻ counter-ion is a discrete atom disconnected from the organic
        cation, giving 8 raw entities in the cell (4 cations + 4 anions).
        The GCD-by-composition step recognises that each species appears
        exactly 4 times and returns Z=4, matching the CIF value.
        """
        cif = _load('tests/examples/multi.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 4

    def test_salt_1000006_finalcif(self):
        """1000006-finalcif.cif — same tetracycline HCl in P 21 21 21, Z=4.

        Regression test: previously returned 8 (raw entity count) instead of
        the crystallographic Z=4.
        """
        cif = _load('test-data/1000006-finalcif.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 4

    def test_empty_atoms_returns_one(self):
        """With no atoms, a safe default of 1 is returned."""
        assert count_z([], ['x, y, z', '-x, -y, -z'], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0)) == 1

    def test_no_symmops_returns_one(self):
        """Without symmetry operations the function cannot expand the unit cell."""
        atoms = [['C1', 'C', 0.5, 0.5, 0.5, 0, 1.0, 0.02]]
        assert count_z(atoms, [], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0)) == 1


# ---------------------------------------------------------------------------
# Disorder filtering integrated with count_z
# ---------------------------------------------------------------------------

class TestCountZWithDisorder:
    """Synthetic tests that verify the disorder filtering does not inflate Z."""

    def _disordered_atoms(self) -> list:
        """Two C atoms with disorder groups 1 and 2 at the same site (split position).

        Only group 1 should survive _filter_disorder, so only one C enters the
        unit-cell expansion.  With P1 (one symmop), one atom → one component → Z=1.
        """
        return [
            ['C1A', 'C', 0.3, 0.3, 0.3, 1, 0.6, 0.02],  # kept
            ['C1B', 'C', 0.31, 0.31, 0.31, 2, 0.4, 0.02],  # dropped
        ]

    def test_disorder_does_not_inflate_z(self):
        symmops = ['x, y, z']  # P1
        cell = (10.0, 10.0, 10.0, 90.0, 90.0, 90.0)
        # Should give Z=1, not Z=2, thanks to disorder filtering.
        z = count_z(self._disordered_atoms(), symmops, cell)
        assert z == 1

    def test_two_molecules_disorder_still_correct(self):
        """Two clearly separated molecules (A and B) with one disordered site each.

        Only disorder group 1 atoms are kept, so we still get two molecules.
        Cell: 20 Å cube, P1.
        """
        # Molecule 1 around (0.1, 0.1, 0.1) - two bonded C atoms
        # Molecule 2 around (0.6, 0.6, 0.6) - two bonded C atoms
        # Each molecule has a disordered site (group 2 atom should be dropped)
        atoms = [
            ['C1A', 'C', 0.10, 0.10, 0.10, 1, 0.6, 0.02],  # mol 1, kept
            ['C1B', 'C', 0.11, 0.11, 0.11, 2, 0.4, 0.02],  # mol 1, dropped
            ['C2',  'C', 0.13, 0.10, 0.10, 0, 1.0, 0.02],  # mol 1, ordered, bonded to C1A
            ['C3A', 'C', 0.60, 0.60, 0.60, 1, 0.7, 0.02],  # mol 2, kept
            ['C3B', 'C', 0.61, 0.61, 0.61, 2, 0.3, 0.02],  # mol 2, dropped
            ['C4',  'C', 0.63, 0.60, 0.60, 0, 1.0, 0.02],  # mol 2, ordered, bonded to C3A
        ]
        symmops = ['x, y, z']
        cell = (20.0, 20.0, 20.0, 90.0, 90.0, 90.0)
        z = count_z(atoms, symmops, cell)
        assert z == 2


# ---------------------------------------------------------------------------
# Tests for Z' determination and ZResult
# ---------------------------------------------------------------------------

class TestZPrime:
    """Unit tests for ZResult attributes and count_z_and_zprime()."""

    def test_zresult_zprime_integer_is_high_confidence(self):
        """Z′ = 1 (Z=4, Z_sg=4) → high confidence."""
        r = ZResult(z=4, z_prime=1.0, z_sg=4)
        assert r.reliable is True
        assert r.confidence == 'high'

    def test_zresult_zprime_half_is_medium_confidence(self):
        """Z′ = 0.5 (molecule on special position) → medium confidence."""
        r = ZResult(z=2, z_prime=0.5, z_sg=4)
        assert r.reliable is True
        assert r.confidence == 'medium'

    def test_zresult_zprime_non_half_is_low_confidence(self):
        """Z′ = 0.25 → not a recognised fraction → low confidence."""
        r = ZResult(z=1, z_prime=0.25, z_sg=4)
        assert r.reliable is False
        assert r.confidence == 'low'

    def test_zresult_zprime_zero_is_unreliable(self):
        r = ZResult(z=0, z_prime=0.0, z_sg=4)
        assert r.reliable is False
        assert r.confidence == 'low'

    def test_zresult_zprime_large_integer_is_high(self):
        """Z′ = 4 is unusual but still a positive integer → high."""
        r = ZResult(z=16, z_prime=4.0, z_sg=4)
        assert r.reliable is True
        assert r.confidence == 'high'

    def test_zresult_zprime_exceeds_eight_is_low(self):
        """Z′ > 8 is physically unreasonable even if it is an integer."""
        r = ZResult(z=36, z_prime=9.0, z_sg=4)
        assert r.reliable is False
        assert r.confidence == 'low'

    def test_z_sg_from_symmops_p21c(self):
        """P 2₁/c has 4 general positions."""
        ops = ['x,y,z', '-x,y+1/2,-z+1/2', '-x,-y,-z', 'x,-y+1/2,z+1/2']
        assert _z_sg_from_symmops(ops) == 4

    def test_z_sg_from_symmops_p1(self):
        """P 1 has 1 general position."""
        assert _z_sg_from_symmops(['x,y,z']) == 1

    def test_z_sg_from_symmops_p212121(self):
        """P 2₁2₁2₁ has 4 general positions."""
        ops = ['x,y,z', '-x+1/2,-y,z+1/2', '-x,y+1/2,-z+1/2', 'x+1/2,-y+1/2,-z']
        assert _z_sg_from_symmops(ops) == 4

    def test_count_z_and_zprime_returns_zresult(self):
        """Return type is ZResult with the expected fields."""
        cif = _load('test-data/1000006-finalcif.cif')
        result = count_z_and_zprime(cif.atoms_fract, cif.symmops, cif.cell[:6])
        assert isinstance(result, ZResult)
        assert result.z == 4
        assert result.z_sg == 4
        assert abs(result.z_prime - 1.0) < 0.01
        assert result.confidence == 'high'

    def test_count_z_and_zprime_triclinic(self):
        """P -1 structure: Z=2, Z_sg=2 → Z′=1, high confidence."""
        cif = _load('test-data/DK_ML7-66-final.cif')
        result = count_z_and_zprime(cif.atoms_fract, cif.symmops, cif.cell[:6])
        assert result.z == 2
        assert result.z_sg == 2
        assert abs(result.z_prime - 1.0) < 0.01
        assert result.confidence == 'high'

    def test_count_z_and_zprime_no_symmops(self):
        """No symmops → Z=1, Z_sg=1, Z′=1."""
        atoms = [['C1', 'C', 0.5, 0.5, 0.5, 0, 1.0, 0.02]]
        result = count_z_and_zprime(atoms, [], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0))
        assert result.z == 1
        assert result.z_sg == 1
        assert abs(result.z_prime - 1.0) < 0.01



