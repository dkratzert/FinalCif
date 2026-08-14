from pathlib import Path
from unittest import TestCase

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.hkl import calculate_rint, reference_domain

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

    def setUp(self) -> None:
        # The .hkl files are not part of the repository, thus the reflections come from a CIF:
        self.hkl = CifContainer(data / 'examples/work/cu_BruecknerJK_153F40_0m.cif').hkl_file

    def test_rint_of_a_shelx_hkl_file(self):
        # This is exactly the value SHELXL wrote into the CIF:
        self.assertEqual(0.0302, calculate_rint(self.hkl, 'P 21 21 2'))

    def test_rint_of_the_hkl_data_in_a_cif(self):
        cif = CifContainer(data / 'examples/work/cu_BruecknerJK_153F40_0m.cif')
        self.assertEqual('0.0302', cif['_diffrn_reflns_av_R_equivalents'])
        self.assertEqual(0.0302, calculate_rint(cif.hkl_file, cif.space_group))

    def test_friedel_opposites_are_only_merged_in_centrosymmetric_groups(self):
        centrosymmetric = calculate_rint(self.hkl, 'P -1')
        self.assertNotEqual(centrosymmetric, calculate_rint(self.hkl, 'P 21 21 2'))

    def test_resolution_limits_of_a_shel_instruction_are_applied(self):
        cell = (5.7859, 12.545, 13.3116, 90.0, 90.0, 90.0)
        self.assertNotEqual(calculate_rint(self.hkl, 'P 21 21 2'),
                            calculate_rint(self.hkl, 'P 21 21 2', cell=cell, resolution=(999.0, 0.9)))

    def test_merged_data_have_no_rint(self):
        hkl = ('   1   0   0 0.36031 0.34981\n'
               '   2   0   0 267.703 5.73431\n'
               '   0   0   0    0.00    0.00\n')
        self.assertIsNone(calculate_rint(hkl, 'P 21 21 2'))

    def test_no_space_group_gives_no_rint(self):
        self.assertIsNone(calculate_rint(self.hkl, ''))

    def test_unknown_space_group_gives_no_rint(self):
        self.assertIsNone(calculate_rint(self.hkl, 'Foo 42'))

    def test_empty_hkl_data_give_no_rint(self):
        self.assertIsNone(calculate_rint('', 'P 21 21 2'))


class TestRintOfTwinnedData(TestCase):
    """
    SHELXL writes no R(int) for HKLF 5 data. Like Olex2, FinalCif calculates it from the singly
    indexed reflections of the reference domain; composite reflections have no equivalents.
    """

    @staticmethod
    def _hkl(*reflections: tuple[int, int, int, float, float, int]) -> str:
        return '\n'.join('{:4d}{:4d}{:4d}{:8.2f}{:8.2f}{:4d}'.format(*x) for x in reflections) + '\n'

    def setUp(self) -> None:
        self.hkl = self._hkl(
            # Singles of domain 1:
            (1, 0, 0, 100.0, 1.0, 1),
            (-1, 0, 0, 110.0, 1.0, 1),
            (0, 1, 0, 200.0, 1.0, 1),
            (0, -1, 0, 200.0, 1.0, 1),
            # A composite reflection of both domains:
            (2, 0, 0, 500.0, 1.0, -1),
            (2, 0, 0, 500.0, 1.0, 2),
            # Singles of domain 2:
            (1, 0, 0, 300.0, 1.0, 2),
            (-1, 0, 0, 330.0, 1.0, 2),
            (0, 0, 0, 0.0, 0.0, 0),
        )

    def test_rint_of_the_domain_with_the_most_singles(self):
        # (|100-105| + |110-105|) / (100 + 110 + 200 + 200)
        self.assertEqual(0.0164, calculate_rint(self.hkl, 'P -1', hklf=5))

    def test_reference_domain_of_a_twst_instruction(self):
        # (|300-315| + |330-315|) / (300 + 330)
        self.assertEqual(0.0476, calculate_rint(self.hkl, 'P -1', hklf=5, twst=2))

    def test_composite_reflections_are_only_included_without_batch_numbers(self):
        without_batches = '\n'.join(x[:28] for x in self.hkl.splitlines())
        self.assertNotEqual(calculate_rint(self.hkl, 'P -1', hklf=5),
                            calculate_rint(without_batches, 'P -1', hklf=4))

    def test_negative_batch_numbers_are_recognized_without_a_hklf_instruction(self):
        self.assertEqual(calculate_rint(self.hkl, 'P -1', hklf=5),
                         calculate_rint(self.hkl, 'P -1', hklf=4))

    def test_data_without_singles_give_no_rint(self):
        hkl = self._hkl((1, 0, 0, 100.0, 1.0, -1),
                        (1, 0, 0, 110.0, 1.0, 2),
                        (0, 0, 0, 0.0, 0.0, 0))
        self.assertIsNone(calculate_rint(hkl, 'P -1', hklf=5))

    def test_reference_domain_is_the_one_with_the_most_singles(self):
        self.assertEqual(1, reference_domain(self.hkl))

    def test_no_reference_domain_without_reflections(self):
        self.assertIsNone(reference_domain(''))
