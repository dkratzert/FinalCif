import os
import sys
from pathlib import Path

from cif.file_reader import CifContainer

DEBUG = True

if DEBUG:
    from PyQt5 import uic, QtCore

from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QLineEdit, QLabel, QPushButton, QFileDialog, \
    QTableWidgetItem

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

- Add file search for data files like .abs file.
#- open cif file and parse it. (With gemmi?)
- put all incomplete information in the CifItemsTable. 
  - Add checkbox to be able to edit all cif values?
  - Or show all ? items first, then all others.
- make second column of CifItemsTable uneditable.
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
        self.missing_data = []
        self.connect_signals_and_slots()
        self.data_sources = {'_exptl_absorpt_correction_type': ['SADABS', 'TWINABS', 'SORTAV'],
                        '_cell_measurement_reflns_used': [self.get_saint(), 'EVAL', 'HKL2000', 'DTREK'],
                        '_cell_measurement_theta_min': ['SAINT', 'EVAL', 'HKL2000', 'DTREK'],
                        '_cell_measurement_theta_max': ['SAINT', 'EVAL', 'HKL2000', 'DTREK'],
                        }
        # only for testing:
        self.get_cif_file_block('test-data/foobar.cif')

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
        self.ui.SelectCif_PushButton.clicked.connect(self.get_cif_file_block)

    @staticmethod
    def cif_file_open_dialog():
        """
        Returns a cif file name from a file dialog.
        """
        filename, _ = QFileDialog.getOpenFileName(filter='CIF file (*.cif, *.CIF);; All Files (*.*)',
                                                  initialFilter='*.cif',
                                                  caption='Open a .cif File')
        # print(filename)
        return filename

    def get_cif_file_block(self, fname):
        """
        Opens the cif file and fills information into the main table.
        """
        if not fname:
            fname = self.cif_file_open_dialog()
        self.ui.SelectCif_LineEdit.setText(fname)
        filepath = Path(fname)
        self.cif_doc = CifContainer(filepath)
        self.cif_doc.open_cif_with_fileparser()
        try:
            # Change the current working Directory
            os.chdir(filepath.absolute().parent)
        except OSError:
            print("Can't change the Current Working Directory")
        self.fill_cif_table()
        self.get_data_sources()

    def get_saint(self):
        """
        TODO: I have to decide which are the valid files. Therfore I need to determine the integration time and the 
              amount of reflections written to the raw/mul file.
              SADABS/TWINABS should read-in the same amount of reflections SAINT has written.
        TODO: parse ._ls file for amount of reflections, alternative the .raw/.mul file.
        """
        p = Path('./')
        saintfiles = p.rglob('*_0m._ls')
        print([i for i in saintfiles])

    def get_data_sources(self):
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.
        """
        for miss in self.missing_data:
            try:
                miss()
            except TypeError:
                pass

    def fill_cif_table(self):
        # self.ui.CifItemsTable.clear()
        self.ui.CifItemsTable.setRowCount(0)
        for key, value in self.cif_doc.key_value_pairs():
            if not value or value == '?':
                self.missing_data.append(key)
            self.addRow(key, value)

    def addRow(self, key, value):
        # Create a empty row at bottom of table
        row_num = self.ui.CifItemsTable.rowCount()
        self.ui.CifItemsTable.insertRow(row_num)
        # Add cif key and value to the row:
        item_key = QTableWidgetItem(key)
        item_val = QTableWidgetItem(value)
        self.ui.CifItemsTable.setVerticalHeaderItem(row_num, item_key)
        self.ui.CifItemsTable.setItem(row_num, 0, item_val)
        # has to be assigned first and then set to uneditable:
        item_val.setFlags(item_val.flags() ^ QtCore.Qt.ItemIsEditable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
