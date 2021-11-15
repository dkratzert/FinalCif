from unittest import TestCase

from finalcif.tools.settings import FinalCifSettings


class TestFinalCifSettings(TestCase):

    def setUp(self) -> None:
        self.s = FinalCifSettings()

    def test_load_property_values_by_key(self):
        result = [(0, ''), (1, 'N~2~'), (2, 'He'), (3, 'vacuum'), (4, 'mother liquor'), (5, 'Ar'), (6, 'H~2~')]
        self.assertEqual(result, self.s.load_property_values_by_key('_diffrn_ambient_environment'))

    def test_load_cif_keys_of_properties(self):
        self.assertEqual(['_cell_measurement_temperature', '_exptl_crystal_colour'],
                         self.s.load_cif_keys_of_properties()[:2])

    def test_load_property_values_by_key_empty(self):
        self.assertEqual([(0, '')], self.s.load_property_values_by_key(''))
