from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.hkl import HKL, Limit, calculate_rint, reference_domain

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


class TestHKLParsing(TestCase):
    reflections = '   1  -2   3   10.00    1.00\n  -4   5  -6   20.00    2.00\n'
    footer = "_computing_structure_solution 'SHELXT 2014/4 (Sheldrick, 2014)'\n"
    limits = Limit(h_max=1, h_min=-4, k_max=5, k_min=-2, l_max=3, l_min=-6)

    def test_footer_without_zero_reflection_is_not_added_to_loop(self):
        hkl = HKL(self.reflections + '\n' + self.footer, 'test')
        loop = hkl.block.find_loop('_refln_index_h').get_loop()
        self.assertEqual(2, loop.length())
        self.assertEqual(5, loop.width())
        self.assertNotIn('_computing_structure_solution', hkl.hkl_as_cif)
        self.assertEqual(self.limits, hkl.get_hkl_min_max())

    def test_single_reflection_defines_loop_width_not_footer(self):
        hkl = HKL(self.reflections.splitlines()[0] + '\n' + self.footer.rstrip() + ' extra\n', 'test')
        loop = hkl.block.find_loop('_refln_index_h').get_loop()
        self.assertEqual(5, loop.width())
        self.assertEqual(1, loop.length())

    def test_hklf3_keeps_amplitude_columns(self):
        hkl = HKL(self.reflections + self.footer, 'test', hklf_type=3)
        self.assertEqual(['10.00', '20.00'], list(hkl.block.find_loop('_refln_F_meas')))
        self.assertEqual(['1.00', '2.00'], list(hkl.block.find_loop('_refln_F_sigma')))
        self.assertEqual(self.limits, hkl.get_hkl_min_max())

    def test_six_column_reflections_keep_batch_numbers(self):
        reflections = ''.join(line + '   2\n' for line in self.reflections.splitlines())
        hkl = HKL(reflections + self.footer, 'test')
        self.assertEqual(['2', '2'], list(hkl.block.find_loop('_refln_scale_group_code')))
        self.assertEqual(self.limits, hkl.get_hkl_min_max())

    def test_zero_reflection_with_extra_batch_stops_before_footer(self):
        hkl = HKL(self.reflections + '   0   0   0    0.00    0.00   0\n'
                  + self.footer + '  99  99  99   99.00    1.00\n', 'test')
        self.assertEqual(3, hkl.block.find_loop('_refln_index_h').get_loop().length())
        self.assertEqual(self.limits, hkl.get_hkl_min_max())

    def test_empty_lines_before_first_reflection_are_skipped(self):
        hkl = HKL('\n  \n' + self.reflections + self.footer, 'test')
        self.assertEqual(2, hkl.block.find_loop('_refln_index_h').get_loop().length())
        self.assertEqual(self.limits, hkl.get_hkl_min_max())

    def test_invalid_reflection_ends_hkl_data(self):
        for invalid in ('bad 1 2 10.00 1.00', '1 bad 2 10.00 1.00', '1 2 bad 10.00 1.00',
                        '1 2 3 bad 1.00', '1 2 3 10.00 bad', '1 2'):
            with self.subTest(invalid=invalid):
                with patch('builtins.print') as warning:
                    hkl = HKL(self.reflections + invalid + '\n   7   8   9   10.00    1.00\n', 'test')
                warning.assert_called_once()
                self.assertIn('HKL data ends at invalid line 3:', warning.call_args.args[0])
                self.assertEqual(2, hkl.block.find_loop('_refln_index_h').get_loop().length())
                self.assertEqual(self.limits, hkl.get_hkl_min_max())

    def test_missing_reflections_raise_explicit_error(self):
        for content in ('', '\n', self.footer):
            with self.subTest(content=content):
                with self.assertRaisesRegex(ValueError, 'No valid HKL reflections found'):
                    HKL(content, 'test')

    def test_loading_cif_with_hkl_footer_calculates_limits(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'hkl_footer.cif'
            path.write_text('data_test\n_shelx_hkl_file\n;\n' + self.reflections + self.footer + ';\n',
                            encoding='ascii', newline='\n')
            cif = CifContainer(path)
            for field, value in self.limits._asdict().items():
                self.assertEqual(str(value), cif['_diffrn_reflns_limit_' + field])
            self.assertEqual((self.reflections + self.footer).strip(), cif.hkl_file.strip())
            self.assertNotIn('_computing_structure_solution', cif.hkl_as_cif)


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
