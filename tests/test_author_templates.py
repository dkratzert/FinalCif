import os
import sys
import unittest
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow

app = QApplication(sys.argv)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.app = AppWindow(self.testcif)
        self.app.running_inside_unit_test = True
        self.app.hide()

    def tearDown(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        Path('tests/other_templates/testexport_author.cif').unlink(missing_ok=True)

    def test_selected_loop_without_selection(self):
        self.assertEqual(self.app.authors.get_selected_loop_name(), '')

    def test_selected_loop_with_selection(self):
        self.delete_test_author()
        self.import_testauthor()
        self.assertEqual('AATest Author', self.app.authors.get_selected_loop_name())

    def delete_test_author(self):
        self.app.ui.LoopTemplatesListWidget.setCurrentRow(0)
        self.app.ui.DeleteLoopAuthorTemplateButton.click()
        self.app.ui.LoopTemplatesListWidget.setCurrentRow(0)
        self.assertNotEqual('AATest Author', self.app.authors.get_selected_loop_name())

    def test_export_selected_author(self):
        self.delete_test_author()
        self.import_testauthor()
        self.app.authors.export_author_template('../other_templates/testexport_author.cif')
        self.assertEqual(True, Path('../other_templates/testexport_author.cif').exists())
        self.assertEqual(Path('../other_templates/testexport_author.cif').read_text(),
                         Path('../other_templates/testexport_author.cif').read_text())

    def import_testauthor(self):
        self.app.authors.import_author('../other_templates/AATest_Author.cif')
        self.app.ui.LoopTemplatesListWidget.setCurrentRow(0)


if __name__ == '__main__':
    unittest.main()
