#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Union, List

import gemmi.cif
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


@dataclass()
class Author:
    name: str
    address: str
    email: str
    phone: str
    orcid: str
    footnote: str
    contact_author: bool
    author_type: str


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

    def make_sure_to_save_only_when_name_field_has_text(self) -> None:
        if not len(self.ui.FullNameLineEdit.text()):
            self.ui.SaveAuthorLoopToTemplateButton.setDisabled(True)
            self.ui.AddThisAuthorToLoopPushButton.setDisabled(True)
        else:
            self.ui.SaveAuthorLoopToTemplateButton.setEnabled(True)
            self.ui.AddThisAuthorToLoopPushButton.setEnabled(True)
        if not self.cif:
            self.ui.SaveAuthorLoopToTemplateButton.setDisabled(True)
            self.ui.AddThisAuthorToLoopPushButton.setDisabled(True)

    def get_author_loop(self, contact_author: bool = False, audit_author: bool = False) -> List:
        author_type = 'publ' if not audit_author else 'audit'
        if contact_author:
            author_loop = [f'_{author_type}_contact_author_name',
                           f'_{author_type}_contact_author_address',
                           f'_{author_type}_contact_author_email',
                           f'_{author_type}_contact_author_phone',
                           f'_{author_type}_contact_author_id_orcid', ]
        else:
            author_loop = [f'_{author_type}_author_name',
                           f'_{author_type}_author_address',
                           f'_{author_type}_author_email',
                           f'_{author_type}_author_phone',
                           f'_{author_type}_author_id_orcid',
                           f'_{author_type}_author_footnote',
                           ]
        return author_loop

    def save_author_to_loop(self):
        author = self.get_author_info()
        row = [author.name, author.address, author.email, author.phone, author.orcid, author.footnote]
        if author.contact_author:
            author_type = f'_{author.author_type}_contact_author_name'
            del row[-1]  # contact author has no footnote
        else:
            author_type = f'_{author.author_type}_author_name'
        if self.cif.block.find_loop(author_type):
            gemmi_loop: Loop = self.cif.block.find_loop(author_type).get_loop()
            if tuple(row) in list(grouper(gemmi_loop.values, len(row))):
                self.app.status_bar.show_message('This author already exists.', 10)
                print('dbg> Author already exists.')
                return
        else:
            gemmi_loop = self.cif.init_loop(self.get_author_loop(author.contact_author))
        self.check_if_loop_and_row_size_fit_together(gemmi_loop, row)
        self.app.make_loops_tables()
        self.show_authors_list()

    def check_if_loop_and_row_size_fit_together(self, gemmi_loop, row):
        if gemmi_loop.width() == len(row):
            gemmi_loop.add_row(row)
        else:
            show_general_warning('An author loop with different size is already in the CIF. Can not proceed.')

    def get_author_info(self) -> Author:
        if self.ui.authorEditTabWidget.currentWidget().objectName() == 'page_publication':
            name = quote(utf8_to_str(self.ui.FullNameLineEdit.text()))
            address = quote(utf8_to_str(self.ui.AddressTextedit.toPlainText()))
            email = quote(utf8_to_str(self.ui.EMailLineEdit.text()))
            footnote = quote(utf8_to_str(self.ui.FootNoteLineEdit.text()))
            orcid = quote(utf8_to_str(self.ui.ORCIDLineEdit.text()))
            phone = quote(utf8_to_str(self.ui.PhoneLineEdit.text()))
            contact: bool = self.ui.ContactAuthorCheckBox.isChecked()
            author_type = 'publ'
        else:
            name = quote(utf8_to_str(self.ui.FullNameLineEdit_cif.text()))
            address = quote(utf8_to_str(self.ui.AddressTextedit_cif.toPlainText()))
            email = quote(utf8_to_str(self.ui.EMailLineEdit_cif.text()))
            footnote = quote(utf8_to_str(self.ui.FootNoteLineEdit_cif.text()))
            orcid = quote(utf8_to_str(self.ui.ORCIDLineEdit_cif.text()))
            phone = quote(utf8_to_str(self.ui.PhoneLineEdit_cif.text()))
            contact: bool = self.ui.ContactAuthorCheckBox_cif.isChecked()
            author_type = 'audit'
        return Author(name=name, address=address, email=email, footnote=footnote,
                      orcid=orcid, phone=phone, contact_author=contact, author_type=author_type)

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
        if not author.name:
            return
        self.general_author_save(author)
        self.clear_fields()

    def general_author_save(self, author: Author):
        if not author.name:
            return
        if author.contact_author:
            itemtext = f'{retranslate_delimiter(as_string(author.name))} (contact author)'
        else:
            itemtext = as_string(author.name)
        if itemtext not in self.authors_list():
            self.settings.save_settings_dict(property='authors_list', name=itemtext, items=author)
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
        contact_author: bool = author.contact_author
        loop = self.get_author_loop(contact_author)
        data = [author.name, author.address, author.email, author.phone, author.orcid, author.footnote]
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
        block: gemmi.cif.Block = doc.sole_block()
        #table_data = {}
        #for item in block:
        #    if item.pair is not None:
        #        key, value = item.pair
        #        if key not in cif_auth_to_str:
        #            continue
        #        key = cif_auth_to_str.get(key)
        #        table_data.update({key: retranslate_delimiter(as_string(value).strip('\n\r ;'))})
        # TODO: Make this work:
        name = block.name.replace('__', ' ')
        name: str = block.find_value('_publ_contact_author_name')
        author = Author(name=name)
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

    def show_authors_list(self) -> None:
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

    def authors_list(self) -> List[str]:
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
    print(l.export_raw_data())
