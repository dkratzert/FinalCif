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
    author_type: str  # 'publ' or 'audit'


class AuthorLoops():
    def __init__(self, ui: Ui_FinalCifWindow, cif: CifContainer, app: 'AppWindow'):
        self.ui = ui
        self.cif = cif
        self.app = app
        self.settings = FinalCifSettings()
        if app:
            self.contact_author_checked(self.ui.ContactAuthorCheckBox.isChecked())
            self.connect_signals_and_slots()
            self.show_authors_list()
            self.make_sure_to_save_only_when_name_field_has_text()

    def connect_signals_and_slots(self):
        self.ui.AddThisAuthorToLoopPushButton.clicked.connect(self.save_author_to_loop)
        self.ui.AddThisAuthorToLoopPushButton_cif.clicked.connect(self.save_author_to_loop)
        self.ui.ContactAuthorCheckBox.stateChanged.connect(self.contact_author_checked)
        self.ui.ContactAuthorCheckBox_cif.stateChanged.connect(self.contact_author_checked)
        self.ui.LoopsTabWidget.currentChanged.connect(
            lambda: self.ui.AddThisAuthorToLoopPushButton.setDisabled(not self.ui.LoopsTabWidget.count()))
        self.ui.authorEditTabWidget.currentChanged.connect(self.contact_author_checked)
        self.ui.SaveAuthorLoopToTemplateButton.clicked.connect(self.save_author_to_loop_template)
        # self.ui.authorEditTabWidget.currentChanged.connect(lambda: self.clear_fields())
        self.ui.LoopTemplatesListWidget.clicked.connect(self.load_selected_loop)
        # self.ui.LoopTemplatesListWidget.doubleClicked.connect(self.save_author_to_loop)
        self.ui.DeleteLoopAuthorTemplateButton.clicked.connect(self.delete_current_author)
        self.ui.ExportAuthorPushButton.clicked.connect(self.export_author_template)
        self.ui.ImportAuthorPushButton.clicked.connect(self.import_author)
        self.ui.FullNameLineEdit.textChanged.connect(self.make_sure_to_save_only_when_name_field_has_text)

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

    def get_author_loop(self, author: Author) -> List:
        contact = 'contact_' if author.contact_author else ''
        author_loop = [f'_{author.author_type}_{contact}author_name',
                       f'_{author.author_type}_{contact}author_address',
                       f'_{author.author_type}_{contact}author_email',
                       f'_{author.author_type}_{contact}author_phone',
                       f'_{author.author_type}_{contact}author_id_orcid', ]
        if not author.contact_author:
            author_loop.append(f'_{author.author_type}_author_footnote')
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
            gemmi_loop = self.cif.init_loop(self.get_author_loop(author))
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
            # _publ_author has no phone number!
            #phone = quote(utf8_to_str(self.ui.PhoneLineEdit.text()))
            phone = ''
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

    def set_author_info(self, author: Union[Dict[str, Union[str, None]], Author]):
        if not author:
            return
        author_type = 'publ' if self.ui.authorEditTabWidget.currentWidget().objectName() == 'page_publication' else 'cif'
        if type(author) == dict:
            author = Author(name=author.get('name'), address=author.get('address'), email=author.get('email'),
                            phone=author.get('phone'), orcid=author.get('orcid'), footnote=author.get('footnote'),
                            contact_author=author.get('contact', False), author_type=author_type)
        # In order to use authors for cif and publication:
        author.author_type = author_type
        self.set_authorinfo(author)
        self.ui.ContactAuthorCheckBox.setChecked(author.contact_author or False)
        self.ui.ContactAuthorCheckBox_cif.setChecked(author.contact_author or False)

    def set_authorinfo(self, author: Author):
        author_type = "_cif" if author.author_type == "cif" else ""
        if author.name:
            getattr(self.ui, f'FullNameLineEdit{author_type}').setText(retranslate_delimiter(as_string(author.name)))
        if author.address:
            getattr(self.ui, f'AddressTextedit{author_type}').setText(retranslate_delimiter(as_string(author.address)))
        if author.email:
            getattr(self.ui, f'EMailLineEdit{author_type}').setText(retranslate_delimiter(as_string(author.email)))
        if author.footnote:
            getattr(self.ui, f'FootNoteLineEdit{author_type}').setText(
                retranslate_delimiter(as_string(author.footnote)))
        if author.orcid:
            getattr(self.ui, f'ORCIDLineEdit{author_type}').setText(retranslate_delimiter(as_string(author.orcid)))
        if author.phone:
            getattr(self.ui, f'PhoneLineEdit{author_type}').setText(retranslate_delimiter(as_string(author.phone)))

    def clear_fields(self):
        self.ui.FullNameLineEdit.clear()
        self.ui.AddressTextedit.clear()
        self.ui.EMailLineEdit.clear()
        self.ui.FootNoteLineEdit.clear()
        self.ui.ORCIDLineEdit.clear()
        self.ui.PhoneLineEdit.clear()
        self.ui.ContactAuthorCheckBox.setChecked(False)
        self.ui.FullNameLineEdit_cif.clear()
        self.ui.AddressTextedit_cif.clear()
        self.ui.EMailLineEdit_cif.clear()
        self.ui.FootNoteLineEdit_cif.clear()
        self.ui.ORCIDLineEdit_cif.clear()
        self.ui.PhoneLineEdit_cif.clear()
        self.ui.ContactAuthorCheckBox_cif.setChecked(False)

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
        loop = self.get_author_loop(author)
        data = [author.name, author.address, author.email, author.phone, author.orcid, author.footnote]
        if author.contact_author:
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
        # table_data = {}
        # for item in block:
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
        page = "_cif" if self.ui.authorEditTabWidget.currentWidget().objectName() == 'page_audit' else ""
        author_type = 'publ' if self.ui.authorEditTabWidget.currentWidget().objectName() == 'page_publication' else 'audit'
        contact = 'contact_' if checked else ''

        print(f'page: {page}, author: {author_type}, contact: {contact}')

        getattr(self.ui, f'FullNameLineEdit{page}').setToolTip(f'_{author_type}_{contact}author_name')
        getattr(self.ui, f'AddressTextedit{page}').setToolTip(f'_{author_type}_{contact}author_address')
        getattr(self.ui, f'EMailLineEdit{page}').setToolTip(f'_{author_type}_{contact}author_email')
        getattr(self.ui, f'PhoneLineEdit{page}').setToolTip(f'_{author_type}_{contact}author_phone')
        getattr(self.ui, f'ORCIDLineEdit{page}').setToolTip(f'_{author_type}_{contact}author_id_orcid')
        getattr(self.ui, f'FootNoteLineEdit{page}').setToolTip(f'_{author_type}_{contact}author_footnote')
        getattr(self.ui, f'footnote_label{page}').setToolTip(f'_{author_type}_{contact}author_footnote')
        if getattr(self.ui, f'ContactAuthorCheckBox{page}').isChecked():
            getattr(self.ui, f'FootNoteLineEdit{page}').setDisabled(True)
            getattr(self.ui, f'footnote_label{page}').setDisabled(True)
        else:
            getattr(self.ui, f'FootNoteLineEdit{page}').setEnabled(True)
            getattr(self.ui, f'footnote_label{page}').setEnabled(True)
        if author_type == 'publ':
            getattr(self.ui, f'PhoneLineEdit{page}').setDisabled(True)
        else:
            getattr(self.ui, f'PhoneLineEdit{page}').setEnabled(True)


if __name__ == '__main__':
    l = AuthorLoops(Ui_FinalCifWindow(), CifContainer('test-data/1000007.cif'), None)
    print(l.export_raw_data())
