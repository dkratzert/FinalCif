import unittest

from finalcif.gui.validators import validators


class TestValidators(unittest.TestCase):
    def test_integer_limits(self):
        v = validators['_chemical_melting_point']
        self.assertTrue(v.valid('5'))
        self.assertFalse(v.valid('-5'))
        self.assertEqual('Must be a positive decimal number between 0.0 and 5000.0.', v.help_text)

    def test_diffrn_reflns_limit_h_min(self):
        v = validators['_diffrn_reflns_limit_h_min']
        self.assertEqual('Integerlimits', v.__class__.__name__)
        self.assertTrue(v.valid('-5'))
        self.assertFalse(v.valid('5'))
        self.assertFalse(v.valid('-5.0'))
        self.assertEqual("Must be a negative integer number between -inf and 0.", v.help_text)

    def test_diffrn_reflns_Laue_measured_fraction_max(self):
        v = validators['_diffrn_reflns_Laue_measured_fraction_max']
        self.assertFalse(v.valid('-5'))
        self.assertEqual('Floatlimits', v.__class__.__name__)
        self.assertEqual('Must be a positive decimal number between 0.0 and 1.0.', v.help_text)

    def test_refine_ls_number_restraints(self):
        v = validators['_refine_ls_number_restraints']
        self.assertFalse(v.valid('-5'))
        self.assertEqual("Must be a positive integer number between 0 and inf.", v.help_text)

    def test_atom_type_scat_dispersion_real(self):
        v = validators['_atom_type_scat_dispersion_real']
        self.assertTrue(v.valid('-5'))
        self.assertTrue(v.valid('5'))
        self.assertEqual('Must be a decimal number between -inf and inf.', v.help_text)

    def test_space_group_crystal_system(self):
        v = validators['_space_group_crystal_system']
        self.assertTrue(v.valid('Triclinic'))
        self.assertFalse(v.valid('Tsdsfgf'))
        self.assertEqual('Textlimits', v.__class__.__name__)
        self.assertEqual("Must be one of: triclinic, monoclinic, orthorhombic, "
                         "tetragonal, trigonal, hexagonal, cubic.", v.help_text)


if __name__ == '__main__':
    unittest.main()
