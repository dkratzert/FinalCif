import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.shred import ShredCIF


class TestShedCifWithData(unittest.TestCase):

    def setUp(self) -> None:
        self.cif = CifContainer(Path('test-data/p21c.cif'))
        self.shred = ShredCIF(self.cif, ui=None)
        self.outfile_hkl = self.cif.finalcif_file.with_suffix('.hkl')
        self.outfile_res = self.cif.finalcif_file.with_suffix('.res')

    def tearDown(self) -> None:
        self.outfile_hkl.unlink(missing_ok=True)
        self.outfile_res.unlink(missing_ok=True)

    def test_no_shred(self):
        self.assertEqual(self.outfile_hkl.exists(), False)
        self.assertEqual(self.outfile_res.exists(), False)
        self.assertEqual(self.shred._statusbar.current_message, '')

    def test_shred(self):
        self.shred.shred_cif()
        self.assertEqual(self.outfile_res.exists(), True)
        self.assertEqual(self.outfile_hkl.exists(), True)
        self.assertEqual('\nFinished writing data to p21c-finalcif.res and p21c-finalcif.hkl.',
                         self.shred._statusbar.current_message)


class TestShedCifNoData(unittest.TestCase):

    def setUp(self) -> None:
        self.cif = CifContainer(Path('test-data/1000007.cif'))
        self.shred = ShredCIF(self.cif, ui=None)
        self.outfile_hkl = self.cif.finalcif_file.with_suffix('.hkl')
        self.outfile_res = self.cif.finalcif_file.with_suffix('.res')

    def tearDown(self) -> None:
        self.outfile_hkl.unlink(missing_ok=True)
        self.outfile_res.unlink(missing_ok=True)

    def test_no_shred(self):
        self.assertEqual(self.outfile_hkl.exists(), False)
        self.assertEqual(self.outfile_res.exists(), False)
        self.assertEqual('', self.shred._statusbar.current_message)

    def test_shred(self):
        self.shred.shred_cif()
        self.assertEqual(self.outfile_res.exists(), False)
        self.assertEqual(self.outfile_hkl.exists(), False)
        self.assertEqual('No .res and .hkl file data found!', self.shred._statusbar.current_message)


class TestExport(unittest.TestCase):

    def setUp(self) -> None:
        self.cif = CifContainer(Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif'))
        self.outfile_hkl = self.cif.finalcif_file.with_suffix('.hkl')
        self.outfile_res = self.cif.finalcif_file.with_suffix('.res')
        self.shred = ShredCIF(self.cif, ui=None)
        self.shred.shred_cif()

    def tearDown(self):
        self.outfile_hkl.unlink(missing_ok=True)
        self.outfile_res.unlink(missing_ok=True)

    def test_export_hkl(self):
        """
        Shredcif test
        """
        test_hkl_file = Path('tests/examples/work/test_hkl_file.txt')
        self.assertEqual(test_hkl_file.read_text().splitlines(keepends=True),
                         self.outfile_hkl.read_text().splitlines(keepends=True))

    def test_export_res(self):
        test_res_file = Path('tests/examples/work/test_res_file.txt')
        self.assertEqual(test_res_file.read_text()#.lstrip()
        ,
                         self.outfile_res.read_text()#.lstrip()
                         )
