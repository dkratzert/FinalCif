from contextlib import suppress
from pathlib import Path

import qtawesome as qta
from PyQt5.QtWidgets import QFileDialog

from gui.finalcif_gui import Ui_FinalCifWindow
from tools.settings import FinalCifSettings


class Options:
    def __init__(self, ui: Ui_FinalCifWindow, settings: FinalCifSettings):
        self.ui = ui
        self.settings = settings
        # initial default, otherwise we have width=0.0 and no picture visible:
        self.ui.PictureWidthDoubleSpinBox.setValue(7.5)
        self._connect_signal_and_slots()
        self._options = {}

    def _connect_signal_and_slots(self):
        self.ui.HAtomsCheckBox.stateChanged.connect(self._state_changed)
        self.ui.ReportTextCheckBox.stateChanged.connect(self._state_changed)
        self.ui.PictureWidthDoubleSpinBox.valueChanged.connect(self._state_changed)
        self.ui.CheckCIFServerURLTextedit.textChanged.connect(self._state_changed)

    def show_options(self):
        """
        This method and pnöy this is called in order to show the options page.
        It also sets the state of the options widgets.
        """
        self.ui.HAtomsCheckBox.setChecked(self.without_H)
        self.ui.ReportTextCheckBox.setChecked(not self.report_text)
        self.ui.PictureWidthDoubleSpinBox.setValue(self.picture_width)
        self.ui.CheckCIFServerURLTextedit.setText(self.checkcif_url)
        self.ui.MainStackedWidget.go_to_options_page()

    def _state_changed(self):
        self._options = {
            'report_text'  : not self.ui.ReportTextCheckBox.isChecked(),
            'without_H'    : self.ui.HAtomsCheckBox.isChecked(),
            'picture_width': self.ui.PictureWidthDoubleSpinBox.value(),
            'checkcif_url' : self.ui.CheckCIFServerURLTextedit.text()
        }
        # print('saving:', self._options)
        self.settings.save_options(self._options)

    @property
    def values(self):
        # print('loading:', self._options, self.settings.load_options())
        return self.settings.load_options()

    def __getitem__(self, item):
        return self.settings.load_options()[item]

    @property
    def report_text(self):
        return self.settings.load_options()['report_text']

    @property
    def without_H(self):
        return self.settings.load_options()['without_H']

    @property
    def picture_width(self):
        return self.settings.load_options()['picture_width']

    @property
    def checkcif_url(self):
        return self.settings.load_options()['checkcif_url']

    def set_report_picture(self) -> None:
        """Sets the picture of the report document."""
        filename, _ = QFileDialog.getOpenFileName(filter="Image Files (*.png *.jpg *.jpeg *.bmp "
                                                         "*.gif *.tif *.tiff *.eps *.emf *.wmf)",
                                                  caption='Open a Report Picture')
        with suppress(Exception):
            self.report_picture = Path(filename)
        if self.report_picture.exists() and self.report_picture.is_file():
            self.ui.ReportPicPushButton.setIcon(qta.icon('fa5.image'))
            self.ui.ReportPicPushButton.setText('')
