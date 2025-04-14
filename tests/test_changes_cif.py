import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from pathlib import Path

from PySide6.QtGui import QIcon

from finalcif import VERSION
from finalcif.appwindow import AppWindow

data = Path('tests')


# noinspection PyMissingTypeHints
class TestChangesTrackingActive(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        self.testcif = data / 'examples/work/cu_BruecknerJK_153F40_0m.cif'
        self.myapp = AppWindow(file=self.testcif)
        self.myapp.finalcif_changes_filename.unlink(missing_ok=True)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(True)
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle(f'FinalCif v{VERSION}')
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)

    def test_filanames(self):
        self.assertEqual(self.testcif.stem + '-finalcif_changes.cif', str(self.myapp.finalcif_changes_filename.name))

    def tearDown(self) -> None:
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)
        self.myapp.finalcif_changes_filename.unlink(missing_ok=True)
        self.myapp.close()

    def test_save_with_keys(self):
        self.myapp.ui.cif_main_table.setText(key='_chemical_formula_moiety', column=2, txt='testauthoradress')
        self.myapp.ui.cif_main_table.setText(key='_chemical_melting_point', column=2, txt='testauthoremail')
        self.myapp.ui.SaveCifButton.click()
        self.assertEqual(True, self.myapp.cif.finalcif_file.exists())
        self.assertEqual(True, self.myapp.finalcif_changes_filename.exists())
        changes = self.myapp.get_changes_cif(self.myapp.finalcif_changes_filename)
        self.assertEqual(['_chemical_formula_moiety', '_chemical_melting_point'], changes.keys())
        self.assertEqual(['testauthoradress', 'testauthoremail'], changes.values())

    def test_save_with_no_changes(self):
        # Track changes is activated in self.setUp()
        self.assertEqual(False, self.myapp.finalcif_changes_filename.exists())
        self.myapp.ui.SaveCifButton.click()
        self.assertEqual(True, self.myapp.cif.finalcif_file.exists())
        self.assertEqual(False, self.myapp.finalcif_changes_filename.exists())
        # This creates a new file:
        changes = self.myapp.get_changes_cif(self.myapp.finalcif_changes_filename)
        # And it is empty
        self.assertEqual('', changes.fileobj.read_text())
        self.assertEqual([], changes.keys())
        self.assertEqual([], changes.values())

    def test_save_with_loop(self):
        self.myapp.cif.add_loop_to_cif(loop_tags=['_foo', '_bar'], row_values=['fooval', 'barval'])
        self.myapp.ui.SaveCifButton.click()
        changes = self.myapp.get_changes_cif(self.myapp.finalcif_changes_filename)
        self.assertEqual(['fooval', 'barval'], changes.loops[0].values)
