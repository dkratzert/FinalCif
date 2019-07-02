import os
import sys
from pathlib import Path

from PyQt5.QtCore import QPoint, Qt, QSize
from PyQt5.QtGui import QColor, QIcon, QPalette

from cif.file_reader import CifContainer, quote
from datafiles.datatools import BrukerData
from multitable.multi_gui import MultitableAppWindow
from tools.misc import predef_equipment_templ, predef_prop_templ, special_fields, text_field_keys
from tools.settings import FinalCifSettings

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

- find DSR string in res file and put descriptive text in cif.
- make an extra thread to load the cif data
- crystallization method templates
- preparationm method templates
- crytsal author: submitter, operator
- show data source on table hover
- references field
- have a recently opened menu
- add response forms
- The click on a cif keyword in the table opens the IuCr help about this key in a popup. (Not easy!)
- Checkcif: http://journals.iucr.org/services/cif/checking/validlist.html
- only let real cif keywords into the EquipmentEditTableWidget and cifKeywordLE.
- action: rightclick on a template -> offer "export template (to .cif)"
- action: rightclick on a template -> offer "import template (from .cif)"
- get correct Rint, Tmin/Tmax from twinabs by combining reflections count with modification time, 
  domain count?, hkl type
- SaveResidualsTableButton -> run multitable.py
- ReportButton -> generate full report with description text and all tables as .docx (and pdf?)
  maybe also a preview? Directly open in MSword/LibreOffice?
- check hkl and res _shelx_res_checksum checksum
- Add button for checkcif report.

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
light_green = QColor(217, 255, 201)
blue = QColor(102, 150, 179)
yellow = QColor(244, 255, 176)


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.show()
        self.vheaderitems = {}
        self.settings = FinalCifSettings(self)
        self.store_predefined_templates()
        self.show_equipment_and_properties()
        self.settings.load_window_position()
        # distribute CifItemsTable Columns evenly:
        hheader = self.ui.CifItemsTable.horizontalHeader()
        hheader.setSectionResizeMode(0, QHeaderView.Stretch)
        hheader.setSectionResizeMode(1, QHeaderView.Stretch)
        hheader.setSectionResizeMode(2, QHeaderView.Stretch)
        # hheader.setAlternatingRowColors(True)
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
        # self.ui.DataFilesGroupBox.hide()
        self.ui.MercuryPushButton.setDisabled(True)
        #self.ui.SaveFullReportButton.setDisabled(True)
        self.ui.CheckcifButton.setDisabled(True)
        if DEBUG:
            # only for testing:
            # self.load_cif_file(r'test-data/twin4.cif')
            self.load_cif_file(r'D:\frames\guest\BruecknerRK_103\work\BruecknerRK_103_Cu_0m_a.cif')
            # self.load_cif_file(r'D:\frames\BB_29\P-1_a.cif')
            # self.load_cif_file(r'D:\frames\guest\Esser_JW283\Esser_JW283\Esser_JW283_0m_a.cif')
        # TODO: Have to find a different method to select the row:
        #self.ui.EquipmentTemplatesListWidget.setCurrentRow(-1)  # Has to he in front in order to work
        #self.ui.EquipmentTemplatesListWidget.setCurrentRow(self.settings.load_last_equipment())
        # Sorting desyncronizes header and columns:
        self.ui.CifItemsTable.setSortingEnabled(False)

    def __del__(self):
        print('saving position')
        x, y = self.pos().x(), self.pos().y()
        self.settings.save_window_position(QPoint(x, y - 30), self.size(), self.isMaximized())
        self.settings.save_favorite_template(self.ui)

    def connect_signals_and_slots(self):
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        self.ui.SelectCif_PushButton.clicked.connect(self.load_cif_file)
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
        self.ui.EquipmentTemplatesListWidget.clicked.connect(self.load_selected_equipment)
        # something like cifItemsTable.selected_field.connect(self.display_data_file)
        ##
        self.ui.SaveFullReportButton.clicked.connect(self.run_multitable)

    def run_multitable(self):
        #app = QApplication(sys.argv)
        w = MultitableAppWindow(self)
        w.show()
        #sys.exit(app.exec_())

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
                    if col == 0 and item != (None or '' or '?'):
                        col0 = item
                    if col == 1 and not col0 and item != (None or '' or '?'):
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
                        self.cif.set_pair_delimited(vhead, quote(col1))
                    if col2:
                        try:
                            self.cif.set_pair_delimited(vhead, quote(col2))
                        except RuntimeError:
                            pass
        fin_file = Path(self.cif.filename.parts[-1][:-4] + '-finalcif.cif')
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
                    tab_item.setBackground(light_green)
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
        equipment_list = self.settings.settings.value('equipment_list') or []
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
            try:
                table_data = table_data[1]
            except:
                pass
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
        filename, _ = QFileDialog.getSaveFileName(filter='CIF file (*.cif, *.CIF), All Files (*.*)',
                                                  initialFilter='*.cif',
                                                  caption='Save .cif File')
        return filename

    def load_cif_file(self, fname):
        """
        Opens the cif file and fills information into the main table.
        """
        if not fname:
            fname = self.cif_file_open_dialog()
        if not fname:
            return
        self.ui.SelectCif_LineEdit.setText(fname)
        filepath = Path(fname)
        if not filepath.exists():
            return
        self.cif = CifContainer(filepath)
        # self.cif_doc.open_cif_with_fileparser()
        not_ok = self.cif.open_cif_with_gemmi()
        if not_ok:
            info = QMessageBox()
            info.setIcon(QMessageBox.Information)
            try:
                line = str(not_ok)[4:].split(':')[1]
            except IndexError:
                line = None
            if line:
                info.setText('This cif file is not readable!\n'
                             'Plese check line {} in\n{}'.format(line, filepath.name))
            else:
                info.setText('This cif file is not readable! "{}"'.format(filepath.name))
            info.show()
            return
        try:
            # Change the current working Directory
            os.chdir(filepath.absolute().parent)
        except OSError:
            print("Can't change the Current Working Directory")
        self.fill_cif_table()
        #self.ui.EquipmentTemplatesListWidget.setCurrentRow(-1)  # Has to he in front in order to work
        #self.ui.EquipmentTemplatesListWidget.setCurrentRow(self.settings.load_last_equipment())

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
                    # sources are lower case!
                    txt = str(sources[miss_data.lower()])
                    tab_item.setText(txt)  # has to be string
                    if txt and txt != '?':
                        tab_item.setBackground(light_green)
                    else:
                        tab_item.setBackground(yellow)
                    # print(sources[miss_data], miss_data)
                    self.ui.CifItemsTable.resizeRowToContents(row_num)
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
        combobox.setEditable(True)  # only editable as new template
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
            if not value or value == '?':
                self.missing_data.append(key)
            self.add_row(key, value)
            # print(key, value)
        self.get_data_sources()
        # self.ui.CifItemsTable.resizeRowsToContents()

    def edit_row(self, vert_key: str = None, new_value=None, column: int = 1):
        """
        This is nowhere used!
        Sets a new value for a specific vertical header key and the respective column.
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
            tab1 = QPlainTextEdit(self)
            tab1.setFrameShape(0)
            tab2 = QPlainTextEdit(self)
            tab2.setFrameShape(0)
            self.ui.CifItemsTable.setCellWidget(row_num, 0, tabitem)
            self.ui.CifItemsTable.setCellWidget(row_num, 1, tab1)
            self.ui.CifItemsTable.setCellWidget(row_num, 2, tab2)
            tabitem.setReadOnly(True)
            tab1.setReadOnly(True)
            # Make QPlainTextEdit fields a bit higher than the rest
            self.ui.CifItemsTable.setRowHeight(row_num, 80)
        #else:
        #if key in text_field_keys:
        #    self.ui.CifItemsTable.setRowHeight(row_num, 60)
        else:
            tabitem = QTableWidgetItem(strval)
            if key == "These are already in:":
                pal = QPalette()
                pal.setColor(QPalette.Foreground, Qt.black)
                item1 = QTableWidgetItem('----------------------')
                item2 = QTableWidgetItem('----------------------')
                item3 = QTableWidgetItem('----------------------')
                item1.setBackground(blue)
                item2.setBackground(blue)
                item3.setBackground(blue)
                self.ui.CifItemsTable.setItem(row_num, 0, item1)
                self.ui.CifItemsTable.setItem(row_num, 1, item2)
                self.ui.CifItemsTable.setItem(row_num, 2, item3)
                self.ui.CifItemsTable.resizeRowToContents(row_num)
            else:
                tab1 = QTableWidgetItem()
                tab2 = QTableWidgetItem()
                self.ui.CifItemsTable.setItem(row_num, 1, tab1)
                self.ui.CifItemsTable.setItem(row_num, 0, tabitem)
                if key == '_computing_publication_material':
                    tab2.setText('FinalCif by Daniel Kratzert, Freiburg 2019')
                    self.ui.CifItemsTable.setItem(row_num, 2, tab2)
                tabitem.setFlags(tabitem.flags() ^ Qt.ItemIsEditable)
                tab1.setFlags(tab1.flags() ^ Qt.ItemIsEditable)
                self.ui.CifItemsTable.resizeRowToContents(row_num)
        self.ui.CifItemsTable.setVerticalHeaderItem(row_num, item_key)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    app.setWindowIcon(QIcon('./icon/multitable.png'))
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())

    # noinspection PyUnreachableCode
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
