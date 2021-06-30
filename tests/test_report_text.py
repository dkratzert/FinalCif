from unittest import TestCase

from docx import Document

from cif.cif_file_io import CifContainer
from report.report_text import Hydrogens


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
