#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
from contextlib import suppress
from pathlib import Path
from typing import Dict, Union, List

from PyQt5.QtWidgets import QListWidgetItem
from gemmi.cif import Loop, as_string

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.text import utf8_to_str, quote, retranslate_delimiter
from finalcif.equip_property.tools import read_document_from_cif_file
from finalcif.gui.dialogs import cif_file_save_dialog, show_general_warning, cif_file_open_dialog
from finalcif.gui.finalcif_gui import Ui_FinalCifWindow
from finalcif.tools.misc import grouper
from finalcif.tools.settings import FinalCifSettings

with suppress(ImportError):
    from finalcif.appwindow import AppWindow


class AuthorLoops():
    def __init__(self, ui: Ui_FinalCifWindow, cif: CifContainer, app: 'AppWindow'):
        self.ui = ui
        self.cif = cif
        self.app = app
        self.settings = FinalCifSettings()
        if app:
            self.contact_author_checked(False)
            self.ui.AddThisAuthorToLoopPushButton.clicked.connect(self.save_author_to_loop)
            self.ui.ContactAuthorCheckBox.stateChanged.connect(lambda: self.contact_author_checked(
                self.ui.ContactAuthorCheckBox.isChecked()))
            self.ui.LoopsTabWidget.currentChanged.connect(
                lambda: self.ui.AddThisAuthorToLoopPushButton.setDisabled(not self.ui.LoopsTabWidget.count()))
            self.ui.SaveAuthorLoopToTemplateButton.clicked.connect(self.save_author_to_loop_template)
            self.ui.LoopTemplatesListWidget.clicked.connect(self.load_selected_loop)
            self.ui.LoopTemplatesListWidget.doubleClicked.connect(self.save_author_to_loop)
            self.ui.DeleteLoopAuthorTemplateButton.clicked.connect(self.delete_current_author)
            self.ui.ExportAuthorPushButton.clicked.connect(self.export_author_template)
            self.ui.ImportAuthorPushButton.clicked.connect(self.import_author)
            self.ui.FullNameLineEdit.textChanged.connect(self.make_sure_to_save_only_when_name_field_has_text)
            self.show_authors_list()
            self.make_sure_to_save_only_when_name_field_has_text()

    def make_sure_to_save_only_when_name_field_has_text(self):
        if not len(self.ui.FullNameLineEdit.text()):
            self.ui.SaveAuthorLoopToTemplateButton.setDisabled(True)
            self.ui.AddThisAuthorToLoopPushButton.setDisabled(True)
        else:
            self.ui.SaveAuthorLoopToTemplateButton.setEnabled(True)
            self.ui.AddThisAuthorToLoopPushButton.setEnabled(True)
        if not self.cif:
            self.ui.SaveAuthorLoopToTemplateButton.setDisabled(True)
            self.ui.AddThisAuthorToLoopPushButton.setDisabled(True)

    def get_author_loop(self, contact_author: bool = False) -> List:
        if contact_author:
            author_loop = ['_publ_contact_author_name',
                           '_publ_contact_author_address',
                           '_publ_contact_author_email',
                           '_publ_contact_author_phone',
                           '_publ_contact_author_id_orcid', ]
        else:
            author_loop = ['_publ_author_name',
                           '_publ_author_address',
                           '_publ_author_email',
                           '_publ_author_phone',
                           '_publ_author_id_orcid',
                           '_publ_author_footnote',
                           ]
        return author_loop

    def save_author_to_loop(self):
        author = self.get_author_info()
        row = [author.get('name'), author.get('address'), author.get('email'), author.get('phone'),
               author.get('orcid'), author.get('footnote')]
        if self.ui.ContactAuthorCheckBox.isChecked():
            author_type = '_publ_contact_author_name'
            contact_author = True
            del row[-1]  # contact author has no footnote
        else:
            author_type = '_publ_author_name'
            contact_author = False
        if self.cif.block.find_loop(author_type):
            gemmi_loop: Loop = self.cif.block.find_loop(author_type).get_loop()
            if tuple(row) in list(grouper(gemmi_loop.values, len(row))):
                self.app.status_bar.show_message('This author already exists.', 10)
                print('author already there')
                return  # Author already exists
        else:
            gemmi_loop = self.cif.init_loop(self.get_author_loop(contact_author))
        self.check_if_loop_and_row_size_fit_together(gemmi_loop, row)
        self.app.make_loops_tables()
        self.show_authors_list()

    def check_if_loop_and_row_size_fit_together(self, gemmi_loop, row):
        if gemmi_loop.width() == len(row):
            gemmi_loop.add_row(row)
        else:
            show_general_warning('An author loop with different size is already in the CIF. Can not proceed.')

    def get_author_info(self) -> Dict[str, Union[str, bool, None]]:
        name = quote(utf8_to_str(self.ui.FullNameLineEdit.text()))
        address = quote(utf8_to_str(self.ui.AddressTextedit.toPlainText()))
        email = quote(utf8_to_str(self.ui.EMailLineEdit.text()))
        footnote = quote(utf8_to_str(self.ui.FootNoteLineEdit.text()))
        orcid = quote(utf8_to_str(self.ui.ORCIDLineEdit.text()))
        phone = quote(utf8_to_str(self.ui.PhoneLineEdit.text()))
        contact: bool = self.ui.ContactAuthorCheckBox.isChecked()
        return {'address': address, 'footnote': footnote, 'email': email,
                'name'   : name, 'orcid': orcid, 'phone': phone, 'contact': contact}

    def set_author_info(self, author: Dict[str, Union[str, None]]):
        if not author:
            return
        if author.get('name'):
            self.ui.FullNameLineEdit.setText(retranslate_delimiter(as_string(author.get('name'))))
        if author.get('address'):
            self.ui.AddressTextedit.setText(retranslate_delimiter(as_string(author.get('address'))))
        if author.get('email'):
            self.ui.EMailLineEdit.setText(retranslate_delimiter(as_string(author.get('email'))))
        if author.get('footnote'):
            self.ui.FootNoteLineEdit.setText(retranslate_delimiter(as_string(author.get('footnote'))))
        if author.get('orcid'):
            self.ui.ORCIDLineEdit.setText(retranslate_delimiter(as_string(author.get('orcid'))))
        if author.get('phone'):
            self.ui.PhoneLineEdit.setText(retranslate_delimiter(as_string(author.get('phone'))))
        self.ui.ContactAuthorCheckBox.setChecked(author.get('contact') or False)

    def clear_fields(self):
        self.ui.FullNameLineEdit.clear()
        self.ui.AddressTextedit.clear()
        self.ui.EMailLineEdit.clear()
        self.ui.FootNoteLineEdit.clear()
        self.ui.ORCIDLineEdit.clear()
        self.ui.PhoneLineEdit.clear()
        self.ui.ContactAuthorCheckBox.setChecked(False)

    def save_author_to_loop_template(self):
        author = self.get_author_info()
        if not author.get('name'):
            return
        self.general_author_save(author)
        self.clear_fields()

    def general_author_save(self, author_dict: dict):
        if not author_dict.get('name'):
            return
        if author_dict.get('contact'):
            itemtext = '{} (contact author)'.format(retranslate_delimiter(as_string(author_dict.get('name'))))
        else:
            itemtext = as_string(author_dict.get('name'))
        if itemtext not in self.authors_list():
            self.settings.save_settings_dict(property='authors_list', name=itemtext, items=author_dict)
        if not itemtext:
            return
        self.show_authors_list()

    def export_author_template(self, filename: str = None) -> None:
        """
        Exports the currently selected author to a file.
        """
        selected_template = self.get_currently_selected_author_name()
        if not selected_template:
            return
        blockname = '__'.join(selected_template.split())
        if not filename:
            filename = cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        author_cif = self.store_author_in_cif_object(blockname, filename)
        try:
            author_cif.save(Path(filename))
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning('No permission to write file to {}'.format(Path(filename).resolve()))

    def store_author_in_cif_object(self, blockname, filename):
        author = self.get_author_info()
        author_cif = CifContainer(filename, new_block=blockname)
        contact_author: bool = author.get('contact')
        loop = self.get_author_loop(contact_author)
        data = [author.get('name'), author.get('address'), author.get('email'), author.get('phone'),
                author.get('orcid'), author.get('footnote')]
        if contact_author:
            del data[-1]
        for key, value in zip(loop, data):
            author_cif.set_pair_delimited(key, as_string(value))
        return author_cif

    def import_author(self, filename=''):
        """
        Import an author from a cif file.
        """
        cif_auth_to_str = {'_publ_contact_author_name'    : 'name',
                           '_publ_contact_author_address' : 'address',
                           '_publ_contact_author_email'   : 'email',
                           '_publ_contact_author_phone'   : 'phone',
                           '_publ_contact_author_id_orcid': 'orcid',
                           #
                           '_publ_author_name'            : 'name',
                           '_publ_author_address'         : 'address',
                           '_publ_author_email'           : 'email',
                           '_publ_author_phone'           : 'phone',
                           '_publ_author_id_orcid'        : 'orcid',
                           '_publ_author_footnote'        : 'footnote', }
        if not filename:
            filename = cif_file_open_dialog(filter="CIF file (*.cif)")
        if not filename:
            return
        doc = read_document_from_cif_file(filename)
        if not doc:
            return
        block = doc.sole_block()
        table_data = {}
        for item in block:
            if item.pair is not None:
                key, value = item.pair
                if key not in cif_auth_to_str:
                    continue
                key = cif_auth_to_str.get(key)
                table_data.update({key: retranslate_delimiter(as_string(value).strip('\n\r ;'))})
        name = block.name.replace('__', ' ')
        if 'contact author' in name:
            table_data.update({'contact': True})
        if not table_data.get('name'):
            return None
        self.general_author_save(table_data)
        self.show_authors_list()

    def delete_current_author(self):
        selected_author_name = self.get_currently_selected_author_name()
        if not selected_author_name:
            return
        self.ui.LoopTemplatesListWidget.clear()
        self.settings.delete_template('authors_list', selected_author_name)
        self.show_authors_list()

    def get_selected_loop_name(self) -> str:
        selected_row_text = self.get_currently_selected_author_name() or ''
        return selected_row_text

    def get_currently_selected_author_name(self):
        return self.ui.LoopTemplatesListWidget.currentIndex().data()

    def load_selected_loop(self):
        self.set_author_info(self.author_loopdata(author_name=self.get_selected_loop_name()))
        self.ui.LoopsTabWidget.setCurrentIndex(0)

    def author_loopdata(self, author_name):
        return self.settings.load_settings_dict('authors_list', author_name)

    def show_authors_list(self):
        self.ui.LoopTemplatesListWidget.clear()
        for author in sorted(self.authors_list()):
            if author:
                self.ui.LoopTemplatesListWidget.addItem(QListWidgetItem(author))

    def export_raw_data(self) -> List[Dict]:
        """Export all authors in order to export them all"""
        authors = []
        for author in self.authors_list():
            author_data = self.author_loopdata(author)
            authors.append(author_data)
        return authors

    def import_raw_data(self, authors_data: List[Dict]):
        """Import all authors from an external file"""
        for author in authors_data:
            if author:
                self.general_author_save(author)

    def authors_list(self):
        return self.settings.list_saved_items(property='authors_list')

    def contact_author_checked(self, checked: bool):
        """
        :parameter checked: state of the ContactAuthorCheckBox
        """
        if checked:
            self.ui.FullNameLineEdit.setToolTip('_publ_contact_author_name')
            self.ui.AddressTextedit.setToolTip('_publ_contact_author_address')
            self.ui.EMailLineEdit.setToolTip('_publ_contact_author_email')
            self.ui.PhoneLineEdit.setToolTip('_publ_contact_author_phone')
            self.ui.ORCIDLineEdit.setToolTip('_publ_contact_author_id_orcid')
            self.ui.FootNoteLineEdit.setDisabled(True)
            self.ui.footnote_label.setDisabled(True)
        else:
            self.ui.FullNameLineEdit.setToolTip('_publ_author_name')
            self.ui.AddressTextedit.setToolTip('_publ_author_address')
            self.ui.EMailLineEdit.setToolTip('_publ_author_email')
            self.ui.PhoneLineEdit.setToolTip('_publ_author_phone')
            self.ui.ORCIDLineEdit.setToolTip('_publ_author_id_orcid')
            self.ui.FootNoteLineEdit.setToolTip('_publ_author_footnote')
            self.ui.FootNoteLineEdit.setEnabled(True)
            self.ui.footnote_label.setEnabled(True)


if __name__ == '__main__':
    l = AuthorLoops(Ui_FinalCifWindow(), CifContainer('test-data/1000007.cif'), None)
    l.export_data()
