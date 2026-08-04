from qtpy.QtWidgets import QApplication
app = QApplication.instance()
if app is None:
    app = QApplication([])

import shutil
import unittest
from pathlib import Path

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.import_selector import ImportSelector, is_empty_value
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
        self.assertEqual(6, self.imp.keys_to_import)
        self.assertEqual(1, self.imp.loops_to_import)

    def test_is_empty_value(self):
        self.assertTrue(is_empty_value('_foo', '?'))
        self.assertTrue(is_empty_value('_foo', ''))
        self.assertFalse(is_empty_value('_foo', 'bar'))
        self.assertTrue(is_empty_value('_vrf_PLAT029_title', ';\nPROBLEM: something\nRESPONSE: ?\n;'))
        self.assertTrue(is_empty_value('_vrf_PLAT029_title', ';\nPROBLEM: something\nRESPONSE:\n;'))
        self.assertFalse(is_empty_value('_vrf_PLAT029_title', ';\nPROBLEM: something\nRESPONSE: all fine\n;'))

    def test_import_methods(self):
        self.assertEqual(['_foo_bar', '_hello', '_empty_key', '_vrf_PLAT029_title', '_vrf_PLAT911_title'],
                         self.imp.get_keys(include=True))
        self.assertEqual([['_my_atom_type_symbol',
                           '_my_atom_type_description',
                           '_my_atom_type_scat_dispersion_real']], self.imp.get_loops(include=True))

    def test_import_methods_excluded(self):
        self.assertEqual(['_cell_length_a'], self.imp.get_keys(include=False))
        self.assertEqual([], self.imp.get_loops(include=False))

    def test_vrf_with_response_is_selected_by_select_only_new(self):
        self.imp._select_only_new()
        self.assertIn('_vrf_PLAT911_title', self.imp.get_keys(include=True))

    def test_vrf_without_response_is_not_selected_by_select_only_new(self):
        self.imp._select_only_new()
        self.assertNotIn('_vrf_PLAT029_title', self.imp.get_keys(include=True))

    def test_empty_key_is_preselected_initially(self):
        self.assertIn('_empty_key', self.imp.get_keys(include=True))

    def test_select_only_new_skips_empty_values(self):
        self.imp._select_only_new()
        self.assertNotIn('_empty_key', self.imp.get_keys(include=True))
        self.assertIn('_hello', self.imp.get_keys(include=True))

    def test_select_only_new_skips_existing_keys(self):
        self.imp._select_only_new()
        self.assertNotIn('_cell_length_a', self.imp.get_keys(include=True))

    def test_empty_keys_are_detected(self):
        self.assertEqual({'_empty_key', '_vrf_PLAT029_title'}, self.imp._empty_keys)

    def test_save_selection_ignores_empty_keys(self):
        self.imp._select_only_new()
        self.imp._save_selection()
        self.assertEqual(['_cell_length_a'], self.imp.settings.load_value_of_key('do_not_import_keys'))
        self.imp._empty_saved_selection()

    def test_other(self):
        self.assertEqual('import_cif.cif', self.imp.import_cif.filename)
        self.assertEqual('p21c-copy.cif', self.imp.target_cif.filename)


if __name__ == '__main__':
    unittest.main()
