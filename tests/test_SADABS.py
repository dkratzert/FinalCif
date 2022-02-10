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
        self.s = Sadabs(r'test-data/IK_WU19.abs')  # this is a sadabs file

    def test_twincomp(self):
        self.assertEqual(1, self.s.twin_components)

    def test_hkl_file(self):
        print('###', Path('.').resolve())
        self.assertEqual('IK_WU19_0m.hkl', self.s.dataset(0).hklfile)

    def test_rint(self):
        print(self.s.filename)
        self.assertEqual(0.0472, self.s.Rint)

    def test_transmission(self):
        self.assertEqual([0.7135, 0.7459], self.s.dataset(0).transmission)

    def test_version(self):
        self.assertEqual('SADABS-2016/2 - Bruker AXS area detector scaling and absorption correction: Krause, L., '
                         'Herbst-Irmer, R., Sheldrick G.M. & Stalke D., J. Appl. Cryst. 48 (2015) 3-10',
                         self.s.version)

    def test_written_reflections(self):
        self.assertEqual(152800, self.s.dataset(0).written_reflections)


class TestTWINABS(unittest.TestCase):
    def setUp(self) -> None:
        self.s = Sadabs(r'test-data/twin-4-5.abs')  # this is a twinabs file

    def test_transmission(self):
        self.assertEqual([0.794433, 0.86207], self.s.dataset(0).transmission)
        self.assertEqual([0.793942, 0.862070], self.s.dataset(1).transmission)

    def test_rint(self):
        self.assertEqual(0.0376, self.s.Rint)

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


if __name__ == '__main__':
    unittest.main()
