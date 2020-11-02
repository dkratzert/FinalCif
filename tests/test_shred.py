import os
import unittest
from pathlib import Path

from cif.cif_file_io import CifContainer
from finalcif import AppWindow
from tests.test_finalcif import unify_line_endings
from tools.shred import ShredCIF


class TestShedCifWithData(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.cif = CifContainer(Path('test-data/p21c.cif'))
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
        os.chdir(Path(__file__).absolute().parent.parent)
        self.cif = CifContainer(Path('test-data/1000007.cif'))
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


class TestExport(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.myapp = AppWindow(Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').absolute())
        self.myapp.hide()  # For full screen view
        self.outfile_hkl = Path('cu_BruecknerJK_153F40_0m-finalcif.hkl')
        self.outfile_res = Path('cu_BruecknerJK_153F40_0m-finalcif.res')

    def tearDown(self):
        self.outfile_hkl.unlink()
        self.outfile_res.unlink()

    def test_export_hkl_res(self):
        """
        Shredcif test
        """
        self.myapp.ui.ShredCifButton.click()
        # testing the res file export:
        test_res_file = Path('test_res_file.txt')
        self.assertEqual(test_res_file.read_text().splitlines(keepends=True),
                         self.outfile_res.read_text().splitlines(keepends=True))
        # testing the hkl file export:
        test_res_file = Path('test_hkl_file.txt')
        self.assertEqual(test_res_file.read_text().splitlines(keepends=True),
                         self.outfile_hkl.read_text().splitlines(keepends=True))
        message = "\nFinished writing data to cu_BruecknerJK_153F40_0m-finalcif.res \nand cu_BruecknerJK_153F40_0m-finalcif.hkl."
        self.assertEqual(unify_line_endings(self.myapp.status_bar.current_message), unify_line_endings(message))
