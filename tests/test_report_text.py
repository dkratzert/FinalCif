import unittest
from unittest import TestCase
from unittest.mock import Mock

from docx import Document
from docx.text.paragraph import Paragraph

from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.report_text import Hydrogens, MachineType, Crystallization, CrystalSelection, DataCollection


class MyMock(Mock):
    def __repr__(self):
        return 'mocked_block_name'


class CifMock:
    def __init__(self, cif=None):
        self.cif = cif
        self.block = MyMock()

    def __getitem__(self, item):
        return self.cif.get(item)


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


class TestTextParagraphs(unittest.TestCase):

    def setUp(self) -> None:
        document = Document()
        self.paragraph: Paragraph = document.add_paragraph()

    def test_crystallization(self):
        cif = {'_exptl_crystal_recrystallization_method': 'The compound was crystallized '
                                                          'from water by evaporation at 25 °C.'}
        # noinspection PyTypeChecker
        Crystallization(cif, paragraph=self.paragraph)
        self.assertEqual('The compound was crystallized from water by evaporation at 25 °C. ', self.paragraph.text)

    def test_empty_crystallization(self):
        cif = {'_exptl_crystal_recrystallization_method': ''}
        # noinspection PyTypeChecker
        Crystallization(cif, paragraph=self.paragraph)
        self.assertEqual(("[No _exptl_crystal_recrystallization_method like 'The compound was "
                          "crystallized from methanol by evaporation at 25 °C.' was given]. "), self.paragraph.text)

    def test_crystallization_with_a_newline_in_the_input(self):
        cif = {'_exptl_crystal_recrystallization_method': 'The compound was crystallized\n'
                                                          'from water by evaporation at 25 °C.'}
        # noinspection PyTypeChecker
        Crystallization(cif, paragraph=self.paragraph)
        # The formatting of gstr should always turn a newline into a space char:
        self.assertEqual('The compound was crystallized from water by evaporation at 25 °C. ', self.paragraph.text)

    def test_crystal_selection(self):
        data = {'_exptl_crystal_description'          : 'block',
                '_exptl_crystal_colour'               : 'yellow',
                '_diffrn_measurement_specimen_support': 'Nylon loop'}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A yellow, block shaped crystal of mocked_block_name was mounted on a Nylon '
                          'loop with perfluoroether oil. '), self.paragraph.text)

    def test_crystal_selection_empty(self):
        data = {'_exptl_crystal_description'          : '',
                '_exptl_crystal_colour'               : '',
                '_diffrn_measurement_specimen_support': ''}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A [No _exptl_crystal_description given] shaped crystal of mocked_block_name '
                          'was mounted on a [No _diffrn_measurement_specimen_support given] with '
                          'perfluoroether oil. '), self.paragraph.text)

    def test_data_collection(self):
        cif = {'_diffrn_ambient_temperature': '100(2)'}
        # noinspection PyTypeChecker
        DataCollection(cif, paragraph=self.paragraph)
        self.assertEqual('Data were collected from a shock-cooled single crystal at 100(2)\xa0K', self.paragraph.text)

    def test_data_collection_empty(self):
        cif = {'_diffrn_ambient_temperature': ''}
        # noinspection PyTypeChecker
        DataCollection(cif, paragraph=self.paragraph)
        self.assertEqual(('Data were collected from a single crystal at [No _diffrn_ambient_temperature '
                          'given]\xa0K'), self.paragraph.text)

    def test_machine_type_empty(self):
        cif = {
            '_diffrn_measurement_device_type'                    : '',
            '_diffrn_measurement_device'                         : '',
            '_diffrn_source'                                     : '',
            '_diffrn_radiation_monochromator'                    : '',
            '_olex2_diffrn_ambient_temperature_device'           : '',
            '_diffrn_measurement_ambient_temperature_device_make': '',
            '_diffrn_radiation_type'                             : '',
            '_diffrn_radiation_wavelength'                       : '',
            '_diffrn_detector_type'                              : '',
        }
        # noinspection PyTypeChecker
        MachineType(cif, paragraph=self.paragraph)
        self.assertEqual(('on a [No _diffrn_measurement_device_type given] [No '
                          '_diffrn_measurement_device given] with a [No _diffrn_source given] using a '
                          '[No _diffrn_radiation_monochromator given] as monochromator and a [No '
                          '_diffrn_detector_type given] detector. The diffractometer was equipped with '
                          'a low temperature device and used [No _diffrn_radiation_type given] '
                          'radiation (λ = [No _diffrn_radiation_wavelength given]\xa0Å). '), self.paragraph.text)

    def test_machine_type_1(self):
        cif = {
            '_diffrn_measurement_device_type'                    : 'Bruker Foo Bar  ',
            '_diffrn_measurement_device'                         : 'four-circle diffractometer',
            '_diffrn_source'                                     : 'sealed X-ray tube',
            '_diffrn_radiation_monochromator'                    : 'Ge 220',
            '_olex2_diffrn_ambient_temperature_device'           : '',
            '_diffrn_measurement_ambient_temperature_device_make': 'Oxford Cryostream 800',
            '_diffrn_radiation_type'                             : 'Cu Kα',
            '_diffrn_radiation_wavelength'                       : '1.54178',
            '_diffrn_detector_type'                              : 'Photon X',
        }
        # noinspection PyTypeChecker
        MachineType(cif, paragraph=self.paragraph)
        self.assertEqual(('on a Bruker Foo Bar four-circle diffractometer with a sealed X-ray tube '
                          'using a Ge 220 as monochromator and a Photon X detector. The diffractometer '
                          'was equipped with an Oxford Cryostream 800 low temperature device and used '
                          'Cu Kα radiation (λ = 1.54178\xa0Å). '), self.paragraph.text)
