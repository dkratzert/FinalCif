#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import io
from pathlib import Path
from typing import Union, List, Dict
from urllib.parse import urlparse

import requests
from PyQt5.QtWidgets import QTableWidgetItem, QTextBrowser, QFrame

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.cod.deposition_list import CODFetcher
from finalcif.cif.cod.doi import resolve_doi
from finalcif.cif.cod.upload import upload_cif
from finalcif.cif.cod.website_parser import MyCODStructuresParser
from finalcif.cif.hkl import HKL
from finalcif.cif.text import delimit_string
from finalcif.gui.dialogs import cif_file_open_dialog, show_general_warning, show_ok_cancel_warning
from finalcif.gui.finalcif_gui_ui import Ui_FinalCifWindow
from finalcif.tools.options import Options
from finalcif.tools.settings import FinalCifSettings

"""
Ideas:
* Show cif before upload as text with 'upload' and 'abort' button.

_shelx_fab_file
_shelx_fab_checksum

"""


class CODdeposit():

    def __init__(self, ui: Ui_FinalCifWindow, cif: Union[CifContainer, None], options: Options):
        self.hkl_file: Union[io.StringIO, None] = None
        self.ui = ui
        self.settings = FinalCifSettings()
        self._cif = cif
        self.options = options
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
        self.ui.depositCIFpushButton.clicked.connect(self._init_deposit)
        # The full deposit url: self.deposit_url = 'https://www.crystallography.net/cod/cgi-bin/cif-deposit.pl'
        self.username = self.settings.load_value_of_key('cod_username')
        self.ui.CODURLTextedit.textChanged.connect(self.erase_cod_token)
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
            self.add_deposited_structures_to_table(self.settings.load_settings_list('COD', self.username))

    @property
    def deposit_url(self) -> str:
        return self.options.cod_url

    @property
    def main_url(self) -> str:
        return self.get_cod_hostname() + ('/cod-test/' if self.cod_test_version() else '/cod/')

    def erase_cod_token(self):
        self._cod_token = ''

    def author_editor_clicked(self):
        self.ui.MainStackedWidget.go_to_loops_page()
        self.ui.TemplatesStackedWidget.setCurrentIndex(1)

    def get_cod_hostname(self) -> str:
        parsed_url = urlparse(self.ui.CODURLTextedit.text())
        return parsed_url.scheme + "://" + parsed_url.netloc

    @property
    def cod_path(self) -> str:
        return urlparse(self.ui.CODURLTextedit.text()).path

    def cod_test_version(self) -> bool:
        if 'cod-test' in self.cod_path:
            return True
        else:
            return False

    @property
    def cif(self) -> CifContainer:
        return self._cif

    @cif.setter
    def cif(self, obj):
        self.ui.depositCIFpushButton.setEnabled(True)
        self._cif = obj
        self.check_for_publ_author()
        self.hkl_file = None
        self.ui.depositHKLcheckBox.setChecked(len(self._cif['_shelx_hkl_file']))
        self.ui.depositHKLcheckBox.setDisabled(not len(self._cif['_shelx_hkl_file']))

    def _back_to_cod_page(self):
        self.ui.MainStackedWidget.got_to_cod_page()
        self.check_for_publ_author()
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)

    def check_for_publ_author(self):
        try:
            self.author_name = self.cif.get_loop_column('_publ_author_name')[0]
            self.author_email = self.cif.get_loop_column('_publ_author_email')[0]
            # page personal:
            self.ui.ContactAuthorLineEdit.setText(self.author_name)
            self.ui.ContactEmailLineEdit.setText(self.author_email)
            # page pre-publication:
            self.ui.ContactAuthorLineEdit_2.setText(self.author_name)
            self.ui.ContactEmailLineEdit_2.setText(self.author_email)
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
            self.add_deposited_structures_to_table(self.settings.load_settings_list('COD', self.username))
        else:
            parser = self.get_structures_from_cod()
            self.settings.save_settings_list('COD', self.username, parser.structures)
            self.add_deposited_structures_to_table(parser.structures, parser.token)

    def get_structures_from_cod(self):
        f = CODFetcher(main_url=self.main_url)
        if not self._cod_token:
            self._cod_token = f.get_token(username=self.username, password=self.password)
        f.get_table_data_by_token(self._cod_token)
        parser = MyCODStructuresParser()
        parser.feed(f.table_html)
        return parser

    def add_deposited_structures_to_table(self, structures: List[dict], login_token: str = ''):
        self.ui.CODtableWidget.setRowCount(0)
        for row, structure in enumerate(structures):
            num = structure['number']
            date = structure['date']
            time = structure['time']
            if login_token:
                url = self.main_url + 'information_card.php?id={0}&CODSESSION={1}'.format(num, login_token)
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
        status = False
        for key, value in citation.items():
            if not value:
                continue
            if key == '_publ_author_name':
                value = delimit_string(value[0])
            self.ui.DOIResolveTextLabel.setText(self.ui.DOIResolveTextLabel.text() + "{}:\t {}\n".format(key, value))
            self.cif.set_pair_delimited(key, value)
            status = True
        if not status:
            self.ui.DOIResolveTextLabel.setText("Failed to get DOI information!")

    def _init_deposit(self):
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
        data, files = self.prepare_upload(username=self.username,
                                          password=self.password,
                                          author_name=self.author_name,
                                          author_email=self.author_email,
                                          embargo_time=str(self.ui.embargoTimeInMonthsSpinBox.value()),
                                          user_email=self.user_email,
                                          deposition_type=self.deposition_type,
                                          )
        r = upload_cif(self.deposit_url, data, files)
        self.ui.depositOutputTextBrowser.setText(r.text)
        self.set_deposit_button_to_try_again()

    def prepare_upload(self, username, password, author_name, author_email,
                       embargo_time, user_email, deposition_type):
        self.ui.depositOutputTextBrowser.setText('')
        self.switch_to_page('deposit')
        if not self.cif:
            return
        print('starting deposition of ', self.cif.fileobj.name)
        data = {'username'       : username,
                'password'       : password,
                'user_email'     : user_email,
                'deposition_type': deposition_type,  # 'published', 'prepublication' or 'personal'
                'output_mode'    : 'html',
                'filename'       : str(self.cif.finalcif_file),
                # 'progress'       : '1',  # must be 1 if supplied! Otherwise do not submit.
                }
        data = self._enrich_upload_data(author_email, author_name, data, deposition_type, embargo_time)
        files = self._get_files_data_for_upload()
        if 'hkl' not in files and not self.cif.hkl_file \
            and not show_ok_cancel_warning('You are attempting to upload a CIF without hkl data.\n'
                                           'Do you really want to proceed?'):
            self.ui.depositOutputTextBrowser.setText('Deposition aborted.')
            return
        self.ui.depositOutputTextBrowser.setText('Starting deposition of {} in "{}" mode ...'
                                                 .format(self.cif.fileobj.name, deposition_type))
        return data, files

    def _get_files_data_for_upload(self) -> Dict:
        if self.ui.depositHKLcheckBox.isChecked():
            files = {'cif': (self.cif.filename, io.StringIO(self.cif.cif_as_string()), 'multipart/form-data'),
                     'hkl': (str(self.cif.finalcif_file.with_suffix('.hkl')), io.StringIO(self.cif.hkl_as_cif), 'multipart/form-data')}
        elif self.hkl_file:
            files = {'cif': (self.cif.filename, io.StringIO(self.cif.cif_as_string()), 'multipart/form-data'),
                     'hkl': (self.hkl_file.name, self.hkl_file, 'multipart/form-data')}
        else:
            files = {'cif': (self.cif.filename, io.StringIO(self.cif.cif_as_string()), 'multipart/form-data')
                     # no hkl file here
                     }
        return files

    def _enrich_upload_data(self, author_email: str, author_name: str, data: Dict,
                            deposition_type: str, embargo_time: str) -> Dict:
        if deposition_type == 'personal':
            data.update({'author_name' : author_name,
                         'author_email': author_email})
        if deposition_type == 'prepublication':
            # Prepublication and replace option is possible with the REST API, but I think I let users update
            # their deposited files on the website only.
            data.update({'author_name' : author_name,
                         'author_email': author_email,
                         'hold_period' : embargo_time})
        if deposition_type == 'published':
            # Nothing to define extra:
            pass
        return data

    def switch_to_page(self, deposition_type: str):
        self.reset_deposit_button_state_to_initial()
        self.ui.depositionOptionsStackedWidget.setCurrentIndex(self.deposition_type_to_int(deposition_type))

    def reset_deposit_button_state_to_initial(self):
        self.ui.depositCIFpushButton.disconnect()
        self.ui.depositOutputTextBrowser.clear()
        self.ui.depositCIFpushButton.setText("Deposit CIF")
        self.ui.depositCIFpushButton.clicked.connect(self._init_deposit)

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

    def _set_external_hkl_file(self) -> None:
        file = cif_file_open_dialog(filter="HKL file (*.hkl *.fcf)")
        if file.endswith('.hkl'):
            if self.cif.res_file_data:
                hklf = self.cif._hklf_number_from_shelxl_file()
            else:
                hklf = 4
            self.hkl_file = io.StringIO(HKL(file, self.cif.block.name, hklf_type=hklf).hkl_as_cif)
            self.hkl_file.name = Path(file).name
        elif file.endswith('.fcf'):
            cif = CifContainer(file)
            list_code = cif['_shelx_refln_list_code']
            if list_code != '4':
                show_general_warning('Only plain hkl or fcf (LIST 4 style) files should be uploaded.')
                return
            self.hkl_file = io.StringIO(Path(file).read_text())
            self.hkl_file.name = Path(file).name
        elif file == '':
            self.hkl_file = None
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
