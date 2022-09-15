import unittest
from pathlib import Path

from PyQt5.QtGui import QIcon

from finalcif import VERSION
from finalcif.appwindow import AppWindow


class TestChangesTrackingActive(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        self.testcif = Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        self.myapp = AppWindow(self.testcif, unit_test=True)
        self.myapp.finalcif_changes_filename.unlink(missing_ok=True)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()
        self.myapp.ui.trackChangesCifCheckBox.setChecked(True)
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)

    def test_filanames(self):
        self.assertEqual(self.testcif.stem + '-finalcif_changes.cif', str(self.myapp.finalcif_changes_filename.name))

    def tearDown(self) -> None:
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)
        self.myapp.finalcif_changes_filename.unlink(missing_ok=True)
        self.myapp.close()

    def test_save_with_keys(self):
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_address', column=2, txt='testauthoradress')
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_email', column=2, txt='testauthoremail')
        self.myapp.ui.SaveCifButton.click()
        self.assertEqual(True, self.myapp.cif.finalcif_file.exists())
        self.assertEqual(True, self.myapp.finalcif_changes_filename.exists())
        changes = self.myapp.get_changes_cif(self.myapp.finalcif_changes_filename)
        self.assertEqual(['_audit_contact_author_email', '_audit_contact_author_address'], changes.keys())
        self.assertEqual(['testauthoremail', 'testauthoradress'], changes.values())

    def test_save_with_no_changes(self):
        self.assertEqual(False, self.myapp.finalcif_changes_filename.exists())
        self.myapp.ui.SaveCifButton.click()
        self.assertEqual(True, self.myapp.cif.finalcif_file.exists())
        self.assertEqual(True, self.myapp.finalcif_changes_filename.exists())
        changes = self.myapp.get_changes_cif(self.myapp.finalcif_changes_filename)
        self.assertEqual('data_cu_BruecknerJK_153F40_0m_changes\n', changes.fileobj.read_text())
        self.assertEqual([], changes.keys())
        self.assertEqual([], changes.values())

    def test_save_with_loop(self):
        self.myapp.cif.add_loop_to_cif(loop_tags=['_foo', '_bar'], loop_values=['fooval', 'barval'])
        self.myapp.ui.SaveCifButton.click()
        changes = self.myapp.get_changes_cif(self.myapp.finalcif_changes_filename)
        self.assertEqual(['fooval', 'barval'], changes.loops[0].values)
