#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

from finalcif.datafiles.sadabs import Sadabs


class TestSADABSWU19(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = Path('test-data')
        self.s = Sadabs(r'IK_WU19.abs', searchpath=self.test_data)  # this is a sadabs file

    def test_twincomp(self):
        self.assertEqual(1, self.s.twin_components)

    def test_hkl_file(self):
        self.assertEqual('IK_WU19_0m.hkl', self.s.dataset(0).hklfile)

    def test_rint(self):
        # SADABS has no overall R(int), only wR2(int) of the parameter refinement:
        self.assertIsNone(self.s.Rint)
        self.assertEqual(0.0472, self.s.wR2int)

    def test_no_statistics_blocks(self):
        # A SADABS file has no 'Statistics for ...' blocks, only per scan values:
        self.assertEqual([], self.s.statistics)

    def test_point_group_of_the_scaling(self):
        self.assertEqual('2/m', self.s.equivalents_point_group)

    def test_transmission(self):
        self.assertEqual('min: 0.7135, max: 0.7459', str(self.s.dataset(0).transmission))

    def test_version(self):
        self.assertEqual('SADABS-2016/2 - Bruker AXS area detector scaling and absorption correction: Krause, L., '
                         'Herbst-Irmer, R., Sheldrick G.M. & Stalke D., J. Appl. Cryst. 48 (2015) 3-10',
                         self.s.version)

    def test_written_reflections(self):
        self.assertEqual(152800, self.s.dataset(0).written_reflections)


class TestTWINABS(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = Path('test-data')
        self.s = Sadabs(r'twin-4-5.abs', searchpath=self.test_data)  # this is a twinabs file

    def test_transmission(self):
        self.assertEqual([0.794433, 0.86207], [self.s.dataset(0).transmission.tmin, self.s.dataset(0).transmission.tmax])
        self.assertEqual([0.793942, 0.862070], [self.s.dataset(1).transmission.tmin, self.s.dataset(1).transmission.tmax])

    def test_rint(self):
        self.assertEqual(0.0456, self.s.Rint)

    def test_hklfile(self):
        self.assertEqual('twin4.hkl', self.s.dataset(0).hklfile)
        self.assertEqual('twin5.hkl', self.s.dataset(1).hklfile)

    def test_twin_components(self):
        self.assertEqual(2, self.s.twin_components)

    def test_version(self):
        self.assertEqual('TWINABS - Bruker AXS scaling for twinned crystals - Version 2008/4: Krause, L., '
                         'Herbst-Irmer, R., Sheldrick G.M. & Stalke D., J. Appl. Cryst. 48 (2015) 3-10', self.s.version)

    def test_written_reflections(self):
        self.assertEqual(3952, self.s.dataset(0).written_reflections)
        self.assertEqual(5484, self.s.dataset(1).written_reflections)


class TestTWINABSMultipleOutputs(unittest.TestCase):
    """
    A TWINABS run where the user wrote all possible HKLF 4 and HKLF 5 variants in a row.
    """

    def setUp(self) -> None:
        self.s = Sadabs(fileobj=Path('test-data/twinabs_multi_options.abs'))

    def test_all_datasets_are_found(self) -> None:
        self.assertEqual(['t4_dom0.hkl', 't4_dom1.hkl', 't4_dom-2.hkl',
                          't5_dom1.hkl', 't5_dom2.hkl', 't5_dom-2.hkl'],
                         [x.hklfile for x in self.s.datasets])

    def test_hklf_types(self) -> None:
        self.assertEqual([4, 4, 4, 5, 5, 5], [x.filetype for x in self.s.datasets])

    def test_domain_selections(self) -> None:
        self.assertEqual([('all', None), ('single', 1), ('up_to', 2),
                          ('single', 1), ('single', 2), ('up_to', 2)],
                         [(x.domain_mode, x.domain_number) for x in self.s.datasets])

    def test_reflections_number(self) -> None:
        # N(all) for all domains and N(1) for the first domain only:
        self.assertEqual([32954, 20257, 32954, 20257, 32954, 32954],
                         [x.reflections_number for x in self.s.datasets])

    def test_rint(self) -> None:
        # HKLF 4 data use the extraction table, HKLF 5 data the singles of their domain:
        self.assertEqual([0.0438, 0.0398, 0.0438, 0.0313, 0.0442, 0.0313],
                         [x.rint for x in self.s.datasets])

    def test_statistics_blocks(self) -> None:
        self.assertEqual([('singles', 1), ('singles', 2), ('composites', None), ('all', None)],
                         [(x.kind, x.component) for x in self.s.statistics])

    def test_values_of_the_all_scans_row(self) -> None:
        singles = self.s.statistics[0]
        self.assertEqual((0.0313, 12355, 9776), (singles.rint, singles.total, singles.i_gt_2sigma))

    def test_point_group_of_the_equivalent_reflections(self) -> None:
        self.assertEqual('-1', self.s.equivalents_point_group)

    def test_hklf5_of_all_domains_uses_the_domain_with_most_singles(self) -> None:
        self.assertEqual(1, self.s.select_dataset(hkl_basename='t5_dom-2.hkl').singles_statistics.component)

    def test_hklf4_of_first_domain_uses_own_table(self) -> None:
        table = self.s.dataset(1).table
        self.assertEqual((1, 20257, 0.0398, 32215, 0.0429),
                         (table.domain_label, table.n_domain, table.rint_domain, table.n_all, table.rint_all))

    def test_written_reflections_are_the_merged_ones(self) -> None:
        self.assertEqual([3930, 3761, 3930, 5781, 5779, 8954],
                         [x.written_reflections for x in self.s.datasets])

    def test_select_dataset_by_name(self) -> None:
        self.assertEqual(20257, self.s.select_dataset(hkl_basename='t5_dom1.hkl').reflections_number)
        self.assertEqual(20257, self.s.select_dataset(hkl_basename='t5_dom1').reflections_number)

    def test_select_dataset_by_reflection_number(self) -> None:
        self.assertEqual('t5_dom-2.hkl', self.s.select_dataset(reflections=8954).hklfile)

    def test_select_dataset_by_hklf_number(self) -> None:
        self.assertEqual('t5_dom-2.hkl', self.s.select_dataset(hklf=5).hklfile)
        self.assertEqual('t4_dom-2.hkl', self.s.select_dataset(hklf=4).hklfile)

    def test_select_dataset_without_criteria_takes_the_last(self) -> None:
        self.assertEqual('t5_dom-2.hkl', self.s.select_dataset().hklfile)

    def test_transmission_of_every_dataset(self) -> None:
        self.assertEqual([0.692919, 0.692919, 0.692919, 0.693129, 0.691391, 0.691391],
                         [x.transmission.tmin for x in self.s.datasets])


class TestTWINABSHKLF5BeforeTable(unittest.TestCase):
    """
    An HKLF 5 file may be written before any reflection table was printed. The same file name
    can also be written twice, then the last data set wins.
    """

    def setUp(self) -> None:
        self.s = Sadabs(fileobj=Path('test-data/twinabs_hklf5_first.abs'))

    def test_first_dataset_uses_the_table_written_later(self) -> None:
        self.assertEqual(20616, self.s.dataset(0).reflections_number)
        # The R(int) comes from the statistics of the singles of domain 1:
        self.assertEqual(0.0313, self.s.dataset(0).rint)

    def test_last_written_file_wins(self) -> None:
        dataset = self.s.select_dataset(hkl_basename='f5_a.hkl')
        self.assertEqual(8954, dataset.written_reflections)
        self.assertEqual(32954, dataset.reflections_number)


class TestTWINABSRealWorldFile(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Sadabs(fileobj=Path('test-data/DK_ML766_twin.abs'))

    def test_number_of_datasets(self) -> None:
        self.assertEqual(4, len(self.s.datasets))

    def test_hklf4_gets_all_reflections(self) -> None:
        self.assertEqual(32949, self.s.dataset(0).reflections_number)
        self.assertEqual(0.0416, self.s.dataset(0).rint)

    def test_hklf5_of_domain_one(self) -> None:
        self.assertEqual(20615, self.s.dataset(1).reflections_number)
        # Not the 0.0394 of the extraction table, which is a twin fraction refinement residual:
        self.assertEqual(0.0272, self.s.dataset(1).rint)

    def test_scaling_in_point_group_1_is_visible(self) -> None:
        self.assertEqual('1', self.s.equivalents_point_group)

    def test_selection_takes_the_last_file_with_that_name(self) -> None:
        dataset = self.s.select_dataset(hkl_basename='DK_ML766_0m_5.hkl')
        self.assertEqual(6502, dataset.written_reflections)
        self.assertEqual(20615, dataset.reflections_number)


class TestSADABSMultipleOutputs(unittest.TestCase):
    """
    SADABS output files have no reflection table, the written reflections are used instead.
    """

    def setUp(self) -> None:
        self.s = Sadabs(fileobj=Path('test-data/sad.abs'))

    def test_all_datasets_are_found(self) -> None:
        self.assertEqual(['sad_noface_u.hkl', 'sad_noface_m.hkl', 'xd.hkl',
                          'sad_face_u.hkl', 'sad_face_m.hkl', 'xd_face.hkl'],
                         [x.hklfile for x in self.s.datasets])

    def test_reflections_number_is_the_written_one(self) -> None:
        self.assertEqual([275136, 45285, 42035, 275137, 45285, 42039],
                         [x.reflections_number for x in self.s.datasets])

    def test_rint_is_the_global_one(self) -> None:
        # SADABS listings contain no R(int), it is calculated from the reflection data instead:
        self.assertEqual([None] * 6, [x.rint for x in self.s.datasets])

    def test_select_dataset_by_name(self) -> None:
        self.assertEqual(42039, self.s.select_dataset(hkl_basename='xd_face.hkl').reflections_number)


if __name__ == '__main__':
    unittest.main()
