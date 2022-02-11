#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

from finalcif.datafiles.p4p_reader import P4PFile


class TestBrukerFrame(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_str(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual(100, p4p.temperature)

    def test_radiation_type(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual('Mo', p4p.radiation_type)

    def test_measure_date(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual('DK_Zucker2_0m.p4p', p4p.filename.name)

    def test_program(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual('C12H22O11', p4p.chem)

    def test_kilovolts_milliamps(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual([7.7133, 8.6559, 10.8082, 90.0, 102.9627, 90.0], p4p.cell)
        self.assertEqual([0.0011, 0.002, 0.0024, 0.0, 0.0089, 0.0, 0.228], p4p.cellsd)

    def test_radiation_type_temperature(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual('colourless', p4p.crystal_color)

    def test_detector_type(self):
        p4p = P4PFile(basename='DK_Zucker2', searchpath=Path('./test-data'))
        self.assertEqual(['0.126', '0.202', '0.303'], p4p.crystal_size)
