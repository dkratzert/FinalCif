import io
from pathlib import Path
from typing import Union, List

import requests
from PyQt5.QtWidgets import QTableWidgetItem, QTextBrowser, QFrame

from cif.cif_file_io import CifContainer
from cif.cod.deposition_list import CODFetcher
from cif.cod.doi import resolve_doi
from cif.cod.website_parser import MyCODStructuresParser
from cif.hkl import HKL
from gui.dialogs import cif_file_open_dialog, show_general_warning
from gui.finalcif_gui import Ui_FinalCifWindow
from tools.settings import FinalCifSettings
from tools.version import VERSION

"""
COD-number has 7 digits

* In general, each option for replace should habe a textedit input for the 
 change log and a lineEdit to give the COD-ID

Personal Problems:
- Depositing structure 'cif' into TESTCOD:
    -> should be named as _data value
    ----> Test this again

"""


class CODdeposit():

    def __init__(self, ui: Ui_FinalCifWindow, cif: Union[CifContainer, None] = None):
        self.hkl_file: Union[Path, None] = None
        self.ui = ui
        self.settings = FinalCifSettings()
        self._cif = cif
        self._set_checkbox_states()
        self.ui.depositorUsernameLineEdit.textChanged.connect(self._set_username)
        self.ui.depositorPasswordLineEdit.textChanged.connect(self._set_password)
        self.ui.userEmailLineEdit.textChanged.connect(self._set_user_email)
        self.ui.authorEditorPushButton.clicked.connect(self.author_editor_clicked)
        self.ui.authorEditorPushButton_2.clicked.connect(self.author_editor_clicked)
        self.ui.refreshDepositListPushButton.clicked.connect(self._refresh_cod_list)
        self.ui.GetDOIPushButton.clicked.connect(self.get_doi_data)
        self.ui.Upload_hkl_pushButton.clicked.connect(self._set_external_hkl_file)
        #
        self.ui.BackToCODPushButton.clicked.connect(self._back_to_cod_page)
        #
        self.ui.depositCIFpushButton.clicked.connect(self._prepare_deposit)
        # The full deposit url: self.deposit_url = 'http://127.0.0.1:8080/cod/cgi-bin/cif-deposit.pl'
        self.main_url = 'https://www.crystallography.net/cod-test/'
        self.deposit_url = self.main_url + 'cgi-bin/cif-deposit.pl'
        self.username = self.settings.load_value_of_key('cod_username')
        if self.username:
            self.ui.depositorUsernameLineEdit.setText(self.username)
        else:
            self.username = ''
        self.password = ''
        self.author_name = ''
        self.author_email = ''
        self._cod_token = ''
        self.user_email = self.settings.load_value_of_key('cod_user_email')
        if self.user_email:
            self.ui.userEmailLineEdit.setText(self.user_email)
        else:
            self.user_email = ''
        if self.settings.load_settings_list('COD', self.username):
            self.add_structures_to_table(self.settings.load_settings_list('COD', self.username))

    def author_editor_clicked(self):
        self.ui.MainStackedWidget.go_to_loops_page()
        self.ui.TemplatesStackedWidget.setCurrentIndex(1)
        self.ui.BackToCODPushButton.setVisible(True)

    @property
    def cif(self) -> CifContainer:
        return self._cif

    @cif.setter
    def cif(self, obj):
        self.ui.depositCIFpushButton.setEnabled(True)
        self._cif = obj
        self.check_for_publ_author()
        self.ui.depositHKLcheckBox.setChecked(len(self._cif['_shelx_hkl_file']))

    def _back_to_cod_page(self):
        self.ui.BackToCODPushButton.clicked.connect(lambda: self.ui.BackToCODPushButton.setVisible(False))
        self.ui.MainStackedWidget.got_to_cod_page()
        self.check_for_publ_author()
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)

    def check_for_publ_author(self):
        try:
            self.author_name = self.cif.get_loop_column('_publ_author_name')[0]
            self.author_email = self.cif.get_loop_column('_publ_author_email')[0]
            self.ui.ContactAuthorLineEdit.setText(self.author_name)
            self.ui.ContactEmailLineEdit.setText(self.author_email)
            self.ui.ContactAuthorLineEdit_2.setText(self.author_name)
            self.ui.ContactEmailLineEdit_2.setText(self.author_email)
            print(self.author_name, self.author_email)
        except (IndexError, AttributeError):
            self.author_name = ''
            self.author_email = ''
        if not self.author_name:
            self.show_author_edit_button()
        else:
            self.hide_author_edit_button()

    def hide_author_edit_button(self):
        self.ui.authorsFullNamePersonalLabel.setVisible(False)
        self.ui.authorsFullNamePersonalLabel_2.setVisible(False)
        self.ui.authorEditorPushButton.setVisible(False)
        self.ui.authorEditorPushButton_2.setVisible(False)
        self.ui.depositCIFpushButton.setEnabled(True)

    def show_author_edit_button(self):
        self.ui.authorsFullNamePersonalLabel.setVisible(True)
        self.ui.authorsFullNamePersonalLabel_2.setVisible(True)
        self.ui.authorEditorPushButton.setVisible(True)
        self.ui.authorEditorPushButton_2.setVisible(True)
        # self.ui.depositCIFpushButton.setDisabled(True)

    def _set_checkbox_states(self):
        self.ui.prepublicationDepositRadioButton.clicked.connect(self._prepublication_was_toggled)
        self.ui.publishedDepositionRadioButton.clicked.connect(self._published_was_toggled)
        self.ui.personalDepositRadioButton.clicked.connect(self._personal_was_toggled)
        self.ui.personalDepositRadioButton.setChecked(True)
        self.deposition_type = 'personal'
        self.ui.depositionOptionsStackedWidget.setCurrentIndex(0)

    def _personal_was_toggled(self, state: bool):
        self.ui.prepublicationDepositRadioButton.setChecked(False)
        self.ui.publishedDepositionRadioButton.setChecked(False)
        if state:
            self.ui.depositionOptionsStackedWidget.setCurrentIndex(0)
            self.deposition_type = 'personal'
            self.reset_deposit_button_state_to_initial()

    def _prepublication_was_toggled(self, state: bool):
        self.ui.publishedDepositionRadioButton.setChecked(False)
        self.ui.personalDepositRadioButton.setChecked(False)
        if state:
            self.ui.depositionOptionsStackedWidget.setCurrentIndex(1)
            self.deposition_type = 'prepublication'
            self.reset_deposit_button_state_to_initial()

    def _published_was_toggled(self, state: bool):
        self.ui.prepublicationDepositRadioButton.setChecked(False)
        self.ui.personalDepositRadioButton.setChecked(False)
        if state:
            self.ui.depositionOptionsStackedWidget.setCurrentIndex(2)
            self.deposition_type = 'published'
            self.reset_deposit_button_state_to_initial()

    @staticmethod
    def deposition_type_to_int(deposition_type: str):
        if deposition_type == 'personal':
            return 0
        if deposition_type == 'prepublication':
            return 1
        if deposition_type == 'published':
            return 2
        # This is the output page:
        if deposition_type == 'deposit':
            return 3

    def _refresh_cod_list(self):
        if self.settings.load_settings_list('COD', self.username) and self.ui.CODtableWidget.rowCount() == 0:
            self.add_structures_to_table(self.settings.load_settings_list('COD', self.username))
        else:
            parser = self.get_structures_from_cod()
            self.settings.save_settings_list('COD', self.username, parser.structures)
            self.add_structures_to_table(parser.structures, parser.token)

    def get_structures_from_cod(self):
        f = CODFetcher(self.main_url)
        if not self._cod_token:
            self._cod_token = f.get_token(username=self.username, password=self.password)
        f.get_table_data_by_token(self._cod_token)
        parser = MyCODStructuresParser()
        parser.feed(f.table_html)
        return parser

    def add_structures_to_table(self, structures: List[dict], token: str = ''):
        self.ui.CODtableWidget.setRowCount(0)
        for row, structure in enumerate(structures):
            num = structure['number']
            date = structure['date']
            time = structure['time']
            if token:
                url = self.main_url + 'information_card.php?id={0}&CODSESSION={1}'.format(num, token)
                num = num + '*'
            else:
                url = self.main_url + 'information_card.php?id={0}'.format(num)
            self.ui.CODtableWidget.insertRow(row)
            self.ui.CODtableWidget.setItem(row, 0, QTableWidgetItem(num))
            self.ui.CODtableWidget.setItem(row, 1, QTableWidgetItem(date))
            self.ui.CODtableWidget.setItem(row, 2, QTableWidgetItem(time))
            link = '<a href="{}">{}</a>'.format(url, num)
            self._set_link_to_cell(link, row)

    def _set_link_to_cell(self, link, row):
        text_browser = QTextBrowser(self.ui.CODtableWidget)
        text_browser.setText(link)
        text_browser.setFrameShape(QFrame.NoFrame)
        text_browser.setOpenExternalLinks(True)
        text_browser.setStyleSheet("QTextEdit { padding-left:13; padding-top:2; padding-bottom:5; padding-right:10}")
        self.ui.CODtableWidget.setCellWidget(row, 0, text_browser)

    def get_doi_data(self):
        citation = resolve_doi(self.ui.publication_doi_lineedit.text())
        self.ui.DOIResolveTextLabel.clear()
        for key, value in citation.items():
            if key == '_publ_author_name' and value:
                value = value[0]
            self.ui.DOIResolveTextLabel.setText(self.ui.DOIResolveTextLabel.text() + "{}: {}\n\n".format(key, value))
            self.cif.set_pair_delimited(key, value)
        # self.ui.depositCIFpushButton.setEnabled(True)

    def cif_deposit(self):
        self.switch_to_page('deposit')
        if not self.cif:
            print('No cif opened!')
            return
        self.ui.depositOutputTextBrowser.setText('starting deposition in "{}" mode ...'.format(self.deposition_type))
        print('starting deposition of ', self.cif.fileobj.name)
        data = {'username'       : self.username,
                'password'       : self.password,
                'user_email'     : self.user_email,  # 'dkratzert@gmx.de',
                'deposition_type': self.deposition_type,  # published prepublication, personal
                'output_mode'    : 'html',
                # 'progress'       : '1',  # must be 1 if supplied! Otherwise do not submit.
                'filename'       : self.cif.fileobj.name,
                }
        if self.deposition_type == 'personal':
            data.update({'author_name' : self.author_name,
                         'author_email': self.author_email or self.user_email})
        if self.deposition_type == 'prepublication':
            # Prepublication and replace is possible with the REST API. I think I let users update
            # their deposited files on the website only.
            data.update({'author_name' : self.author_name,
                         'author_email': self.author_email or self.user_email,
                         'hold_period' : str(self.ui.embargoTimeInMonthsSpinBox.value())})
        if self.deposition_type == 'published':
            # Nothing to define extra:
            pass
        cif_fileobj = io.StringIO(self.cif.cif_as_string())
        # Path('/Users/daniel/Documents/GitHub/FinalCif/testcif.txt').write_text(cif_fileobj.read())
        if self.ui.depositHKLcheckBox.isChecked():
            # TODO: Always upload hkl data if present, but let the option to choose another hkl if no hkl is in cif
            hkl_fileobj = io.StringIO(self.cif.hkl_as_cif)
            hklname = self.cif.fileobj.stem + '.hkl'
            # Path('test.hkl').write_text(hklf.getvalue())
            files = {'cif': (self.cif.filename, cif_fileobj, 'multipart/form-data'),
                     'hkl': (hklname, hkl_fileobj, 'multipart/form-data')}
        elif self.hkl_file and self.ui.depositHKLcheckBox.isChecked():
            files = {'cif': (self.cif.filename, cif_fileobj, 'multipart/form-data'),
                     'hkl': (self.hkl_file.name, self.hkl_file, 'multipart/form-data')}
        else:
            files = {'cif': (self.cif.filename, cif_fileobj)}
        print('making request')
        # pprint(data)
        r = requests.post(self.deposit_url, data=data, files=files,
                          headers={'User-Agent': 'FinalCif/{}'.format(VERSION)})
        self.ui.depositOutputTextBrowser.setText(r.text)
        self.set_deposit_button_to_try_again()
        return r

    def switch_to_page(self, deposition_type: str):
        self.reset_deposit_button_state_to_initial()
        self.ui.depositionOptionsStackedWidget.setCurrentIndex(self.deposition_type_to_int(deposition_type))

    def reset_deposit_button_state_to_initial(self):
        self.ui.depositCIFpushButton.disconnect()
        self.ui.depositOutputTextBrowser.clear()
        self.ui.depositCIFpushButton.setText("Deposit CIF")
        self.ui.depositCIFpushButton.clicked.connect(self._prepare_deposit)

    def set_deposit_button_to_try_again(self):
        self.ui.depositCIFpushButton.setText("Try Again")
        self.ui.depositCIFpushButton.disconnect()
        self.ui.depositCIFpushButton.clicked.connect(lambda: self.switch_to_page(self.deposition_type))

    def log_response_text(self, resp: requests.Response, *args, **kwargs):
        # logger.warning('Got response %r from %s', resp.text, resp.url)
        print(resp.text)

    def _set_username(self, text: str):
        self.settings.save_key_value('cod_username', text)
        self.username = text

    def _set_password(self, text: str):
        # Do not store this anywhere!
        if len(text) > 4:
            self.ui.refreshDepositListPushButton.setText('Refresh List')
            self.ui.refreshDepositListPushButton.setEnabled(True)
        else:
            self.ui.refreshDepositListPushButton.setText('Enter username and password')
            self.ui.refreshDepositListPushButton.setDisabled(True)
        self.password = text

    def _set_user_email(self, text: str):
        self.settings.save_key_value('cod_user_email', text)
        self.user_email = text

    def _prepare_deposit(self):
        print("#### Deposition in '{}' mode...".format(self.deposition_type))
        self.ui.depositOutputTextBrowser.clear()
        self.switch_to_page('deposit')
        if len(self.username) < 2:
            self.ui.depositOutputTextBrowser.setText('no username given')
            self.set_deposit_button_to_try_again()
            return
        if len(self.password) < 4:
            self.ui.depositOutputTextBrowser.setText('no password given')
            self.set_deposit_button_to_try_again()
            return
        self.cif.save()
        print('Saved cif to:', self.cif.filename)
        self.ui.statusBar.showMessage('  File Saved:  {}'.format(self.cif.filename), 10 * 1000)
        self.cif_deposit()
        # print(r.text)

    def _set_external_hkl_file(self) -> None:
        file = cif_file_open_dialog(filter="HKL file (*.hkl *.fcf)")
        if file.endswith('.hkl'):
            self.hkl_file = io.StringIO(HKL(file, self.cif.block.name, hklf_type=4).hkl_as_cif)
        elif file.endswith('.fcf'):
            cif = CifContainer(file)
            list_code = cif['_shelx_refln_list_code']
            if list_code != '4':
                show_general_warning('Only plain hkl or fcf (LIST 4 style) files should be uploaded.')
                return
            self.hkl_file = Path(file).read_bytes()
        else:
            show_general_warning('Only plain hkl or fcf (LIST 4 style) files should be uploaded.')


if __name__ == '__main__':
    # x = cif_deposit()
    # print(x.request.register_hook(log_response_text()))
    # print("Text from COD:", x.text, '##')
    # print(x.iter_content())
    # print(x.content)
    # print(x.headers)
    # pprint(x.request.headers)
    # pprint(x.request.body)
    # print(x.status_code)
    pass
