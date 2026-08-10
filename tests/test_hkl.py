from pathlib import Path
from unittest import TestCase

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.hkl import calculate_rint

data = Path('tests')


class TestHKL(TestCase):

    def setUp(self) -> None:
        self.cif1 = CifContainer(data / 'examples/1979688.cif')
        self.cif2 = CifContainer(data / 'examples/work/cu_BruecknerJK_153F40_0m.cif')
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


class TestRintCalculation(TestCase):
    """SADABS files contain no overall R(int), it has to be calculated from the reflections."""

    def test_rint_of_a_shelx_hkl_file(self):
        hkl = (data / 'examples/work/p21c.hkl').read_text()
        # SHELXL wrote 0.0302 for the reflections it used:
        self.assertEqual(0.0311, calculate_rint(hkl, 'P 21 21 2'))

    def test_rint_of_the_hkl_data_in_a_cif(self):
        cif = CifContainer(data / 'examples/work/cu_BruecknerJK_153F40_0m.cif')
        self.assertEqual(0.0311, calculate_rint(cif.hkl_file, cif.space_group))

    def test_merged_data_have_no_rint(self):
        hkl = ('   1   0   0 0.36031 0.34981\n'
               '   2   0   0 267.703 5.73431\n'
               '   0   0   0    0.00    0.00\n')
        self.assertIsNone(calculate_rint(hkl, 'P 21 21 2'))

    def test_no_space_group_gives_no_rint(self):
        hkl = (data / 'examples/work/p21c.hkl').read_text()
        self.assertIsNone(calculate_rint(hkl, ''))

    def test_empty_hkl_data_give_no_rint(self):
        self.assertIsNone(calculate_rint('', 'P 21 21 2'))
