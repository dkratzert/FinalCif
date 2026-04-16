import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from qtpy import QtCore
from qtpy.QtTest import QTest
from finalcif.appwindow import AppWindow

data = Path('tests')


class MyTestCase(AppWindowTestCase):

    def setUp(self) -> None:
        self.testcif = data / 'examples/1979688.cif'
        self.authorexport_file = data / 'examples/testexport_author.cif'
        self.testimport_author = data / 'other_templates/AATest_Author.cif'
        self.myapp = AppWindow(self.testcif)
        self.author = {'address': 'address', 'footnote': 'footnote', 'email': 'email',
                       'name'   : 'name', 'orcid': 'orcid', 'phone': 'phone', 'contact': True}
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(0)
        self._delete_test_author()

    def tearDown(self) -> None:
        self.authorexport_file.unlink(missing_ok=True)
        self._delete_test_author()
        self.myapp.close()
        super().tearDown()

    def _import_testauthor(self):
        # To be used in other tests
        self.myapp.authors.import_author(str(self.testimport_author))
        self.myapp.ui.LoopTemplatesListWidget.setCurrentRow(0)

    def test_selected_loop_without_selection(self):
        self.assertEqual('', self.myapp.authors.get_selected_loop_name())

    def test_selected_loop_with_selection(self):
        self.assertEqual('', self.myapp.authors.get_selected_loop_name())
        self._import_testauthor()
        self.assertEqual('AATest Author', self.myapp.authors.get_selected_loop_name())

    def _delete_test_author(self, name='AATest Author'):
        self._select_row_of_author(name)
        self.myapp.ui.DeleteLoopAuthorTemplateButton.click()
        self.assertNotEqual('AATest Author', self.myapp.authors.get_selected_loop_name())

    def _select_row_of_author(self, name):
        listWidget = self.myapp.ui.LoopTemplatesListWidget
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
        self.myapp.authors.export_author_template(str(self.authorexport_file))
        self.assertEqual(True, self.authorexport_file.exists())
        self.assertEqual(self.testimport_author.read_text(), self.authorexport_file.read_text())

    def test_export_selected_author_cif(self):
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(1)
        self.authorexport_file.unlink(missing_ok=True)
        self._import_testauthor()
        self._select_row_of_author('AATest Author')
        self.myapp.authors.export_author_template(str(self.authorexport_file))
        self.assertEqual(True, self.authorexport_file.exists())
        self.assertEqual(self.testimport_author.read_text(), self.authorexport_file.read_text())

    def test_set_name(self):
        self.myapp.ui.FullNameLineEdit.setText('test')
        self.assertEqual('test', self.myapp.authors.get_author_info().name)
        self.myapp.ui.FullNameLineEdit.clear()
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(1)
        self.myapp.ui.FullNameLineEdit_cif.setText('test2')
        self.assertEqual('test2', self.myapp.authors.get_author_info().name)

    def test_set_contact_author(self):
        self.assertEqual(False, self.myapp.ui.ContactAuthorCheckBox.isChecked())
        self.myapp.ui.ContactAuthorCheckBox.setChecked(True)
        self.assertEqual(True, self.myapp.authors.get_author_info().contact_author)
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(1)
        self.assertEqual(False, self.myapp.ui.ContactAuthorCheckBox_cif.isChecked())
        self.myapp.ui.ContactAuthorCheckBox_cif.setChecked(True)
        self.assertEqual(True, self.myapp.authors.get_author_info().contact_author)

    def test_set_address(self):
        self.myapp.ui.AddressTextedit.setText('Eine Adresse 1')
        self.assertEqual("'Eine Adresse 1'", self.myapp.authors.get_author_info().address)
        self.myapp.ui.AddressTextedit.clear()
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(1)
        self.myapp.ui.AddressTextedit_cif.setText('Eine Adresse 2')
        self.assertEqual("'Eine Adresse 2'", self.myapp.authors.get_author_info().address)

    def test_set_footnote(self):
        self.myapp.ui.FootNoteLineEdit.setText('notex')
        self.assertEqual('notex', self.myapp.authors.get_author_info().footnote)

    def test_set_email(self):
        self.myapp.ui.EMailLineEdit.setText('test@foo.de')
        self.assertEqual('test@foo.de', self.myapp.authors.get_author_info().email)
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(1)
        self.myapp.ui.EMailLineEdit.clear()
        self.myapp.ui.EMailLineEdit_cif.setText('test@foo.de')
        self.assertEqual('test@foo.de', self.myapp.authors.get_author_info().email)

    def test_set_orcid(self):
        self.myapp.ui.ORCIDLineEdit.setText('12345a')
        self.assertEqual('12345a', self.myapp.authors.get_author_info().orcid)

    def test_set_phone(self):
        self.myapp.ui.PhoneLineEdit.setText('12345a')
        self.assertEqual('12345a', self.myapp.authors.get_author_info().phone)
        self.myapp.ui.PhoneLineEdit.clear()
        self.myapp.ui.authorEditTabWidget.setCurrentIndex(1)
        self.myapp.ui.PhoneLineEdit_cif.setText('12345b')
        self.assertEqual('12345b', self.myapp.authors.get_author_info().phone)

    def test_set_foo(self):
        self.myapp.ui.IUCRIDLineEdit.setText('123-45a')
        self.assertEqual('123-45a', self.myapp.authors.get_author_info().iucr_id)

    def test_set_author_info(self):
        self.myapp.authors.set_author_info(self.author)
        self.assertEqual('name', self.myapp.ui.FullNameLineEdit.text())
        self.assertEqual('address', self.myapp.ui.AddressTextedit.toPlainText())
        self.assertEqual('email', self.myapp.ui.EMailLineEdit.text())
        self.assertEqual('orcid', self.myapp.ui.ORCIDLineEdit.text())
        self.assertEqual('footnote', self.myapp.ui.FootNoteLineEdit.text())
        self.assertEqual('phone', self.myapp.ui.PhoneLineEdit.text())
        self.assertEqual(True, self.myapp.ui.ContactAuthorCheckBox.isChecked())

    def test_set_author_info_and_clear(self):
        self.myapp.authors.set_author_info(self.author)
        self.myapp.authors.clear_fields()
        self.assertEqual('', self.myapp.ui.FullNameLineEdit.text())
        self.assertEqual('', self.myapp.ui.AddressTextedit.toPlainText())
        self.assertEqual('', self.myapp.ui.EMailLineEdit.text())
        self.assertEqual('', self.myapp.ui.ORCIDLineEdit.text())
        self.assertEqual('', self.myapp.ui.FootNoteLineEdit.text())
        self.assertEqual('', self.myapp.ui.PhoneLineEdit.text())
        self.assertEqual(False, self.myapp.ui.ContactAuthorCheckBox.isChecked())


if __name__ == '__main__':
    unittest.main()
