import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt

from cif.file_reader import CifContainer
from datafiles.datatools import MissingCifData, get_sadabs, get_saint
from tools.settings import FinalCifSettings

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
- rightclick on main table field opens menu with "assign template"->"list of templates to select from"
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
- check hkl and res checksum
- Add button for checkcif report.
- Check if unit cell in cif fits to atoms provided.

"""


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.show()
        self.settings = FinalCifSettings(self)
        self.settings.load_window_position()
        # distribute CifItemsTable Columns evenly:
        hheader = self.ui.CifItemsTable.horizontalHeader()
        hheader.setSectionResizeMode(0, QHeaderView.Stretch)
        hheader.setSectionResizeMode(1, QHeaderView.Stretch)
        hheader.setSectionResizeMode(2, QHeaderView.Stretch)
        hheader.setAlternatingRowColors(True)
        # Make sure the start page is shown and not the edit page:
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)
        self.ui.EquipmentEditTableWidget.verticalHeader().hide()
        self.ui.PropertiesEditTableWidget.verticalHeader().hide()
        self.cif_doc = None
        self.missing_data = []
        self.connect_signals_and_slots()
        self.miss_data = MissingCifData()

        self.manufacturer = 'bruker'
        # only for testing:
        self.get_cif_file_block('test-data/twin4.cif')

    def __del__(self):
        self.settings.save_window_position(self.pos(), self.size())

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
        ##
        self.ui.EditEquipmentTemplateButton.clicked.connect(self.edit_equipment_template)
        self.ui.SaveEquipmentButton.clicked.connect(self.save_equipment_template)
        self.ui.CancelEquipmentButton.clicked.connect(self.cancel_equipment_template)
        ##
        self.ui.EditPropertiyTemplateButton.clicked.connect(self.edit_property_template)
        self.ui.SavePropertiesButton.clicked.connect(self.save_property_template)
        self.ui.CancelPropertiesButton.clicked.connect(self.cancel_property_template)
        self.ui.EquipmentEditTableWidget.cellPressed.connect(self.foo)
        # something like cifItemsTable.selected_field.connect(self.display_data_file)

    def new_equipment_template(self):
        """
        """
        pass

    def foo(self):
        rowcount = self.ui.EquipmentEditTableWidget.rowCount()
        cont = 0
        for n in range(rowcount):
            txt = ''
            try:
                txt = self.ui.EquipmentEditTableWidget.item(n, 0).data()
            except (AttributeError, TypeError):
                pass
            if txt:
                cont += 1
            print(txt)
        if cont == rowcount:
            self.ui.EquipmentEditTableWidget.insertRow(cont + 1)

    def edit_equipment_template(self):
        """
        Edit the key/value list of an equipment entry.
        """
        index = self.ui.EquipmentTemplatesListWidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            return
        selected_row_text = self.ui.EquipmentTemplatesListWidget.currentIndex().data()
        equipment_data = self.settings.load_template(selected_row_text)
        # first load the previous values:
        if equipment_data:
            n = 0
            for key, value in equipment_data.items():
                print(n, key, value)
                if not key or not value:
                    continue
                self.ui.EquipmentEditTableWidget.insertRow(n)
                                                # row, column
                self.ui.EquipmentEditTableWidget.setItem(n, 0, QTableWidgetItem(key))
                self.ui.EquipmentEditTableWidget.setItem(n, 1, QTableWidgetItem(value))
                n += 1
            print(equipment_data)
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(1)
        rowcount = self.ui.EquipmentEditTableWidget.rowCount()
        print(rowcount, '##')

    def save_equipment_template(self):
        print('saved')
        selected_teplate_text = self.ui.EquipmentTemplatesListWidget.currentIndex().data()
        data = {}
        ncolumns = self.ui.EquipmentEditTableWidget.rowCount()
        print(ncolumns)
        for rownum in range(ncolumns):
            try:
                key = self.ui.EquipmentEditTableWidget.item(rownum, 0).text()
            except AttributeError:
                key = ''
            try:
                value = self.ui.EquipmentEditTableWidget.item(rownum, 1).text()
            except AttributeError:
                value = ''
            data[key] = value
        print(data, '###')
        self.settings.save_template(selected_teplate_text, data)
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)

    def cancel_equipment_template(self):
        print('cancelled')
        self.ui.EquipmentEditTableWidget.clearContents()
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)

    ##

    def edit_property_template(self):
        """
        TODO: onclick in table->create row if no rows, edit row if a row there
        """
        print('edit')
        index = self.ui.PropertiesTemplatesListWidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            return
        selected_row_text = self.ui.PropertiesTemplatesListWidget.currentIndex().data()
        property_data = self.settings.load_template(selected_row_text)
        print(property_data)
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(1)

    def save_property_template(self):
        print('saved')
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)

    def cancel_property_template(self):
        print('cancelled')
        self.ui.PropertiesEditTableWidget.clearContents()
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)

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

    def get_data_sources(self):
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.

        TODO: should I do it that a click on a field in question runs the get_source data for this specific field?
              It should at least show the specific data source in DataFilesGroupBox().
        """
        if self.manufacturer == 'bruker':
            saint_data = get_saint()
            sadabs_data = get_sadabs()
            try:
                abstype = 'multi-scan' if not sadabs_data.dataset(-1).numerical else 'numerical'
                t_min = min(sadabs_data.dataset(-1).transmission)
                # TODO: determine the correct dataset number:
                t_max = max(sadabs_data.dataset(-1).transmission)
            except (KeyError, AttributeError):
                # no abs file found
                abstype = '?'
                t_min = '?'
                t_max = '?'
            # TODO: make a Sources class that returns either the parser object itself or the respective value from the key:
            sources = {'_cell_measurement_reflns_used'  : saint_data.cell_reflections,
                       '_cell_measurement_theta_min'    : saint_data.cell_res_min_theta,
                       '_cell_measurement_theta_max'    : saint_data.cell_res_max_theta,
                       '_computing_cell_refinement'     : saint_data.version,
                       '_computing_data_reduction'      : saint_data.version,
                       '_exptl_absorpt_correction_type' : abstype,
                       '_exptl_absorpt_correction_T_min': str(t_min),
                       '_exptl_absorpt_correction_T_max': str(t_max),
                       }
            # print(sources)
            vheaderitems = {}
            # Build a dictionary of cif keys and row number values:
            for item in range(self.ui.CifItemsTable.model().rowCount()):
                head = self.ui.CifItemsTable.model().headerData(item, Qt.Vertical)
                vheaderitems[head] = item
            # get missing items from sources and put them into the corresponding rows:
            for miss in self.missing_data:
                # add missing item to data sources column:
                try:
                    tab_item = QTableWidgetItem(str(sources[miss]))  # Has to be string. TODO: round float numbers?
                    self.ui.CifItemsTable.setItem(vheaderitems[miss], 1, tab_item)
                except KeyError:
                    pass

    def fill_cif_table(self):
        self.ui.CifItemsTable.setRowCount(0)
        for key, value in self.cif_doc.key_value_pairs():
            if not value or value == '?':
                self.missing_data.append(key)
            self.addRow(key, value)
        self.get_data_sources()

    def edit_row(self, vert_key: str = None, new_value=None, column: int = 1):
        if not vert_key:
            return None
        vheaderitems = {}
        for item in range(self.ui.CifItemsTable.model().rowCount()):
            head = self.ui.CifItemsTable.model().headerData(item, Qt.Vertical)
            vheaderitems[head] = item
        item_val = QTableWidgetItem(new_value)
        self.ui.CifItemsTable.setItem(vheaderitems[vert_key], column, item_val)

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
