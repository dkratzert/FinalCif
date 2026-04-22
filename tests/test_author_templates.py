import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path
from unittest.mock import patch

from finalcif.appwindow import AppWindow
from finalcif.equip_property.author_loop_templates import AuthorLoops, Author, AuthorType

data = Path('tests')


class MyTestCase(AppWindowTestCase):

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
        super().tearDown()

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
                listWidget.setCurrentRow(row)
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

    def test_import_multiple_authors(self):
        multi_author_cif = data / 'examples/multi_author_test.cif'
        self.app.authors.import_author(str(multi_author_cif))

        self._select_row_of_author('Contact Author')
        self.app.authors.load_selected_loop()
        self.assertEqual('Contact Author (contact author)', self.app.authors.get_selected_loop_name())
        self.assertEqual('single@contact.de', self.app.authors.get_author_info().email)
        self.assertEqual(True, self.app.authors.get_author_info().contact_author)
        self._delete_test_author('Contact Author (contact author)')

        self._select_row_of_author('Author One')
        self.app.authors.load_selected_loop()
        self.assertEqual('Author One', self.app.authors.get_selected_loop_name())
        self.assertEqual('one@test.de', self.app.authors.get_author_info().email)
        self.assertEqual(False, self.app.authors.get_author_info().contact_author)
        self._delete_test_author('Author One')

        self._select_row_of_author('Author Two')
        self.app.authors.load_selected_loop()
        self.assertEqual('Author Two', self.app.authors.get_selected_loop_name())
        self.assertEqual("''", self.app.authors.get_author_info().email)
        self.assertEqual(False, self.app.authors.get_author_info().contact_author)
        self._delete_test_author('Author Two')


class UniqueAuthorNameTestCase(unittest.TestCase):
    """Unit tests for AuthorLoops._unique_author_name — no GUI needed."""

    def _make_loops(self, existing: list[str]) -> AuthorLoops:
        loops = AuthorLoops.__new__(AuthorLoops)
        loops._rename_old_name = ''
        loops._rename_menu = None
        loops.authors_list = lambda: list(existing)
        return loops

    def test_unique_name_returns_base_when_no_clash(self):
        loops = self._make_loops(['Alice'])
        self.assertEqual('Bob', loops._unique_author_name('Bob'))

    def test_unique_name_appends_2_on_first_clash(self):
        loops = self._make_loops(['Alice'])
        self.assertEqual('Alice 2', loops._unique_author_name('Alice'))

    def test_unique_name_skips_taken_numbers(self):
        loops = self._make_loops(['Alice', 'Alice 2', 'Alice 3'])
        self.assertEqual('Alice 4', loops._unique_author_name('Alice'))

    def test_unique_name_empty_list(self):
        loops = self._make_loops([])
        self.assertEqual('Alice', loops._unique_author_name('Alice'))

    def test_author_template_name_regular(self):
        loops = self._make_loops([])
        author = Author(name='John Doe', address='', email='', phone='',
                        orcid='', footnote='', contact_author=False,
                        author_type=AuthorType.publ)
        self.assertEqual('John Doe', loops._author_template_name(author))

    def test_author_template_name_contact_author(self):
        loops = self._make_loops([])
        author = Author(name='John Doe', address='', email='', phone='',
                        orcid='', footnote='', contact_author=True,
                        author_type=AuthorType.publ)
        self.assertEqual('John Doe (contact author)', loops._author_template_name(author))


class ImportAuthorDeduplicationTestCase(AppWindowTestCase):
    """Integration tests: importing the same CIF author twice must deduplicate."""

    def setUp(self) -> None:
        self.testcif = data / 'examples/1979688.cif'
        self.testimport_author = data / 'other_templates/AATest_Author.cif'
        self.app = AppWindow(self.testcif)
        self.app.ui.authorEditTabWidget.setCurrentIndex(0)
        self._cleanup()

    def tearDown(self) -> None:
        self._cleanup()
        self.app.close()
        super().tearDown()

    def _cleanup(self):
        for name in list(self.app.authors.authors_list()):
            if name and name.startswith('AATest Author'):
                self.app.authors.settings.delete_template('authors_list', name)
        self.app.authors.show_authors_list()

    def test_import_same_author_twice_creates_distinct_entries(self):
        self.app.authors.import_author(str(self.testimport_author))
        self.app.authors.import_author(str(self.testimport_author))
        authors = self.app.authors.authors_list()
        self.assertIn('AATest Author', authors)
        self.assertIn('AATest Author 2', authors)

    def test_import_three_times_creates_three_entries(self):
        for _ in range(3):
            self.app.authors.import_author(str(self.testimport_author))
        authors = self.app.authors.authors_list()
        self.assertIn('AATest Author', authors)
        self.assertIn('AATest Author 2', authors)
        self.assertIn('AATest Author 3', authors)

    def test_reimport_does_not_overwrite_existing_entry(self):
        self.app.authors.import_author(str(self.testimport_author))
        first_data = self.app.authors.author_loopdata('AATest Author')
        self.app.authors.import_author(str(self.testimport_author))
        after_data = self.app.authors.author_loopdata('AATest Author')
        self.assertEqual(first_data, after_data)


if __name__ == '__main__':
    unittest.main()
