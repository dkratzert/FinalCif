from contextlib import suppress
from pathlib import Path

import qtawesome as qta
from PyQt5.QtWidgets import QFileDialog

from cif.cif_file_io import CifContainer
from gui.finalcif_gui import Ui_FinalCifWindow
from tools.settings import FinalCifSettings


class Options:
    def __init__(self, cif: CifContainer, ui: Ui_FinalCifWindow, settings: FinalCifSettings):
        self.cif: CifContainer = cif
        self.ui = ui
        self.settings = settings

    def save_options(self) -> None:
        options = {
            'report_text'  : not self.ui.ReportTextCheckBox.isChecked(),
            'picture_width': self.ui.PictureWidthDoubleSpinBox.value(),
            'without_H'    : self.ui.HAtomsCheckBox.isChecked(),
        }
        self.settings.save_report_options(options)
        chkcif_options = {
            'checkcif_url': self.ui.CheckCIFServerURLTextedit.text()
        }
        self.checkcif_options = chkcif_options
        self.settings.save_checkcif_options(chkcif_options)
        print('options saved')

    def show_options(self) -> None:
        """
        {'report_text': True,
         'picture_width': 7.5,
         'without_H': False,
         }
         """
        report_options = self.settings.load_report_options()
        checkcif_options = self.settings.load_checkcif_options()
        if checkcif_options.get('checkcif_url'):
            self.ui.CheckCIFServerURLTextedit.setText(checkcif_options.get('checkcif_url'))
        if report_options.get('report_text') is not None:
            self.ui.ReportTextCheckBox.setChecked(not report_options.get('report_text'))
        if report_options.get('without_H') is not None:
            self.ui.HAtomsCheckBox.setChecked(report_options.get('without_H'))
        if report_options.get('picture_width'):
            self.ui.PictureWidthDoubleSpinBox.setValue(report_options.get('picture_width'))
        # Do I need this?
        #if not self.cif:
        #    return
        # This has to be here:
        self.ui.HAtomsCheckBox.clicked.connect(self.save_options)
        self.ui.ReportTextCheckBox.clicked.connect(self.save_options)
        self.ui.PictureWidthDoubleSpinBox.valueChanged.connect(self.save_options)
        self.ui.CheckCIFServerURLTextedit.textChanged.connect(self.save_options)

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