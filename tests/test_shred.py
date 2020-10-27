import unittest
from os import chdir
from pathlib import Path

from cif.cif_file_io import CifContainer
from tools.shred import ShredCIF


class TestShedCifWithData(unittest.TestCase):

    def setUp(self) -> None:
        chdir(Path(__file__).absolute().parent)
        self.cif = CifContainer(Path('../test-data/p21c.cif'))
        self.shred = ShredCIF(self.cif, ui=None)

    def tearDown(self) -> None:
        Path('p21c-finalcif.hkl').unlink(missing_ok=True)
        Path('p21c-finalcif.res').unlink(missing_ok=True)

    def test_no_shred(self):
        self.assertEqual(Path('../test-data/p21c-finalcif.hkl').exists(), False)
        self.assertEqual(Path('../test-data/p21c-finalcif.res').exists(), False)
        self.assertEqual(self.shred._statusbar.current_message, '')

    def test_shred(self):
        self.shred.shred_cif()
        self.assertEqual(Path('p21c-finalcif.res').exists(), True)
        self.assertEqual(Path('p21c-finalcif.hkl').exists(), True)
        self.assertEqual(self.shred._statusbar.current_message,
                         '\nFinished writing data to p21c-finalcif.res \nand p21c-finalcif.hkl.')


class TestShedCifNoData(unittest.TestCase):

    def setUp(self) -> None:
        chdir(Path(__file__).absolute().parent)
        self.cif = CifContainer(Path('../test-data/1000007.cif'))
        self.shred = ShredCIF(self.cif, ui=None)

    def tearDown(self) -> None:
        Path('p21c-finalcif.hkl').unlink(missing_ok=True)
        Path('p21c-finalcif.res').unlink(missing_ok=True)

    def test_no_shred(self):
        self.assertEqual(Path('../test-data/p21c-finalcif.hkl').exists(), False)
        self.assertEqual(Path('../test-data/p21c-finalcif.res').exists(), False)
        self.assertEqual(self.shred._statusbar.current_message, '')

    def test_shred(self):
        self.shred.shred_cif()
        self.assertEqual(Path('p21c-finalcif.res').exists(), False)
        self.assertEqual(Path('p21c-finalcif.hkl').exists(), False)
        self.assertEqual(self.shred._statusbar.current_message,
                         'No .res and .hkl file data found!')
