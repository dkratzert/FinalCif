#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import json
import os
import subprocess
import sys
import time
import traceback
from pathlib import Path, WindowsPath

from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from gemmi import cif
from requests import ReadTimeout

from cif.core_dict import cif_core
from datafiles.rigaku_data import RigakuData
from report.tables import make_report_from
from tools.checkcif import MakeCheckCif, MyHTMLParser
from tools.update import mainurl
from tools.version import VERSION

DEBUG = False

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    os.environ['PATH'] = sys._MEIPASS + os.pathsep + os.environ['PATH']
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

if DEBUG:
    from PyQt5 import uic

    print('Compiling ui ...')
    uic.compileUiDir(os.path.join(application_path, './gui'))
    # uic.compileUi('./gui/finalcif_gui.ui', open('./gui/finalcif_gui.py', 'w'))

from PyQt5.QtCore import QPoint, Qt, QUrl, QObject, QEvent
from PyQt5.QtGui import QColor, QFont, QIcon, QPalette
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QHeaderView, QListWidget, QListWidgetItem, \
    QMainWindow, QMessageBox, QPlainTextEdit, QSizePolicy, QStackedWidget, QStyle, QTableWidget, QTableWidgetItem

from cif.cif_file_io import CifContainer, set_pair_delimited, retranslate_delimiter
from datafiles.bruker_data import BrukerData
from datafiles.platon import Platon
from tools.misc import high_prio_keys, predef_equipment_templ, predef_prop_templ, combobox_fields, \
    text_field_keys, to_float, find_line, strip_finalcif_of_name
from tools.settings import FinalCifSettings

"""
TODO:
- add loops to templates
- write more tests!
- calculate space group and crystal system if missing
- support stoe cif
- support all of .cifod
- try QNetworkRequest for checkcif
- Add one picture of the vzs file
- option for default directory?
- add button for zip file with cif, report and checkcif pdf
- Checkcif: http://journals.iucr.org/services/cif/checking/validlist.html
- load pairs and loops, add new content with order, write back

- spgr = gemmi.find_spacegroup_by_ops(gemmi.GroupOps([gemmi.Op(o) for o in ['x,y,z', ...]]))
- ops = [op.triplet() for op in gemmi.find_spacegroup_by_name('I2').operations()]

c = CifContainer(Path('test-data/DK_zucker2_0m-finalcif.cif'))
cdic = json.loads(c.as_json())
[cdic[x]['_name'] for x in cdic.keys() if '_name' in cdic[x]]

as dict:
{str(cdic[x]['_name']): ' '.join(cdic[x]['_definition'].split()) for x in cdic.keys() if '_name' in cdic[x]}

for item in c.block:
    if item.line_number < 670:
        if item.pair is not None:
            print('pair', item.pair)
        elif item.loop is not None:
            print('loop', item.loop)
            print([c.block.find_values(x) for x in item.loop.tags])
"""
light_green = QColor(217, 255, 201)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)
from gui.finalcif_gui import Ui_FinalCifWindow


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        # To make file drag&drop working:
        self.setAcceptDrops(True)
        self.show()
        self.statusBar().showMessage('FinalCif version {}'.format(VERSION))
        self.vheaderitems = list()
        self.settings = FinalCifSettings(self)
        self.store_predefined_templates()
        self.show_equipment_and_properties()
        self.settings.load_window_position()
        self.ui.CifItemsTable.installEventFilter(self)
        # distribute CifItemsTable Columns evenly:
        hheader = self.ui.CifItemsTable.horizontalHeader()
        hheader.setSectionResizeMode(0, QHeaderView.Stretch)
        hheader.setSectionResizeMode(1, QHeaderView.Stretch)
        hheader.setSectionResizeMode(2, QHeaderView.Stretch)
        # hheader.setAlternatingRowColors(True)
        # self.ui.CifItemsTable.verticalHeader().setAlternatingRowColors(True)
        # Make sure the start page is shown and not the edit page:
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)
        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.EquipmentEditTableWidget.verticalHeader().hide()
        self.ui.PropertiesEditTableWidget.verticalHeader().hide()
        self.ui.CheckcifButton.setDisabled(True)
        self.ui.CheckcifOnlineButton.setDisabled(True)
        self.ui.CheckcifPDFOnlineButton.setDisabled(True)
        self.ui.SaveCifButton.setDisabled(True)
        self.ui.ExploreDirButton.setDisabled(True)
        self.cif = None
        self.fin_file = Path()
        self.missing_data = []
        self.vheader_clicked = -1  # This is the index number of the vheader that got clicked last
        self.connect_signals_and_slots()
        self.manufacturer = 'bruker'
        self.rigakucif = None
        self.ui.SaveCifButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.ui.CheckcifButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        self.ui.CheckcifOnlineButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
        self.ui.CheckcifPDFOnlineButton.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
        self.ui.SaveFullReportButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.ui.SelectCif_PushButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogContentsView))
        self.ui.BackPushButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogBack))
        self.ui.BacktoMainpushButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogBack))
        if len(sys.argv) > 1:
            self.load_cif_file(sys.argv[1])
        # Sorting desyncronizes header and columns:
        self.ui.CifItemsTable.setSortingEnabled(False)
        self.setWindowIcon(QIcon('./icon/finalcif.png'))
        self.load_recent_cifs_list()
        self.netman = QNetworkAccessManager()
        self.netman.finished.connect(self.show_update_warning)
        self.checkfor_version()

    def __del__(self):
        print('saving position')
        x, y = self.pos().x(), self.pos().y()
        self.settings.save_window_position(QPoint(x, y - 30), self.size(), self.isMaximized())
        self.settings.save_favorite_template(self.ui)

    def connect_signals_and_slots(self):
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        self.ui.BackPushButton.clicked.connect(self.back_to_main)
        self.ui.ExploreDirButton.clicked.connect(self.explore_dir)
        ##
        self.ui.CheckcifButton.clicked.connect(self.do_offline_checkcif)
        self.ui.CheckcifOnlineButton.clicked.connect(self.do_html_checkcif)
        self.ui.CheckcifPDFOnlineButton.clicked.connect(self.do_pdf_checkcif)
        self.ui.BacktoMainpushButton.clicked.connect(self.back_to_main)
        ##
        self.ui.SelectCif_PushButton.clicked.connect(self.load_cif_file)
        self.ui.SaveCifButton.clicked.connect(self.save_cif_and_display)
        ##
        self.ui.EquipmentTemplatesListWidget.doubleClicked.connect(self.edit_equipment_template)
        self.ui.EditEquipmentTemplateButton.clicked.connect(self.edit_equipment_template)
        self.ui.SaveEquipmentButton.clicked.connect(self.save_equipment_template)
        self.ui.CancelEquipmentButton.clicked.connect(self.cancel_equipment_template)
        self.ui.DeleteEquipmentButton.clicked.connect(self.delete_equipment)
        self.ui.ExportEquipmentButton.clicked.connect(self.export_equipment_template)
        self.ui.ImportEquipmentTemplateButton.clicked.connect(self.import_equipment_from_file)
        ##
        self.ui.PropertiesTemplatesListWidget.doubleClicked.connect(self.edit_property_template)
        self.ui.EditPropertyTemplateButton.clicked.connect(self.edit_property_template)
        self.ui.SavePropertiesButton.clicked.connect(self.save_property_template)
        self.ui.CancelPropertiesButton.clicked.connect(self.cancel_property_template)
        self.ui.DeletePropertiesButton.clicked.connect(self.delete_property)
        ##
        self.ui.EquipmentEditTableWidget.cellPressed.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemSelectionChanged.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemEntered.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.cellChanged.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.currentItemChanged.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemActivated.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemPressed.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemClicked.connect(self.add_eq_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemChanged.connect(self.add_eq_row_if_needed)
        ##
        self.ui.PropertiesEditTableWidget.itemSelectionChanged.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.cellPressed.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemEntered.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.cellChanged.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.currentItemChanged.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemActivated.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemPressed.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemClicked.connect(self.add_eq_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemChanged.connect(self.add_eq_row_if_needed)
        #
        self.ui.ImportPropertyTemplateButton.clicked.connect(self.import_property_from_file)
        self.ui.ExportPropertyButton.clicked.connect(self.export_property_template)
        ##
        self.ui.NewEquipmentTemplateButton.clicked.connect(self.new_equipment)
        self.ui.NewPropertyTemplateButton.clicked.connect(self.new_property)
        ##
        self.ui.EquipmentTemplatesListWidget.currentRowChanged.connect(self.load_selected_equipment)
        self.ui.EquipmentTemplatesListWidget.clicked.connect(self.load_selected_equipment)
        # something like cifItemsTable.selected_field.connect(self.display_data_file)
        ##
        self.ui.SaveFullReportButton.clicked.connect(self.make_table)
        # vertical header click:
        view = self.ui.CifItemsTable.verticalHeader()
        view.setSectionsClickable(True)
        view.sectionClicked.connect(self.vheader_section_click)
        ###
        self.ui.RecentComboBox.currentIndexChanged.connect(self.load_recent_file)

    def checkfor_version(self):
        url = QUrl(mainurl + 'version.txt')
        req = QNetworkRequest(url)
        self.netman.get(req)

    def show_update_warning(self, reply: QNetworkReply):
        """
        Reads the reply from the server and displays a warning in case of an old version.
        """
        remote_version = 0
        try:
            remote_version = int(bytes(reply.readAll()).decode('ascii', 'ignore'))
        except Exception:
            pass
        if remote_version > VERSION:
            print('Version {} is outdated (actual is {}).'.format(VERSION, remote_version))
            self.show_general_warning(
                r"A newer version {} of FinalCif is available under: <br>"
                r"<a href='https://www.xs3.uni-freiburg.de/research/finalcif'>"
                r"https://www.xs3.uni-freiburg.de/research/finalcif</a>".format(remote_version))

    def explore_dir(self):
        try:
            curdir = self.cif.fileobj.absolute().parent
        except AttributeError:
            return
        if sys.platform == "win" or sys.platform == "win32":
            subprocess.Popen(['explorer', str(curdir)], shell=True)
        if sys.platform == 'darwin':
            subprocess.call(['open', curdir])
        if sys.platform == 'linux':
            subprocess.call(['xdg-open', curdir])

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Handles drop events.
        """
        from urllib.parse import urlparse
        p = urlparse(e.mimeData().text())
        if sys.platform.startswith('win'):
            final_path = p.path[1:]  # remove strange / at start
        else:
            final_path = p.path
        _, ending = os.path.splitext(final_path)
        # print(final_path, ending)
        if ending.lower() == '.cif':
            self.load_cif_file(final_path)

    def back_to_main(self):
        """
        Get back to the main table.
        """
        self.load_cif_file(str(self.fin_file.absolute()))
        self.ui.MainStackedWidget.setCurrentIndex(0)

    def do_html_checkcif(self):
        """
        Performs an online checkcif via checkcif.iucr.org.
        """
        self.ui.statusBar.showMessage('Sending html report request...')
        self.save_current_cif_file()
        htmlfile = Path(strip_finalcif_of_name('checkcif-' + self.cif.fileobj.stem) + '-finalcif.html')
        try:
            htmlfile.unlink()
        except FileNotFoundError:
            pass
        try:
            ckf = MakeCheckCif(self, self.fin_file, outfile=htmlfile)
            ckf.show_html_report()
        except ReadTimeout:
            self.show_general_warning(r"The check took too long. Try it at"
                                      r" <a href='https://checkcif.iucr.org/'>https://checkcif.iucr.org/</a> directly.")
        except Exception as e:
            print('Can not do checkcif:')
            print(e)
            return
        # The picture file linked in the html file:
        imageobj = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.gif')
        parser = MyHTMLParser()
        parser.feed(htmlfile.read_text())
        gif = parser.get_image()
        imageobj.write_bytes(gif)
        self.ui.statusBar.showMessage('Report finished.')

    def do_pdf_checkcif(self):
        """
        Performs an online checkcif and shows the result as pdf.
        """
        self.ui.statusBar.showMessage('Sending pdf report request...')
        self.save_current_cif_file()
        htmlfile = Path('checkpdf-' + self.cif.fileobj.stem + '.html')
        try:
            htmlfile.unlink()
        except FileNotFoundError:
            pass
        try:
            ckf = MakeCheckCif(self, self.fin_file, outfile=htmlfile)
            ckf.show_pdf_report()
        except ReadTimeout:
            self.show_general_warning(r"The check took too long. Try it at"
                                      r" <a href='https://checkcif.iucr.org/'>https://checkcif.iucr.org/</a> directly.")
        except Exception as e:
            print('Can not do checkcif:')
            print(e)
        self.ui.statusBar.showMessage('Report finished.')
        try:
            htmlfile.unlink()
        except FileNotFoundError:
            pass

    def do_offline_checkcif(self):
        """
        Performs a checkcif with platon and displays it in the text editor of the MainStackedWidget.
        """
        table = self.ui.CifItemsTable
        table.setCurrentItem(None)  # makes sure also the currently edited item is saved
        self.save_current_cif_file()
        try:
            p = Platon(self.fin_file)
        except Exception as e:
            print(e)
            # self.ui.CheckcifButton.setDisabled(True)
            return
        self.ui.MainStackedWidget.setCurrentIndex(1)
        ccpe = self.ui.CheckcifPlaintextEdit
        ccpe.setPlainText('Platon output: \nThis might not be the same as the IUCr Checkcif!')
        ccpe.appendPlainText(p.platon_output)
        ccpe.appendPlainText('\n' + '#' * 80)
        doc = ccpe.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        font.setStyleHint(QFont.Monospace)
        # increases the pont size every time a bit more :)
        # size = font.pointSize()
        font.setPointSize(14)
        doc.setDefaultFont(font)
        ccpe.setLineWrapMode(QPlainTextEdit.NoWrap)
        if p.chk_file_text:
            try:
                ccpe.appendPlainText(p.chk_file_text)
                ccpe.appendPlainText('\n' + '#' * 27 + ' Validation Response Forms ' + '#' * 26 + '\n')
                ccpe.appendPlainText(p.vrf_txt)
            except AttributeError:
                pass
        ccpe.verticalScrollBar().setValue(0)

    def load_recent_file(self, file_index):
        combo = self.ui.RecentComboBox
        if file_index > 0:
            txt = combo.itemText(file_index)
            self.load_cif_file(txt)

    def vheader_section_click(self, section):
        item = self.ui.CifItemsTable.verticalHeaderItem(section)
        itemtext = item.text()
        # be sure not to get vheader with name of last click:
        if section != self.vheader_clicked and self.vheader_clicked > -1:
            self.restore_vertical_header()
            self.vheader_clicked = -1
            return
            # get back previous name
        if self.vheader_clicked > -1:
            item.setText(self.vheaderitems[self.vheader_clicked])
            self.vheader_clicked = -1
            return
        try:
            txt = high_prio_keys[itemtext]
            if txt:
                item.setText(txt)
            self.vheader_clicked = section
            return
        except KeyError:
            pass

    def restore_vertical_header(self):
        for row_num, key in enumerate(self.vheaderitems):
            item_key = QTableWidgetItem(key)
            self.ui.CifItemsTable.setVerticalHeaderItem(row_num, item_key)

    def make_table(self):
        """
        Runs the multitable program to make a report table.
        """
        not_ok = None
        if self.cif:
            self.save_current_cif_file()
            output_filename = strip_finalcif_of_name('report_{}'.format(self.cif.fileobj.stem)) + '-finalcif.docx'
            try:
                make_report_from(self.fin_file, output_filename=output_filename, path=application_path,
                                 without_H=self.ui.HAtomsCheckBox.isChecked())
            except FileNotFoundError as e:
                if DEBUG:
                    raise
                print('Unable to open cif file')
                not_ok = e
                self.unable_to_open_message(self.cif.fileobj, not_ok)
                return
            except PermissionError:
                if DEBUG:
                    raise
                print('Unable to open cif file')
                self.show_general_warning('The report document {} could not be opened.\n'
                                          'Is the file already opened?'.format(output_filename))
                return
            if os.name == 'nt':
                os.startfile(Path(output_filename).absolute())
            if sys.platform == 'darwin':
                subprocess.call(['open', Path(output_filename).absolute()])

    def save_current_recent_files_list(self, file):
        if os.name == 'nt':
            file = WindowsPath(file).absolute()
        else:
            file = Path(file).absolute()
        recent = list(self.settings.settings.value('recent_files', type=list))
        if str(file) not in recent:
            # file has to be str not Path():
            recent.insert(0, str(file))
        if len(recent) > 7:
            recent.pop()
        self.settings.settings.setValue('recent_files', recent)
        # print(recent, 'save')

    def load_recent_cifs_list(self):
        self.ui.RecentComboBox.clear()
        recent = list(self.settings.settings.value('recent_files', type=list))
        self.ui.RecentComboBox.addItem('Recent Files')
        for n, file in enumerate(recent):
            if not isinstance(file, str):
                del recent[n]
            try:
                if not Path(file).exists():
                    del recent[n]
            except OSError:
                pass
            self.ui.RecentComboBox.addItem(file, n)

    def save_cif_and_display(self):
        self.save_current_cif_file()
        self.display_saved_cif()

    def get_table_item(self, table, row, col) -> str:
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
        if not item:
            try:
                item = table.cellWidget(row, col).currentText()
            except AttributeError:
                item = None
        return item

    def save_current_cif_file(self):
        """
        Saves the current cif file and stores the information of the third column.
        """
        # restore header, otherwise item is not saved:
        self.restore_vertical_header()
        table = self.ui.CifItemsTable
        table.setCurrentItem(None)  # makes sure also the currently edited item is saved
        rowcount = table.model().rowCount()
        columncount = table.model().columnCount()
        for row in range(rowcount):
            col0 = None  # cif content
            col1 = None  # from datafiles
            col2 = None  # own text
            for col in range(columncount):
                item = self.get_table_item(table, row, col)
                if item:
                    if col == 0 and item != (None or '' or '?'):
                        col0 = item
                    # removed: not col0 and
                    if col == 1 and item != (None or '' or '?'):
                        col1 = item
                    try:
                        if col == 2 and item != (None or ''):
                            col2 = item
                    except AttributeError:
                        pass
                if col == 2:
                    vhead = self.ui.CifItemsTable.model().headerData(row, Qt.Vertical)
                    if not str(vhead).startswith('_'):
                        continue
                    # This is my row information
                    # print('col2:', vhead, col0, col1, col2, '#')
                    if col1 and not col2:
                        set_pair_delimited(self.cif.block, vhead, col1)
                    if col2:
                        try:
                            set_pair_delimited(self.cif.block, vhead, col2)
                        except RuntimeError:
                            pass
        try:
            self.fin_file = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.cif')
            self.cif.save(self.fin_file.name)
            self.ui.statusBar.showMessage('  File Saved:  {}'.format(self.fin_file.name), 10000)
            print('File saved ...')
        except (AttributeError, UnicodeEncodeError, PermissionError) as e:
            print('Unable to save file:')
            print(e)
            self.show_general_warning('Can not save file: ' + str(e))
            return

    def display_saved_cif(self):
        """
        Displays the saved cif file into a textfield.
        """
        self.ui.MainStackedWidget.setCurrentIndex(2)
        final_textedit = self.ui.FinalCifFilePlainTextEdit
        doc = final_textedit.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        font.setStyleHint(QFont.Monospace)
        # increases the pont size every time a bit more :)
        # size = font.pointSize()
        font.setPointSize(14)
        doc.setDefaultFont(font)
        final_textedit.setLineWrapMode(QPlainTextEdit.NoWrap)
        final_textedit.setPlainText(self.fin_file.read_text(encoding='utf-8', errors='ignore'))

    def show_equipment_and_properties(self):
        """
        Display saved items in the equipment and properties lists.
        """
        self.ui.EquipmentTemplatesListWidget.clear()
        self.ui.PropertiesTemplatesListWidget.clear()
        for eq in self.settings.get_equipment_list():
            if eq:
                item = QListWidgetItem(eq)
                self.ui.EquipmentTemplatesListWidget.addItem(item)
        property_list = self.settings.settings.value('property_list')
        if property_list:
            property_list.sort()
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
            for key in equipment:
                if key not in self.vheaderitems:
                    self.add_new_table_key(key)
                # add missing item to data sources column:
                if key in text_field_keys:
                    # special treatments for text fields:
                    tabitem = QPlainTextEdit(self)
                    pal = tabitem.palette()
                    pal.setColor(QPalette.Base, light_green)
                    tabitem.setPalette(pal)
                    txtlst = equipment[key].split(r'\n')
                    # special treatment for text fields in order to get line breaks:
                    for txt in txtlst:
                        tabitem.appendPlainText(txt)
                    tabitem.setFrameShape(0)  # no fram earound the field
                    # tabitem.setPalette(pal)
                    row = self.vheaderitems.index(key)
                    column = 1
                    self.ui.CifItemsTable.setCellWidget(row, column, tabitem)
                else:
                    try:
                        tab_item = QTableWidgetItem(str(equipment[key]))
                        # vheaderitems contain the cif keywords in the vertical header, the 1 is the data sources column.
                        row = self.vheaderitems.index(key)
                        column = 1
                        self.ui.CifItemsTable.setItem(row, column, tab_item)
                        tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)
                        tab_item.setBackground(light_green)
                    except ValueError as e:
                        print('not in list:', e)

    def add_new_table_key(self, key: str) -> None:
        """
        Adds a new row with a respective vheaderitem to the main table.
        Also the currently opened cif file is updated.
        """
        if not key.startswith('_'):
            return
        self.vheaderitems.insert(0, key)
        self.add_row(key=key, value='?', at_start=True)
        if key in [x.lower() for x in combobox_fields]:
            self.add_property_combobox(combobox_fields[key], 0)
        self.missing_data.append(key)
        # This is a crude hack to get the new values to the start of the cif file:
        # It seems to be fast and stable though...
        if not self.cif.block.find_value(key):
            cif_lst = self.cif.cif_file_text.splitlines()
            data_position = find_line(cif_lst, '^data_')
            cif_lst.insert(data_position + 1, key + ' ' * (31 - len(key)) + '    ?')
            self.cif.cif_file_text = "\n".join(cif_lst)
            self.cif.open_cif_by_string()

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
        # I do these both to clear the list:
        self.store_predefined_templates()
        self.show_equipment_and_properties()

    def new_property(self):
        item = QListWidgetItem('')
        self.ui.PropertiesTemplatesListWidget.addItem(item)
        self.ui.PropertiesTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.PropertiesTemplatesListWidget.editItem(item)
        self.ui.cifKeywordLineEdit.clear()

    def add_eq_row_if_needed(self):
        """
        Adds an empty row at the bottom of either the EquipmentEditTableWidget, or the PropertiesEditTableWidget.
        """
        if self.ui.EquipmentEditTableWidget.hasFocus():
            table = self.ui.EquipmentEditTableWidget
        elif self.ui.PropertiesEditTableWidget.hasFocus():
            table = self.ui.PropertiesEditTableWidget
        else:
            return
        rowcount = table.rowCount()
        cont = 0
        for row in range(rowcount):
            key = ''
            try:
                key = table.item(row, 0).text()
            except (AttributeError, TypeError) as e:
                pass
            if key:  # don't count empty key rows
                cont += 1
        diff = rowcount - cont
        if diff < 4:
            table.insertRow(rowcount)

    def add_equipment_row(self, table: QTableWidget, key: str = '', value: str = ''):
        """
        Add a new row with content to the table (Equipment or Property).
        """
        if not isinstance(value, str):
            return
        if not isinstance(key, str):
            return
        # Create a empty row at bottom of table
        row_num = table.rowCount()
        table.insertRow(row_num)
        if len(value) > 38:
            tab_item = QPlainTextEdit()
            tab_item.setFrameShape(0)
            tab_item.setPlainText(retranslate_delimiter(value))
            table.setCellWidget(row_num, 1, tab_item)
        else:
            item_val = QTableWidgetItem(retranslate_delimiter(value))
            # Add cif key and value to the row:
            table.setItem(row_num, 1, item_val)
        item_key = QTableWidgetItem(key)
        table.setItem(row_num, 0, item_key)

    # The equipment templates:

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
            self.ui.EquipmentEditTableWidget.blockSignals(False)
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
        else:
            # new empty equipment:
            for _ in range(8):
                self.add_equipment_row(table, '', '')
        table.insertRow(n)
        self.ui.EquipmentEditTableWidget.blockSignals(False)
        stackedwidget.setCurrentIndex(1)
        self.ui.EquipmentEditTableWidget.resizeRowsToContents()

    def save_equipment_template(self):
        """
        Saves the currently selected equipment template to the config file.
        """
        selected_template_text, table_data = self.get_equipment_entry_data()
        # warn if key is not official:
        for key, _ in table_data:
            if key not in cif_core:
                if not key.startswith('_'):
                    self.show_general_warning('"{}" is not a valid keyword! '
                                              '\nChange the name in order to save.\n'
                                              'Keys must start with an underscore.'.format(key))
                    return
                self.show_general_warning('"{}" is not an official CIF keyword!'.format(key))
        self.settings.save_template('equipment/' + selected_template_text, table_data)
        self.settings.append_to_equipment_list(selected_template_text)
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('saved')

    def import_equipment_from_file(self):
        """
        Import an equipment entry from a cif file.
        """
        filename = self.cif_file_open_dialog()
        if not filename:
            return
        try:
            doc = cif.read_file(filename)
        except RuntimeError as e:
            self.show_general_warning(str(e))
            return
        block = doc.sole_block()
        data = json.loads(doc.as_json(mmjson=True))
        table_data = []
        name = block.name.replace('__', ' ')
        for key in data['data_' + block.name].keys():
            key = '_' + key
            d = [key, cif.as_string(block.find_value(key))]
            if d:
                table_data.append(d)
        self.settings.save_template('equipment/' + name, table_data)
        self.settings.append_to_equipment_list(name)
        self.show_equipment_and_properties()

    def get_equipment_entry_data(self):
        """
        Returns the string of the currently selected entry and the table date behind it.
        """
        table = self.ui.EquipmentEditTableWidget
        # Set None Item to prevent loss of the currently edited item:
        # The current item is closed and thus saved.
        table.setCurrentItem(None)
        selected_template_text = self.ui.EquipmentTemplatesListWidget.currentIndex().data()
        table_data = []
        ncolumns = table.rowCount()
        for rownum in range(ncolumns):
            key = ''
            try:
                key = self.get_table_item(table, rownum, 0)
                value = self.get_table_item(table, rownum, 1)
            except AttributeError:
                value = ''
            if key and value:
                table_data.append([key, value])
        return selected_template_text, table_data

    def export_equipment_template(self):
        """
        exports the currently selected equipment entry to a file.
        """
        selected_template, table_data = self.get_equipment_entry_data()
        if not selected_template:
            return
        doc = cif.Document()
        blockname = '__'.join(selected_template.split())
        block = doc.add_new_block(blockname)
        for key, value in table_data:
            set_pair_delimited(block, key, value)
        filename = self.cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        try:
            Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            self.show_general_warning('No permission to write file to {}'.format(Path(filename).absolute()))

    def cancel_equipment_template(self):
        """
        Cancel Equipment editing.
        """
        table = self.ui.EquipmentEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('cancelled equipment')

    # The properties templates:

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
        # I do these both to clear the list:
        self.store_predefined_templates()
        self.show_equipment_and_properties()

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
        self.load_property_from_settings(table, stackedwidget, listwidget)
        table.resizeRowsToContents()

    def save_property_template(self):
        table = self.ui.PropertiesEditTableWidget
        stackedwidget = self.ui.PropertiesTemplatesStackedWidget
        listwidget = self.ui.PropertiesTemplatesListWidget
        keyword = self.ui.cifKeywordLineEdit.text()
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

    def export_property_template(self):
        """
        Exports the currently selected property entry to a file.
        """
        selected_row_text = self.ui.PropertiesTemplatesListWidget.currentIndex().data()
        if not selected_row_text:
            return
        prop_data = self.settings.load_template('property/' + selected_row_text)
        table_data = []
        cif_key = ''
        if prop_data:
            cif_key = prop_data[0]
            try:
                table_data = prop_data[1]
            except:
                pass
        if not cif_key:
            return
        doc = cif.Document()
        blockname = '__'.join(selected_row_text.split())
        block = doc.add_new_block(blockname)
        loop = block.init_loop(cif_key, [''])
        for value in table_data:
            loop.add_row([value])
        filename = self.cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        try:
            Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            self.show_general_warning('No permission to write file to {}'.format(Path(filename).absolute()))

    def import_property_from_file(self):
        filename = self.cif_file_open_dialog()
        if not filename:
            return
        try:
            doc = cif.read_file(filename)
        except RuntimeError as e:
            self.show_general_warning(str(e))
            return
        property_list = self.settings.settings.value('property_list')
        if not property_list:
            property_list = ['']
        block = doc.sole_block()
        block_name = block.name.replace('__', ' ')
        property_list.append(block_name)
        table = self.ui.PropertiesEditTableWidget
        table.setRowCount(0)
        data = json.loads(doc.as_json(mmjson=True))['data_' + block.name]
        loop_column_name = list(data.keys())[0]
        template_list = [x for x in block.find_loop('_' + loop_column_name)]
        self.ui.cifKeywordLineEdit.setText(loop_column_name)
        newlist = [x for x in list(set(property_list)) if x]
        newlist.sort()
        # this list keeps track of the equipment items:
        self.settings.save_template('property_list', newlist)
        template_list.insert(0, '')
        # save as dictionary for properties to have "_cif_key : itemlist"
        # for a table item as dropdown menu in the main table.
        table_data = [block_name, template_list]
        self.settings.save_template('property/' + block_name, table_data)
        self.show_equipment_and_properties()

    def load_property_from_settings(self, table: QTableWidget, stackedwidget: QStackedWidget, listwidget: QListWidget):
        """
        Load/Edit the value list of a property entry.
        """
        #self.ui.PropertiesEditTableWidget.blockSignals(True)
        property_list = self.settings.settings.value('property_list')
        if not property_list:
            property_list = ['']
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            #self.ui.PropertiesEditTableWidget.blockSignals(False)
            return
        selected_row_text = listwidget.currentIndex().data()
        table_data = self.settings.load_template('property/' + selected_row_text)
        if table_data:
            cif_key = table_data[0]
            try:
                table_data = table_data[1]
            except:
                pass
            self.ui.cifKeywordLineEdit.setText(cif_key)
        n = 0
        if not table_data:
            table_data = ['', '', '', '', '', '']
        for value in table_data:
            try:
                self.add_propeties_row(table, str(value))
            except TypeError:
                print('Bad value in property table')
                continue
            n += 1
        property_list.append(selected_row_text)
        newlist = [x for x in list(set(property_list)) if x]
        # this list keeps track of the equipment items:
        self.settings.save_template('property_list', newlist)
        stackedwidget.setCurrentIndex(1)
        #self.ui.PropertiesEditTableWidget.blockSignals(False)
        table.setWordWrap(False)
        table.resizeRowsToContents()

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
        print('canceled property')

    @staticmethod
    def cif_file_open_dialog():
        """
        Returns a cif file name from a file dialog.
        """
        filename, _ = QFileDialog.getOpenFileName(filter="CIF file (*.cif)",
                                                  initialFilter="CIF file (*.cif)",
                                                  caption='Open a .cif File')
        return filename

    @staticmethod
    def cif_file_save_dialog(filename: str) -> str:
        """
        Returns a cif file name from a file dialog.
        """
        dialog = QFileDialog(filter="CIF file (*.cif)", caption='Save .cif File')
        dialog.setDefaultSuffix('.cif')
        dialog.selectFile(filename)
        filename, _ = dialog.getSaveFileName(None, 'Select file name', filename)
        return filename

    def load_cif_file(self, fname):
        """
        Opens the cif file and fills information into the main table.
        """
        self.vheaderitems.clear()
        self.ui.MainStackedWidget.setCurrentIndex(0)
        self.ui.CifItemsTable.setRowCount(0)
        self.ui.CifItemsTable.clear()
        self.ui.CifItemsTable.clearContents()
        self.ui.CheckcifPlaintextEdit.clear()
        if not fname:
            fname = self.cif_file_open_dialog()
        if not fname:
            return
        if os.name == 'nt':
            self.ui.SelectCif_LineEdit.setText(str(WindowsPath(fname).absolute()))
        else:
            self.ui.SelectCif_LineEdit.setText(fname)
        self.save_current_recent_files_list(fname)
        self.load_recent_cifs_list()
        try:
            filepath = Path(fname)
            if not filepath.exists():
                return
        except OSError:
            print('Something failed during cif file opening...')
            return
        not_ok = None
        try:
            e = None
            self.cif = CifContainer(filepath)
        except Exception as e:
            print('Unable to open cif file...')
            if DEBUG:
                raise
            print(e)
            not_ok = e
        if not_ok:
            self.unable_to_open_message(filepath, not_ok)
            return
        try:
            # Change the current working Directory
            os.chdir(filepath.absolute().parent)
        except OSError:
            print("Can't change the Current Working Directory")
        try:
            rigaku = Path('./').glob('*.cif_od').__next__()
            if rigaku.exists():
                self.manufacturer = 'rigaku'
                self.rigakucif = RigakuData(rigaku)
        except StopIteration:
            pass
        self.ui.CifItemsTable.clearContents()
        # self.ui.CifItemsTable.clear() # clears header
        try:
            self.fill_cif_table()
        except RuntimeError as e:
            not_ok = e
            if DEBUG:
                raise
            self.unable_to_open_message(filepath, not_ok)
        self.ui.CheckcifButton.setEnabled(True)
        self.ui.CheckcifOnlineButton.setEnabled(True)
        self.ui.CheckcifPDFOnlineButton.setEnabled(True)
        self.ui.SaveCifButton.setEnabled(True)
        self.ui.ExploreDirButton.setEnabled(True)
        # self.ui.EquipmentTemplatesListWidget.setCurrentRow(-1)  # Has to he in front in order to work
        # self.ui.EquipmentTemplatesListWidget.setCurrentRow(self.settings.load_last_equipment())

    def unable_to_open_message(self, filepath, not_ok):
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        print('Output from gemmi:', not_ok)
        try:
            line = str(not_ok)[4:].split(':')[1]
        except IndexError:
            line = None
        if line:
            info.setText('This cif file is not readable!\n'
                         'Please check line {} in\n{}'.format(line, filepath.name))
        else:
            info.setText('This cif file is not readable! "{}"\n{}'.format(filepath.name, not_ok))
        info.show()
        info.exec()
        return

    def test_checksums(self):
        """
        A method to check wether the checksums in the cif file fit to the content.
        """
        cif_res_ckecksum = 0
        if self.cif.res_checksum_calcd > 0:
            cif_res_ckecksum = int(self.cif.block.find_value('_shelx_res_checksum')) or -1
        if cif_res_ckecksum > 0 and cif_res_ckecksum != self.cif.res_checksum_calcd:
            self.show_checksum_warning()
        cif_hkl_ckecksum = 0
        if self.cif.hkl_checksum_calcd > 0:
            cif_hkl_ckecksum = int(self.cif.block.find_value('_shelx_hkl_checksum')) or -1
        if cif_hkl_ckecksum > 0 and cif_hkl_ckecksum != self.cif.hkl_checksum_calcd:
            self.show_checksum_warning(res=False)

    def show_checksum_warning(self, res=True):
        """
        A message box to display if the checksums do not agree.
        """
        info = QMessageBox()
        info.setIcon(QMessageBox.Warning)
        if res:
            info.setText('The "_shelx_res_checksum" is not\nconsistent with the .res file content!')
        else:
            info.setText('The "_shelx_hkl_checksum" is not\nconsistent with the .hkl file content!')
        info.show()
        info.exec()

    def show_general_warning(self, warn_text=''):
        """
        A message box to display if the checksums do not agree.
        """
        if not warn_text:
            return
        QMessageBox(self).warning(self, ' ', warn_text)

    def check_Z(self):
        """
        Crude check if Z is much too high e.h. a SEHLXT solution with "C H N O" sum formula.
        """
        Z = to_float(self.cif['_cell_formula_units_Z'])
        density = to_float(self.cif['_exptl_crystal_density_diffrn'])
        csystem = self.cif.crystal_system
        bad = False
        ntypes = len(self.cif['_chemical_formula_sum'].split())
        if all([ntypes, density]):
            if ntypes > 2.0 and density < 0.6 or density > 4.0:
                bad = True
        if Z and Z > 8.0 and (csystem == 'tricilinic' or csystem == 'monoclinic'):
            bad = True
        if Z and Z > 16.0 and (csystem == 'orthorhombic' or csystem == 'tetragonal' or csystem == 'trigonal'
                               or csystem == 'hexagonal' or csystem == 'cubic'):
            bad = True
        if bad:
            zinfo = QMessageBox()
            zinfo.setIcon(QMessageBox.Information)
            zinfo.setText('The number of formula units Z={:.0f} is probably wrong.'
                          '\nYou may restart refinement with a correct value.'.format(Z))
            zinfo.show()
            zinfo.exec()

    def get_data_sources(self):
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.
        """
        sources = None
        self.check_Z()
        if self.manufacturer == 'bruker':
            sources = BrukerData(self, self.cif).sources
        if self.manufacturer == 'rigaku':
            sources = self.rigakucif.sources
        # Build a dictionary of cif keys and row number values in order to fill the first column
        # of CifItemsTable with cif values:
        for num in range(self.ui.CifItemsTable.model().rowCount()):
            vhead = self.ui.CifItemsTable.model().headerData(num, Qt.Vertical)
            if not vhead in self.vheaderitems:
                self.vheaderitems.append(vhead)
        # They are needed for the comboboxes:
        property_fields = self.settings.load_property_keys()
        # get missing items from sources and put them into the corresponding rows:
        # These will be yellow if not filled in:
        self.missing_data.append('_cell_measurement_temperature')
        self.missing_data.append('_diffrn_ambient_temperature')
        self.missing_data.append('_publ_section_references')
        for miss_data in self.missing_data:
            # add missing item to data sources column:
            try:
                row_num = self.vheaderitems.index(miss_data)
            except ValueError:
                continue
            tab_item = QTableWidgetItem()
            try:
                # sources are lower case!
                txt = str(sources[miss_data.lower()][0])
                tooltiptext = str(sources[miss_data.lower()][1])
                if miss_data in text_field_keys:
                    tab_item = QPlainTextEdit(self.ui.CifItemsTable)
                    tab_item.setReadOnly(True)
                    tab_item.setFrameShape(0)
                    self.ui.CifItemsTable.setCellWidget(row_num, 1, tab_item)
                    tab_item.setPlainText(txt)
                    pal = tab_item.palette()
                    if txt and txt != '?':
                        pal.setColor(QPalette.Base, light_green)
                    else:
                        pal.setColor(QPalette.Base, yellow)
                    tab_item.setPalette(pal)
                else:
                    #                             # row  column  item
                    self.ui.CifItemsTable.setItem(row_num, 1, tab_item)
                    tab_item.setText(txt)  # has to be string
                    if txt and txt != '?':
                        tab_item.setBackground(light_green)
                    else:
                        tab_item.setBackground(yellow)
                tab_item.setToolTip(tooltiptext)
                # print(sources[miss_data], miss_data)
                # self.ui.CifItemsTable.resizeRowToContents(row_num)
            except KeyError as e:
                # print(e, '##')
                pass
            # items from data sources should not be editable
            if not miss_data in text_field_keys:
                tab_item.setFlags(tab_item.flags() ^ Qt.ItemIsEditable)
            # creating comboboxes for special keywords like _exptl_crystal_colour.
            # In case a property for this key exists, it will show this list:
            if miss_data.lower() in [x.lower() for x in property_fields]:
                self.add_property_combobox(self.settings.load_property_by_key(miss_data), row_num)
            elif miss_data.lower() in [x.lower() for x in combobox_fields]:
                self.add_property_combobox(combobox_fields[miss_data], row_num)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel and widget and not widget.hasFocus():
            event.ignore()
            return True
        if event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Backtab:
            row = self.ui.CifItemsTable.currentRow()
            if row > 0:
                self.ui.CifItemsTable.setCurrentCell(row - 1, 2)
            return True
        if event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Tab:
            row = self.ui.CifItemsTable.currentRow()
            self.ui.CifItemsTable.setCurrentCell(row, 2)
            return True
        return QObject.eventFilter(self, widget, event)

    def add_property_combobox(self, miss_data: str, row_num: int):
        """
        Adds a QComboBox to the CifItemsTable with the content of special_fields or property templates.
        """
        combobox = QComboBox()
        # Works in combination with the event filter:
        combobox.setFocusPolicy(Qt.StrongFocus)
        combobox.installEventFilter(self)
        # combobox.currentIndexChanged.connect(self.print_combo)
        # print('special:', row_num, miss_data)
        self.ui.CifItemsTable.setCellWidget(row_num, 2, combobox)
        self.ui.CifItemsTable.setHorizontalScrollBarPolicy(1)
        # combobox.setFixedWidth(self.ui.CifItemsTable.columnWidth(2))
        # Otherwise, the combobox will be longer than the column:
        combobox.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        combobox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
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
            if not value or value == '?' or value == "'?'":
                self.missing_data.append(key)
                value = '?'
            self.add_row(key, value)
            # print(key, value)
        self.test_checksums()
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

    def add_row(self, key, value, at_start=False):
        """
        Create a empty row at bottom of CifItemsTable. This method only fills cif data in the
        first column. Not the data from external sources!
        """
        if at_start:
            row_num = 0
        else:
            row_num = self.ui.CifItemsTable.rowCount()
        self.ui.CifItemsTable.insertRow(row_num)
        # Add cif key and value to the row:
        item_key = QTableWidgetItem(key)
        if value is None:
            strval = '?'
        else:
            strval = str(value).strip(" ").strip("'").strip(';\n')  # or '?')
        if not key:
            strval = ''
        if key in text_field_keys:
            # print(key, strval)
            tabitem = QPlainTextEdit(self.ui.CifItemsTable)
            tabitem.setPlainText(strval)
            tabitem.setFrameShape(0)  # no frame (border)
            tab1 = QPlainTextEdit(self.ui.CifItemsTable)
            tab1.setFrameShape(0)
            tab2 = QPlainTextEdit(self.ui.CifItemsTable)
            tab2.setTabChangesFocus(True)
            tab2.setFrameShape(0)
            self.ui.CifItemsTable.setCellWidget(row_num, 0, tabitem)
            self.ui.CifItemsTable.setCellWidget(row_num, 1, tab1)
            self.ui.CifItemsTable.setCellWidget(row_num, 2, tab2)
            tabitem.setReadOnly(True)
            tab1.setReadOnly(True)
            # Make QPlainTextEdit fields a bit higher than the rest
            self.ui.CifItemsTable.setRowHeight(row_num, 90)
        # else:
        # if key in text_field_keys:
        #    self.ui.CifItemsTable.setRowHeight(row_num, 60)
        else:
            tabitem = QTableWidgetItem(strval)
            if key == "These below are already in:":
                # pal = QPalette()
                # pal.setColor(QPalette.Foreground, Qt.black)
                item1 = QTableWidgetItem('')
                item2 = QTableWidgetItem('')
                item3 = QTableWidgetItem('')
                item1.setBackground(blue)
                item1.setFlags(item1.flags() ^ Qt.ItemIsEditable)
                item2.setBackground(blue)
                item2.setFlags(item2.flags() ^ Qt.ItemIsEditable)
                item3.setBackground(blue)
                item3.setFlags(item3.flags() ^ Qt.ItemIsEditable)
                self.ui.CifItemsTable.setItem(row_num, 0, item1)
                self.ui.CifItemsTable.setItem(row_num, 1, item2)
                self.ui.CifItemsTable.setItem(row_num, 2, item3)
                self.ui.CifItemsTable.resizeRowToContents(row_num)
            else:
                tab1 = QTableWidgetItem()
                tab2 = QTableWidgetItem()
                self.ui.CifItemsTable.setItem(row_num, 1, tab1)
                self.ui.CifItemsTable.setItem(row_num, 0, tabitem)
                if key == '_audit_creation_method':
                    # or better _audit_update_record?
                    """'A record of any changes to the data block. The '
                    'update format is a date (yyyy-mm-dd) followed by a '
                    'description of the changes. The latest update entry '
                    'is added to the bottom of this record.'"""
                    tab2.setText('FinalCif by Daniel Kratzert, Freiburg 2019')
                    self.ui.CifItemsTable.setItem(row_num, 2, tab2)
                tabitem.setFlags(tabitem.flags() ^ Qt.ItemIsEditable)
                tab1.setFlags(tab1.flags() ^ Qt.ItemIsEditable)
                self.ui.CifItemsTable.resizeRowToContents(row_num)
        self.ui.CifItemsTable.setVerticalHeaderItem(row_num, item_key)


if __name__ == '__main__':
    def my_exception_hook(exctype, value, error_traceback):
        """
        Hooks into Exceptions to create debug reports.
        """
        errortext = 'FinalCif crash report\n\n'
        errortext += time.asctime(time.localtime(time.time())) + '\n'
        errortext += "Finalcif crashed during the following opertaion:" + '\n'
        errortext += '-' * 80 + '\n'
        errortext += ''.join(traceback.format_tb(error_traceback)) + '\n'
        errortext += str(exctype.__name__) + ': '
        errortext += str(value) + '\n'
        errortext += '-' * 80 + '\n'
        logfile = Path(r'./finalcif-crash.txt')
        try:
            logfile.write_text(errortext)
        except PermissionError:
            pass
        sys.__excepthook__(exctype, value, error_traceback)
        # Hier Fesnter für meldung öffnen
        window = AppWindow()
        text = 'FinalCif encountered an error.<br>Please send the file <br>"{}" <br>to Daniel Kratzert:  ' \
               '<a href="mailto:daniel.kratzert@ac.uni-freiburg.de?subject=FinalCif version {} crash report">' \
               'daniel.kratzert@ac.uni-freiburg.de</a>'.format(logfile.absolute(), VERSION)
        QMessageBox.warning(window, 'Warning', text)
        window.show()
        sys.exit(1)


    sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    w = AppWindow()
    app.setWindowIcon(QIcon('./icon/finalcif.png'))
    w.setWindowTitle('FinalCif v{}'.format(VERSION))
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
