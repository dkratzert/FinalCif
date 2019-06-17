import os
import sys
from pathlib import Path

from cif_g import file_reader

DEBUG = True

if DEBUG:
    from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QLineEdit, QLabel, QPushButton, QFileDialog

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if DEBUG:
    uic.compileUiDir(os.path.join(application_path, './gui'))
from gui.finalcif_gui import Ui_FinalCifWindow


"""
TODO:

- the working directory has to be the directory of the currently opened cif file
- open cif file and parse it. (With gemmi?)
- put all incomplete information in the CifItemsTable. 
  - Add checkbox to be able to edit all cif values?
  - Or show all ? items first, then all others.
- make first and second column of CifItemsTable uneditable.
- Own data in CifItemsTable overrides From Data Source. 
  (maybe with a signal to grey out the data source onEdit of Own Data)
- make "save cif" work.
- think about a possibility to save and edit templates: QSettings()
- signal: if edit template clicked -> got to TemplatesStackedWidgetPage1
- signal: if Save template clicked -> got to TemplatesStackedWidgetPage0
- signal: if delete clicked -> delete current template table line
- signal: if edit Own Data field -> grey out From Data Source field in same line.
- action: rightclick on a template -> offer "delete template"
- action: rightclick on a template -> offer "export template (to .cif)"
- action: rightclick on a template -> offer "import template (from .cif)"
- selecting a row in the cif items table changes the view in the Data Sources table and offers
  possible files as data sources. For example a .abs file for Tmin/Tmax
- method: clear_data_sources_list() -> clear all in DataFilesGroupBox
- get correct Rint, Tmin/Tmax from twinabs by combining reflections count with modification time, 
  domain count?, hkl type
- SaveResidualsTableButton -> run multitable.py
- SaveFullReportButton -> generate full report with description text and all tables as .docx (and pdf?)
  maybe also a preview? Directly open in MSword/LibreOffice?
- prioritise The cif items with "necessary for checkcif" like "crystal habit", less important but generally accepted
  as needed like "publication picture program" and unimportant "like melting point". 
- Dropdown menu for colors, software versions, ...
- Template editor for colors, software, ...  with predefined values.
- Add a sfrm file parser: 
    - get measurement date 
    - Determine Manufakturer, kv/mA, tube, runlist 
- Determine the Manufacturer:
    - work directory: 1 Punkt
    - .abs file existiert: 1 Punkt
    - Sfrm Frames 2 Punkte 
    - Xxx Frames 2punkte
    - ...
- dann ein Dopdown mit „Manufakturer: 'bruker'“ (change)
- select templates according to Points
- Manufakturer has sub categories with Tube Type , housing, radiation, Cooling, goniometer, Detektor 
- save cif file with "name_fin.cif"

- Add button for checkcif report.

"""


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.show()
        # distribute CifItemsTable Columns evenly:
        hheader = self.ui.CifItemsTable.horizontalHeader()
        hheader.setSectionResizeMode(0, QHeaderView.Stretch)
        hheader.setSectionResizeMode(1, QHeaderView.Stretch)
        hheader.setSectionResizeMode(2, QHeaderView.Stretch)
        hheader.setAlternatingRowColors(True)
        self.cif_doc = None

    def add_new_datafile(self, n: int, label_text: str, placeholder: str = ''):
        """
        Adds a new file input as data source for the currently selected cif key/value pair
        """
        data_file_label = QLabel(self.DataFilesGroupBox)
        data_file_label.setText(label_text)
        data_file_edit = QLineEdit(self.ui.DataFilesGroupBox)
        data_file_edit.setPlaceholderText(placeholder)
        data_file_button = QPushButton(self.DataFilesGroupBox)
        data_file_button.setText('Select File')
        self.ui.DataSourcesGridLayout.addWidget(data_file_label, n, 0, 1, 1)
        self.ui.DataSourcesGridLayout.addWidget(data_file_edit, n, 1, 1, 1)
        self.ui.DataSourcesGridLayout.addWidget(data_file_button, n, 2, 1, 1)

    def connect_signals_and_slots(self):
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        self.ui.SelectCif_PushButton.clicked.connect(self.get_cif_file_block())

    def cif_file_open_dialog(self):
        """
        Returns a cif file name from a file dialog.
        """
        filename, _ = QFileDialog.getOpenFileName(filter='CIF file (*.cif, *.CIF);;All Files (*.*)',
                                                   initialFilter='*.cif',
                                                   caption='Open .cif Files')
        #print(filename)
        return filename

    def get_cif_file_block(self, fname: str=None):
        if not fname:
            fname = self.cif_file_open_dialog()
        self.ui.SelectCif_LineEdit.setText(fname)
        doc = file_reader.open_cif_file(Path(fname))
        self.cif_doc = doc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    #w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
