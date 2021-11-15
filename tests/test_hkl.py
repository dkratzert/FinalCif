import os
from pathlib import Path
from unittest import TestCase

from finalcif.cif.cif_file_io import CifContainer


class TestHKL(TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.cif1 = CifContainer('tests/examples/1979688.cif')
        self.cif2 = CifContainer('tests/examples/work/cu_BruecknerJK_153F40_0m.cif')
        self.first_result = """data_cu_BruecknerJK_153F40_0m
loop_
_refln_index_h
_refln_index_k
_refln_index_l
_refln_F_squared_meas
_refln_F_squared_sigma
_refln_scale_group_code
1 0 0 0.36031 0.34981 12
-1 0 0 -0.0279 0.03389 7
-1 0 0 0.09539 0.01993 4
2 0 0 267.703 5.73431 4
-"""
        self.last_result = """ 11.9484 0.44464 6
4 -25 5 21.6867 0.78969 3
-4 -25 -5 20.1847 0.67411 2
4 -25 5 23.2039 0.82305 9
0 -26 5 0.50707 0.25345 9
-1 -26 -5 13.2994 0.55025 2
1 -26 5 14.5278 0.78618 9
-1 -26 5 13.3125 0.51513 9
2 -26 5 33.6128 0.98525 9
0 0 0 0.00 0.00 0
"""

    def test_hkl_as_cif_first_lines(self):
        self.assertEqual(self.first_result, self.cif1.hkl_as_cif[:250])

    def test_hkl_as_cif_last_lines(self):
        self.assertEqual(self.last_result, self.cif1.hkl_as_cif[-250:])

    def test_hkl2_as_cif_first_lines(self):
        self.assertEqual(self.first_result, self.cif2.hkl_as_cif[:250])

    def test_hkl2_as_cif_last_lines(self):
        self.assertEqual(self.last_result, self.cif1.hkl_as_cif[-250:])
