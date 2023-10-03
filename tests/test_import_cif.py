import shutil
import unittest
from pathlib import Path

from finalcif.appwindow import app
from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.import_selector import ImportSelector
from finalcif.tools.settings import FinalCifSettings


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        imp_cif = CifContainer('tests/statics/import_cif.cif')
        shutil.copyfile('test-data/p21c.cif', 'test-data/p21c-copy.cif')
        targetcif = CifContainer('test-data/p21c-copy.cif')
        settings = FinalCifSettings()
        self.imp = ImportSelector(None, import_cif=imp_cif, target_cif=targetcif, settings=settings)
        self.imp.show_import_window()

    def tearDown(self) -> None:
        Path('test-data/p21c-copy.cif').unlink(missing_ok=True)

    def test_keys_to_import(self):
        self.assertEqual(3, self.imp.keys_to_import)
        self.assertEqual(1, self.imp.loops_to_import)

    def test_import_methods(self):
        self.assertEqual(['_foo_bar', '_hello'], self.imp.get_keys_to_import())
        self.assertEqual([['_my_atom_type_symbol',
                           '_my_atom_type_description',
                           '_my_atom_type_scat_dispersion_real']], self.imp.get_loops_to_import())

    def test_other(self):
        self.assertEqual('import_cif.cif', self.imp.import_cif.filename)
        self.assertEqual('p21c-copy.cif', self.imp.target_cif.filename)


if __name__ == '__main__':
    unittest.main()
