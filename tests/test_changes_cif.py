import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from qtpy.QtGui import QIcon

from finalcif import VERSION
from finalcif.appwindow import AppWindow

data = Path('tests')


# noinspection PyMissingTypeHints
class TestChangesTrackingActive(AppWindowTestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        self.testcif = data / 'examples/work/cu_BruecknerJK_153F40_0m.cif'
        self.app = AppWindow(file=self.testcif)
        self.app.finalcif_changes_filename.unlink(missing_ok=True)
        self.app.ui.trackChangesCifCheckBox.setChecked(True)
        self.app.setWindowIcon(QIcon('./icon/multitable.png'))
        self.app.setWindowTitle(f'FinalCif v{VERSION}')
        self.app.cif.finalcif_file.unlink(missing_ok=True)

    def test_filanames(self):
        self.assertEqual(self.testcif.stem + '-finalcif_changes.cif', str(self.app.finalcif_changes_filename.name))

    def tearDown(self) -> None:
        self.app.ui.trackChangesCifCheckBox.setChecked(False)
        self.app.cif.finalcif_file.unlink(missing_ok=True)
        self.app.finalcif_changes_filename.unlink(missing_ok=True)
        self.app.close()
        super().tearDown()

    def test_save_with_keys(self):
        self.app.ui.cif_main_table.setText(key='_chemical_formula_moiety', column=2, txt='testauthoradress')
        self.app.ui.cif_main_table.setText(key='_chemical_melting_point', column=2, txt='testauthoremail')
        self.app.ui.SaveCifButton.click()
        self.assertEqual(True, self.app.cif.finalcif_file.exists())
        self.assertEqual(True, self.app.finalcif_changes_filename.exists())
        changes = self.app.get_changes_cif(self.app.finalcif_changes_filename)
        self.assertEqual(['_chemical_formula_moiety', '_chemical_melting_point'], changes.keys())
        self.assertEqual(['testauthoradress', 'testauthoremail'], changes.values())

    def test_save_with_no_changes(self):
        # Track changes is activated in self.setUp()
        self.assertEqual(False, self.app.finalcif_changes_filename.exists())
        self.app.ui.SaveCifButton.click()
        self.assertEqual(True, self.app.cif.finalcif_file.exists())
        self.assertEqual(False, self.app.finalcif_changes_filename.exists())
        # This creates a new file:
        changes = self.app.get_changes_cif(self.app.finalcif_changes_filename)
        # And it is empty
        self.assertEqual('', changes.fileobj.read_text())
        self.assertEqual([], changes.keys())
        self.assertEqual([], changes.values())

    def test_save_with_loop(self):
        self.app.cif.add_loop_to_cif(loop_tags=['_foo', '_bar'], row_values=['fooval', 'barval'])
        self.app.ui.SaveCifButton.click()
        changes = self.app.get_changes_cif(self.app.finalcif_changes_filename)
        self.assertEqual(['fooval', 'barval'], changes.loops[0].values)
