import io
from typing import Union

import requests

from cif.cif_file_io import CifContainer
from gui.finalcif_gui import Ui_FinalCifWindow


class COD_Deposit():
    def __init__(self, ui: Ui_FinalCifWindow, cif: Union[CifContainer, None] = None):
        self.ui = ui
        self._cif = cif
        if not self.cif:
            self.ui.depositCIFpushButton.setDisabled(True)
        self._set_checkbox_states()
        self.ui.depositorUsernameLineEdit.textChanged.connect(self._set_username)
        self.ui.depositorPasswordLineEdit.textChanged.connect(self._set_password)
        #self.ui.
        self.ui.depositCIFpushButton.clicked.connect(self._prepare_deposit)
        # production url:
        # url = 'https://www.crystallography.net/cod-test/cgi-bin/cif-deposit.pl'
        # test_url:
        self.url = 'https://www.crystallography.net/cod-test/cgi-bin/cif-deposit.pl'
        self.username = ''
        self.password = ''
        self.author_name = ''
        self.author_email = ''
        self.user_email = ''
        self.user_email = 'dkratzert@gmx.de'

    @property
    def cif(self):
        return self._cif

    @cif.setter
    def cif(self, obj):
        self.ui.depositCIFpushButton.setEnabled(True)
        self._cif = obj

    def _set_checkbox_states(self):
        self.ui.prepublicationDepositCheckBox.clicked.connect(self._prepublication_was_toggled)
        self.ui.publishedDepositionCheckBox.clicked.connect(self._published_was_toggled)
        self.ui.personalDepositCheckBox.clicked.connect(self._personal_was_toggled)
        self.ui.personalDepositCheckBox.setChecked(True)
        self.deposition_type = 'personal'
        self.ui.depositionOptionsStackedWidget.setCurrentIndex(0)

    def _personal_was_toggled(self, state: bool):
        self.ui.prepublicationDepositCheckBox.setChecked(False)
        self.ui.publishedDepositionCheckBox.setChecked(False)
        if state == True:
            self.ui.depositionOptionsStackedWidget.setCurrentIndex(0)
            self.deposition_type = 'personal'

    def _prepublication_was_toggled(self, state: bool):
        self.ui.publishedDepositionCheckBox.setChecked(False)
        self.ui.personalDepositCheckBox.setChecked(False)
        if state == True:
            self.ui.depositionOptionsStackedWidget.setCurrentIndex(1)
            self.deposition_type = 'prepublication'

    def _published_was_toggled(self, state: bool):
        self.ui.prepublicationDepositCheckBox.setChecked(False)
        self.ui.personalDepositCheckBox.setChecked(False)
        if state == True:
            self.ui.depositionOptionsStackedWidget.setCurrentIndex(2)
            self.deposition_type = 'published'

    def cif_deposit(self):
        if not self.cif:
            print('No cif opened!')
            return
        print('starting deposition')
        with open(self.cif.fileobj.absolute(), 'rb') as fileobj:
            data = {'username'       : self.username,
                    # Path('/Users/daniel/cod_username.txt').read_text(encoding='ascii'),
                    'password'       : self.password,
                    # Path('/Users/daniel/cod_password.txt').read_text(encoding='ascii'),
                    'user_email'     : self.user_email,  # 'dkratzert@gmx.de',
                    'deposition_type': self.deposition_type,  # published prepublication, personal
                    'output_mode'    : 'stdout',
                    #'progress'       : '1',  # must be 1 if supplied!
                    'filename'       : self.cif.fileobj.name,
                    }
            if self.author_email:
                data.update({'author_email': self.author_email})
            if self.author_name:
                data.update({'author_name': self.author_name})

            if self.ui.depositHKLcheckBox.isChecked():
                files = {'cif': fileobj, 'hkl': io.StringIO(self.cif.hkl_file)}
            else:
                files = {'cif': fileobj}
            print('making request')
            r = requests.post(self.url, files=files, data=data)
            # hooks={'response': self.log_response_text})
            print(r.text)
        return r

    def log_response_text(self, resp: requests.Response, *args, **kwargs):
        # logger.warning('Got response %r from %s', resp.text, resp.url)
        print(resp.text)

    def _set_username(self, text: str):
        # TODO: save username in settings
        self.username = text

    def _set_password(self, text: str):
        # Do not store this anywhere!
        self.password = text

    def _prepare_deposit(self):
        if len(self.username) < 2:
            print('no username given')
            return
        if len(self.password) < 4:
            print('no password given')
            return
        r = self.cif_deposit()
        # print(r.text)


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
