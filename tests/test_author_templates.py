import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtTest import QTest
from finalcif.appwindow import AppWindow

data = Path('tests')


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.testcif = data / 'examples/1979688.cif'
        self.authorexport_file = data / 'examples/testexport_author.cif'
        self.testimport_author = data / 'other_templates/AATest_Author.cif'
        self.app = AppWindow(self.testcif)
        self.author = {'address': 'address', 'footnote': 'footnote', 'email': 'email',
                       'name'   : 'name', 'orcid': 'orcid', 'phone': 'phone', 'contact': True}
        self.app.ui.authorEditTabWidget.setCurrentIndex(0)
        self._delete_test_author()

    def tearDown(self) -> None:
        self.authorexport_file.unlink(missing_ok=True)
        self._delete_test_author()
        self.app.close()

    def _import_testauthor(self):
        # To be used in other tests
        self.app.authors.import_author(str(self.testimport_author))
        self.app.ui.LoopTemplatesListWidget.setCurrentRow(0)

    def test_selected_loop_without_selection(self):
        self.assertEqual('', self.app.authors.get_selected_loop_name())

    def test_selected_loop_with_selection(self):
        self.assertEqual('', self.app.authors.get_selected_loop_name())
        self._import_testauthor()
        self.assertEqual('AATest Author', self.app.authors.get_selected_loop_name())

    def _delete_test_author(self, name='AATest Author'):
        self._select_row_of_author(name)
        self.app.ui.DeleteLoopAuthorTemplateButton.click()
        self.assertNotEqual('AATest Author', self.app.authors.get_selected_loop_name())

    def _select_row_of_author(self, name):
        listWidget = self.app.ui.LoopTemplatesListWidget
        for row in range(listWidget.count()):
            item = listWidget.item(row)
            if item is not None and item.text().startswith(name):
                item_widget = listWidget.itemWidget(item)
                if item_widget is not None:
                    QTest.mouseClick(item_widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier,
                                     item_widget.rect().center())
                    break

    def test_export_selected_author(self):
        self.authorexport_file.unlink(missing_ok=True)
        self._import_testauthor()
        self._select_row_of_author('AATest Author')
        self.app.authors.export_author_template(str(self.authorexport_file))
        self.assertEqual(True, self.authorexport_file.exists())
        self.assertEqual(self.testimport_author.read_text(), self.authorexport_file.read_text())

    def test_export_selected_author_cif(self):
        self.app.ui.authorEditTabWidget.setCurrentIndex(1)
        self.authorexport_file.unlink(missing_ok=True)
        self._import_testauthor()
        self._select_row_of_author('AATest Author')
        self.app.authors.export_author_template(str(self.authorexport_file))
        self.assertEqual(True, self.authorexport_file.exists())
        self.assertEqual(self.testimport_author.read_text(), self.authorexport_file.read_text())

    def test_set_name(self):
        self.app.ui.FullNameLineEdit.setText('test')
        self.assertEqual('test', self.app.authors.get_author_info().name)
        self.app.ui.FullNameLineEdit.clear()
        self.app.ui.authorEditTabWidget.setCurrentIndex(1)
        self.app.ui.FullNameLineEdit_cif.setText('test2')
        self.assertEqual('test2', self.app.authors.get_author_info().name)

    def test_set_contact_author(self):
        self.assertEqual(False, self.app.ui.ContactAuthorCheckBox.isChecked())
        self.app.ui.ContactAuthorCheckBox.setChecked(True)
        self.assertEqual(True, self.app.authors.get_author_info().contact_author)
        self.app.ui.authorEditTabWidget.setCurrentIndex(1)
        self.assertEqual(False, self.app.ui.ContactAuthorCheckBox_cif.isChecked())
        self.app.ui.ContactAuthorCheckBox_cif.setChecked(True)
        self.assertEqual(True, self.app.authors.get_author_info().contact_author)

    def test_set_address(self):
        self.app.ui.AddressTextedit.setText('Eine Adresse 1')
        self.assertEqual("'Eine Adresse 1'", self.app.authors.get_author_info().address)
        self.app.ui.AddressTextedit.clear()
        self.app.ui.authorEditTabWidget.setCurrentIndex(1)
        self.app.ui.AddressTextedit_cif.setText('Eine Adresse 2')
        self.assertEqual("'Eine Adresse 2'", self.app.authors.get_author_info().address)

    def test_set_footnote(self):
        self.app.ui.FootNoteLineEdit.setText('notex')
        self.assertEqual('notex', self.app.authors.get_author_info().footnote)

    def test_set_email(self):
        self.app.ui.EMailLineEdit.setText('test@foo.de')
        self.assertEqual('test@foo.de', self.app.authors.get_author_info().email)
        self.app.ui.authorEditTabWidget.setCurrentIndex(1)
        self.app.ui.EMailLineEdit.clear()
        self.app.ui.EMailLineEdit_cif.setText('test@foo.de')
        self.assertEqual('test@foo.de', self.app.authors.get_author_info().email)

    def test_set_orcid(self):
        self.app.ui.ORCIDLineEdit.setText('12345a')
        self.assertEqual('12345a', self.app.authors.get_author_info().orcid)

    def test_set_phone(self):
        self.app.ui.PhoneLineEdit.setText('12345a')
        self.assertEqual('12345a', self.app.authors.get_author_info().phone)
        self.app.ui.PhoneLineEdit.clear()
        self.app.ui.authorEditTabWidget.setCurrentIndex(1)
        self.app.ui.PhoneLineEdit_cif.setText('12345b')
        self.assertEqual('12345b', self.app.authors.get_author_info().phone)

    def test_set_foo(self):
        self.app.ui.IUCRIDLineEdit.setText('123-45a')
        self.assertEqual('123-45a', self.app.authors.get_author_info().iucr_id)

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


if __name__ == '__main__':
    unittest.main()
