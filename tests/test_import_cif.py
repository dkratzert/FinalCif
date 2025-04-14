import os

from PySide6.QtWidgets import QApplication
app = QApplication.instance()
if app is None:
    app = QApplication([])

os.environ["RUNNING_TEST"] = 'True'
import shutil
import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.import_selector import ImportSelector
from finalcif.tools.settings import FinalCifSettings

data = Path('tests')
testdata = Path('test-data')




class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        imp_cif = CifContainer(data / 'statics/import_cif.cif')
        shutil.copyfile(testdata / 'p21c.cif', testdata / 'p21c-copy.cif')
        targetcif = CifContainer(testdata / 'p21c-copy.cif')
        settings = FinalCifSettings()
        self.imp = ImportSelector(None, import_cif=imp_cif, target_cif=targetcif, settings=settings)
        self.imp._empty_saved_selection()
        self.imp.show_import_window()

    def tearDown(self) -> None:
        Path(testdata / 'p21c-copy.cif').unlink(missing_ok=True)
        self.imp.deleteLater()
        self.imp.close()

    def test_keys_to_import(self):
        self.assertEqual(3, self.imp.keys_to_import)
        self.assertEqual(1, self.imp.loops_to_import)

    def test_import_methods(self):
        self.assertEqual(['_foo_bar', '_hello'], self.imp.get_keys(include=True))
        self.assertEqual([['_my_atom_type_symbol',
                           '_my_atom_type_description',
                           '_my_atom_type_scat_dispersion_real']], self.imp.get_loops(include=True))

    def test_import_methods_excluded(self):
        self.assertEqual(['_cell_length_a'], self.imp.get_keys(include=False))
        self.assertEqual([], self.imp.get_loops(include=False))

    def test_other(self):
        self.assertEqual('import_cif.cif', self.imp.import_cif.filename)
        self.assertEqual('p21c-copy.cif', self.imp.target_cif.filename)


if __name__ == '__main__':
    unittest.main()
