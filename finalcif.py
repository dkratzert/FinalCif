import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette

from cif.file_reader import CifContainer, quote
from datafiles.datatools import BrukerData
from tools.misc import predef_equipment_templ, predef_prop_templ, special_fields, text_field_keys
from tools.settings import FinalCifSettings

# noinspection PyUnreachableCode
if __debug__:
    DEBUG = True
else:
    # else is with "python -O file.py"
    DEBUG = False

if DEBUG:
    from PyQt5 import uic

from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QFileDialog, \
    QTableWidgetItem, QTableWidget, QStackedWidget, QListWidget, QListWidgetItem, QComboBox, QMessageBox, QPlainTextEdit

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if DEBUG:
    print('Compiling ui ...')
    uic.compileUiDir(os.path.join(application_path, './gui'))
from gui.finalcif_gui import Ui_FinalCifWindow

"""
TODO:

- add response forms
- test garbage cif files an make groper warnings how to solve the problems.
- The click on a cif keyword in the table opens the IuCr help about this key in a popup.
- find DSR string in res file and put descriptive text in cif.
- determine centrosymmetric or not and remove _chemical_absolute_configuration accordingly.
- Checkcif: http://journals.iucr.org/services/cif/checking/validlist.html
- Check if space group symbol is written correctly.
- Use a cif file parser that can write files
- make sure that cif items with whitespace have correct delimiter like 'foo bar' and
  ;
  foo long text bar
  ;
  during file save operation.
- allow to add own cif keywords in the table. (maybe not?) 
- Either use gemmi or platon for the moiety formula and _space_group_IT_number 
- if cell measurement_temp aleady in, propose the same for ambient_temp and vice versa
- handle _computing_structure_solution
- maybe add properties templates as tabwidget behind equipment templates (saves space).
- Improve file search for data files like .abs file. Determine if there is a common naming sheme like "Esser_JW314_0m"
- Determine the res file name from cif file. That can give a hint for the naming sheme or space group chaos naming.
- put all incomplete information in the CifItemsTable. 
- Own data in CifItemsTable overrides From Data Source. 
  (maybe with a signal to grey out the data source onEdit of Own Data)
- make "save cif" work.
- only let real cif keywords into the EquipmentEditTableWidget and cifKeywordLE.
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
- check hkl and res _shelx_res_checksum checksum
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
        self.cif = None
        self.missing_data = []
        # self.equipment_settings = []
        self.connect_signals_and_slots()
        # self.miss_data = MissingCifData()  # this is nowhere used!
        self.manufacturer = 'bruker'
        # only for testing:
        # self.get_cif_file_block(r'test-data/twin4.cif')
        # self.ui.DataFilesGroupBox.hide()
        self.get_cif_file_block(r'/Volumes/nifty/test_workordner/Esser_JW344/Esser_JW344_0m_a.cif')
        self.ui.EquipmentTemplatesListWidget.setCurrentRow(self.settings.load_last_equipment())

    def __del__(self):
        print('saving position')
        self.settings.save_window_position(self.pos(), self.size())
        self.settings.save_favorite_template(self.ui)

    '''def add_new_datafile(self, n: int, label_text: str, placeholder: str = '') -> (QLineEdit, QPushButton):
        """
        TODO: use this for all data files
        Adds a new file input as data source for the currently selected cif key/value pair
        """
        data_file_label = QLabel(self.ui.DataFilesGroupBox)
        data_file_label.setText(label_text)
        data_file_edit = QLineEdit(self.ui.DataFilesGroupBox)
        data_file_edit.setPlaceholderText(placeholder)
        data_file_button = QPushButton(self.ui.DataFilesGroupBox)
        data_file_button.setText('Select File')
        self.ui.DataSourcesGridLayout.addWidget(data_file_label, n, 0, 1, 1)
        self.ui.DataSourcesGridLayout.addWidget(data_file_edit, n, 1, 1, 1)
        self.ui.DataSourcesGridLayout.addWidget(data_file_button, n, 2, 1, 1)
        return data_file_edit, data_file_button'''

    def connect_signals_and_slots(self):
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        self.ui.SelectCif_PushButton.clicked.connect(self.get_cif_file_block)
        self.ui.SaveCifButton.clicked.connect(self.save_current_cif_file)
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

    def save_current_cif_file(self):
        table = self.ui.CifItemsTable
        table.setCurrentItem(None)  # makes sure also the currently edited item is saved
        rowcount = table.model().rowCount()
        columncount = table.model().columnCount()
        for row in range(rowcount):
            col0 = None  # cif content
            col1 = None  # from datafiles
            col2 = None  # own text
            for col in range(columncount):
                try:
                    item = table.item(row, col).text()
                except AttributeError:
                    item = None
                if not item:
                    try:
                        item = table.item(row, col).data(0)
                    except AttributeError:
                        item = None
                if not item:
                    try:
                        # This is for QPlaintextWidget items in the table:
                        item = table.cellWidget(row, col).toPlainText()
                    except AttributeError:
                        item = None
                if item:
                    if col == 0 and item != (None or ''):
                        col0 = item
                    if col == 1 and item != (None or ''):
                        col1 = item
                    try:
                        if col == 2 and item != (None or ''):
                            col2 = item
                    except AttributeError:
                        pass
                try:
                    txt = table.cellWidget(row, col).currentText()
                except AttributeError:
                    txt = None
                if col == 2 and txt:
                    col2 = txt
                if col == 2:
                    vhead = self.ui.CifItemsTable.model().headerData(row, Qt.Vertical)
                    if not str(vhead).startswith('_'):
                        continue
                    # This is my row information
                    # print('col2:', vhead, col0, col1, col2, '#')
                    if col1 and not col2:
                        self.cif.block.set_pair(vhead, quote(col1))
                    if col2:
                        try:
                            self.cif.block.set_pair(vhead, quote(col2))
                        except RuntimeError:
                            pass
        fin_file = Path(self.cif.filename.parts[-1][:-4] + '-final.cif')
        if DEBUG:
            if fin_file.exists():
                # a file save dialog is so anying:
                filename = self.cif_file_save_dialog(self.cif.filename)
                fin_file = Path(filename)
                if not filename:
                    return 'Not saved!'
        self.cif.save(fin_file.name)
        self.ui.statusBar.showMessage('  File Saved:  {}'.format(fin_file.name), 5000)
        print('File saved ...')

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
        equipment_list = self.settings.settings.value('equipment_list')
        for item in predef_equipment_templ:
            if not item['name'] in equipment_list:
                equipment_list.append(item['name'])
                newlist = [x for x in list(set(equipment_list)) if x]
                # this list keeps track of the equipment items:
                self.settings.save_template('equipment_list', newlist)
                self.settings.save_template('equipment/' + item['name'], item['items'])

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
            try:
                self.add_propeties_row(table, value)
            except TypeError:
                print('Bad value in property table')
                continue
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
        # make sure to have always a blank item first:
        table_data.insert(0, '')
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
        filename, _ = QFileDialog.getOpenFileName(filter='CIF file (*.cif, *.CIF), All Files (*.*)',
                                                  initialFilter='*.cif',
                                                  caption='Open a .cif File')
        return filename

    @staticmethod
    def cif_file_save_dialog(filename: Path = Path('.')) -> str:
        """
        Returns a cif file name from a file dialog.
        """
        # dialog = QFileDialog()
        # dialog.selectFile(str(filename))
        # dialog.selectFile(str(filename.parts[-1]))
        filename, _ = QFileDialog.getSaveFileName(filter='CIF file (*.cif, *.CIF), All Files (*.*)',
                                                  initialFilter='*.cif',
                                                  caption='Save .cif File')
        return filename

    def get_cif_file_block(self, fname):
        """
        Opens the cif file and fills information into the main table.
        """
        if not fname:
            fname = self.cif_file_open_dialog()
        if not fname:
            return
        self.ui.SelectCif_LineEdit.setText(fname)
        filepath = Path(fname)
        self.cif = CifContainer(filepath)
        # self.cif_doc.open_cif_with_fileparser()
        not_ok = self.cif.open_cif_with_gemmi()
        if not_ok:
            info = QMessageBox()
            info.setIcon(QMessageBox.Information)
            info.setText('This cif file is not readable!\n'
                         'Plese check line {} in\n{}'.format(str(not_ok).split(':')[1], filepath.name))
            info.show()
        try:
            # Change the current working Directory
            os.chdir(filepath.absolute().parent)
        except OSError:
            print("Can't change the Current Working Directory")
        self.fill_cif_table()

    def get_data_sources(self):
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.
        """
        if self.manufacturer == 'bruker':
            sources = BrukerData(self, self.cif).sources
            # Build a dictionary of cif keys and row number values in order to fill the first column
            # of CifItemsTable with cif values:
            for item in range(self.ui.CifItemsTable.model().rowCount()):
                head = self.ui.CifItemsTable.model().headerData(item, Qt.Vertical)
                self.vheaderitems[head] = item
            # They are needed for the comboboxes:
            property_fields = self.settings.load_property_keys()
            # get missing items from sources and put them into the corresponding rows:
            self.missing_data.append('_cell_measurement_temperature')
            self.missing_data.append('_diffrn_ambient_temperature')
            for miss_data in self.missing_data:
                # add missing item to data sources column:
                row_num = self.vheaderitems[miss_data]
                tab_item = QTableWidgetItem()
                #                               # row  column  item
                self.ui.CifItemsTable.setItem(row_num, 1, tab_item)
                try:
                    #                   sources are lower case!
                    tab_item.setText(str(sources[miss_data.lower()]))  # has to be string
                    # print(sources[miss_data], miss_data)
                except KeyError as e:
                    # print(e, '##')
                    pass
                # items from data sources should not be editable
                tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)
                # creating comboboxes for special keywords like _exptl_crystal_colour.
                # In case a property for this key exists, it will show this list:
                if miss_data.lower() in [x.lower() for x in property_fields]:
                    self.add_property_combobox(self.settings.load_property_by_key(miss_data), row_num)
                elif miss_data.lower() in [x.lower() for x in special_fields]:
                    self.add_property_combobox(special_fields[miss_data], row_num)

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
            try:
                combobox.addItem(value, num)
            except TypeError:
                print('Bad value in property:', value)
                continue
        combobox.setCurrentIndex(0)

    def fill_cif_table(self):
        """
        Adds the cif content to the main table. also add reference to FinalCif.
        """
        self.ui.CifItemsTable.setRowCount(0)
        for key, value in self.cif.key_value_pairs():
            if key == '_computing_publication_material':
                value = 'FinalCif by Daniel Kratzert, Freiburg 2019'
            if not value or value == '?':
                self.missing_data.append(key)
            self.add_row(key, value)
            # print(key, value)
        self.get_data_sources()

    def edit_row(self, vert_key: str = None, new_value=None, column: int = 1):
        """
        This is nowhere used!
        """
        if not vert_key:
            return None
        vheaderitems = {}
        for item in range(self.ui.CifItemsTable.model().rowCount()):
            head = self.ui.CifItemsTable.model().headerData(item, Qt.Vertical)
            vheaderitems[head] = item
        tab_item = QTableWidgetItem(new_value)
        self.ui.CifItemsTable.setItem(vheaderitems[vert_key], column, tab_item)
        # tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)

    def add_row(self, key, value):
        """
        # Create a empty row at bottom of CifItemsTable
        """
        row_num = self.ui.CifItemsTable.rowCount()
        self.ui.CifItemsTable.insertRow(row_num)
        # Add cif key and value to the row:
        item_key = QTableWidgetItem(key)
        if value is None:
            strval = '?'
        else:
            strval = str(value)  # or '?')
        if not key:
            strval = ''
        if key in text_field_keys:
            tabitem = QPlainTextEdit(self)
            tabitem.setPlainText(strval)
            tabitem.setFrameShape(0)  # no frame
            tabempty = QPlainTextEdit(self)
            tabempty.setFrameShape(0)
            tabempty2 = QPlainTextEdit(self)
            tabempty2.setFrameShape(0)
            self.ui.CifItemsTable.setCellWidget(row_num, 0, tabitem)
            self.ui.CifItemsTable.setCellWidget(row_num, 1, tabempty)
            self.ui.CifItemsTable.setCellWidget(row_num, 2, tabempty2)
            tabitem.setReadOnly(True)
            tabempty.setReadOnly(True)
        else:
            tabitem = QTableWidgetItem(strval)
            if key == "These are already in:":
                pal = QPalette()
                pal.setColor(QPalette.Foreground, Qt.black)
                item1 = QTableWidgetItem('----------------------')
                item2 = QTableWidgetItem('----------------------')
                item3 = QTableWidgetItem('----------------------')
                item1.setBackground(Qt.gray)
                item2.setBackground(Qt.gray)
                item3.setBackground(Qt.gray)
                self.ui.CifItemsTable.setItem(row_num, 0, item1)
                self.ui.CifItemsTable.setItem(row_num, 1, item2)
                self.ui.CifItemsTable.setItem(row_num, 2, item3)
            else:
                tabempty = QTableWidgetItem()
                self.ui.CifItemsTable.setItem(row_num, 1, tabempty)
                self.ui.CifItemsTable.setItem(row_num, 0, tabitem)
                tabitem.setFlags(tabitem.flags() ^ Qt.ItemIsEditable)
                tabempty.setFlags(tabempty.flags() ^ Qt.ItemIsEditable)
        self.ui.CifItemsTable.setVerticalHeaderItem(row_num, item_key)
        self.ui.CifItemsTable.resizeRowToContents(row_num)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
