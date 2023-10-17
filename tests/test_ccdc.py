#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer
from finalcif.datafiles.ccdc_mail import CCDCMail

data = Path('.')


class TestCCDC(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(file=data / 'tests/examples/work/cu_BruecknerJK_153F40_0m.cif')

    def test_ccdc_num(self):
        ccdc = CCDCMail(self.cif)
        self.assertEqual(1979688, ccdc.depnum)
        self.assertEqual('CCDC Depository Request.eml', ccdc.emlfile.name)


class TestCCDCnoMail(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer(file=data / 'test-data/DK_Zucker2_0m.cif')

    def test_ccdc_num(self):
        ccdc = CCDCMail(self.cif)
        self.assertEqual(0, ccdc.depnum)
        self.assertEqual('', ccdc.emlfile.name)

    def test_same_cell(self):
        ccdc = CCDCMail(self.cif)
        self.assertEqual(True, ccdc.is_same_cell(self.cif, [7.716, 8.664, 10.812]))
