from qtpy.QtWidgets import QApplication
app = QApplication.instance()
if app is None:
    app = QApplication([])

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
        self.assertEqual(6, self.imp.keys_to_import)
        self.assertEqual(1, self.imp.loops_to_import)

    def test_import_methods(self):
        self.assertEqual(['_foo_bar', '_hello', '_empty_key'], self.imp.get_keys(include=True))
        self.assertEqual([['_my_atom_type_symbol',
                           '_my_atom_type_description',
                           '_my_atom_type_scat_dispersion_real']], self.imp.get_loops(include=True))

    def test_import_methods_excluded(self):
        self.assertEqual(['_cell_length_a', '_vrf_PLAT029_title', '_vrf_PLAT911_title'],
                         self.imp.get_keys(include=False))
        self.assertEqual([], self.imp.get_loops(include=False))

    def test_vrf_keys_are_never_preselected_after_select_only_new(self):
        self.imp._select_only_new()
        self.assertNotIn('_vrf_PLAT029_title', self.imp.get_keys(include=True))
        self.assertNotIn('_vrf_PLAT911_title', self.imp.get_keys(include=True))

    def test_skip_empty_values_unchecked_keeps_empty_key(self):
        self.assertFalse(self.imp.ui.skipEmptyValuesCheckBox.isChecked())
        self.assertIn('_empty_key', self.imp.get_keys(include=True))

    def test_skip_empty_values_checked_removes_empty_key(self):
        self.imp.ui.skipEmptyValuesCheckBox.setChecked(True)
        self.assertNotIn('_empty_key', self.imp.get_keys(include=True))
        self.assertIn('_hello', self.imp.get_keys(include=True))

    def test_skip_empty_values_toggled_back(self):
        self.imp.ui.skipEmptyValuesCheckBox.setChecked(True)
        self.imp.ui.skipEmptyValuesCheckBox.setChecked(False)
        self.assertIn('_empty_key', self.imp.get_keys(include=True))

    def test_skip_empty_values_applies_to_select_only_new(self):
        self.imp.ui.skipEmptyValuesCheckBox.setChecked(True)
        self.imp._select_only_new()
        self.assertNotIn('_empty_key', self.imp.get_keys(include=True))

    def test_save_selection_ignores_auto_excluded_keys(self):
        self.imp._save_selection()
        self.assertEqual(['_cell_length_a'], self.imp.settings.load_value_of_key('do_not_import_keys'))
        self.imp._empty_saved_selection()

    def test_other(self):
        self.assertEqual('import_cif.cif', self.imp.import_cif.filename)
        self.assertEqual('p21c-copy.cif', self.imp.target_cif.filename)


if __name__ == '__main__':
    unittest.main()
