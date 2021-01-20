#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
from contextlib import suppress
from pathlib import Path
from typing import Dict, Union

from PyQt5.QtWidgets import QListWidgetItem
from gemmi import cif

from cif.cif_file_io import CifContainer
from cif.text import utf8_to_str, quote, retranslate_delimiter, set_pair_delimited
from gui.dialogs import cif_file_save_dialog, show_general_warning, cif_file_open_dialog
from gui.finalcif_gui import Ui_FinalCifWindow
from tools.misc import grouper
from tools.settings import FinalCifSettings

with suppress(ImportError):
    from appwindow import AppWindow


class AuthorLoops():
    def __init__(self, ui: Ui_FinalCifWindow, cif: CifContainer, app: 'AppWindow'):
        self.ui = ui
        self.cif = cif
        self.app = app
        self.settings = FinalCifSettings()
        self.ui.AddThisAuthorToLoopPushButton.clicked.connect(self.save_author_to_loop)
        self.ui.ContactAuthorCheckBox.stateChanged.connect(lambda: self.ui.FootNoteLineEdit.setDisabled(
            self.ui.ContactAuthorCheckBox.isChecked()))
        self.ui.LoopsTabWidget.currentChanged.connect(
            lambda: self.ui.AddThisAuthorToLoopPushButton.setDisabled(not self.ui.LoopsTabWidget.count()))
        self.ui.SaveAuthorLoopToTemplateButton.clicked.connect(self.save_author_to_loop_template)
        self.ui.LoopTemplatesListWidget.clicked.connect(self.load_selected_loop)
        self.ui.DeleteLoopAuthorTemplateButton.clicked.connect(self.delete_current_author)
        self.ui.ExportAuthorPushButton.clicked.connect(self.export_author_template)
        self.ui.ImportAuthorPushButton.clicked.connect(self.import_author)
        self.ui.FullNameLineEdit.textChanged.connect(self.make_sure_to_save_only_when_name_field_has_text)
        self.show_author_loops()
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
            g_loop: cif.Loop = self.cif.block.find_loop(author_type).get_loop()
            if tuple(row) in list(grouper(g_loop.values, len(row))):
                self.app.status_bar.show_message('This author already exists.', 10)
                print('author already there')
                return  # Author already exists
        else:
            g_loop = self.cif.init_author_loop(contact_author)
        g_loop.add_row(row)
        self.app.make_loops_tables()
        self.show_author_loops()

    def get_author_info(self) -> Dict[str, Union[str, None]]:
        name = quote(utf8_to_str(self.ui.FullNameLineEdit.text()))
        address = quote(utf8_to_str(self.ui.AddressTextedit.toPlainText()))
        email = quote(utf8_to_str(self.ui.EMailLineEdit.text()))
        footnote = quote(utf8_to_str(self.ui.FootNoteLineEdit.text()))
        orcid = quote(utf8_to_str(self.ui.ORCIDLineEdit.text()))
        phone = quote(utf8_to_str(self.ui.PhoneLineEdit.text()))
        contact = self.ui.ContactAuthorCheckBox.isChecked()
        return {'address': address, 'footnote': footnote, 'email': email,
                'name'   : name, 'orcid': orcid, 'phone': phone, 'contact': contact}

    def set_author_info(self, author: Dict[str, Union[str, None]]):
        if not author:
            return
        if author.get('name'):
            self.ui.FullNameLineEdit.setText(retranslate_delimiter(cif.as_string(author.get('name'))))
        if author.get('address'):
            self.ui.AddressTextedit.setText(retranslate_delimiter(cif.as_string(author.get('address'))))
        if author.get('email'):
            self.ui.EMailLineEdit.setText(retranslate_delimiter(cif.as_string(author.get('email'))))
        if author.get('footnote'):
            self.ui.FootNoteLineEdit.setText(retranslate_delimiter(cif.as_string(author.get('footnote'))))
        if author.get('orcid'):
            self.ui.ORCIDLineEdit.setText(retranslate_delimiter(cif.as_string(author.get('orcid'))))
        if author.get('phone'):
            self.ui.PhoneLineEdit.setText(retranslate_delimiter(cif.as_string(author.get('phone'))))
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
        if author.get('name') == '' or None:
            return
        self.general_author_save(author)
        self.clear_fields()

    def general_author_save(self, author: dict):
        if not author.get('name'):
            return
        if author.get('contact'):
            itemtext = '{} (contact author)'.format(retranslate_delimiter(cif.as_string(author.get('name'))))
        else:
            itemtext = cif.as_string(author.get('name'))
        authors = self.settings.get_equipment_list(equipment='authors_list')
        if itemtext not in authors:
            self.settings.save_loop_template(name=itemtext, items=author)
            self.settings.save_to_equipment_list(itemtext, templ_type='authors_list')
        if not itemtext:
            return
        self.show_author_loops()

    def export_author_template(self, filename: str = None) -> None:
        """
        Exports the currently selected author to a file.
        """
        table_data = self.get_author_info()
        selected_template = self.ui.LoopTemplatesListWidget.currentIndex().data()
        if not selected_template:
            return
        doc = cif.Document()
        blockname = '__'.join(selected_template.split())
        block = doc.add_new_block(blockname)
        contact_author = table_data.get('contact')
        for key, value in zip(table_data.keys(), table_data.values()):
            if key == 'name':
                key = '_publ_contact_author_name' if contact_author else '_publ_author_name'
            elif key == 'address':
                key = '_publ_contact_author_address' if contact_author else '_publ_author_address'
            elif key == 'email':
                key = '_publ_contact_author_email' if contact_author else '_publ_author_email'
            elif key == 'footnote':
                if contact_author:
                    continue
                key = '_publ_author_footnote'
            elif key == 'phone':
                key = '_publ_contact_author_phone' if contact_author else '_publ_author_phone'
            elif key == 'orcid':
                key = '_publ_contact_author_id_orcid' if contact_author else '_publ_author_id_orcid'
            else:
                continue
            set_pair_delimited(block, key, cif.as_string(value.strip('\n\r ')))
        if not filename:
            filename = cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=cif.Style.Indent35)
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning('No permission to write file to {}'.format(Path(filename).absolute()))

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
        try:
            doc = cif.read_file(filename)
        except RuntimeError as e:
            show_general_warning(str(e))
            return
        block = doc.sole_block()
        table_data = {}
        for item in block:
            if item.pair is not None:
                key, value = item.pair
                if not key in cif_auth_to_str:
                    continue
                key = cif_auth_to_str.get(key)
                table_data.update({key: retranslate_delimiter(cif.as_string(value).strip('\n\r ;'))})
        name = block.name.replace('__', ' ')
        if 'contact author' in name:
            table_data.update({'contact': True})
        if not table_data.get('name'):
            return None
        self.general_author_save(table_data)
        self.show_author_loops()

    def delete_current_author(self):
        index = self.ui.LoopTemplatesListWidget.currentIndex()
        selected_template_text = index.data()
        if not selected_template_text:
            return
        self.ui.LoopTemplatesListWidget.clear()
        self.settings.delete_template('authors_list/' + selected_template_text)
        authors_list = self.settings.settings.value('authors_list') or []
        try:
            authors_list.remove(selected_template_text)
        except ValueError:
            pass
        self.settings.save_template('authors_list', authors_list)
        self.show_author_loops()

    def get_selected_loop_name(self) -> str:
        listwidget = self.ui.LoopTemplatesListWidget
        selected_row_text = listwidget.currentIndex().data()
        if not selected_row_text:
            return ''
        return selected_row_text

    def load_selected_loop(self):
        author_loopdata = self.settings.load_loop_template(self.get_selected_loop_name())
        self.set_author_info(author_loopdata)

    def show_author_loops(self):
        self.ui.LoopTemplatesListWidget.clear()
        l = self.settings.get_equipment_list(equipment='authors_list')
        for loop in sorted(l):
            if loop:
                item = QListWidgetItem(loop)
                self.ui.LoopTemplatesListWidget.addItem(item)
