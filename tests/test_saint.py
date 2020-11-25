#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

from datafiles.saint import SaintListFile
from tests.helpers import unify_line_endings


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)

    def test_saint_repr(self):
        output = 'Version: SAINT V8.38A, file: D:\GitHub\FinalCif\\test-data\TB_fs20_v1_0m._ls\n' \
                 'Number of samples: 1 with 1 components.\n' \
                 'Used Reflections: 9478\n' \
                 'min thata: 2.33\n' \
                 'max theta: 27.3635\n' \
                 'min 2 theta: 4.660\n' \
                 'max 2 theta: 54.727\n' \
                 'Twin integration False\n'
        saint = SaintListFile(name_patt='*._ls', direct_name='test-data/TB_fs20_v1_0m._ls')
        self.assertEqual(unify_line_endings(output), unify_line_endings(str(saint)))


if __name__ == '__main__':
    unittest.main()
