from unittest import TestCase

from docx import Document

from cif.cif_file_io import CifContainer
from report.report_text import Hydrogens, MachineType


class TestHydrogens(TestCase):
    def setUp(self) -> None:
        document = Document()
        self.paragraph = document.add_paragraph()

    def test_has_no_isotropic_displacement_parameters(self):
        cif = CifContainer('test-data/p21c.cif')
        h = Hydrogens(cif, self.paragraph)
        self.assertEqual(0, h.number_of_isotropic_atoms())

    def test_has_isotropic_displacement_parameters(self):
        cif = CifContainer('test-data/1923_Aminoff, G._Ni As_P 63.m m c_Nickel arsenide.cif')
        h = Hydrogens(cif, self.paragraph)
        self.assertEqual(2, h.number_of_isotropic_atoms())


class TestMachineType(TestCase):

    def test__get_cooling_device_iucr(self):
        cif = CifContainer('tests/statics/temp_device_iucr.cif')
        self.assertEqual('Oxford Cryostream 850 ', MachineType._get_cooling_device(cif))

    def test__get_cooling_device_olx(self):
        cif = CifContainer('tests/statics/temp_device_olx.cif')
        self.assertEqual('Oxford Cryostream 810 ', MachineType._get_cooling_device(cif))

    def test__get_cooling_device_both(self):
        cif = CifContainer('tests/statics/temp_device_both.cif')
        self.assertEqual('Oxford Cryostream 900 ', MachineType._get_cooling_device(cif))

    def test__get_no_cooling_device(self):
        cif = CifContainer('tests/statics/temp_no_device.cif')
        self.assertEqual('', MachineType._get_cooling_device(cif))
