import sys
import unittest

from PyQt5.QtWidgets import QApplication

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.loop_creator import LoopCreator

app = QApplication(sys.argv)


class TestLoopCreator(unittest.TestCase):
    def setUp(self) -> None:
        self.cif = CifContainer('test-data/1000006.cif')
        self.lc = LoopCreator(cif=self.cif)
        self.lc.saveLoopPushButton.clicked.connect(self.lc.save_new_loop_to_cif)
        # For testing:
        # self.show_app()

    def show_app(self):
        self.lc.show()
        app.exec_()

    def test_search(self):
        self.assertEqual(1407, self.lc.availableKeysListWidget.count())
        self.lc.searchLineEdit.setText('footnote')
        self.assertEqual(2, self.lc.availableKeysListWidget.count())

    def test_push_key_right(self):
        # We have a list with many available keys:
        self.assertEqual(1407, self.lc.availableKeysListWidget.count())
        # we select one of them:
        self.lc.availableKeysListWidget.setCurrentRow(2)
        # The selected is still visible:
        self.assertFalse(self.lc.availableKeysListWidget.item(2).isHidden())
        # We push it to the right:
        self.lc.rightPushButton.click()
        # It is hidden on the left now:
        self.assertTrue(self.lc.availableKeysListWidget.item(2).isHidden())
        # But still there:
        self.assertEqual(1407, self.lc.availableKeysListWidget.count())
        # But it is visible in the right list:
        self.assertEqual(1, self.lc.newLoopKeysListWidget.count())
        # It has this text:
        self.assertEqual('_atom_site_Cartn_x', self.lc.availableKeysListWidget.item(2).text())
        # self.show_app()

    def test_push_key_left(self):
        self.lc.availableKeysListWidget.setCurrentRow(2)
        # We push it to the right:
        self.lc.rightPushButton.click()
        # and back to the left again:
        self.lc.newLoopKeysListWidget.setCurrentRow(0)
        self.lc.leftPushButton.click()
        # It is visible on the left side again:
        self.assertFalse(self.lc.availableKeysListWidget.item(2).isHidden())
        # And removed from the left:
        self.assertEqual(1, self.lc.newLoopKeysListWidget.count())
        # self.show_app()

    def test_tooltip(self):
        self.lc.availableKeysListWidget.setCurrentRow(2)
        self.assertEqual(('<pre><h2>_atom_site_Cartn_x</h2> The atom-site coordinates in angstroms '
                          'specified according to a\n'
                          ' set of orthogonal Cartesian axes related to the cell axes as\n'
                          ' specified by the _atom_sites_Cartn_transform_axes description.</pre>'),
                         self.lc.availableKeysListWidget.item(2).toolTip())

    def test_save_to_cif(self):
        self.lc.availableKeysListWidget.setCurrentRow(2)
        self.lc.rightPushButton.click()
        self.lc.rightPushButton.click()
        self.lc.save_new_loop_to_cif()
        self.assertEqual(['_atom_site_Cartn_x', '_atom_site_Cartn_y'], self.cif.loops[-1].tags)
        self.assertEqual(['?', '?'], self.cif.loops[-1].values)
        self.cif.finalcif_file.unlink(missing_ok=True)
