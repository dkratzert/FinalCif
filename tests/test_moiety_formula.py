"""Tests for charge-aware moiety formula generation.

The expected strings follow the IUCr ``_chemical_formula_moiety`` rules:
moieties separated by ``', '``, elements in Hill order separated by spaces,
and the charge appended after a space (``'B F4 1-'``).  A multiplier other
than one wraps the whole moiety in parentheses (``'2(N O3 1-)'``).
"""
from pathlib import Path
import math
import re

import pytest

from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.formal_charge import (
    ChargeAtom,
    SpeciesCharge,
    balance_charges,
    format_charge,
    is_metal,
    parse_oxidation_state,
    perceive_fragment_charge,
)
from finalcif.tools.sumformula import (NORMAL, SUBSCRIPT, SUPERSCRIPT, formula_parts,
                                       formula_str_to_dict, formula_to_html)
from finalcif.tools.z_from_packing import (_build_bond_graph, _expand_to_unit_cell,
                                           _parts_may_bond, count_z_and_zprime,
                                           moiety_formula_from_components)


def _load(relative_path: str) -> CifContainer:
    return CifContainer(Path(relative_path))


def _atoms(*symbols_with_neighbours) -> tuple[ChargeAtom, ...]:
    """Build ChargeAtom records from ``(element, [(neighbour, degree), ...])`` pairs."""
    return tuple(ChargeAtom(element=element, neighbours=tuple(neighbours))
                 for element, neighbours in symbols_with_neighbours)


def _flat(elements: str) -> tuple[ChargeAtom, ...]:
    """Build unconnected ChargeAtom records from a space-separated element list."""
    return tuple(ChargeAtom(element=element) for element in elements.split())


def _composition(**counts: float) -> dict[str, float]:
    return {element: float(count) for element, count in counts.items()}


_MOIETY_RE = re.compile(r'^\s*(?:(?P<multiplier>[\d.]+)\s*\()?(?P<formula>[^()]+?)\)?\s*$')


def _sum_moiety(moiety: str) -> dict[str, float]:
    """Add up all moieties of a formula string into one ``{element: count}`` dict."""
    total: dict[str, float] = {}
    for part in moiety.split(','):
        match = _MOIETY_RE.match(part)
        assert match is not None, part
        multiplier = float(match['multiplier'] or 1)
        formula = re.sub(r'\s*\d*[+-]\s*$', '', match['formula'])
        for element, count in formula_str_to_dict(formula).items():
            total[element] = total.get(element, 0.0) + multiplier * count
    return total


# ---------------------------------------------------------------------------
# Oxidation-state suffixes of CIF type symbols
# ---------------------------------------------------------------------------

class TestParseOxidationState:
    @pytest.mark.parametrize('symbol, expected', [
        ('Fe3+', 3),
        ('Cl1-', -1),
        ('O2-', -2),
        ('Na1+', 1),
        ('O-', -1),
        ('K+', 1),
        ('Ni0+', 0),
    ])
    def test_suffix_is_parsed(self, symbol, expected):
        assert parse_oxidation_state(symbol) == expected

    @pytest.mark.parametrize('symbol', ['C', 'Cl', 'Fe', '', 'H'])
    def test_plain_symbol_has_no_oxidation_state(self, symbol):
        assert parse_oxidation_state(symbol) is None


class TestIsMetal:
    @pytest.mark.parametrize('element', ['Na', 'Fe', 'Cu', 'Zn', 'La', 'U', 'Al', 'Sn'])
    def test_metals(self, element):
        assert is_metal(element) is True

    @pytest.mark.parametrize('element', ['C', 'N', 'O', 'B', 'Si', 'As', 'Sb', 'Te', 'Cl'])
    def test_non_metals_and_metalloids(self, element):
        assert is_metal(element) is False


class TestFormatCharge:
    @pytest.mark.parametrize('charge, expected', [
        (1, '1+'), (2, '2+'), (-1, '1-'), (-3, '3-'), (0, ''),
    ])
    def test_iucr_charge_token(self, charge, expected):
        assert format_charge(charge) == expected


# ---------------------------------------------------------------------------
# Per-fragment charge perception
# ---------------------------------------------------------------------------

class TestPerceiveFragmentCharge:
    def test_chloride_ion(self):
        result = perceive_fragment_charge(_flat('Cl'), _composition(Cl=1))
        assert (result.charge, result.confident) == (-1, True)

    def test_sodium_ion(self):
        result = perceive_fragment_charge(_flat('Na'), _composition(Na=1))
        assert (result.charge, result.confident) == (1, True)

    def test_ambiguous_metal_stays_unconfident(self):
        """Copper has several common oxidation states — leave it to charge balancing."""
        result = perceive_fragment_charge(_flat('Cu'), _composition(Cu=1))
        assert (result.charge, result.confident) == (0, False)

    def test_lone_oxygen_is_not_an_oxide(self):
        """A bare oxygen is far more often a water whose hydrogens were not modelled."""
        result = perceive_fragment_charge(_flat('O'), _composition(O=1))
        assert result.confident is False

    def test_tetrafluoroborate(self):
        result = perceive_fragment_charge(_flat('B F F F F'), _composition(B=1, F=4))
        assert (result.charge, result.confident) == (-1, True)

    def test_hexafluorophosphate(self):
        result = perceive_fragment_charge(_flat('P F F F F F F'), _composition(P=1, F=6))
        assert (result.charge, result.confident) == (-1, True)

    def test_perchlorate(self):
        result = perceive_fragment_charge(_flat('Cl O O O O'), _composition(Cl=1, O=4))
        assert (result.charge, result.confident) == (-1, True)

    def test_nitrate(self):
        result = perceive_fragment_charge(_flat('N O O O'), _composition(N=1, O=3))
        assert (result.charge, result.confident) == (-1, True)

    def test_sulfate(self):
        result = perceive_fragment_charge(_flat('S O O O O'), _composition(S=1, O=4))
        assert (result.charge, result.confident) == (-2, True)

    def test_phosphate(self):
        result = perceive_fragment_charge(_flat('P O O O O'), _composition(P=1, O=4))
        assert (result.charge, result.confident) == (-3, True)

    def test_ammonium(self):
        result = perceive_fragment_charge(_flat('N H H H H'), _composition(N=1, H=4))
        assert (result.charge, result.confident) == (1, True)

    def test_water_is_neutral_and_confident(self):
        result = perceive_fragment_charge(_flat('O H H'), _composition(O=1, H=2))
        assert (result.charge, result.confident) == (0, True)

    def test_common_solvent_is_neutral_and_confident(self):
        result = perceive_fragment_charge(_flat('C H H H H O'), _composition(C=1, H=4, O=1))
        assert (result.charge, result.confident) == (0, True)

    @pytest.mark.parametrize('composition', [
        {'C': 4, 'H': 8, 'O': 1},                  # THF
        {'C': 5, 'H': 5, 'N': 1},                  # pyridine
        {'C': 12, 'H': 24, 'O': 6},                # 18-crown-6
        {'C': 6, 'H': 16, 'N': 2},                 # TMEDA
        {'C': 18, 'H': 15, 'P': 1},                # triphenylphosphane
        {'C': 4, 'H': 4, 'S': 1},                  # thiophene
        {'C': 6, 'H': 5, 'Cl': 1},                 # chlorobenzene
        {'C': 60},                                 # fullerene C60
        {'O': 2, 'S': 1},                          # sulfur dioxide
    ])
    def test_solvents_and_coformers_are_neutral(self, composition):
        result = perceive_fragment_charge((), _composition(**composition))
        assert (result.charge, result.confident) == (0, True)

    def test_trifluoroacetate_is_an_anion(self):
        result = perceive_fragment_charge((), _composition(C=2, F=3, O=2))
        assert (result.charge, result.confident) == (-1, True)

    def test_trifluoroacetic_acid_is_neutral(self):
        result = perceive_fragment_charge((), _composition(C=2, H=1, F=3, O=2))
        assert (result.charge, result.confident) == (0, True)

    def test_hydrocarbon_is_neutral_and_confident(self):
        result = perceive_fragment_charge(_flat('C C C C C C H H H H H H'),
                                          _composition(C=6, H=6))
        assert (result.charge, result.confident) == (0, True)

    def test_quaternary_nitrogen_is_a_cation(self):
        """Four-coordinate nitrogen (ammonium / iminium) carries a 1+ charge."""
        fragment = _atoms(('N', [('C', 4), ('C', 4), ('C', 4), ('C', 4)]),
                          ('C', [('N', 4)]), ('C', [('N', 4)]),
                          ('C', [('N', 4)]), ('C', [('N', 4)]))
        result = perceive_fragment_charge(fragment, _composition(C=4, N=1))
        assert (result.charge, result.confident) == (1, False)

    def test_amine_n_oxide_is_neutral(self):
        """R3N+-O- has two cancelling formal charges — the fragment is neutral."""
        fragment = _atoms(('N', [('C', 4), ('C', 4), ('C', 4), ('O', 1)]),
                          ('O', [('N', 4)]))
        result = perceive_fragment_charge(fragment, _composition(C=3, N=1, O=1))
        assert result.charge == 0

    def test_amine_nitrogen_is_neutral(self):
        fragment = _atoms(('N', [('C', 4), ('H', 1), ('H', 1)]),)
        result = perceive_fragment_charge(fragment, _composition(C=1, N=1, H=2))
        assert result.charge == 0

    def test_nitrogen_coordinating_a_metal_is_neutral(self):
        """Metal-ligand bonds are excluded, so a coordinating amine stays neutral."""
        fragment = _atoms(('N', [('H', 1), ('H', 1), ('H', 1)]),)
        result = perceive_fragment_charge(fragment, _composition(N=1, H=3, Cu=1))
        assert result.charge == 0

    def test_tetraphenylborate_is_an_anion(self):
        fragment = _atoms(('B', [('C', 3), ('C', 3), ('C', 3), ('C', 3)]),)
        result = perceive_fragment_charge(fragment, _composition(B=1, C=24, H=20))
        assert result.charge == -1

    def test_phosphonium_is_a_cation(self):
        fragment = _atoms(('P', [('C', 4), ('C', 4), ('C', 4), ('C', 4)]),)
        result = perceive_fragment_charge(fragment, _composition(P=1, C=4))
        assert result.charge == 1

    def test_phosphine_oxide_is_neutral(self):
        fragment = _atoms(('P', [('C', 4), ('C', 4), ('C', 4), ('O', 1)]),)
        result = perceive_fragment_charge(fragment, _composition(P=1, C=3, O=1))
        assert result.charge == 0

    def test_explicit_oxidation_states_win(self):
        fragment = (ChargeAtom(element='Fe', oxidation=3),
                    ChargeAtom(element='O', oxidation=-2),
                    ChargeAtom(element='O', oxidation=-2))
        result = perceive_fragment_charge(fragment, _composition(Fe=1, O=2))
        assert (result.charge, result.confident) == (-1, True)

    def test_explicit_oxidation_state_of_monatomic_ion(self):
        fragment = (ChargeAtom(element='Cu', oxidation=2),)
        result = perceive_fragment_charge(fragment, _composition(Cu=1))
        assert (result.charge, result.confident) == (2, True)


# ---------------------------------------------------------------------------
# Charge balancing across the formula unit
# ---------------------------------------------------------------------------

class TestBalanceCharges:
    def test_already_neutral_is_unchanged(self):
        species = [SpeciesCharge(1, False, 1.0, 20.0), SpeciesCharge(-1, True, 1.0, 1.0)]
        assert balance_charges(species) == [1, -1]

    def test_unknown_cation_is_derived_from_a_known_anion(self):
        """Organic base + BF4- → the organic must be 1+."""
        species = [SpeciesCharge(0, False, 1.0, 22.0), SpeciesCharge(-1, True, 1.0, 5.0)]
        assert balance_charges(species) == [1, -1]

    def test_unknown_anion_is_derived_from_a_known_cation(self):
        """Sodium benzoate: Na+ is known, so the carboxylate must be 1-."""
        species = [SpeciesCharge(0, False, 1.0, 14.0), SpeciesCharge(1, True, 1.0, 1.0)]
        assert balance_charges(species) == [-1, 1]

    def test_multiplier_is_taken_into_account(self):
        """Calcium dicarboxylate: two anions share the 2+ of the cation."""
        species = [SpeciesCharge(0, False, 2.0, 7.0), SpeciesCharge(2, True, 1.0, 1.0)]
        assert balance_charges(species) == [-1, 2]

    def test_charge_lands_on_the_largest_neutral_species_not_on_the_solvent(self):
        organic = SpeciesCharge(0, False, 1.0, 30.0)
        water = SpeciesCharge(0, True, 2.0, 3.0)
        chloride = SpeciesCharge(-1, True, 1.0, 1.0)
        assert balance_charges([organic, water, chloride]) == [1, 0, -1]

    def test_unresolvable_imbalance_returns_none(self):
        """Every species is confident, yet the cell is not neutral → give up."""
        species = [SpeciesCharge(-1, True, 1.0, 1.0), SpeciesCharge(-1, True, 1.0, 1.0)]
        assert balance_charges(species) is None

    def test_non_integer_derived_charge_returns_none(self):
        species = [SpeciesCharge(0, False, 2.0, 10.0), SpeciesCharge(-1, True, 1.0, 1.0)]
        assert balance_charges(species) is None

    def test_empty_species_list(self):
        assert balance_charges([]) == []


# ---------------------------------------------------------------------------
# Moiety strings built from bond-graph components
# ---------------------------------------------------------------------------

def _component(*records) -> list:
    """Build a component of ``(element, occupancy, neighbours)`` atom records."""
    return [(element, 1.0, tuple(neighbours)) for element, neighbours in records]


class TestMoietyFormulaWithCharges:
    def test_organic_cation_with_chloride(self):
        cation = (_component(('N', [('C', 4), ('C', 4), ('C', 4), ('C', 4)]))
                  + [('C', 1.0, (('N', 4),))] * 4 + [('H', 1.0, (('C', 4),))] * 12)
        chloride = [('Cl', 1.0, ())]
        result = moiety_formula_from_components([cation, cation, chloride, chloride], z=2)
        assert result == 'C4 H12 N 1+, Cl 1-'

    def test_two_chlorides_per_dication(self):
        dication = ([('N', 1.0, (('C', 4), ('C', 4), ('C', 4), ('C', 4)))] * 2
                    + [('C', 1.0, (('N', 4),))] * 6 + [('H', 1.0, (('C', 4),))] * 18)
        chloride = [('Cl', 1.0, ())]
        components = [dication] + [chloride] * 2
        result = moiety_formula_from_components(components, z=1)
        assert result == 'C6 H18 N2 2+, 2(Cl 1-)'

    def test_neutral_structure_has_no_charge_tokens(self):
        organic = [('C', 1.0, ())] * 10 + [('H', 1.0, ())] * 8 + [('N', 1.0, ())] * 2
        assert moiety_formula_from_components([organic], z=1) == 'C10 H8 N2'

    def test_sodium_salt_charge_is_derived(self):
        carboxylate = ([('C', 1.0, ())] * 2 + [('H', 1.0, ())] * 3
                       + [('O', 1.0, ())] * 2)
        sodium = [('Na', 1.0, ())]
        result = moiety_formula_from_components([carboxylate, sodium], z=1)
        assert result == 'C2 H3 O2 1-, Na 1+'

    def test_solvent_keeps_its_neutrality(self):
        cation = [('N', 1.0, (('C', 4), ('C', 4), ('C', 4), ('C', 4)))]
        chloride = [('Cl', 1.0, ())]
        water = [('O', 1.0, (('H', 1), ('H', 1))),
                 ('H', 1.0, (('O', 2),)), ('H', 1.0, (('O', 2),))]
        result = moiety_formula_from_components([cation, chloride, water], z=1)
        # All three species have a single non-hydrogen atom, so the discovery
        # order decides (see the PLATON ordering rule).
        assert result == 'N 1+, Cl 1-, H2 O'

    def test_explicit_oxidation_states_from_type_symbols(self):
        sodium = [('Na1+', 1.0, ())]
        chloride = [('Cl1-', 1.0, ())]
        result = moiety_formula_from_components([sodium, chloride], z=1)
        assert result == 'Na 1+, Cl 1-'

    def test_charges_are_dropped_when_the_cell_cannot_be_balanced(self):
        chloride = [('Cl', 1.0, ())]
        result = moiety_formula_from_components([chloride, chloride], z=1)
        assert result == '2(Cl)'

    def test_plain_two_tuple_records_are_still_accepted(self):
        organic = [('C', 1.0)] * 10 + [('H', 1.0)] * 8 + [('N', 1.0)] * 2
        assert moiety_formula_from_components([organic], z=1) == 'C10 H8 N2'


class TestMultipliersArePerFormulaUnit:
    """Multipliers describe one formula unit, so the moiety sums to the sum formula."""

    def test_half_a_solvent_keeps_a_fractional_multiplier(self):
        organic = [('C', 1.0, ())] * 26 + [('O', 1.0, ())] * 6
        methanol = [('C', 0.5, ()), ('O', 0.5, ())]
        components = [organic, organic, methanol, methanol]
        assert moiety_formula_from_components(components, z=2) == 'C26 O6, 0.5(C O)'

    def test_three_quarters_solvent(self):
        organic = [('C', 1.0, ())] * 10
        water = [('H', 0.75, ()), ('H', 0.75, ()), ('O', 0.75, ())]
        components = [organic] * 4 + [water] * 4
        assert moiety_formula_from_components(components, z=4) == 'C10, 0.75(H2 O)'

    def test_integer_multipliers(self):
        organic = [('C', 1.0, ())] * 10
        water = [('H', 1.0, ()), ('H', 1.0, ()), ('O', 1.0, ())]
        components = [organic, water, water]
        assert moiety_formula_from_components(components, z=1) == 'C10, 2(H2 O)'

    def test_partial_occupancy_solvent(self):
        organic = [('C', 1.0, ())] * 10
        solvent = [('C', 0.9, ()), ('O', 0.9, ())]
        assert moiety_formula_from_components([organic, solvent], z=1) == 'C10, 0.9(C O)'


# ---------------------------------------------------------------------------
# End-to-end tests on real structures
# ---------------------------------------------------------------------------

class TestMoietyFormulaOfRealStructures:
    def _moiety(self, path: str) -> str:
        cif = _load(path)
        return count_z_and_zprime(
            cif.atoms_fract, cif.symmops, cif.cell[:6],
            formula_sum=cif['_chemical_formula_sum'],
        ).moiety_formula

    def test_tetrafluoroborate_salt(self):
        """Esser_JW367_0m: organic cation + BF4- anion (P 2₁/n, Z=4).

        PLATON finds the same two fragments (``'C9 H9 Br Cl N2, B F4'``) but
        reports no charges.
        """
        assert self._moiety('tests/examples/Esser_JW367_0m.cif') == 'C9 H9 Br Cl N2 1+, B F4 1-'

    def test_tetracycline_hydrochloride(self):
        """1000006: protonated dimethylamino group + chloride.

        PLATON: ``'C22 H25 N2 O8, Cl'`` — same fragments, no charges.
        """
        assert self._moiety('test-data/1000006.cif') == 'C22 H25 N2 O8 1+, Cl 1-'

    def test_neutral_molecule_gets_no_charge(self):
        assert self._moiety('test-data/DK_ML7-66-final.cif') == 'C23 H21 N O'

    def test_solvate_keeps_the_per_formula_unit_multiplier(self):
        """Half a methanol per molecule, so the moiety still sums to the sum formula.

        PLATON reports the same ratio as ``'2(C38 H38 O12), C H4 O'`` because it
        halves Z for this structure (``Z = 2[Calc], 4[Rep]``).  We keep the Z of
        the CIF, which makes the moiety add up to ``_chemical_formula_sum``.
        """
        assert self._moiety('tests/examples/1979688.cif') == 'C38 H38 O12, 0.5(C H4 O)'

    def test_sucrose_is_neutral(self):
        assert self._moiety('test-data/DK_Zucker2_0m.cif') == 'C12 H22 O11'

    def test_disordered_anion_precedes_the_larger_cation(self):
        """1548072: PLATON reports ``'4(C16 Al F36 O4), C60 H48 In4 N12'``.

        The aluminate has fewer atoms in its formula than the indium cation but
        is disordered over more sites, so its residue holds the larger number of
        modelled non-hydrogen atoms and PLATON lists it first.
        """
        assert (self._moiety('test-data/1548072_many_atoms.cif')
                == '4(C16 Al F36 O4), C60 H48 In4 N12')


class TestMoietyOrderFollowsPlaton:
    """PLATON orders moieties by descending modelled non-hydrogen atom count.

    Every disorder part counts once and occupancies are ignored, so a
    disordered fragment can precede a chemically larger, ordered one.  A
    deviating sequence makes checkCIF raise ``042_ALERT_1_C``.
    """

    def test_disordered_fragment_comes_first(self):
        ordered = [('C', 1.0, ())] * 10
        # Two parts of the same six-carbon molecule: six carbons in the formula,
        # but twelve modelled carbons.
        disordered = [('C', 0.6, ())] * 6 + [('C', 0.4, ())] * 6
        assert moiety_formula_from_components([ordered, disordered], z=1) == 'C6, C10'

    def test_equal_counts_keep_the_discovery_order(self):
        first = [('Na', 1.0, ())]
        second = [('Cl', 1.0, ())]
        assert moiety_formula_from_components([first, second], z=1) == 'Na 1+, Cl 1-'


# ---------------------------------------------------------------------------
# Regression fixtures taken from the Crystallography Open Database
# ---------------------------------------------------------------------------

# Each entry reproduces both the deposited _chemical_formula_moiety and
# _cell_formula_units_Z of the COD structure exactly.  PLATON (`platon -U`)
# arrives at the same fragmentation and the same Z for all of them; it only
# omits the charges, which it never reports:
#
#   1517679  PLATON: 'C18 H18 N4, 2(B F4)'                            Z=4
#   1513675  PLATON: 'C20 H38 N6 P2 Si2, 2(Cl4 Ga), C H2 Cl2'         Z=4
#   1517303  PLATON: 'C24 H24 Br2 N O P Pd, C H2 Cl2'                 Z=2
#   1508702  PLATON: 'C16 H22 N2 O3 S'                                Z=4
#   1506408  PLATON: 'C10 H14 N2 O2 S'                                Z=16
_COD_MOIETY_CASES = [
    ('test-data/1517679.cif', 'C18 H18 N4 2+, 2(B F4 1-)', 4,
     'organic dication with two tetrafluoroborates, P 21/n'),
    ('test-data/1513675.cif', 'C20 H38 N6 P2 Si2 2+, 2(Cl4 Ga 1-), C H2 Cl2', 4,
     'dication, two tetrachlorogallates and a dichloromethane solvate, P 21/c'),
    ('test-data/1517303.cif', 'C24 H24 Br2 N O P Pd, C H2 Cl2', 2,
     'neutral palladium complex with dichloromethane solvate, P 21'),
    ('test-data/1508702.cif', 'C16 H22 N2 O3 S', 4,
     'neutral organic, P 21/n'),
    ('test-data/1506408.cif', 'C10 H14 N2 O2 S', 16,
     'neutral organic in the high-symmetry group F dd 2, Z = 16'),
]


@pytest.mark.parametrize('path, expected_moiety, expected_z, description',
                         _COD_MOIETY_CASES,
                         ids=[Path(case[0]).stem for case in _COD_MOIETY_CASES])
class TestCodMoietyFormulas:
    """The generated moiety formula and Z must match the COD deposit."""

    def _result(self, path: str):
        cif = _load(path)
        return count_z_and_zprime(
            cif.atoms_fract, cif.symmops, cif.cell[:6],
            formula_sum=cif['_chemical_formula_sum'],
        )

    def test_moiety_formula(self, path, expected_moiety, expected_z, description):
        assert self._result(path).moiety_formula == expected_moiety

    def test_z(self, path, expected_moiety, expected_z, description):
        assert self._result(path).z == expected_z

    def test_z_matches_the_cif(self, path, expected_moiety, expected_z, description):
        assert int(_load(path)['_cell_formula_units_Z']) == expected_z

    def test_moiety_sums_to_the_sum_formula(self, path, expected_moiety, expected_z, description):
        """The moiety of one formula unit must add up to ``_chemical_formula_sum``."""
        cif = _load(path)
        expected = formula_str_to_dict(cif['_chemical_formula_sum'])
        summed = _sum_moiety(self._result(path).moiety_formula)
        assert set(summed) == set(expected)
        for element, count in expected.items():
            assert summed[element] == pytest.approx(count, abs=0.02)


# ---------------------------------------------------------------------------
# Rendering of a charged moiety formula in reports
# ---------------------------------------------------------------------------

class TestDisorderedSolventPocket:
    """Two different solvents sharing one pocket must stay separate moieties.

    Following the SHELXL ``PART`` convention, atoms of different non-zero
    disorder groups are alternative positions and are never bonded to each
    other.  Without that rule the bond graph fuses e.g. a benzene and a
    fluorobenzene occupying the same void into one component whose composition
    is a meaningless average such as ``'C6 F0.4'``.
    """

    CELL = (20.0, 20.0, 20.0, 90.0, 90.0, 90.0)

    def _ring(self, occupancy: float, disorder_group: int, *,
              twist: float = 0.0, with_fluorine: bool = False) -> list:
        """A flat six-membered carbon ring centred at (14, 14, 10) Angstrom."""
        atoms = []
        for i in range(6):
            angle = math.radians(60 * i + twist)
            atoms.append([f'C{disorder_group}{i}', 'C',
                          (14.0 + 1.39 * math.cos(angle)) / 20.0,
                          (14.0 + 1.39 * math.sin(angle)) / 20.0,
                          0.5, disorder_group, occupancy, 0.02])
        if with_fluorine:
            angle = math.radians(twist)
            atoms.append([f'F{disorder_group}', 'F',
                          (14.0 + 2.74 * math.cos(angle)) / 20.0,
                          (14.0 + 2.74 * math.sin(angle)) / 20.0,
                          0.5, disorder_group, occupancy, 0.02])
        return atoms

    def _main_molecule(self) -> list:
        """A chain of eight carbons, far away from the solvent pocket."""
        return [[f'M{i}', 'C', (2.0 + 1.5 * i) / 20.0, 0.05, 0.05, 0, 1.0, 0.02]
                for i in range(8)]

    def _moiety(self, atoms: list) -> str:
        return count_z_and_zprime(atoms, ['x,y,z'], self.CELL).moiety_formula

    def test_two_different_solvents_stay_separate(self):
        atoms = (self._main_molecule()
                 + self._ring(0.6, disorder_group=1)
                 + self._ring(0.4, disorder_group=2, twist=7.0, with_fluorine=True))
        assert self._moiety(atoms) == 'C8, 0.4(C6 F), 0.6(C6)'

    def test_composition_is_never_averaged(self):
        """The fused token 'C6 F0.4' of the old behaviour must not reappear."""
        atoms = (self._main_molecule()
                 + self._ring(0.6, disorder_group=1)
                 + self._ring(0.4, disorder_group=2, twist=7.0, with_fluorine=True))
        assert 'F0.4' not in self._moiety(atoms)

    def test_same_solvent_over_two_parts_is_one_species(self):
        """Two PARTs of the *same* molecule add up to one whole solvent."""
        atoms = (self._main_molecule()
                 + self._ring(0.7, disorder_group=1)
                 + self._ring(0.3, disorder_group=2, twist=7.0))
        assert self._moiety(atoms) == 'C8, C6'

    def test_ordered_atoms_still_bridge_disorder_parts(self):
        """An ordered atom bonded to both PARTs keeps the molecule in one piece."""
        bridge = [['B0', 'C', 14.0 / 20.0, (14.0 + 1.39) / 20.0, 0.43, 0, 1.0, 0.02]]
        atoms = (self._main_molecule() + bridge
                 + self._ring(0.6, disorder_group=1)
                 + self._ring(0.4, disorder_group=2, twist=7.0))
        # The bridging carbon fuses both parts into a single seven-carbon unit.
        # Its 13 modelled carbons outnumber the eight of the main chain, so it
        # is listed first (PLATON orders by modelled non-hydrogen atom count).
        assert self._moiety(atoms) == 'C7, C8'

    def test_a_fully_occupied_pivot_inside_a_part_still_bridges(self):
        """The pivot of a rotationally disordered group may sit in a PART itself.

        Deposited CF3 groups regularly carry their carbon in PART 1 while the
        fluorines are spread over PARTs 1, 2 and 3.  The fully occupied carbon
        belongs to all of them, so nothing may be torn off it.
        """
        bridge = [['B1', 'C', 14.0 / 20.0, (14.0 + 1.39) / 20.0, 0.43, 1, 1.0, 0.02]]
        atoms = (self._main_molecule() + bridge
                 + self._ring(0.6, disorder_group=1)
                 + self._ring(0.4, disorder_group=2, twist=7.0))
        assert self._moiety(atoms) == 'C7, C8'


class TestAggregateMerging:
    """A molecule bonded to a symmetry copy of itself must not be counted twice.

    Such a molecule appears both whole and as the fused aggregate, each with a
    fractional multiplier.  Chemically there is only the monomer.
    """

    def _species(self, atoms_per_unit: int, copies: int, occupancy: float) -> list:
        """A component of ``copies × atoms_per_unit`` carbon atoms at *occupancy*."""
        return [('C', occupancy, ())] * (atoms_per_unit * copies)

    def test_dimer_and_monomer_are_folded_together(self):
        """0.25(C20) + 0.5(C10) = 1.0 monomer, as PLATON reports it."""
        monomer = self._species(10, 1, 0.5)
        dimer = self._species(10, 2, 0.25)
        assert moiety_formula_from_components([monomer, dimer], z=1) == 'C10'

    def test_trimer_and_monomer(self):
        """0.5(C30) + 0.5(C10) = 2 monomers."""
        monomer = self._species(10, 1, 0.5)
        trimer = self._species(10, 3, 0.5)
        assert moiety_formula_from_components([monomer, trimer], z=1) == '2(C10)'

    def test_genuine_dimer_plus_monomer_is_kept(self):
        """Two whole-numbered species are a real mixture and stay separate."""
        monomer = self._species(10, 1, 1.0)
        dimer = self._species(10, 2, 1.0)
        result = moiety_formula_from_components([monomer, dimer], z=1)
        assert result == 'C20, C10'

    def test_non_integral_total_is_kept(self):
        """``0.03833(H12 O6), 2(H2 O)`` must survive: 2 + 6*0.03833 is not whole."""
        water = [('H', 1.0, ()), ('H', 1.0, ()), ('O', 1.0, ())]
        hexamer = [('H', 0.03833, ())] * 12 + [('O', 0.03833, ())] * 6
        result = moiety_formula_from_components([water, water, hexamer], z=1)
        assert result == '0.03833(H12 O6), 2(H2 O)'

    def test_different_elements_are_never_folded(self):
        """A composition that is not an exact multiple is left alone."""
        first = [('C', 0.5, ())] * 10
        second = [('C', 0.5, ())] * 20 + [('N', 0.5, ())]
        result = moiety_formula_from_components([first, second], z=1)
        assert result == '0.5(C20 N), 0.5(C10)'


class TestUnitCellExpansion:
    """The expansion must place every site inside one unit cell.

    Deposited fractional coordinates are often slightly outside ``[0, 1)``.
    gemmi passes them through unchanged, so the symmetry copies of a molecule
    can end up spread over three cells — which the ±1 periodic image search of
    the bond graph cannot bridge, tearing molecules apart.
    """

    def test_coordinates_are_wrapped_into_the_unit_cell(self):
        atoms = [['C1', 'C', 1.0632, -0.25, 2.5, 0, 1.0, 0.02]]
        expanded = _expand_to_unit_cell(atoms, ['x,y,z'], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0))
        assert expanded
        for _element, position, _occupancy, _group in expanded:
            for coordinate in position:
                assert 0.0 <= coordinate < 1.0

    def test_wrapping_keeps_the_atom_count(self):
        atoms = [['C1', 'C', 0.1, 0.2, 0.3, 0, 1.0, 0.02],
                 ['C2', 'C', 1.1, -0.8, 0.3, 0, 1.0, 0.02]]
        expanded = _expand_to_unit_cell(atoms, ['x,y,z'], (10.0, 10.0, 10.0, 90.0, 90.0, 90.0))
        assert len(expanded) == 2


class TestHydrogenBonding:
    """Two hydrogens must never be bonded to each other.

    Their covalent-radii cutoff is 1.4 Angstrom, so without this rule a short
    H...H contact — which only arises between the alternative positions of a
    disordered molecule — is taken for a bond and fuses the alternatives.
    """

    CELL = (20.0, 20.0, 20.0, 90.0, 90.0, 90.0)

    def _site(self, element: str, x: float) -> tuple:
        return (element, (x / 20.0, 0.5, 0.5), 1.0, 0)

    def test_two_close_hydrogens_are_not_bonded(self):
        expanded = [self._site('H', 5.0), self._site('H', 6.0)]
        adjacency = _build_bond_graph(expanded, self.CELL)
        assert adjacency[0] == set()

    def test_hydrogen_still_bonds_to_carbon(self):
        expanded = [self._site('C', 5.0), self._site('H', 6.0)]
        adjacency = _build_bond_graph(expanded, self.CELL)
        assert adjacency[0] == {1}

    def test_short_carbon_hydrogen_bond_is_kept(self):
        """Old structures place H as close as 0.7 Angstrom; that bond must survive."""
        expanded = [self._site('O', 5.0), self._site('H', 5.7)]
        adjacency = _build_bond_graph(expanded, self.CELL)
        assert adjacency[0] == {1}


class TestPartsMayBond:
    """Unit tests for the SHELXL PART bonding rule."""

    def test_same_group_may_bond(self):
        assert _parts_may_bond(1, 1) is True

    def test_ordered_atoms_bond_to_everything(self):
        assert _parts_may_bond(0, 0) is True
        assert _parts_may_bond(0, 3) is True
        assert _parts_may_bond(3, 0) is True

    def test_different_non_zero_groups_never_bond(self):
        assert _parts_may_bond(1, 2) is False
        assert _parts_may_bond(2, 1) is False
        assert _parts_may_bond(3, 5) is False

    def test_a_fully_occupied_atom_is_shared_between_parts(self):
        """A pivot atom left inside a PART still bonds to the other PARTs.

        A rotationally disordered CF3 group is often deposited with its carbon
        in PART 1 and the fluorines spread over PARTs 1, 2 and 3.  The carbon is
        fully occupied, so it belongs to every alternative.
        """
        assert _parts_may_bond(1, 2, 1.0, 0.33) is True
        assert _parts_may_bond(2, 1, 0.33, 1.0) is True

    def test_two_partial_atoms_in_different_parts_still_never_bond(self):
        assert _parts_may_bond(1, 2, 0.6, 0.4) is False
        assert _parts_may_bond(1, 2, 0.904, 0.096) is False


class TestFormulaParts:
    def test_counts_become_subscripts(self):
        assert formula_parts('H2 O') == [('H', NORMAL), ('2', SUBSCRIPT), ('O', NORMAL)]

    def test_spaces_between_elements_are_dropped(self):
        assert ''.join(text for text, _style in formula_parts('C12 H22 O11')) == 'C12H22O11'

    def test_charge_becomes_a_superscript(self):
        parts = formula_parts('B F4 1-')
        assert parts[-1] == ('1-', SUPERSCRIPT)
        assert parts[-2] == ('4', SUBSCRIPT)

    def test_moiety_separator_keeps_a_space(self):
        parts = formula_parts('C9 H9 Br Cl N2 1+, B F4 1-')
        assert (', ', NORMAL) in parts
        assert [text for text, style in parts if style == SUPERSCRIPT] == ['1+', '1-']

    def test_leading_multiplier_is_not_a_subscript(self):
        parts = formula_parts('C38 H38 O12, 0.5(C H4 O)')
        assert ('0.5', NORMAL) in parts
        assert ('0.5', SUBSCRIPT) not in parts

    def test_post_multiplier_is_not_a_subscript(self):
        """IUCr example ``(Cd 2+)3`` — the trailing 3 multiplies the whole moiety."""
        parts = formula_parts('(Cd 2+)3')
        assert parts == [('(', NORMAL), ('Cd', NORMAL), ('2+', SUPERSCRIPT),
                         (')', NORMAL), ('3', NORMAL)]

    def test_empty_formula(self):
        assert formula_parts('') == []


class TestFormulaToHtml:
    def test_charges_and_counts(self):
        assert formula_to_html('C9 H9 Br Cl N2 1+, B F4 1-') == (
            '<html><body>'
            'C<sub>9</sub>H<sub>9</sub>BrClN<sub>2</sub><sup>1+</sup>, '
            'BF<sub>4</sub><sup>1-</sup>'
            '</body></html>')

    def test_fractional_multiplier_survives(self):
        assert formula_to_html('C38 H38 O12, 0.5(C H4 O)') == (
            '<html><body>C<sub>38</sub>H<sub>38</sub>O<sub>12</sub>, '
            '0.5(CH<sub>4</sub>O)</body></html>')

    @pytest.mark.parametrize('value', ['', '?', '.', "  '?'  ", '   '])
    def test_missing_values_give_an_empty_string(self, value):
        assert formula_to_html(value) == ''

    def test_multiplier_without_parentheses_keeps_its_space(self):
        """``'2 B F4 1-'`` must not render as ``2BF4``, which reads as a count."""
        assert formula_to_html('2 B F4 1-') == (
            '<html><body>2 BF<sub>4</sub><sup>1-</sup></body></html>')
