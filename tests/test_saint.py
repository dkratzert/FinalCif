#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import unittest
from pathlib import Path

from finalcif.datafiles.saint import SaintListFile
from finalcif.tools.misc import unify_line_endings

data = Path('.')


class MyTestCase(unittest.TestCase):

    def test_saint_repr(self):
        output = 'Version: SAINT V8.38A, file: TB_fs20_v1_0m._ls\n' \
                 'Number of samples: 1 with 1 components.\n' \
                 'Used Reflections: 9478\n' \
                 'min thata: 2.33\n' \
                 'max theta: 27.3635\n' \
                 'min 2 theta: 4.660\n' \
                 'max 2 theta: 54.727\n' \
                 'Twin integration False\n'
        saint = SaintListFile(name_patt='TB_fs20_v1_0m._ls', directory=data / 'test-data')
        self.assertEqual(unify_line_endings(output), unify_line_endings(str(saint)))

    def test_reflections_of_repeated_summary_are_not_summed_up(self):
        """The same component may be listed in several reflection summaries."""
        saint = SaintListFile(name_patt='DK_Zucker2_0m._ls', directory=data / 'test-data')
        self.assertEqual('9640', saint.cell_reflections)
        self.assertEqual('5.910', saint.cell_res_min_2t)
        self.assertEqual('111.661', saint.cell_res_max_2t)


class TwinReflectionsTestCase(unittest.TestCase):
    """
    All twin domains have to be counted for _cell_measurement_reflns_used.
    """

    def test_components_of_separate_summaries_are_summed_up(self):
        saint = SaintListFile(name_patt='DK_ML766_twin._ls', directory=data / 'test-data')
        # 3680 (domain 1) + 2356 (domain 2):
        self.assertEqual('6036', saint.cell_reflections)

    def test_theta_range_covers_all_components(self):
        saint = SaintListFile(name_patt='DK_ML766_twin._ls', directory=data / 'test-data')
        self.assertEqual('4.455', saint.cell_res_min_2t)
        self.assertEqual('54.000', saint.cell_res_max_2t)
        self.assertEqual(2.2275, saint.cell_res_min_theta)
        self.assertEqual(27.0, saint.cell_res_max_theta)

    def test_all_line_is_used_if_present(self):
        saint = SaintListFile(name_patt='test766_0m._ls', directory=data / 'test-data')
        self.assertEqual('6002', saint.cell_reflections)
        self.assertEqual('4.455', saint.cell_res_min_2t)
        self.assertEqual('57.808', saint.cell_res_max_2t)


if __name__ == '__main__':
    unittest.main()
