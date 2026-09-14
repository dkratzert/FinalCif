#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   Dr. Daniel Kratzert
#   ----------------------------------------------------------------------------
import unittest

from finalcif.tools.solvents import ALIASES, SOLVENTS, resolve_solvent, solvent_names
from finalcif.tools.squeeze import electrons_from_formula, resolve_formula


class TestResolveSolvent(unittest.TestCase):

    def test_canonical_name(self):
        self.assertEqual('C4H8O', resolve_solvent('tetrahydrofuran'))

    def test_alias(self):
        self.assertEqual('C4H8O', resolve_solvent('thf'))

    def test_case_insensitive(self):
        self.assertEqual('C7H8', resolve_solvent('ToLuEnE'))

    def test_whitespace_insensitive(self):
        self.assertEqual('C4H10O', resolve_solvent('  diethyl   ether '))

    def test_underscores(self):
        self.assertEqual('C2H6OS', resolve_solvent('dimethyl_sulfoxide'))

    def test_unknown_name(self):
        self.assertIsNone(resolve_solvent('unobtainium'))

    def test_empty(self):
        self.assertIsNone(resolve_solvent(''))

    def test_all_aliases_point_to_known_solvent(self):
        for alias, canonical in ALIASES.items():
            self.assertIn(canonical, SOLVENTS, f'{alias} points to unknown {canonical}')

    def test_solvent_names_contains_names_and_aliases(self):
        names = solvent_names()
        self.assertIn('toluene', names)
        self.assertIn('thf', names)
        self.assertEqual(sorted(names), names)


class TestResolveFormula(unittest.TestCase):

    def test_plain_name(self):
        self.assertEqual('C4H8O', resolve_formula('thf'))

    def test_name_with_space_multiplier(self):
        self.assertEqual('2(C4H8O)', resolve_formula('2 thf'))

    def test_name_with_parentheses_multiplier(self):
        self.assertEqual('2(C4H8O)', resolve_formula('2(thf)'))

    def test_multiplier_one_is_dropped(self):
        self.assertEqual('H2O', resolve_formula('1 water'))

    def test_formula_unchanged(self):
        self.assertEqual('C4H8O', resolve_formula('C4H8O'))

    def test_squeeze_formula_unchanged(self):
        self.assertEqual('2(H2O)', resolve_formula('2(H2O)'))

    def test_anion_unchanged(self):
        self.assertEqual('1 PF6-', resolve_formula('1 PF6-'))

    def test_empty_unchanged(self):
        self.assertEqual('', resolve_formula(''))


class TestElectronsFromSolventName(unittest.TestCase):

    def test_water_name(self):
        self.assertEqual(10, electrons_from_formula('water'))

    def test_two_thf(self):
        # C4H8O: 4*6 + 8*1 + 8 = 40
        self.assertEqual(80, electrons_from_formula('2(thf)'))

    def test_two_thf_space(self):
        self.assertEqual(80, electrons_from_formula('2 thf'))

    def test_toluene(self):
        # C7H8: 7*6 + 8 = 50
        self.assertEqual(50, electrons_from_formula('toluene'))


if __name__ == '__main__':
    unittest.main()
