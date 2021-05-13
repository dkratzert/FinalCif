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
        self.author = {'address': 'address', 'footnote': 'footnote', 'email': 'email',
                       'name'   : 'name', 'orcid': 'orcid', 'phone': 'phone', 'contact': True}

    def tearDown(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        Path('tests/other_templates/testexport_author.cif').unlink(missing_ok=True)

    def _import_testauthor(self):
        # To be used in other tests
        self.app.authors.import_author('../other_templates/AATest_Author.cif')
        self.app.ui.LoopTemplatesListWidget.setCurrentRow(0)

    def test_selected_loop_without_selection(self):
        self.assertEqual(self.app.authors.get_selected_loop_name(), '')

    def test_selected_loop_with_selection(self):
        self._delete_test_author()
        self._import_testauthor()
        self.assertEqual('AATest Author', self.app.authors.get_selected_loop_name())

    def _delete_test_author(self, name='AATest Author'):
        self._select_row_of_author(name)
        self.app.ui.DeleteLoopAuthorTemplateButton.click()
        self.assertNotEqual('AATest Author', self.app.authors.get_selected_loop_name())

    def _select_row_of_author(self, name):
        listw = self.app.ui.LoopTemplatesListWidget
        for row in range(listw.count()):
            listw.setCurrentRow(row)
            if listw.currentItem().text().startswith(name):
                break

    def test_export_selected_author(self):
        self._delete_test_author()
        self._import_testauthor()
        self.app.authors.export_author_template(str(Path('../other_templates/testexport_author.cif').resolve(strict=True)))
        self.assertEqual(True, Path('../other_templates/testexport_author.cif').exists())
        self.assertEqual(Path('../other_templates/testexport_author.cif').read_text(),
                         Path('../other_templates/testexport_author.cif').read_text())

    def test_set_name(self):
        self.app.ui.FullNameLineEdit.setText('test')
        self.assertEqual('test', self.app.authors.get_author_info().get('name'))

    def test_set_contact_author(self):
        self.assertEqual(False, self.app.ui.ContactAuthorCheckBox.isChecked())
        self.app.ui.ContactAuthorCheckBox.setChecked(True)
        self.assertEqual(True, self.app.authors.get_author_info().get('contact'))

    def test_set_address(self):
        self.app.ui.AddressTextedit.setText('Eine Adresse 1')
        self.assertEqual("'Eine Adresse 1'", self.app.authors.get_author_info().get('address'))

    def test_set_footnote(self):
        self.app.ui.FootNoteLineEdit.setText('notex')
        self.assertEqual('notex', self.app.authors.get_author_info().get('footnote'))

    def test_set_email(self):
        self.app.ui.EMailLineEdit.setText('test@foo.de')
        self.assertEqual('test@foo.de', self.app.authors.get_author_info().get('email'))

    def test_set_orcid(self):
        self.app.ui.ORCIDLineEdit.setText('12345a')
        self.assertEqual('12345a', self.app.authors.get_author_info().get('orcid'))

    def test_set_phone(self):
        self.app.ui.PhoneLineEdit.setText('12345a')
        self.assertEqual('12345a', self.app.authors.get_author_info().get('phone'))

    def test_set_foo(self):
        self.assertEqual(None, self.app.authors.get_author_info().get('foo'))

    def test_set_author_info(self):
        self.app.authors.set_author_info(self.author)
        self.assertEqual('name', self.app.ui.FullNameLineEdit.text())
        self.assertEqual('address', self.app.ui.AddressTextedit.toPlainText())
        self.assertEqual('email', self.app.ui.EMailLineEdit.text())
        self.assertEqual('orcid', self.app.ui.ORCIDLineEdit.text())
        self.assertEqual('footnote', self.app.ui.FootNoteLineEdit.text())
        self.assertEqual('phone', self.app.ui.PhoneLineEdit.text())
        self.assertEqual(True, self.app.ui.ContactAuthorCheckBox.isChecked())

    def test_set_author_info_and_clear(self):
        self.app.authors.set_author_info(self.author)
        self.app.authors.clear_fields()
        self.assertEqual('', self.app.ui.FullNameLineEdit.text())
        self.assertEqual('', self.app.ui.AddressTextedit.toPlainText())
        self.assertEqual('', self.app.ui.EMailLineEdit.text())
        self.assertEqual('', self.app.ui.ORCIDLineEdit.text())
        self.assertEqual('', self.app.ui.FootNoteLineEdit.text())
        self.assertEqual('', self.app.ui.PhoneLineEdit.text())
        self.assertEqual(False, self.app.ui.ContactAuthorCheckBox.isChecked())

    def test_save_author(self):
        pass


if __name__ == '__main__':
    unittest.main()
