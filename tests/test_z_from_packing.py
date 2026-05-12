"""Tests for the unit-cell packing Z estimator."""
from pathlib import Path

import gemmi as _g
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
    _normalize_element,
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
        assert _z_from_components([[('C', 1.0), ('H', 1.0), ('O', 1.0)]]) == 1

    def test_two_copies_same_formula(self):
        # Z=2 structure: 2 components with identical composition.
        assert _z_from_components([[('C', 1.0), ('O', 1.0)], [('C', 1.0), ('O', 1.0)]]) == 2

    def test_salt_four_copies(self):
        # Tetracycline HCl: 4 organic + 4 Cl  →  GCD(4, 4) = 4.
        org = [('C', 1.0)] * 22 + [('H', 1.0)] * 25 + [('N', 1.0)] * 2 + [('O', 1.0)] * 8
        components = [org] * 4 + [[('Cl', 1.0)]] * 4
        assert _z_from_components(components) == 4

    def test_cocrystal_two_species(self):
        # 1:1 co-crystal, Z=2: two copies of each species → GCD(2, 2) = 2.
        a = [('C', 1.0), ('C', 1.0), ('O', 1.0)]
        b = [('N', 1.0), ('H', 1.0)]
        assert _z_from_components([a, a, b, b]) == 2

    def test_empty_returns_one(self):
        assert _z_from_components([]) == 1

    def test_minor_partial_occ_component_excluded_from_gcd(self):
        """Two full-occ molecules + one minor partial-occ fragment → Z=2, not 1.

        This replicates the 1519506.cif scenario: a disordered solvent (dg=0,
        occ=0.5, no disorder-group label) expands to a small isolated fragment
        that appears only once in the component list.  Without filtering it would
        drag GCD(2, 1) down to 1; the fix excludes it so GCD(2) = 2.
        """
        mol = [('C', 1.0)] * 70 + [('O', 1.0)] * 15 + [('Si', 1.0)] * 10
        minor = [('O', 0.5)] * 4  # disordered solvent, all partial occ
        components = [mol, mol, minor]
        assert _z_from_components(components) == 2

    def test_all_partial_occ_falls_back_to_all_components(self):
        """When every component is partial-occupancy (molecule on special position),
        no filtering is applied and the GCD is computed from all components."""
        # Centrosymmetric molecule on inversion centre: all occ=0.5, appears once.
        mol = [('C', 0.5)] * 10 + [('O', 0.5)] * 3
        assert _z_from_components([mol]) == 1


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
        cif = _load('test-data/DK_Zucker2_0m.cif')
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
        """1000006.cif — same tetracycline HCl in P 21 21 21, Z=4.

        Regression test: previously returned 8 (raw entity count) instead of
        the crystallographic Z=4.
        """
        cif = _load('test-data/1000006.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 4

    def test_empty_atoms_returns_one(self):
        """With no atoms, a safe default of 1 is returned."""
        assert count_z([], ['x, y, z', '-x, -y, -z'], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0)) == 1

    def test_no_symmops_returns_one(self):
        """Without symmetry operations the function cannot expand the unit cell."""
        atoms = [['C1', 'C', 0.5, 0.5, 0.5, 0, 1.0, 0.02]]
        assert count_z(atoms, [], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0)) == 1

    def test_partial_occ_solvent_dg0_does_not_reduce_z(self):
        """1519506.cif — P -1, Z=2, siloxane framework with two disordered O atoms
        (dg=0, occ=0.5) that form an isolated minor solvent fragment.

        Without the minor-component filter the isolated {O:4} fragment (count=1)
        forces GCD(2, 1)=1.  With the fix, the minor component is excluded and
        GCD(2)=2 is returned correctly.
        """
        cif = _load('test-data/1519506.cif')
        assert count_z(cif.atoms_fract, cif.symmops, cif.cell[:6]) == 2


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
        """Z′ = 0.5 (molecule on 2-fold special position) → medium confidence."""
        r = ZResult(z=2, z_prime=0.5, z_sg=4)
        assert r.reliable is True
        assert r.confidence == 'medium'

    def test_zresult_zprime_third_is_medium_confidence(self):
        """Z′ = ⅓ (molecule on 3-fold axis, trigonal/hexagonal groups) → medium."""
        r = ZResult(z=2, z_prime=round(1 / 3, 6), z_sg=6)
        assert r.reliable is True
        assert r.confidence == 'medium'

    def test_zresult_zprime_sixth_is_medium_confidence(self):
        """Z′ = ⅙ (molecule on 6-fold axis, hexagonal groups) → medium."""
        r = ZResult(z=1, z_prime=round(1 / 6, 6), z_sg=6)
        assert r.reliable is True
        assert r.confidence == 'medium'

    def test_zresult_zprime_quarter_is_medium_confidence(self):
        """Z′ = ¼ (molecule on 4-fold axis, tetragonal groups) → medium."""
        r = ZResult(z=1, z_prime=0.25, z_sg=4)
        assert r.reliable is True
        assert r.confidence == 'medium'

    def test_zresult_zprime_two_thirds_is_medium_confidence(self):
        """Z′ = ⅔ (2/3, valid for 3-fold axis) → medium."""
        r = ZResult(z=4, z_prime=round(2 / 3, 6), z_sg=6)
        assert r.reliable is True
        assert r.confidence == 'medium'

    def test_zresult_zprime_non_crystallographic_is_low_confidence(self):
        """Z′ = 0.4 is not k/n for any n in {1,2,3,4,6} → low confidence.

        Nearest valid fractions are ⅓ (diff=0.067) and ½ (diff=0.10),
        both outside the 0.05 tolerance.
        """
        r = ZResult(z=2, z_prime=0.4, z_sg=5)
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

    def test_zresult_formula_derived_gives_formula_confidence(self):
        """formula_derived=True always yields confidence='formula' regardless of Z'."""
        r = ZResult(z=2, z_prime=round(1 / 12, 6), z_sg=24, formula_derived=True)
        assert r.confidence == 'formula'

    def test_zresult_formula_derived_false_gives_normal_confidence(self):
        """formula_derived=False (default) does not affect confidence logic."""
        r = ZResult(z=4, z_prime=1.0, z_sg=4, formula_derived=False)
        assert r.confidence == 'high'

    def test_zresult_default_formula_derived_is_false(self):
        """ZResult.formula_derived defaults to False."""
        r = ZResult(z=4, z_prime=1.0, z_sg=4)
        assert r.formula_derived is False

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
        cif = _load('test-data/1000006.cif')
        result = count_z_and_zprime(cif.atoms_fract, cif.symmops, cif.cell[:6])
        assert isinstance(result, ZResult)
        assert result.z == 4
        assert result.z_sg == 4
        assert abs(result.z_prime - 1.0) < 0.01
        assert result.confidence == 'high'
        assert result.formula_derived is False

    def test_count_z_and_zprime_triclinic(self):
        """P -1 structure: Z=2, Z_sg=2 → Z′=1, high confidence."""
        cif = _load('test-data/DK_ML7-66-final.cif')
        result = count_z_and_zprime(cif.atoms_fract, cif.symmops, cif.cell[:6])
        assert result.z == 2
        assert result.z_sg == 2
        assert abs(result.z_prime - 1.0) < 0.01
        assert result.confidence == 'high'
        assert result.formula_derived is False

    def test_count_z_and_zprime_no_symmops(self):
        """No symmops → Z=1, Z_sg=1, Z′=1."""
        atoms = [['C1', 'C', 0.5, 0.5, 0.5, 0, 1.0, 0.02]]
        result = count_z_and_zprime(atoms, [], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0))
        assert result.z == 1
        assert result.z_sg == 1
        assert abs(result.z_prime - 1.0) < 0.01


# ---------------------------------------------------------------------------
# Tests for element-symbol normalization
# ---------------------------------------------------------------------------

class TestNormalizeElement:
    """Unit tests for _normalize_element() — stripping oxidation-state suffixes."""

    def test_plain_element_unchanged(self):
        assert _normalize_element('C') == 'C'

    def test_plain_element_capitalized(self):
        assert _normalize_element('c') == 'C'

    def test_two_letter_element(self):
        assert _normalize_element('Fe') == 'Fe'

    def test_two_letter_element_lowercase(self):
        assert _normalize_element('fe') == 'Fe'

    def test_positive_oxidation_state_stripped(self):
        assert _normalize_element('Fe3+') == 'Fe'

    def test_negative_oxidation_state_stripped(self):
        assert _normalize_element('O1-') == 'O'

    def test_zero_oxidation_stripped(self):
        assert _normalize_element('Ni0+') == 'Ni'

    def test_arsenic_ionic_stripped(self):
        assert _normalize_element('As0+') == 'As'

    def test_chloride_stripped(self):
        assert _normalize_element('Cl1-') == 'Cl'

    def test_nitrogen_anion_stripped(self):
        assert _normalize_element('N1-') == 'N'


# ---------------------------------------------------------------------------
# Tests for inorganic / polymeric structures
# ---------------------------------------------------------------------------

class TestCountZPolymeric:
    """Tests for Z estimation in polymeric and extended inorganic structures."""

    def test_nicas_z2_with_formula(self):
        """NiAs — P 6₃/mmc, Z=2, fully polymeric inorganic structure.

        All unit-cell atoms form one connected network (Ni and As are bonded
        throughout the crystal), so the bond-graph GCD alone gives Z=1.  With
        the chemical formula 'As1 Ni1' the per-element ratio correction recovers
        the correct Z=2.  The result is marked formula_derived=True.

        Also exercises element-symbol normalization: the CIF stores type symbols
        as 'Ni0+' and 'As0+'; after normalization the formula comparison works.
        """
        cif = _load('test-data/1923_Aminoff, G._Ni As_P 63.m m c_Nickel arsenide.cif')
        # Read the formula_sum from the CIF (as the appwindow does).
        formula_val = _g.cif.as_string(cif.block.find_value('_chemical_formula_sum'))
        result = count_z_and_zprime(
            cif.atoms_fract, cif.symmops, cif.cell[:6], formula_sum=formula_val
        )
        assert result.z == 2
        assert result.formula_derived is True
        assert result.confidence == 'formula'

    def test_ionic_element_symbols_covalent_radii(self):
        """Bond detection still works when type_symbol contains oxidation states.

        Two 'Fe3+' atoms placed 2.3 Å apart (well within Fe covalent bond range
        of ~2*1.32+0.40=3.04 Å) must bond; two 'Fe3+' atoms at 5.0 Å must not.
        """
        # Orthorhombic cell 10×10×10 Å, P1.
        symmops = ['x, y, z']
        cell = (10.0, 10.0, 10.0, 90.0, 90.0, 90.0)
        # Two iron atoms 2.3 Å apart along x.
        # Fractional difference = 0.23; Cartesian distance = 0.23 × 10.0 Å = 2.3 Å.
        close_atoms = [
            ['Fe1', 'Fe3+', 0.10, 0.10, 0.10, 0, 1.0, 0.02],
            ['Fe2', 'Fe3+', 0.33, 0.10, 0.10, 0, 1.0, 0.02],  # Δx=0.23 → 2.3 Å
        ]
        z_close = count_z(close_atoms, symmops, cell)
        assert z_close == 1, "Bonded Fe atoms should form one component"

        # Two iron atoms 5.0 Å apart (fractional 0.50 in 10 Å cell).
        far_atoms = [
            ['Fe1', 'Fe3+', 0.10, 0.10, 0.10, 0, 1.0, 0.02],
            ['Fe2', 'Fe3+', 0.60, 0.10, 0.10, 0, 1.0, 0.02],  # Δx=0.50 → 5.0 Å
        ]
        z_far = count_z(far_atoms, symmops, cell)
        assert z_far == 2, "Distant Fe atoms should be two separate components"

    def test_ionic_element_symbols_composition_grouping(self):
        """Composition-based GCD still groups components correctly for ionic symbols.

        Two identical 'Fe3+Cl1-' ion pairs should give Z=2.
        """
        symmops = ['x, y, z']
        cell = (20.0, 20.0, 20.0, 90.0, 90.0, 90.0)
        # Two ion-pair clusters separated by ~7 Å — no bonds between them.
        # Within each cluster Fe and Cl are 1.5 Å apart (bonded).
        # Fractional Δx=0.075 in a 20 Å cell → 20 × 0.075 = 1.5 Å (Cartesian).
        atoms = [
            ['Fe1', 'Fe3+', 0.10, 0.10, 0.10, 0, 1.0, 0.02],
            ['Cl1', 'Cl1-', 0.175, 0.10, 0.10, 0, 1.0, 0.02],  # Δx=0.075 → 1.5 Å
            ['Fe2', 'Fe3+', 0.60, 0.60, 0.60, 0, 1.0, 0.02],
            ['Cl2', 'Cl1-', 0.675, 0.60, 0.60, 0, 1.0, 0.02],  # Δx=0.075 → 1.5 Å
        ]
        z = count_z(atoms, symmops, cell)
        assert z == 2


# ---------------------------------------------------------------------------
# Comprehensive parametrized test suite covering COD-database structure types
# ---------------------------------------------------------------------------

def _load_cif_raw(path: str) -> tuple:
    """Load a CIF file directly via gemmi and return (atoms, symmops, cell, formula, z_cif).

    Works with any CIF layout — does not require CifContainer — so it can read
    the minimal fixture files in tests/examples/cod/ as well as the full
    FinalCif CIF files in test-data/.

    Reads ``_atom_site_disorder_group`` and ``_atom_site_occupancy`` when
    present so that partial-occupancy disorder filtering works identically to
    :class:`~finalcif.cif.cif_file_io.CifContainer`.

    Returns ``None`` for ``z_cif`` when ``_cell_formula_units_Z`` is absent.
    """
    doc = _g.cif.read(path)
    block = doc[0]

    # Symmetry operations
    for tag in ('_space_group_symop_operation_xyz', '_symmetry_equiv_pos_as_xyz'):
        col = block.find_values(tag)
        if col:
            symmops = [_g.cif.as_string(v).strip().strip("'\"") for v in col]
            break
    else:
        symmops = []

    # Unit cell
    cell = tuple(
        float(_g.cif.as_string(block.find_value(t)).split('(')[0])
        for t in ('_cell_length_a', '_cell_length_b', '_cell_length_c',
                  '_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma')
    )

    # Atom sites — try to include disorder_group and occupancy columns.
    # fall back gracefully if either column is absent.
    loop_full = block.find('_atom_site_', ['label', 'type_symbol',
                                           'fract_x', 'fract_y', 'fract_z',
                                           'disorder_group', 'occupancy'])
    loop_no_dis = block.find('_atom_site_', ['label', 'type_symbol',
                                             'fract_x', 'fract_y', 'fract_z',
                                             'occupancy'])
    loop_bare = block.find('_atom_site_', ['label', 'type_symbol',
                                           'fract_x', 'fract_y', 'fract_z'])
    loop = loop_full or loop_no_dis or loop_bare

    atoms = []
    for row in loop:
        try:
            label = _g.cif.as_string(row[0])
            typ = _g.cif.as_string(row[1])
            x = float(_g.cif.as_string(row[2]).split('(')[0])
            y = float(_g.cif.as_string(row[3]).split('(')[0])
            z = float(_g.cif.as_string(row[4]).split('(')[0])
            if loop is loop_full:
                dg_raw = _g.cif.as_string(row[5]).strip()
                try:
                    dg = int(dg_raw) if dg_raw not in ('', '.', '?') else 0
                except ValueError:
                    dg = 0
                occ_raw = _g.cif.as_string(row[6]).split('(')[0]
                try:
                    occ = float(occ_raw) if occ_raw not in ('', '.', '?') else 1.0
                except ValueError:
                    occ = 1.0
            elif loop is loop_no_dis:
                dg = 0
                occ_raw = _g.cif.as_string(row[5]).split('(')[0]
                try:
                    occ = float(occ_raw) if occ_raw not in ('', '.', '?') else 1.0
                except ValueError:
                    occ = 1.0
            else:
                dg, occ = 0, 1.0
            atoms.append([label, typ, x, y, z, dg, occ, 0.02])
        except (ValueError, IndexError):
            continue

    # Chemical formula sum
    fv = block.find_value('_chemical_formula_sum')
    formula = _g.cif.as_string(fv).strip("'\" ") if fv else None

    # Z from CIF header
    zv = block.find_value('_cell_formula_units_Z')
    try:
        z_cif = int(float(_g.cif.as_string(zv))) if zv else None
    except (ValueError, TypeError):
        z_cif = None

    return atoms, symmops, cell, formula, z_cif


# ── Existing COD structures from test-data/ ──────────────────────────────────
# Each entry: (relative_path, expected_Z, expected_confidence, description)

_COD_TESTDATA_CASES = [
    # path                                    Z   confidence  description
    ('test-data/1000006.cif',                 4,  'high',    'tetracycline HCl, P212121 (organic salt)'),
    ('test-data/1519506.cif',                 2,  'high',    'siloxane macrocycle, P-1, with disordered minor fragment'),
    ('test-data/4060308.cif',                 2,  'high',    'W carbene complex, P-1'),
    ('test-data/4060314.cif',                 4,  'formula', 'Au2Cl14 / Tl salt, P21/n — bond-graph undercount corrected by formula'),
    ('test-data/406äöü0310.cif',              2,  'high',    'Re complex with encoding edge-case filename, P-1'),
    ('test-data/SH2185_Cu.cif',               4,  'high',    'organic amine, P212121'),
    ('test-data/alert_example.cif',           2,  'high',    'organic, P-1'),
    ('test-data/p21c.cif',                    4,  'high',    'organic, P21/c, Z=4'),
    ('test-data/p31c.cif',                    2,  'medium',  'P31c hexagonal, Z=2, Z′=⅓ (3-fold special position)'),
    ('test-data/sad-final.cif',               2,  'medium',  'P31c hexagonal, Z=2, Z′=⅓ (3-fold special position)'),
    ('test-data/1923_Aminoff, G._Ni As_P 63.m m c_Nickel arsenide.cif',
                                              2,  'formula', 'NiAs — fully polymeric inorganic, ionic type_symbols'),
]

# ── Synthetic COD-like fixtures in tests/examples/cod/ ───────────────────────
# These represent well-known inorganic structure types that are common in the COD
# and exercise features introduced in the recent ionic/polymeric improvements.

_COD_FIXTURE_CASES = [
    # path                                    Z   confidence  description
    ('tests/examples/cod/nacl.cif',           4,  'formula', 'NaCl rock salt — Fm-3m, ionic Na1+/Cl1- type symbols, fully polymeric'),
    ('tests/examples/cod/tio2_rutile.cif',    2,  'formula', 'Rutile TiO2 — P4_2/mnm, ionic type symbols, polymeric oxide'),
    ('tests/examples/cod/zno_wurtzite.cif',   2,  'formula', 'ZnO wurtzite — P6_3mc, hexagonal polymeric, ionic symbols'),
    ('tests/examples/cod/cuo_tenorite.cif',   4,  'formula', 'CuO tenorite — C2/c, centered monoclinic ionic oxide'),
    ('tests/examples/cod/calcite.cif',        6,  'formula', 'Calcite CaCO3 — R-3c, trigonal carbonate, ionic symbols'),
    ('tests/examples/cod/urea.cif',           2,  'medium',  'Urea — P-42_1m, organic on special position, Z′=¼'),
]


def _make_cod_test_id(val):
    """Return a short test ID from the CIF path string."""
    if isinstance(val, str):
        return Path(val).stem
    return str(val)


@pytest.mark.parametrize(
    'cif_path, expected_z, expected_confidence, description',
    _COD_TESTDATA_CASES + _COD_FIXTURE_CASES,
    ids=[_make_cod_test_id(c[0]) for c in _COD_TESTDATA_CASES + _COD_FIXTURE_CASES],
)
class TestZCodSuite:
    """Parametrized Z + Z′ test suite covering diverse COD-database structure types.

    Each test case loads a CIF file (either from ``test-data/`` or from the
    minimal fixtures in ``tests/examples/cod/``), runs :func:`count_z_and_zprime`
    with the CIF's own ``_chemical_formula_sum``, and asserts that the computed Z
    matches ``_cell_formula_units_Z`` and that the confidence level is as expected.

    The fixture files in ``tests/examples/cod/`` were generated from real
    crystallographic data (same atom positions and unit-cell parameters as the
    reference structures) using gemmi's space-group engine to expand the full
    operator list.  They cover structure types that are abundant in the COD
    database but absent from the regular ``test-data/`` organics:

    * **Ionic / polymeric inorganics** (NaCl, TiO2, ZnO, CuO, CaCO3) — these
      always yield ``confidence='formula'`` because the bond graph spans the
      entire crystal and the GCD-by-composition step is needed to recover Z.
    * **Organic on special position** (urea, Z′=¼) — yields ``confidence='medium'``
      (non-integer but crystallographically valid Z′).
    * **Formula-corrected organometallics** (4060314, NiAs) — yield
      ``confidence='formula'`` via the formula-override path.
    * **Standard organic structures** (P-1, P21/c, P212121, P31c) — yield
      ``confidence='high'`` or ``'medium'`` from the bond-graph GCD directly.

    .. note::
        ``1548072_many_atoms.cif`` is intentionally excluded: its F atoms sit
        partially on crystallographic special positions, so the expanded cell
        count (1146) disagrees with ``144 × Z = 1152`` for Z=8, preventing the
        formula correction.  The bond-graph GCD returns Z=2; both paths are
        incorrect.  This is a documented current limitation for structures where
        atoms on special positions cause the formula ratio to be non-integer.
    """

    def test_z_matches_cif(self, cif_path, expected_z, expected_confidence, description):
        """Computed Z must equal the CIF-reported ``_cell_formula_units_Z``."""
        atoms, symmops, cell, formula, z_cif = _load_cif_raw(cif_path)
        assert z_cif == expected_z, (
            f"Fixture mismatch: CIF {cif_path!r} reports Z={z_cif}, but test "
            f"expects Z={expected_z}.  Update the test if the fixture was changed."
        )
        result = count_z_and_zprime(atoms, symmops, cell, formula_sum=formula)
        assert result.z == expected_z, (
            f"{description} — expected Z={expected_z}, got Z={result.z} "
            f"(Z′={result.z_prime:.4f}, conf={result.confidence})"
        )

    def test_confidence_level(self, cif_path, expected_z, expected_confidence, description):
        """Confidence level must match the expected value for this structure type."""
        atoms, symmops, cell, formula, _z_cif = _load_cif_raw(cif_path)
        result = count_z_and_zprime(atoms, symmops, cell, formula_sum=formula)
        assert result.confidence == expected_confidence, (
            f"{description} — expected confidence={expected_confidence!r}, "
            f"got {result.confidence!r} (Z={result.z}, Z′={result.z_prime:.4f})"
        )

    def test_zprime_is_positive(self, cif_path, expected_z, expected_confidence, description):
        """Z′ must always be a finite positive number."""
        atoms, symmops, cell, formula, _z_cif = _load_cif_raw(cif_path)
        result = count_z_and_zprime(atoms, symmops, cell, formula_sum=formula)
        assert result.z_prime > 0 and not (result.z_prime != result.z_prime), (
            f"{description} — Z′={result.z_prime!r} is not a positive finite number"
        )

    def test_z_sg_equals_symmop_count(self, cif_path, expected_z, expected_confidence, description):
        """Z_sg must equal the number of symmetry operations in the CIF."""
        atoms, symmops, cell, formula, _z_cif = _load_cif_raw(cif_path)
        result = count_z_and_zprime(atoms, symmops, cell, formula_sum=formula)
        assert result.z_sg == len(symmops), (
            f"{description} — Z_sg={result.z_sg} but CIF has {len(symmops)} symmops"
        )

