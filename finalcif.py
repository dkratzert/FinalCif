import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt

from cif.file_reader import CifContainer
from datafiles.datatools import MissingCifData, get_frame, get_sadabs, get_saint
from tools.misc import special_fields, predef_prop_templ
from tools.settings import FinalCifSettings

DEBUG = True

if DEBUG:
    from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QLineEdit, QLabel, QPushButton, QFileDialog, \
    QTableWidgetItem, QTableWidget, QStackedWidget, QListWidget, QListWidgetItem, QComboBox

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

- Use a cif file parser that can write files
- if cell measurement_temp aleady in, propose the same for ambient_temp and vice versa
- handle _computing_structure_solution
- maybe add properties templates as tabwidget behind equipment templates (saves space).
- Add file search for data files like .abs file.
- put all incomplete information in the CifItemsTable. 
- Own data in CifItemsTable overrides From Data Source. 
  (maybe with a signal to grey out the data source onEdit of Own Data)
- make "save cif" work.
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
- Determine the Manufacturer:
    - work directory: 1 Punkt
    - .abs file existiert: 1 Punkt
    - Sfrm Frames 2 Punkte 
    - Xxx Frames 2punkte
    - ...
- select templates according to Points 
- save cif file with "name_fin.cif"
- check hkl and res checksum
- Add button for checkcif report.
- Check if unit cell in cif fits to atoms provided.

Idea for checkcif:

import os
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl, QEventLoop
from PyQt5.QtWebEngineWidgets import QWebEngineView

class WebPage(QWebEngineView):
    def __init__(self):
        QWebEngineView.__init__(self)
        self.load(QUrl("https://www.url.com"))
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self):
        print("Finished Loading")
        self.page().toHtml(self.Callable)

    def Callable(self, html_str):
        self.html = html_str
        self.page().runJavaScript("document.getElementsByName('loginid')[0].value = 'email@email.com'")
        self.page().runJavaScript("document.getElementsByName('password')[0].value = 'test'")
        self.page().runJavaScript ("document.getElementById('signin').click()")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    web = WebPage()
    web.show()
    sys.exit(app.exec_()) 

"""


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.show()
        self.vheaderitems = {}
        self.settings = FinalCifSettings(self)
        self.store_predefined_templates()
        self.settings.load_window_position()
        self.show_equipment_and_properties()
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
        # self.equipment_settings = []
        self.connect_signals_and_slots()
        self.miss_data = MissingCifData()
        self.manufacturer = 'bruker'
        # only for testing:
        self.get_cif_file_block(r'test-data/twin4.cif')

    def __del__(self):
        print('saving position')
        self.settings.save_window_position(self.pos(), self.size())

    def add_new_datafile(self, n: int, label_text: str, placeholder: str = ''):
        """
        TODO: use this for all data files
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
        self.ui.DeleteEquipmentButton.clicked.connect(self.delete_equipment)
        ##
        self.ui.EditPropertiyTemplateButton.clicked.connect(self.edit_property_template)
        self.ui.SavePropertiesButton.clicked.connect(self.save_property_template)
        self.ui.CancelPropertiesButton.clicked.connect(self.cancel_property_template)
        self.ui.DeletePropertiesButton.clicked.connect(self.delete_property)
        ##
        self.ui.EquipmentEditTableWidget.cellPressed.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemSelectionChanged.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemEntered.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.cellChanged.connect(self.add_eq_row_if_needed)
        ##
        self.ui.PropertiesEditTableWidget.cellPressed.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemSelectionChanged.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemEntered.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.cellChanged.connect(self.add_eq_row_if_needed)
        ##
        self.ui.NewEquipmentTemplateButton.clicked.connect(self.new_equipment)
        self.ui.NewPropertyTemplateButton.clicked.connect(self.new_property)
        ##
        self.ui.EquipmentTemplatesListWidget.currentRowChanged.connect(self.load_selected_equipment)
        # something like cifItemsTable.selected_field.connect(self.display_data_file)

    def show_equipment_and_properties(self):
        """
        Display saved items in the equipment and properties lists.
        """
        equipment_list = self.settings.settings.value('equipment_list')
        if equipment_list:
            for eq in equipment_list:
                if eq:
                    item = QListWidgetItem(eq)
                    self.ui.EquipmentTemplatesListWidget.addItem(item)
        property_list = self.settings.settings.value('property_list')
        if property_list:
            for pr in property_list:
                if pr:
                    item = QListWidgetItem(pr)
                    self.ui.PropertiesTemplatesListWidget.addItem(item)

    def load_selected_equipment(self):
        """
        Load equipment data to be used in the main table
        """
        listwidget = self.ui.EquipmentTemplatesListWidget
        selected_row_text = listwidget.currentIndex().data()
        if not selected_row_text:
            return None
        # table_data = self.settings.load_template('equipment/' + selected_row_text)
        # self.equipment_settings = table_data
        equipment = self.settings.load_equipment_template_as_dict(selected_row_text)
        if self.vheaderitems:
            for data in equipment:
                # add missing item to data sources column:
                try:
                    tab_item = QTableWidgetItem(str(equipment[data]))
                    # vheaderitems contain the cif keywords in the vertical header, the 1 is the data sources column.
                    row = self.vheaderitems[data]
                    column = 1
                    self.ui.CifItemsTable.setItem(row, column, tab_item)
                    tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)
                except KeyError:
                    pass

    def new_equipment(self):
        item = QListWidgetItem('')
        self.ui.EquipmentTemplatesListWidget.addItem(item)
        self.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.EquipmentTemplatesListWidget.editItem(item)

    def delete_equipment(self):
        # First delete the list entries
        index = self.ui.EquipmentTemplatesListWidget.currentIndex()
        selected_template_text = index.data()
        self.settings.delete_template('equipment/' + selected_template_text)
        equipment_list = self.settings.settings.value('equipment_list') or []
        try:
            equipment_list.remove(selected_template_text)
        except ValueError:
            pass
        self.settings.save_template('equipment_list', equipment_list)
        # now make it invisible:
        self.ui.EquipmentTemplatesListWidget.takeItem(index.row())
        self.cancel_equipment_template()

    def new_property(self):
        item = QListWidgetItem('')
        self.ui.PropertiesTemplatesListWidget.addItem(item)
        self.ui.PropertiesTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.PropertiesTemplatesListWidget.editItem(item)
        self.ui.cifKeywordLE.clear()

    def add_eq_row_if_needed(self):
        """
        Adds an empty row at the bottom of either the EquipmentEditTableWidget, or the PropertiesEditTableWidget.
        """
        if self.ui.EquipmentEditTableWidget.hasFocus():
            table = self.ui.EquipmentEditTableWidget
        else:
            table = self.ui.PropertiesEditTableWidget
        rowcount = table.rowCount()
        cont = 0
        for n in range(rowcount):
            key = ''
            try:
                key = table.item(n, 0).text()
            except (AttributeError, TypeError):
                pass
            if key:  # don't count empty key rows
                cont += 1
        if cont == rowcount:
            table.insertRow(rowcount)

    @staticmethod
    def add_equipment_row(table: QTableWidget, key: str = '', value: str = ''):
        """
        Add a new row with content to the table (Equipment or Property).
        """
        # Create a empty row at bottom of table
        row_num = table.rowCount()
        table.insertRow(row_num)
        # Add cif key and value to the row:
        item_key = QTableWidgetItem(key)
        item_val = QTableWidgetItem(value)
        table.setItem(row_num, 0, item_key)
        table.setItem(row_num, 1, item_val)

    ## The equipment templates:

    def edit_equipment_template(self):
        it = self.ui.EquipmentTemplatesListWidget.currentItem()
        self.ui.EquipmentTemplatesListWidget.setCurrentItem(None)
        self.ui.EquipmentTemplatesListWidget.setCurrentItem(it)
        self.ui.CancelPropertiesButton.click()
        table = self.ui.EquipmentEditTableWidget
        stackedwidget = self.ui.EquipmentTemplatesStackedWidget
        listwidget = self.ui.EquipmentTemplatesListWidget
        self.load_equipment(table, stackedwidget, listwidget)

    def load_equipment(self, table: QTableWidget, stackedwidget: QStackedWidget, listwidget: QListWidget):
        """
        Load/Edit the key/value list of an equipment entry.
        """
        self.ui.EquipmentEditTableWidget.blockSignals(True)
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            return
        selected_row_text = listwidget.currentIndex().data()
        table_data = self.settings.load_template('equipment/' + selected_row_text)
        # first load the previous values:
        n = 0
        if table_data:
            for key, value in table_data:
                if not key or not value:
                    continue
                self.add_equipment_row(table, key, value)
                n += 1
        table.insertRow(n)
        self.ui.EquipmentEditTableWidget.blockSignals(False)
        stackedwidget.setCurrentIndex(1)

    def save_equipment_template(self):
        table = self.ui.EquipmentEditTableWidget
        stackedwidget = self.ui.EquipmentTemplatesStackedWidget
        listwidget = self.ui.EquipmentTemplatesListWidget
        self.save_equipment(table, stackedwidget, listwidget)

    def save_equipment(self, table: QTableWidget, stackwidget: QStackedWidget, listwidget: QListWidget):
        """
        Saves the currently selected equipment template to the config file.
        """
        # Set None Item to prevent loss of the currently edited item:
        # The current item is closed and thus saved.
        table.setCurrentItem(None)
        selected_template_text = listwidget.currentIndex().data()
        equipment_list = self.settings.settings.value('equipment_list')
        if not equipment_list:
            equipment_list = ['']
        table_data = []
        ncolumns = table.rowCount()
        for rownum in range(ncolumns):
            key = ''
            try:
                key = table.item(rownum, 0).text()
                value = table.item(rownum, 1).text()
            except AttributeError:
                value = ''
            if key and value:
                table_data.append([key, value])
        self.settings.save_template('equipment/' + selected_template_text, table_data)
        equipment_list.append(selected_template_text)
        newlist = [x for x in list(set(equipment_list)) if x]
        # this list keeps track of the equipment items:
        self.settings.save_template('equipment_list', newlist)
        stackwidget.setCurrentIndex(0)
        print('saved')

    def cancel_equipment_template(self):
        """
        Cancel Equipment editing.
        """
        table = self.ui.EquipmentEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('cancelled')

    ## The properties templates:

    @staticmethod
    def add_propeties_row(table: QTableWidget, value: str = ''):
        """
        Add a new row with a value to the Property table.
        """
        # Create a empty row at bottom of table
        row_num = table.rowCount()
        table.insertRow(row_num)
        # Add cif key and value to the row:
        item_val = QTableWidgetItem(value)
        table.setItem(row_num, 0, item_val)

    def delete_property(self):
        # First delete the list entries
        index = self.ui.PropertiesTemplatesListWidget.currentIndex()
        selected_template_text = index.data()
        self.settings.delete_template('property/' + selected_template_text)
        property_list = self.settings.settings.value('property_list')
        property_list.remove(selected_template_text)
        self.settings.save_template('property_list', property_list)
        # now make it invisible:
        self.ui.PropertiesTemplatesListWidget.takeItem(index.row())
        self.cancel_property_template()

    def edit_property_template(self):
        """
        Edit the Property table.
        """
        # make sure the current item doesnt get lost:
        it = self.ui.PropertiesTemplatesListWidget.currentItem()
        self.ui.PropertiesTemplatesListWidget.setCurrentItem(None)
        self.ui.PropertiesTemplatesListWidget.setCurrentItem(it)
        self.ui.CancelEquipmentButton.click()
        table = self.ui.PropertiesEditTableWidget
        stackedwidget = self.ui.PropertiesTemplatesStackedWidget
        listwidget = self.ui.PropertiesTemplatesListWidget
        self.load_property(table, stackedwidget, listwidget)

    def save_property_template(self):
        table = self.ui.PropertiesEditTableWidget
        stackedwidget = self.ui.PropertiesTemplatesStackedWidget
        listwidget = self.ui.PropertiesTemplatesListWidget
        keyword = self.ui.cifKeywordLE.text()
        self.save_property(table, stackedwidget, listwidget, keyword)

    def store_predefined_templates(self):
        property_list = self.settings.settings.value('property_list') or []
        for item in predef_prop_templ:
            if not item['name'] in property_list:
                property_list.append(item['name'])
                newlist = [x for x in list(set(property_list)) if x]
                # this list keeps track of the equipment items:
                self.settings.save_template('property_list', newlist)
                self.settings.save_template('property/' + item['name'], item['values'])

    def load_property(self, table: QTableWidget, stackedwidget: QStackedWidget, listwidget: QListWidget):
        """
        Load/Edit the value list of a property entry.
        """
        self.ui.PropertiesEditTableWidget.blockSignals(True)
        property_list = self.settings.settings.value('property_list')
        if not property_list:
            property_list = ['']
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            return
        selected_row_text = listwidget.currentIndex().data()
        table_data = self.settings.load_template('property/' + selected_row_text)
        if table_data:
            cif_key = table_data[0]
            table_data = table_data[1]
            self.ui.cifKeywordLE.setText(cif_key)
        n = 0
        if not table_data:
            table_data = ['']
        for value in table_data:
            self.add_propeties_row(table, value)
            n += 1
        property_list.append(selected_row_text)
        newlist = [x for x in list(set(property_list)) if x]
        # this list keeps track of the equipment items:
        self.settings.save_template('property_list', newlist)
        stackedwidget.setCurrentIndex(1)
        self.ui.PropertiesEditTableWidget.blockSignals(False)

    def save_property(self, table: QTableWidget,
                      stackwidget: QStackedWidget,
                      listwidget: QListWidget,
                      keyword: str = ''):
        """
        Saves the currently selected Property template to the config file.
        """
        # Set None Item to prevent loss of the currently edited item:
        # The current item is closed and thus saved.
        table.setCurrentItem(None)
        selected_template_text = listwidget.currentIndex().data()
        table_data = []
        ncolumns = table.rowCount()
        for rownum in range(ncolumns):
            try:
                # only one column!
                value = table.item(rownum, 0).text()
            except AttributeError:
                value = ''
            if value:
                table_data.append(value)
        # table_data.extend([''])
        if keyword:
            # save as dictionary for properties to have "_cif_key : itemlist"
            # for a table item as dropdown menu in the main table.
            table_data = [keyword, table_data]
        self.settings.save_template('property/' + selected_template_text, table_data)
        stackwidget.setCurrentIndex(0)
        print('saved')

    def cancel_property_template(self):
        """
        Cancel editing of the current template.
        """
        table = self.ui.PropertiesEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)

    @staticmethod
    def cif_file_open_dialog():
        """
        Returns a cif file name from a file dialog.
        """
        filename, _ = QFileDialog.getOpenFileName(filter='CIF file (*.cif, *.CIF);; All Files (*.*)',
                                                  initialFilter='*.cif',
                                                  caption='Open a .cif File')
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
              Maybe better if this method itself determines the data sources.
        """
        if self.manufacturer == 'bruker':
            saint_data = get_saint()
            sadabs_data = get_sadabs()
            frame_header = get_frame()
            # TODO: determine the correct dataset number:
            dataset_num = -1
            try:
                abstype = 'multi-scan' if not sadabs_data.dataset(-1).numerical else 'numerical'
                t_min = min(sadabs_data.dataset(dataset_num).transmission)
                t_max = max(sadabs_data.dataset(dataset_num).transmission)
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
                       '_diffrn_reflns_av_R_equivalents': sadabs_data.Rint,
                       '_cell_measurement_temperature'  : frame_header.temperature,
                       '_diffrn_ambient_temperature'    : frame_header.temperature,
                       '_exptl_absorpt_process_details' : sadabs_data.version
                       }

            # Build a dictionary of cif keys and row number values in order to fill the first column
            # of CifItemsTable with cif values:
            for item in range(self.ui.CifItemsTable.model().rowCount()):
                head = self.ui.CifItemsTable.model().headerData(item, Qt.Vertical)
                self.vheaderitems[head] = item
            # They are needed for the comboboxes:
            property_fields = self.settings.load_property_keys()
            # get missing items from sources and put them into the corresponding rows:
            for miss_data in self.missing_data:
                # add missing item to data sources column:
                row_num = self.vheaderitems[miss_data]
                tab_item = QTableWidgetItem()
                try:
                    tab_item.setText(str(sources[miss_data]))  # has to be string
                except KeyError:
                    pass
                #                               # row  column  item
                self.ui.CifItemsTable.setItem(row_num, 1, tab_item)
                # items from data sources should not be editable
                tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)
                # creating comboboxes for special keywords like _exptl_crystal_colour.
                # In case a property for this key exists, it will show this list:
                if miss_data in property_fields:
                    self.add_property_combobox(self.settings.load_property_by_key(miss_data), row_num)
                elif miss_data in special_fields:
                    self.add_property_combobox(special_fields[miss_data], row_num)

    def print_combo(self, foo):
        print('combobox has now:', foo)

    def add_property_combobox(self, miss_data: str, row_num: int):
        """
        Adds a QComboBox to the CifItemsTable with the content of special_fields or property templates.
        """
        combobox = QComboBox()
        # combobox.currentIndexChanged.connect(self.print_combo)
        # print('special:', row_num, miss_data)
        self.ui.CifItemsTable.setCellWidget(row_num, 2, combobox)
        combobox.setEditable(False)  # only editable as new template
        for num, value in miss_data:
            combobox.addItem(value, num)
        combobox.setCurrentIndex(0)

    def fill_cif_table(self):
        """
        Adds the cif content to the main table.
        """
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
        tab_item = QTableWidgetItem(new_value)
        self.ui.CifItemsTable.setItem(vheaderitems[vert_key], column, tab_item)
        # tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)

    def addRow(self, key, value):
        # Create a empty row at bottom of table
        row_num = self.ui.CifItemsTable.rowCount()
        self.ui.CifItemsTable.insertRow(row_num)
        # Add cif key and value to the row:
        item_key = QTableWidgetItem(key)
        tabitem = QTableWidgetItem(value)
        tabempty = QTableWidgetItem()
        tabempty.setFlags(tabitem.flags() ^ Qt.ItemIsEditable)
        self.ui.CifItemsTable.setVerticalHeaderItem(row_num, item_key)
        self.ui.CifItemsTable.setItem(row_num, 0, tabitem)
        self.ui.CifItemsTable.setItem(row_num, 1, tabempty)
        # has to be assigned first and then set to uneditable:
        tabitem.setFlags(tabitem.flags() ^ Qt.ItemIsEditable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
