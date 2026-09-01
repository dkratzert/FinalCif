"""Robustness tests for moiety formulae of pathological structure models.

The structures in ``test-data/pathological/`` are deliberately awful: whole
molecules disordered without any PART label, alternative positions 0.5 Angstrom
apart, fullerene cages smeared over a dozen disorder groups, deposited sum
formulae that contradict the atom list, and solvent that was squeezed away.
For such models there is no single correct moiety formula — PLATON, the COD
deposit and FinalCif all disagree, and often all three are wrong.

These tests therefore assert *invariants that must hold no matter how bad the
model is*, rather than pinning exact output strings:

* generation never raises and never returns nonsense,
* the result is syntactically valid per the IUCr ``_chemical_formula_moiety``
  rules,
* every multiplier and every element count is positive and finite,
* the moieties use exactly the elements present in the atom list, and
* **mass is conserved**: the moiety formula multiplied by Z reproduces the
  occupancy-weighted content of the unit cell.

The last one is the strong one.  It is what catches a disorder alternative that
was counted twice or a fragment that was silently dropped.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

import pytest

from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.z_from_packing import (_expand_to_unit_cell, _normalize_element,
                                           _split_disorder, count_z_and_zprime)

FIXTURE_DIR = Path('test-data/pathological')

# (file stem, what makes the model pathological, what PLATON reports)
#
# PLATON's answer is recorded for orientation only.  It is not asserted: on
# these models PLATON is sometimes better than us (1508699, 1515019, 1517016),
# sometimes identical (1542256), and sometimes equally lost (1512154, 1514866).
_PATHOLOGICAL_CASES = [
    ('1502416',
     'whole molecule disordered over five PARTs plus dg=0 half-occupancy atoms',
     '2(C31 H24 S12), C7 H3, 2(C7 H8)'),
    ('1503204',
     'dichloromethane smeared over four PARTs, deposited formula has H0.44 O0.22',
     'C189.86 H148 Cl3.72 N16, 0.442(O)'),
    ('1508699',
     'whole molecule disordered at occ=0.5 with no PART labels at all',
     'C15 H23 N O3'),
    ('1512154',
     'three chloroform sites disordered without PART labels',
     '2(C37 H36 O8), 2.5(C H Cl3), 0.5(C Cl2), 0.5(Cl), 0.5(H)'),
    ('1514866',
     'endohedral fullerene over fifteen disorder groups including negative PARTs',
     '2(C73 Sc0.42), 2(C36 H44 N4 Ni), 1.824(C6 H6), 2.616(C3 H3), ...'),
    ('1515019',
     'hexamine cage and nitromethane disordered without PART labels',
     'C22 H28 I4 N8 O8, 4(C H3 N O2)'),
    ('1517016',
     'thiophene rings disordered over negative PARTs, 2% solvent-accessible void',
     'C45 H33 Mn3 N3 O13 S6, C2 H3 N'),
    ('1542256',
     'dichloromethane and water at fractional occupancy, deposited Z disagrees',
     'C42 H42 Cl6 N6 Pd3, 2.145(C H2 Cl2), 0.167(O3), 1.945(O)'),
]

# One element symbol with an optional, possibly fractional, count.
_ELEMENT = re.compile(r'^([A-Z][a-z]?)(\d+(?:\.\d+)?)?$')
# A trailing charge such as '1+' or '2-'.
_CHARGE = re.compile(r'^(\d+)([+-])$')
# A leading multiplier such as '2(' or '0.75('.
_MULTIPLIER = re.compile(r'^(\d+(?:\.\d+)?)\((.*)\)$')


class ParsedMoiety:
    """One moiety of a ``_chemical_formula_moiety`` string."""

    def __init__(self, multiplier: float, composition: dict[str, float], charge: int) -> None:
        self.multiplier = multiplier
        self.composition = composition
        self.charge = charge


def parse_moiety_formula(formula: str) -> list[ParsedMoiety]:
    """Parse *formula*, raising ``AssertionError`` on any syntax violation.

    Implements the grammar of the IUCr core dictionary: moieties separated by
    commas, elements separated by spaces within a moiety, an optional
    multiplier in front of a parenthesised moiety, and an optional charge at the
    end separated from the last element by a space.
    """
    assert formula, 'empty moiety formula'
    assert '((' not in formula, f'nested parentheses in {formula!r}'
    moieties = []
    for chunk in formula.split(','):
        text = chunk.strip()
        assert text, f'empty moiety in {formula!r}'
        multiplier = 1.0
        match = _MULTIPLIER.match(text)
        if match:
            multiplier = float(match.group(1))
            text = match.group(2)
        assert '(' not in text and ')' not in text, f'stray parenthesis in {chunk!r}'

        tokens = text.split()
        assert tokens, f'moiety without elements in {chunk!r}'
        charge = 0
        charge_match = _CHARGE.match(tokens[-1])
        if charge_match:
            charge = int(charge_match.group(1))
            if charge_match.group(2) == '-':
                charge = -charge
            tokens = tokens[:-1]
        assert tokens, f'moiety with only a charge in {chunk!r}'

        composition: dict[str, float] = {}
        for token in tokens:
            element_match = _ELEMENT.match(token)
            assert element_match, f'invalid element token {token!r} in {chunk!r}'
            element = element_match.group(1)
            assert element not in composition, f'element {element} repeated in {chunk!r}'
            composition[element] = float(element_match.group(2) or 1)
        moieties.append(ParsedMoiety(multiplier, composition, charge))
    return moieties


def unit_cell_content(cif: CifContainer) -> dict[str, float]:
    """Return the occupancy-weighted element counts of the whole unit cell.

    Atoms in a negative SHELXL PART sit on a special position and are not
    symmetry-expanded, but they are still generated by every symmetry
    operation; their occupancy already accounts for the sharing on that special
    position.  Their unit-cell contribution is therefore ``occupancy × n_symmops``,
    which is what the generator uses as well.  Verified against the deposited
    ``_chemical_formula_sum × Z`` of these fixtures.
    """
    regular, special = _split_disorder(list(cif.atoms_fract))
    n_symmops = max(1, len(list(cif.symmops)))
    content: Counter[str] = Counter()
    for atom in _expand_to_unit_cell(regular, cif.symmops, cif.cell[:6]):
        content[_normalize_element(atom[0])] += atom[2]
    for atom in special:
        content[_normalize_element(atom[1])] += float(atom[6]) * n_symmops
    return dict(content)


def _load(stem: str) -> CifContainer:
    return CifContainer(FIXTURE_DIR / f'{stem}.cif')


def _result(stem: str):
    cif = _load(stem)
    return cif, count_z_and_zprime(cif.atoms_fract, cif.symmops, cif.cell[:6],
                                   formula_sum=cif['_chemical_formula_sum'])


@pytest.mark.parametrize('stem, description, platon_reference', _PATHOLOGICAL_CASES,
                         ids=[case[0] for case in _PATHOLOGICAL_CASES])
class TestPathologicalModels:
    """Invariants that must hold however bad the deposited model is."""

    def test_generation_succeeds(self, stem, description, platon_reference):
        _cif, result = _result(stem)
        assert result.moiety_formula, f'no moiety formula for a {description}'

    def test_z_is_a_positive_integer(self, stem, description, platon_reference):
        _cif, result = _result(stem)
        assert isinstance(result.z, int)
        assert result.z >= 1

    def test_formula_is_syntactically_valid(self, stem, description, platon_reference):
        _cif, result = _result(stem)
        parse_moiety_formula(result.moiety_formula)

    def test_multipliers_are_positive_and_finite(self, stem, description, platon_reference):
        _cif, result = _result(stem)
        for moiety in parse_moiety_formula(result.moiety_formula):
            assert math.isfinite(moiety.multiplier)
            assert moiety.multiplier > 0

    def test_element_counts_are_positive_and_finite(self, stem, description, platon_reference):
        _cif, result = _result(stem)
        for moiety in parse_moiety_formula(result.moiety_formula):
            for element, count in moiety.composition.items():
                assert math.isfinite(count), f'{element} count is not finite'
                assert count > 0, f'{element} count is not positive'

    def test_charges_are_plausible(self, stem, description, platon_reference):
        """No moiety may carry an absurd charge, and the cell must stay neutral."""
        _cif, result = _result(stem)
        moieties = parse_moiety_formula(result.moiety_formula)
        for moiety in moieties:
            assert abs(moiety.charge) <= 8
        total = sum(moiety.multiplier * moiety.charge for moiety in moieties)
        assert abs(total) < 0.02, f'unit cell is not electrically neutral: {total}'

    def test_only_elements_that_are_present_are_reported(self, stem, description,
                                                         platon_reference):
        cif, result = _result(stem)
        present = {_normalize_element(atom[1]) for atom in cif.atoms_fract}
        reported = {element
                    for moiety in parse_moiety_formula(result.moiety_formula)
                    for element in moiety.composition}
        assert reported <= present, f'invented elements: {sorted(reported - present)}'

    def test_mass_is_conserved(self, stem, description, platon_reference):
        """``moiety × Z`` must reproduce the content of the unit cell.

        This is the invariant that catches a disorder alternative counted twice
        or a fragment dropped on the floor, and it holds no matter how poor the
        underlying structure model is.

        The tolerance only has to absorb the rounding the generator applies to
        multipliers and element counts.  Across these eight models the worst
        real deviation is 0.016 atoms (0.24 %), so the limits below leave a
        comfortable margin while still failing if a whole moiety goes missing.
        """
        cif, result = _result(stem)
        expected = unit_cell_content(cif)
        produced: Counter[str] = Counter()
        for moiety in parse_moiety_formula(result.moiety_formula):
            for element, count in moiety.composition.items():
                produced[element] += moiety.multiplier * count

        for element, count in expected.items():
            tolerance = max(0.05, 0.005 * count)
            assert abs(produced[element] * result.z - count) <= tolerance, (
                f'{element}: unit cell has {count:.2f}, '
                f'moiety implies {produced[element] * result.z:.2f}'
            )

    def test_result_is_deterministic(self, stem, description, platon_reference):
        _cif, first = _result(stem)
        _cif2, second = _result(stem)
        assert first.moiety_formula == second.moiety_formula
        assert first.z == second.z


class TestKnownCorrectAnswers:
    """Cases in this directory whose chemistry is unambiguous.

    These three were shredded until the symmetry expansion learnt to wrap
    fractional coordinates into ``[0, 1)``.  Deposited coordinates outside that
    range (1515019 has y = 1.063) made the symmetry copies of one molecule span
    three cells, which the ±1 image search of the bond graph cannot bridge.
    """

    def _moiety(self, stem: str) -> str:
        _cif, result = _result(stem)
        return result.moiety_formula

    def test_hexamine_iodosuccinimide_nitromethane(self):
        """1515019 — visibly a hexamine cage, N-iodosuccinimide and nitromethane.

        Matches the COD deposit.  PLATON fuses the cage with the succinimide
        into ``'C22 H28 I4 N8 O8, 4(C H3 N O2)'`` through the I...N halogen bond.
        """
        assert self._moiety('1515019') == 'C6 H12 N4, 4(C4 H4 I N O2), 4(C H3 N O2)'

    def test_whole_molecule_disordered_without_part_labels(self):
        """1508699 — every atom at occ=0.5 and dg=0; PLATON agrees."""
        assert self._moiety('1508699') == 'C15 H23 N O3'

    def test_three_chloroform_solvates(self):
        """1512154 — matches the COD deposit; PLATON splits the chloroform."""
        assert self._moiety('1512154') == '2(C37 H36 O8), 3(C H Cl3)'


class TestParseMoietyFormula:
    """The grammar checker used above must itself reject invalid strings."""

    def test_simple_formula(self):
        parsed = parse_moiety_formula('C10 H8 N2')
        assert len(parsed) == 1
        assert parsed[0].composition == {'C': 10, 'H': 8, 'N': 2}
        assert parsed[0].multiplier == 1
        assert parsed[0].charge == 0

    def test_charge_and_multiplier(self):
        parsed = parse_moiety_formula('C18 H18 N4 2+, 2(B F4 1-)')
        assert parsed[0].charge == 2
        assert parsed[1].multiplier == 2
        assert parsed[1].charge == -1
        assert parsed[1].composition == {'B': 1, 'F': 4}

    def test_fractional_counts_and_multipliers(self):
        parsed = parse_moiety_formula('C42 H42 Cl6, 2.145(C H2 Cl2), 0.1666(O3)')
        assert parsed[1].multiplier == pytest.approx(2.145)
        assert parsed[2].composition == {'O': 3}

    @pytest.mark.parametrize('invalid', [
        '',
        'C10, ',
        'c10 h8',
        '2((C10))',
        'C10 H8 (N2',
        '1+',
        'C10 H8 N2 N3',
    ])
    def test_invalid_strings_are_rejected(self, invalid):
        with pytest.raises(AssertionError):
            parse_moiety_formula(invalid)
