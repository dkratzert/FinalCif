from unittest import TestCase

from docx import Document

from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.report_text import Hydrogens, MachineType


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
