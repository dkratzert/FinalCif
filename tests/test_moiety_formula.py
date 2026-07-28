"""Tests for charge-aware moiety formula generation.

The expected strings follow the IUCr ``_chemical_formula_moiety`` rules:
moieties separated by ``', '``, elements in Hill order separated by spaces,
and the charge appended after a space (``'B F4 1-'``).  A multiplier other
than one wraps the whole moiety in parentheses (``'2(N O3 1-)'``).
"""
from pathlib import Path
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
from finalcif.tools.sumformula import NORMAL, SUBSCRIPT, SUPERSCRIPT, formula_parts, formula_str_to_dict
from finalcif.tools.z_from_packing import count_z_and_zprime, moiety_formula_from_components


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
        assert result == 'H2 O, N 1+, Cl 1-'

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
        """Esser_JW367_0m: organic cation + BF4- anion (P 2₁/n, Z=4)."""
        assert self._moiety('tests/examples/Esser_JW367_0m.cif') == 'C9 H9 Br Cl N2 1+, B F4 1-'

    def test_tetracycline_hydrochloride(self):
        """1000006: protonated dimethylamino group + chloride."""
        assert self._moiety('test-data/1000006.cif') == 'C22 H25 N2 O8 1+, Cl 1-'

    def test_neutral_molecule_gets_no_charge(self):
        assert self._moiety('test-data/DK_ML7-66-final.cif') == 'C23 H21 N O'

    def test_solvate_keeps_the_per_formula_unit_multiplier(self):
        """Half a methanol per molecule, so the moiety still sums to the sum formula."""
        assert self._moiety('tests/examples/1979688.cif') == 'C38 H38 O12, 0.5(C H4 O)'

    def test_sucrose_is_neutral(self):
        assert self._moiety('test-data/DK_Zucker2_0m.cif') == 'C12 H22 O11'


# ---------------------------------------------------------------------------
# Regression fixtures taken from the Crystallography Open Database
# ---------------------------------------------------------------------------

# Each entry reproduces both the deposited _chemical_formula_moiety and
# _cell_formula_units_Z of the COD structure exactly.
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
