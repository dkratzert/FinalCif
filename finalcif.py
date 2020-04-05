#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

DEBUG = False

import os

from app_path import application_path

if DEBUG:
    from PyQt5 import uic

    print('Compiling ui ...')
    uic.compileUiDir(os.path.join(application_path, './gui'))
    # uic.compileUi('./gui/finalcif_gui.ui', open('./gui/finalcif_gui.py', 'w'))
import subprocess
import sys
import time
import traceback
import displaymol
from shutil import copy2
from tempfile import TemporaryDirectory
from contextlib import suppress
from math import radians, sin
from pathlib import Path, WindowsPath
from typing import Tuple

import qtawesome as qta
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt5.QtWebEngineWidgets import QWebEngineView
# noinspection PyUnresolvedReferences
from gemmi import cif
from qtpy.QtGui import QDesktopServices, QKeySequence
from requests import ReadTimeout

from cif.cif_file_io import CifContainer, set_pair_delimited, utf8_to_str, retranslate_delimiter
from cif.core_dict import cif_core
from datafiles.bruker_data import BrukerData
from datafiles.platon import Platon
from datafiles.rigaku_data import RigakuData
from displaymol import mol_file_writer, write_html
from displaymol.sdm import SDM
from gui.vrf_classes import MyVRFContainer, VREF
from report.archive_report import ArchiveReport
from report.tables import make_report_from
from tools.checkcif import AlertHelp, MakeCheckCif, MyHTMLParser
from tools.misc import combobox_fields, excluded_imports, predef_equipment_templ, predef_prop_templ, \
    strip_finalcif_of_name, text_field_keys, to_float, next_path, celltxt
from tools.settings import FinalCifSettings
from tools.version import VERSION

from PyQt5.QtCore import QPoint, Qt, QUrl, QEvent
from PyQt5.QtGui import QFont, QIcon, QBrush, QResizeEvent, QMoveEvent
from PyQt5.QtWidgets import QApplication, QFileDialog, QHeaderView, QListWidget, QListWidgetItem, \
    QMainWindow, QMessageBox, QPlainTextEdit, QStackedWidget, QTableWidget, QSplashScreen, QShortcut, QCheckBox, \
    QHBoxLayout, QWidget

"""
TODO:
- add loops to templates
- Add one picture of the vzs video file to report.
- Improve handling of SQUEEZEd data
- matplolib-3d

# cif core dictionary to python dictionary:
c = CifContainer(Path('cif_core_dict.cif'))
cdic = json.loads(c.as_json())
[cdic[x]['_name'] for x in cdic.keys() if '_name' in cdic[x]]

as dict:
{str(cdic[x]['_name']): ' '.join(cdic[x]['_definition'].split()) for x in cdic.keys() if '_name' in cdic[x]}
"""
# They must be here in order to have directly updated ui files from the ui compiler:
from gui.finalcif_gui import Ui_FinalCifWindow
from gui.responseformseditor import Ui_ResponseFormsEditor
from gui.custom_classes import MyComboBox, MyEQTableWidget, MyQPlainTextEdit, \
    MyTableWidgetItem, blue, light_green, yellow, COL_CIF, COL_DATA, COL_EDIT


class AppWindow(QMainWindow):
    cif: CifContainer

    def __init__(self):
        super().__init__()
        self.sources = None
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        # To make file drag&drop working:
        self.setAcceptDrops(True)
        self.show()
        self.statusBar().showMessage('FinalCif version {}'.format(VERSION))
        self.settings = FinalCifSettings(self)
        self.settings.load_window_position()
        self.store_predefined_templates()
        self.show_equipment_and_properties()
        self.ui.cif_main_table.installEventFilter(self)
        # distribute cif_main_table Columns evenly:
        hheader = self.ui.cif_main_table.horizontalHeader()
        hheader.setSectionResizeMode(COL_CIF, QHeaderView.Stretch)
        hheader.setSectionResizeMode(COL_DATA, QHeaderView.Stretch)
        hheader.setSectionResizeMode(COL_EDIT, QHeaderView.Stretch)
        hheader.setAlternatingRowColors(True)
        self.ui.cif_main_table.verticalHeader().setAlternatingRowColors(True)
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
        self.ui.DetailsPushButton.setDisabled(True)
        self.ui.SourcesPushButton.setDisabled(True)
        # noinspection PyTypeChecker
        self.cif = None
        self.view = None
        self.final_cif_file_name = Path()
        self.missing_data = []
        # True if line with "these are already in" reached:
        self.complete_data_row = -1
        self.connect_signals_and_slots()
        self.manufacturer = 'bruker'
        self.rigakucif: RigakuData

        self.ui.CheckcifButton.setIcon(qta.icon('mdi.file-document-box-outline'))
        self.ui.CheckcifOnlineButton.setIcon(qta.icon('mdi.file-document-box-check'))
        self.ui.CheckcifPDFOnlineButton.setIcon(qta.icon('mdi.file-document-box-check-outline'))
        self.ui.SaveFullReportButton.setIcon(qta.icon('mdi.file-table-outline'))
        self.ui.ExploreDirButton.setIcon(qta.icon('fa5.folder-open'))
        self.ui.SaveCifButton.setIcon(qta.icon('fa5.save'))
        options = [{'color': 'darkgreen'}]
        self.ui.SelectCif_PushButton.setIcon(qta.icon('fa5.file-alt', options=options))
        #self.ui.SelectCif_PushButton.setIcon(qta.icon('fa5s.spinner', color='red',
        #             animation=qta.Spin(self.ui.SelectCif_PushButton)))
        self.ui.SourcesPushButton.setIcon(qta.icon('fa5s.tasks'))
        self.ui.DetailsPushButton.setIcon(qta.icon('fa5s.crow'))

        self.ui.NewEquipmentTemplateButton.setIcon(qta.icon('mdi.playlist-plus'))
        self.ui.EditEquipmentTemplateButton.setIcon(qta.icon('mdi.playlist-edit'))
        self.ui.DeleteEquipmentButton.setIcon(qta.icon('mdi.playlist-minus'))
        self.ui.ImportEquipmentTemplateButton.setIcon(qta.icon('mdi.import'))
        self.ui.SaveEquipmentButton.setIcon(qta.icon('mdi.content-save-outline'))
        self.ui.CancelEquipmentButton.setIcon(qta.icon('mdi.cancel'))
        self.ui.ExportEquipmentButton.setIcon(qta.icon('mdi.export'))

        self.ui.NewPropertyTemplateButton.setIcon(qta.icon('mdi.playlist-plus'))
        self.ui.EditPropertyTemplateButton.setIcon(qta.icon('mdi.playlist-edit'))
        self.ui.ImportPropertyTemplateButton.setIcon(qta.icon('mdi.import'))
        self.ui.DeletePropertiesButton.setIcon(qta.icon('mdi.playlist-minus'))
        self.ui.SavePropertiesButton.setIcon(qta.icon('mdi.content-save-outline'))
        self.ui.CancelPropertiesButton.setIcon(qta.icon('mdi.cancel'))
        self.ui.ExportPropertyButton.setIcon(qta.icon('mdi.export'))

        self.ui.BackPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackpushButtonDetails.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackFromPlatonPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))

        self.ui.CCDCpushButton.setIcon(qta.icon('fa5s.upload'))
        self.ui.CODpushButton.setIcon(qta.icon('mdi.upload'))

        if len(sys.argv) > 1:
            self.load_cif_file(sys.argv[1])
        # Sorting desyncronizes header and columns:
        self.ui.cif_main_table.setSortingEnabled(False)
        self.load_recent_cifs_list()
        self.netman = QNetworkAccessManager()
        self.netman.finished.connect(self.show_update_warning)
        self.netman_checkdef = QNetworkAccessManager()
        self.checkdef = []
        self.netman_checkdef.finished.connect(self._save_checkdef)
        self.checkfor_version()
        self.get_checkdef()
        self.subwin = Ui_ResponseFormsEditor()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super(AppWindow, self).resizeEvent(a0)
        with suppress(AttributeError):
            self.view.reload()
        with suppress(AttributeError):
            self._savesize()

    def moveEvent(self, a0: QMoveEvent) -> None:
        super(AppWindow, self).moveEvent(a0)
        with suppress(AttributeError):
            self._savesize()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            with suppress(AttributeError):
                self._savesize()

    def _savesize(self):
        # print('saving position')
        x, y = self.pos().x(), self.pos().y()
        self.settings.save_window_position(QPoint(x, y), self.size(), self.isMaximized())

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
        self.ui.BackFromPlatonPushButton.clicked.connect(self.back_to_main_noload)
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
        self.ui.EquipmentEditTableWidget.cellPressed.connect(self.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemSelectionChanged.connect(
            self.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.ui.EquipmentEditTableWidget.itemEntered.connect(self.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.ui.EquipmentEditTableWidget.cellChanged.connect(self.ui.EquipmentEditTableWidget.add_row_if_needed)
        self.ui.EquipmentEditTableWidget.currentItemChanged.connect(self.ui.EquipmentEditTableWidget.add_row_if_needed)
        ##
        self.ui.PropertiesEditTableWidget.itemSelectionChanged.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.cellPressed.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemEntered.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.cellChanged.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.currentItemChanged.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemActivated.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemPressed.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemClicked.connect(self.add_property_row_if_needed)
        self.ui.PropertiesEditTableWidget.itemChanged.connect(self.add_property_row_if_needed)
        #
        self.ui.ImportPropertyTemplateButton.clicked.connect(self.import_property_from_file)
        self.ui.ExportPropertyButton.clicked.connect(self.export_property_template)
        ##
        self.ui.NewEquipmentTemplateButton.clicked.connect(self.new_equipment)
        self.ui.NewPropertyTemplateButton.clicked.connect(self.new_property)
        ##
        self.ui.EquipmentTemplatesListWidget.currentRowChanged.connect(self.load_selected_equipment)
        self.ui.EquipmentTemplatesListWidget.clicked.connect(self.load_selected_equipment)
        ##
        self.ui.SaveFullReportButton.clicked.connect(self.make_table)
        self.ui.RecentComboBox.currentIndexChanged.connect(self.load_recent_file)
        #
        self.ui.cif_main_table.row_deleted.connect(self._deleted_row)
        #
        self.ui.CODpushButton.clicked.connect(
            (lambda: QDesktopServices.openUrl(QUrl('http://www.crystallography.net/cod/'))))
        self.ui.CCDCpushButton.clicked.connect(self._ccdc_deposit)
        #
        save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.save_current_cif_file)
        save_shortcut = QShortcut(QKeySequence('Ctrl+H'), self)
        save_shortcut.activated.connect(self.do_html_checkcif)
        save_shortcut = QShortcut(QKeySequence('Ctrl+P'), self)
        save_shortcut.activated.connect(self.do_pdf_checkcif)
        #
        self.ui.DetailsPushButton.clicked.connect(self.show_properties)
        self.ui.BackpushButtonDetails.clicked.connect(self.back_to_main_noload)
        self.ui.growCheckBox.toggled.connect(self.redraw_molecule)
        #
        self.ui.SourcesPushButton.clicked.connect(self.show_sources)
        self.ui.BackSourcesPushButton.clicked.connect(self.back_to_main_noload)

    def _ccdc_deposit(self):
        """
        Open the CCDC deposit web page.
        """
        QDesktopServices.openUrl(QUrl('https://www.ccdc.cam.ac.uk/deposit'))
        self.explore_dir()

    def _deleted_row(self, key: str):
        """
        Deletes a row of the main table and reloads the cif file.
        """
        if self.cif.block.find_pair(key):
            print('found')
            self.cif.block.find([key]).erase()
            self.save_current_cif_file()
            self.load_cif_file(self.final_cif_file_name)

    def checkfor_version(self):
        mainurl = "https://xs3-data.uni-freiburg.de/finalcif/"
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

    def erase_disabled_items(self):
        table = self.ui.SourcesTableWidget
        for row in range(table.rowCount()):
            if not table.cellWidget(row, 0).isChecked():
                cifkey = table.item(row, 1).data(2)
                try:
                    row_num = self.ui.cif_main_table.vheaderitems.index(cifkey)
                except ValueError:
                    continue
                self.cif.block.set_pair(cifkey, '?')
                self.ui.cif_main_table.item(row_num, COL_CIF).setText('?')
                self.ui.cif_main_table.item(row_num, COL_DATA).setText('')

    def show_sources(self):
        COL_key = 1
        COL_source_data = 2
        if not self.sources:
            return
        table = self.ui.SourcesTableWidget
        table.setRowCount(0)
        for num, s in enumerate(self.sources):
            if not self.sources[s]:
                continue
            # if not self.source[s][0]:
            #    continue
            table.insertRow(num)
            box = QCheckBox()
            box.clicked.connect(self.erase_disabled_items)
            table.setCellWidget(num, 0, box)
            box.setChecked(True)
            box.setStyleSheet("margin-left:10%; margin-right:0%;")
            source_item = MyTableWidgetItem(s)
            source_item.setUneditable()
            data_item = MyTableWidgetItem(self.sources[s][1])
            data_item.setUneditable()
            table.setItem(num, COL_key, source_item)
            table.setItem(num, COL_source_data, data_item)
        table.resizeColumnToContents(0)
        table.resizeColumnToContents(1)
        table.resizeColumnToContents(2)
        self.ui.MainStackedWidget.setCurrentIndex(4)

    def get_checkdef(self):
        """
        Sends a get request to the platon server in order to get the current check.def file.
        """
        url = QUrl('https://www.platonsoft.nl/spek/xraysoft/unix/platon/check.def')
        req = QNetworkRequest(url)
        self.netman_checkdef.get(req)

    def _save_checkdef(self, reply: QNetworkReply) -> None:
        """
        Is called by the finished signal from the network manager.
        """
        txt = bytes(reply.readAll()).decode('ascii', 'ignore')
        self.checkdef = txt.splitlines(keepends=False)

    def get_checkdef_help(self, alert: str) -> str:
        """
        Parses check.def from PLATON in order to get help about an Alert from Checkcif.

        :param alert: alert number of the respective checkcif alert as three digit string or 'PLAT' + three digits
        """
        found = False
        helptext = []
        if len(alert) > 4:
            alert = alert[4:]
        for line in self.checkdef:
            if line.startswith('_' + alert):
                found = True
                continue
            if found and line.startswith('#==='):
                return '\n'.join(helptext[2:])
            if found:
                helptext.append(line)
        return ''

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

    def dragEnterEvent(self, e: QEvent):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QEvent):
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
        Get back to the main table and load the new cif file.
        """
        self.load_cif_file(str(self.final_cif_file_name.absolute()))
        self.ui.MainStackedWidget.setCurrentIndex(0)

    def back_to_main_noload(self):
        """
        Get back to the main table. Without loading a new cif file.
        """
        self.ui.MainStackedWidget.setCurrentIndex(0)
        if self.view:
            self.ui.moleculeLayout.removeWidget(self.view)

    def show_splash(self, text: str):
        splash = QSplashScreen()
        splashFont = QFont()
        # splashFont.setFamily("Arial")
        splashFont.setBold(True)
        splashFont.setPixelSize(16)
        splashFont.setStretch(120)
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
        splash = QSplashScreen()
        splash.show()
        splash.setStyleSheet("background-color:#fcc77c;")
        splash.setFont(splashFont)
        splash.setMinimumWidth(400)
        splash.setMaximumHeight(100)
        splash.showMessage(text, alignment=Qt.AlignCenter, )
        return splash

    def do_html_checkcif(self):
        """
        Performs an online checkcif via checkcif.iucr.org.
        """
        splash = self.show_splash("Running Checkcif. Please wait...")
        self.ui.statusBar.showMessage('Sending html report request...')
        self.save_current_cif_file()
        self.load_cif_file(self.final_cif_file_name)
        htmlfile = Path(strip_finalcif_of_name('checkcif-' + self.cif.fileobj.stem) + '-finalcif.html')
        try:
            htmlfile.unlink()
        except FileNotFoundError:
            pass
        try:
            ckf = MakeCheckCif(cif=self.cif, outfile=htmlfile, hkl=(not self.ui.structfactCheckBox.isChecked()))
            ckf._get_checkcif(pdf=False)
        except ReadTimeout:
            splash.finish(self)
            self.show_general_warning(r"The check took too long. Try it at"
                                      r" <a href='https://checkcif.iucr.org/'>https://checkcif.iucr.org/</a> directly.")
        except Exception as e:
            print('Can not do checkcif::')
            if DEBUG:
                raise
            print(e)
            return
        try:
            parser = MyHTMLParser(htmlfile.read_text())
        except FileNotFoundError:
            # happens if checkcif fails, e.g. takes too much time.
            return
        browser = QWebEngineView()
        # web_settings = browser. settings()
        url = QUrl.fromLocalFile(str(htmlfile.absolute()))
        dialog = QMainWindow(self)
        self.subwin.setupUi(dialog)
        self.subwin.reportLayout.addWidget(browser)
        self.subwin.show_report_Button.hide()
        self.subwin.show_report_Button.clicked.connect(self._switch_to_report)
        self.subwin.show_Forms_Button.clicked.connect(self._switch_to_vrf)
        self.subwin.SavePushButton.setIcon(qta.icon('mdi.content-save'))
        self.subwin.show_report_Button.setIcon(qta.icon('mdi.format-columns'))
        self.subwin.show_Forms_Button.setIcon(qta.icon('mdi.book-open-outline'))
        browser.load(url)
        self.subwin.stackedWidget.setCurrentIndex(0)
        dialog.setMinimumWidth(900)
        dialog.setMinimumHeight(700)
        dialog.move(QPoint(100, 50))
        dialog.show()
        # The picture file linked in the html file:
        imageobj = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.gif')
        gif = parser.get_image()
        self.ui.statusBar.showMessage('Report finished.')
        splash.finish(self)
        forms = parser.response_forms
        # makes all gray:
        # self.subwin.responseFormsListWidget.setStyleSheet("background: 'gray';")
        a = AlertHelp(self.checkdef)
        self.vrfs = []
        for form in forms:
            # print(form)
            vrf = MyVRFContainer(form, a.get_help(form['alert_num']))
            vrf.setAutoFillBackground(False)
            self.vrfs.append(vrf)
            item = QListWidgetItem()
            item.setSizeHint(vrf.sizeHint())
            self.subwin.responseFormsListWidget.addItem(item)
            self.subwin.responseFormsListWidget.setItemWidget(item, vrf)
        if not forms:
            iteme = QListWidgetItem(' ')
            item = QListWidgetItem(' No level A or B alerts to explain.')
            self.subwin.responseFormsListWidget.addItem(iteme)
            self.subwin.responseFormsListWidget.addItem(item)
        dialog.show()
        self.subwin.SavePushButton.clicked.connect(self.save_responses)
        if gif:
            imageobj.write_bytes(gif)

    def save_responses(self):
        """
        Saves the validation response form text to _vrf_ CIF entries.
        :return: None
        """
        n = 0
        for response_row in range(self.subwin.responseFormsListWidget.count()):
            txt = self.vrfs[response_row].response_text_edit.toPlainText()
            if not txt:
                # No response was written
                continue
            n += 1
            v = VREF()
            v.key = self.vrfs[response_row].form['name']
            v.problem = self.vrfs[response_row].form['problem']
            v.response = txt
            # add a key with '?' as value
            self.add_new_table_key(v.key, v.value)
            # add data to this key:
            self.ui.cif_main_table.setText(v.key, COL_EDIT, v.value)
        self.save_cif_and_display()
        if n:
            self.subwin.statusBar.showMessage('Forms saved')
        else:
            self.subwin.statusBar.showMessage('No forms were filled in.')

    def _switch_to_report(self):
        self.subwin.show_Forms_Button.show()
        self.subwin.show_report_Button.hide()
        self.subwin.stackedWidget.setCurrentIndex(0)

    def _switch_to_vrf(self):
        self.subwin.show_Forms_Button.hide()
        self.subwin.show_report_Button.show()
        self.subwin.stackedWidget.setCurrentIndex(1)

    def do_pdf_checkcif(self):
        """
        Performs an online checkcif and shows the result as pdf.
        """
        splash = self.show_splash("Running Checkcif. Please wait...")
        self.ui.statusBar.showMessage('Sending pdf report request...')
        self.save_current_cif_file()
        self.load_cif_file(self.final_cif_file_name)
        htmlfile = Path('checkpdf-' + self.cif.fileobj.stem + '.html')
        try:
            htmlfile.unlink()
        except FileNotFoundError:
            pass
        try:
            ckf = MakeCheckCif(cif=self.cif, outfile=htmlfile, hkl=(not self.ui.structfactCheckBox.isChecked()))
            ckf.show_pdf_report()
        except ReadTimeout:
            splash.finish(self)
            self.show_general_warning(r"The check took too long. Try it at"
                                      r" <a href='https://checkcif.iucr.org/'>https://checkcif.iucr.org/</a> directly.")
            return
        except Exception as e:
            print('Can not do checkcif:')
            if DEBUG:
                raise
            print(e)
        self.ui.statusBar.showMessage('Report finished.')
        try:
            htmlfile.unlink()
        except FileNotFoundError:
            pass
        splash.finish(self)

    def do_offline_checkcif(self):
        """
        Performs a checkcif with platon and displays it in the text editor of the MainStackedWidget.
        """
        splash = self.show_splash("Running Checkcif locally. Please wait...")
        # makes sure also the currently edited item is saved:
        self.ui.cif_main_table.setCurrentItem(None)
        self.ui.CheckcifPlaintextEdit.clear()
        self.save_current_cif_file()
        self.load_cif_file(self.final_cif_file_name)
        self.ui.MainStackedWidget.setCurrentIndex(1)
        try:
            p = Platon(self.final_cif_file_name)
        except Exception as e:
            print(e)
            # self.ui.CheckcifButton.setDisabled(True)
            return
        ccpe = self.ui.CheckcifPlaintextEdit
        ccpe.setPlainText('Platon output: \nThis might not be the same as the IUCr Checkcif!')
        p.run_platon()
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
        p.parse_chk_file()
        if p.chk_file_text:
            try:
                ccpe.appendPlainText(p.chk_file_text)
                ccpe.appendPlainText('\n' + '#' * 27 + ' Validation Response Forms ' + '#' * 26 + '\n')
                ccpe.appendPlainText(p.vrf_txt)
            except AttributeError:
                pass
        ccpe.verticalScrollBar().setValue(0)
        splash.finish(self)
        moiety = self.ui.cif_main_table.getTextFromKey(key='_chemical_formula_moiety', col=0)
        if p.formula_moiety and moiety in ['', '?']:
            self.ui.MainStackedWidget.setCurrentIndex(0)
            self.ui.cif_main_table.setText(key='_chemical_formula_moiety', txt=p.formula_moiety, column=COL_EDIT)
        self.ui.MainStackedWidget.setCurrentIndex(1)

    def load_recent_file(self, file_index: int) -> None:
        combo = self.ui.RecentComboBox
        if file_index > 0:
            txt = combo.itemText(file_index)
            self.load_cif_file(txt)

    def make_table(self) -> None:
        """
        Runs the multitable program to make a report table.
        """
        not_ok = None
        if self.cif:
            self.save_current_cif_file()
            self.load_cif_file(self.final_cif_file_name)
            report_filename = strip_finalcif_of_name('report_{}'.format(self.cif.fileobj.stem)) + '-finalcif.docx'
            try:
                make_report_from(self.final_cif_file_name, output_filename=report_filename, path=application_path,
                                 without_H=self.ui.HAtomsCheckBox.isChecked())
            except FileNotFoundError as e:
                if DEBUG:
                    raise
                print('Unable to make report from cif file.')
                not_ok = e
                self.unable_to_open_message(self.cif.fileobj, not_ok)
                return
            except PermissionError:
                if DEBUG:
                    raise
                print('Unable to open cif file')
                self.show_general_warning('The report document {} could not be opened.\n'
                                          'Is the file already opened?'.format(report_filename))
                return
            if Path(report_filename).absolute().exists():
                if os.name == 'nt':
                    os.startfile(Path(report_filename).absolute())
                if sys.platform == 'darwin':
                    subprocess.call(['open', Path(report_filename).absolute()])
            zipfile = Path(strip_finalcif_of_name(self.cif.fileobj.stem) + '-finalcif.zip')
            if zipfile.exists():
                zipfile = next_path(zipfile.stem + '-%s.zip')
            with suppress(Exception):
                arc = ArchiveReport(zipfile)
            with suppress(Exception):
                arc.zip.write(report_filename)
            with suppress(Exception):
                arc.zip.write(self.final_cif_file_name)
            with suppress(Exception):
                pdfname = Path(strip_finalcif_of_name('checkcif-' + self.cif.fileobj.stem) + '-finalcif.pdf').name
                arc.zip.write(pdfname)

    def save_current_recent_files_list(self, file: Path) -> None:
        if os.name == 'nt':
            file = WindowsPath(file.absolute()).absolute()
        else:
            file = Path(file.absolute()).absolute()
        recent = list(self.settings.settings.value('recent_files', type=list))
        while str(file) in recent:
            recent.remove(str(file))
        # file has to be str not Path():
        recent.insert(0, str(file))
        recent = recent[:8]
        self.settings.settings.setValue('recent_files', recent)
        # print(recent, 'save')

    def load_recent_cifs_list(self) -> None:
        self.ui.RecentComboBox.clear()
        recent = list(self.settings.settings.value('recent_files', type=list))
        self.ui.RecentComboBox.addItem('Recent Files')
        for n, file in enumerate(recent):
            if not isinstance(file, str):
                del recent[n]
            try:
                if not Path(file).exists():
                    del recent[n]
                    continue
            except OSError as e:
                print(e)
                pass
            self.ui.RecentComboBox.addItem(file, n)

    def save_cif_and_display(self) -> None:
        saved = self.save_current_cif_file()
        if saved:
            self.display_cif_text()

    def save_current_cif_file(self) -> bool:
        """
        Saves the current cif file and stores the information of the third column.
        """
        # restore header, otherwise item is not saved:
        table = self.ui.cif_main_table
        table.restore_vertical_header()
        table.setCurrentItem(None)  # makes sure also the currently edited item is saved
        for row in range(self.ui.cif_main_table.rows_count):
            # col0 = None  # cif content
            col1 = None  # from datafiles
            col2 = None  # own text
            for col in range(self.ui.cif_main_table.columns_count):
                txt = table.text(row, col)
                if txt:
                    # if col == COL_CIF and txt != (None or '' or '?'):
                    #    col0 = txt
                    # removed: not col0 and
                    if col == COL_DATA and txt != (None or '' or '?'):
                        col1 = txt
                    try:
                        if col == COL_EDIT and txt != (None or ''):
                            col2 = txt
                    except AttributeError as e:
                        # print(e)
                        pass
                if col == COL_EDIT:
                    vhead = self.ui.cif_main_table.vheader_text(row)
                    # vertical header item is surely not a cif keyword:
                    if not vhead.startswith('_'):
                        continue
                    # This is my row information
                    # print('col2:', vhead, col0, col1, col2, '#')
                    if col1 and not col2:
                        set_pair_delimited(self.cif.block, vhead, col1)
                    if col2:
                        try:
                            set_pair_delimited(self.cif.block, vhead, col2)
                        except RuntimeError as e:
                            print('Can not take cif info from table:', e)
                            pass
        try:
            self.final_cif_file_name = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.cif')
            self.cif.save(self.final_cif_file_name.name)
            self.ui.statusBar.showMessage('  File Saved:  {}'.format(self.final_cif_file_name.name), 10000)
            print('File saved ...')
            return True
        except Exception as e:
            print('Unable to save file:')
            print(e)
            self.show_general_warning('Can not save file: ' + str(e))
            return False

    def display_cif_text(self) -> None:
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
        final_textedit.setPlainText(self.final_cif_file_name.read_text(encoding='utf-8', errors='ignore'))

    def show_equipment_and_properties(self) -> None:
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

    def load_selected_equipment(self) -> None:
        """
        Loads equipment data to be shown in the main Cif table.
        Not for template edititng!
        """
        listwidget = self.ui.EquipmentTemplatesListWidget
        selected_row_text = listwidget.currentIndex().data()
        if not selected_row_text:
            return None
        equipment = self.settings.load_equipment_template_as_dict(selected_row_text)
        if self.ui.cif_main_table.vheaderitems:
            for key in equipment:
                if key not in self.ui.cif_main_table.vheaderitems:
                    self.add_new_table_key(key, equipment[key])
                # add missing item to data sources column:
                self.ui.cif_main_table.setText(key, COL_DATA, equipment[key])
                self.ui.cif_main_table.setBackground(key, COL_DATA, light_green)
                self.ui.cif_main_table.setText(key, COL_EDIT, equipment[key])

    def add_new_table_key(self, key: str, value: str = '?') -> None:
        """
        Adds a new row with a respective vheaderitem to the main cif table.
        Also the currently opened cif file is updated.
        """
        # Make sure new (unknown) cif items get to the start of the cif:
        if key not in self.cif.order:
            self.cif.order.insert(0, key)
        if not key.startswith('_'):
            return
        self.ui.cif_main_table.vheaderitems.insert(0, key)
        self.add_row(key=key, value=value, at_start=True)
        if key in [x for x in combobox_fields]:
            self.add_property_combobox(combobox_fields[key], 0)
        self.missing_data.append(key)
        if not self.cif.block.find_value(key):
            self.cif.add_to_cif(key, value)

    def new_property(self) -> None:
        item = QListWidgetItem('')
        self.ui.PropertiesTemplatesListWidget.addItem(item)
        self.ui.PropertiesTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.PropertiesTemplatesListWidget.editItem(item)
        self.ui.cifKeywordLineEdit.clear()

    def add_property_row_if_needed(self) -> None:
        """
        Adds an empty row at the bottom of either the EquipmentEditTableWidget, or the PropertiesEditTableWidget.
        """
        table = self.ui.PropertiesEditTableWidget
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

    # The equipment templates:

    def new_equipment(self) -> None:
        item = QListWidgetItem('')
        self.ui.EquipmentTemplatesListWidget.addItem(item)
        self.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        item.setFlags(Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.ui.EquipmentTemplatesListWidget.editItem(item)

    def delete_equipment(self) -> None:
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

    def edit_equipment_template(self) -> None:
        it = self.ui.EquipmentTemplatesListWidget.currentItem()
        self.ui.EquipmentTemplatesListWidget.setCurrentItem(None)
        self.ui.EquipmentTemplatesListWidget.setCurrentItem(it)
        self.ui.CancelPropertiesButton.click()
        table = self.ui.EquipmentEditTableWidget
        stackedwidget = self.ui.EquipmentTemplatesStackedWidget
        listwidget = self.ui.EquipmentTemplatesListWidget
        self.load_equipment_to_edit(table, stackedwidget, listwidget)

    def load_equipment_to_edit(self, table: MyEQTableWidget, stackedwidget: QStackedWidget,
                               listwidget: QListWidget) -> None:
        """
        Load/Edit the key/value list of an equipment entry.
        """
        table.blockSignals(True)
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            return
        selected_row_text = listwidget.currentIndex().data()
        table_data = self.settings.load_template('equipment/' + selected_row_text)
        # first load the previous values:
        if table_data:
            for key, value in table_data:
                if not key or not value:
                    continue
                table.add_equipment_row(key, retranslate_delimiter(value))
        else:
            # new empty equipment:
            for _ in range(8):
                table.add_equipment_row('', '')
        table.add_equipment_row('', '')
        table.add_equipment_row('', '')
        stackedwidget.setCurrentIndex(1)
        table.resizeRowsToContents()
        table.blockSignals(False)

    def save_equipment_template(self) -> None:
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

    def import_equipment_from_file(self) -> None:
        """
        Import an equipment entry from a cif file.
        """
        import gemmi
        filename = self.cif_file_open_dialog(filter="CIF file (*.cif *.cif_od)")
        if not filename:
            return
        try:
            doc = cif.read_file(filename)
        except RuntimeError as e:
            self.show_general_warning(str(e))
            return
        block = doc.sole_block()
        table_data = []
        for item in block:
            if item.pair is not None:
                key, value = item.pair
                if key in excluded_imports:
                    continue
                table_data.append([key, retranslate_delimiter(gemmi.cif.as_string(value)).strip('\n\r ')])
        if filename.endswith('.cif_od'):
            name = Path(filename).stem
        else:
            name = block.name.replace('__', ' ')
        self.settings.save_template('equipment/' + name, table_data)
        self.settings.append_to_equipment_list(name)
        self.show_equipment_and_properties()

    def get_loop(self, item) -> None:
        """
        TODO: use this to load loops from machine cifs
        """
        # for item in block:
        if item.loop is not None:
            n = 0
            while True:
                try:
                    row = [item.loop.val(n, x) for x in range(len(item.loop.tags))]
                    if not row[0]:
                        break
                    n += 1
                except Exception:
                    break
        #####
        """
        # get columns:
        for item in block:
            if item.loop is not None:
                for tag in item.loop.tags:
                    val = block.find_values(tag)
                    print([str(x) for x in val])
        
        # get rows:
        for item in block:
            if item.loop is not None:
                tags = item.loop.tags
                table = block.find(tags)
                print('table columns, rows:', table.width(), len(table))
                row = [x for x in table]
                for r in row:
                    print([x for x in r])
        """

    def get_equipment_entry_data(self) -> Tuple[str, list]:
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
                key = table.text(rownum, 0)
                value = table.text(rownum, 1).strip('\n\r ')
            except AttributeError:
                value = ''
            if key and value:
                table_data.append([key, value])
        return selected_template_text, table_data

    def export_equipment_template(self, filename: str = None) -> None:
        """
        Exports the currently selected equipment entry to a file.

        I order to export, we have to run self.edit_equipment_template() first!
        """
        selected_template, table_data = self.get_equipment_entry_data()
        if not selected_template:
            return
        doc = cif.Document()
        blockname = '__'.join(selected_template.split())
        block = doc.add_new_block(blockname)
        for key, value in table_data:
            set_pair_delimited(block, key, value.strip('\n\r '))
        if not filename:
            filename = self.cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=cif.Style.Indent35)
            # Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            self.show_general_warning('No permission to write file to {}'.format(Path(filename).absolute()))

    def cancel_equipment_template(self) -> None:
        """
        Cancel Equipment editing.
        """
        table = self.ui.EquipmentEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        print('cancelled equipment')

    # The properties templates:

    def delete_property(self) -> None:
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

    def edit_property_template(self) -> None:
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
        # table.resizeRowsToContents()

    def save_property_template(self) -> None:
        table = self.ui.PropertiesEditTableWidget
        stackedwidget = self.ui.PropertiesTemplatesStackedWidget
        listwidget = self.ui.PropertiesTemplatesListWidget
        keyword = self.ui.cifKeywordLineEdit.text()
        self.save_property(table, stackedwidget, listwidget, keyword)

    def store_predefined_templates(self) -> None:
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

    def export_property_template(self) -> None:
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
            with suppress(Exception):
                table_data = prop_data[1]
        if not cif_key:
            return
        doc = cif.Document()
        blockname = '__'.join(selected_row_text.split())
        block = doc.add_new_block(blockname)
        try:
            loop = block.init_loop(cif_key, [''])
        except RuntimeError:
            # Not a valid loop key
            self.show_general_warning('"{}" is not a valid cif keyword.'.format(cif_key))
            return
        for value in table_data:
            if value:
                loop.add_row([cif.quote(utf8_to_str(value))])
        filename = self.cif_file_save_dialog(blockname.replace('__', '_') + '.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=cif.Style.Indent35)
            # Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            self.show_general_warning('No permission to write file to {}'.format(Path(filename).absolute()))

    def import_property_from_file(self) -> None:
        """
        Imports a cif file as entry of the property list.
        """
        filename = self.cif_file_open_dialog(filter="CIF file (*.cif *.cif_od)")
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
        template_list = []
        loop_column_name = ''
        for i in block:
            if i.loop is not None:
                if len(i.loop.tags) > 0:
                    loop_column_name = i.loop.tags[0]
                for n in range(i.loop.length()):
                    value = i.loop.val(n, 0)
                    template_list.append(retranslate_delimiter(value.strip(" '")))
        block_name = block.name.replace('__', ' ')
        # This is the list shown in the Main menu:
        property_list.append(block_name)
        table = self.ui.PropertiesEditTableWidget
        table.setRowCount(0)
        self.ui.cifKeywordLineEdit.setText(loop_column_name)
        newlist = [x for x in list(set(property_list)) if x]
        newlist.sort()
        # this list keeps track of the equipment items:
        self.settings.save_template('property_list', newlist)
        template_list.insert(0, '')
        template_list = list(set(template_list))
        # save as dictionary for properties to have "_cif_key : itemlist"
        # for a table item as dropdown menu in the main table.
        table_data = [loop_column_name, template_list]
        self.settings.save_template('property/' + block_name, table_data)
        self.show_equipment_and_properties()

    def load_property_from_settings(self, table: QTableWidget, stackedwidget: QStackedWidget,
                                    listwidget: QListWidget) -> None:
        """
        Load/Edit the value list of a property entry.
        """
        table.blockSignals(True)
        property_list = self.settings.settings.value('property_list')
        if not property_list:
            property_list = ['']
        table.clearContents()
        table.setRowCount(0)
        index = listwidget.currentIndex()
        if index.row() == -1:
            # nothing selected
            # self.ui.PropertiesEditTableWidget.blockSignals(False)
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
        if not table_data:
            table_data = ['', '', '']
        for value in table_data:
            try:
                self.add_propeties_row(table, retranslate_delimiter(str(value)))
            except TypeError:
                print('Bad value in property table')
                continue
        self.add_propeties_row(table, '')
        property_list.append(selected_row_text)
        newlist = [x for x in list(set(property_list)) if x]
        # this list keeps track of the equipment items:
        self.settings.save_template('property_list', newlist)
        stackedwidget.setCurrentIndex(1)
        table.blockSignals(False)
        # table.setWordWrap(False)
        table.resizeRowsToContents()

    @staticmethod
    def add_propeties_row(table: QTableWidget, value: str = '') -> None:
        """
        Add a new row with a value to the Property table.
        """
        # Create a empty row at bottom of table
        row_num = table.rowCount()
        table.insertRow(row_num)
        # Add cif key and value to the row:
        item_val = MyTableWidgetItem(value)
        table.setItem(row_num, 0, item_val)

    def save_property(self, table: QTableWidget,
                      stackwidget: QStackedWidget,
                      listwidget: QListWidget,
                      keyword: str = '') -> None:
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

    def cancel_property_template(self) -> None:
        """
        Cancel editing of the current template.
        """
        table = self.ui.PropertiesEditTableWidget
        table.clearContents()
        table.setRowCount(0)
        self.ui.PropertiesTemplatesStackedWidget.setCurrentIndex(0)
        print('canceled property')

    ##   end of properties

    @staticmethod
    def cif_file_open_dialog(filter: str = "CIF file (*.cif)") -> str:
        """
        Returns a cif file name from a file dialog.
        """
        filename, _ = QFileDialog.getOpenFileName(filter=filter,
                                                  initialFilter=filter,
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

    def load_cif_file(self, fname: str) -> None:
        """
        Opens the cif file and fills information into the main table.
        """
        with suppress(AttributeError):
            self.ui.moleculeLayout.removeWidget(self.view)
        self.ui.MainStackedWidget.setCurrentIndex(0)
        # clean table before loading:
        self.ui.cif_main_table.delete_content()
        if not fname:
            try:
                # loading last working directory:
                last = self.settings.load_last_workdir()
            except TypeError:
                last = ''
            if last and Path(last).exists():
                os.chdir(last)
            fname = self.cif_file_open_dialog()
        if not fname:
            return
        if os.name == 'nt':
            self.ui.SelectCif_LineEdit.setText(str(WindowsPath(fname).absolute()))
        else:
            self.ui.SelectCif_LineEdit.setText(str(fname))
        try:
            filepath = Path(fname)
            if not filepath.exists():
                self.show_general_warning("The file you tried to open does not exist!")
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
        if not self.cif.chars_ok:
            self.show_general_warning("You have non-ascii characters like umlauts in the SHELX file "
                                      "attached to this CIF.\n\n"
                                      "FinalCif tries to convert them, but be warned "
                                      "(they are not allowed in CIF1 files anyway).\n")
        try:
            # Change the current working Directory
            os.chdir(filepath.absolute().parent)
        except OSError:
            print("Can't change the Current Working Directory")
        try:
            rigaku = self.cif.fileobj.parent.glob('*.cif_od').__next__()
            if rigaku.exists():
                self.manufacturer = 'rigaku'
                self.rigakucif = RigakuData(rigaku)
        except StopIteration:
            pass
        # quick hack in order to support STOE:
        # TODO: Make this clean
        try:
            rigaku = self.cif.fileobj.parent.glob('*.cfx').__next__()
            if rigaku.exists():
                self.manufacturer = 'rigaku'
                self.rigakucif = RigakuData(rigaku)
        except StopIteration:
            pass
        # don't do this:
        # self.ui.cif_main_table.clear()
        try:
            self.fill_cif_table()
        except RuntimeError as e:
            not_ok = e
            if DEBUG:
                raise
            self.unable_to_open_message(filepath, not_ok)
        # Do this only when sure we can load the file:
        self.save_current_recent_files_list(filepath)
        self.load_recent_cifs_list()
        self.ui.CheckcifButton.setEnabled(True)
        self.ui.CheckcifOnlineButton.setEnabled(True)
        self.ui.CheckcifPDFOnlineButton.setEnabled(True)
        self.ui.SaveCifButton.setEnabled(True)
        self.ui.ExploreDirButton.setEnabled(True)
        if self.cif:
            curdir = str(self.cif.fileobj.absolute().parent)
            # saving current cif dir as last working directory:
            self.settings.save_current_dir(curdir)
            self.ui.DetailsPushButton.setEnabled(True)
            self.ui.SourcesPushButton.setEnabled(True)

    def show_properties(self):
        self.save_current_cif_file()
        try:
            self.cif.fileobj
        except AttributeError:
            return
        self.ui.MainStackedWidget.setCurrentIndex(3)
        self.ui.cellField.setText(celltxt.format(*self.cif.cell, self.cif['_space_group_centring_type']))
        try:
            spgr = self.cif.space_group()
        except RuntimeError:
            spgr = ''
        intnum = self.cif['_space_group_IT_number'] if self.cif['_space_group_IT_number'] else self.cif[
            '_symmetry_Int_Tables_number']
        if intnum:
            intnum = '({})'.format(intnum)
        self.ui.SpaceGroupLineEdit.setText("{} {}".format(spgr, intnum))

        self.ui.SumformLabel.setText(self.cif['_chemical_formula_sum'].strip(" '"))
        self.ui.zLineEdit.setText(self.cif['_cell_formula_units_Z'])
        self.ui.temperatureLineEdit.setText(self.cif['_diffrn_ambient_temperature'])
        self.ui.wR2LineEdit.setText(self.cif['_refine_ls_wR_factor_ref'])
        self.ui.r1LineEdit.setText(self.cif['_refine_ls_R_factor_gt'])
        self.ui.goofLineEdit.setText(self.cif['_refine_ls_goodness_of_fit_ref'])
        self.ui.maxShiftLineEdit.setText(self.cif['_refine_ls_shift/su_max'])
        self.ui.rintLineEdit.setText(self.cif['_diffrn_reflns_av_R_equivalents'])
        self.ui.rsigmaLineEdit.setText(
            self.cif['_diffrn_reflns_av_unetI/netI'] if self.cif['_diffrn_reflns_av_unetI/netI']
            else self.cif['_diffrn_reflns_av_sigmaI/netI'])
        self.ui.cCDCNumberLineEdit.setText(self.cif['_database_code_depnum_ccdc_archive'])
        self.ui.flackXLineEdit.setText(self.cif['_refine_ls_abs_structure_Flack'])
        try:
            dat_param = float(self.cif['_refine_ls_number_reflns']) / float(self.cif['_refine_ls_number_parameters'])
        except (ValueError, ZeroDivisionError, TypeError):
            dat_param = 0.0
        self.ui.dataReflnsLineEdit.setText("{:<5.1f}".format(dat_param))
        self.ui.numParametersLineEdit.setText(self.cif['_refine_ls_number_parameters'])
        wavelen = self.cif['_diffrn_radiation_wavelength']
        thetamax = self.cif['_diffrn_reflns_theta_max']
        # d = lambda/2sin(theta):
        try:
            d = float(wavelen) / (2 * sin(radians(float(thetamax))))
        except(ZeroDivisionError, TypeError, ValueError):
            d = 0.0
        self.ui.numRestraintsLineEdit.setText(self.cif['_refine_ls_number_restraints'])
        self.ui.thetaMaxLineEdit.setText(thetamax)
        self.ui.thetaFullLineEdit.setText(self.cif['_diffrn_reflns_theta_full'])
        self.ui.dLineEdit.setText("{:5.3f}".format(d))
        try:
            compl = float(self.cif['_diffrn_measured_fraction_theta_max']) * 100
            if not compl:
                compl = 0.0
        except (TypeError, ValueError):
            compl = 0.0
        try:
            self.ui.completeLineEdit.setText("{:<5.1f}".format(compl))
        except ValueError:
            pass
        self.ui.wavelengthLineEdit.setText("{}".format(wavelen))
        self.ui.reflTotalLineEdit.setText(self.cif['_diffrn_reflns_number'])
        self.ui.uniqReflLineEdit.setText(self.cif['_refine_ls_number_reflns'])
        self.ui.refl2sigmaLineEdit.setText(self.cif['_reflns_number_gt'])
        peak = self.cif['_refine_diff_density_max']
        if peak:
            self.ui.peakLineEdit.setText("{} / {}".format(peak, self.cif['_refine_diff_density_min']))
        try:
            self.init_webview()
        except Exception as e:
            print(e, '###')
        # because this is fast with small structures and slow with large:
        if len(self.cif.atomic_struct.sites) < 400:
            self.ui.growCheckBox.setChecked(True)
        else:
            self.view_molecule()

    def view_molecule(self):
        blist = []
        if self.ui.growCheckBox.isChecked():
            self.ui.molGroupBox.setTitle('Completed Molecule')
            # atoms = self.structures.get_atoms_table(structure_id, cartesian=False, as_list=True)
            atoms = list(self.cif.atoms_fract)
            if atoms:
                sdm = SDM(atoms, self.cif.symmops, self.cif.cell[:6])
                try:
                    needsymm = sdm.calc_sdm()
                    atoms = sdm.packer(sdm, needsymm)
                except IndexError:
                    atoms = []
        else:
            self.ui.molGroupBox.setTitle('Asymmetric Unit')
            atoms = self.cif.atoms_orth
            blist = []
        try:
            mol = ' '
            if atoms:
                mol = mol_file_writer.MolFile(atoms, blist)
                mol = mol.make_mol()
        except (TypeError, KeyError):
            print("Error while writing mol file.")
            mol = ' '
            if DEBUG:
                raise
        content = write_html.write(mol, self.ui.molGroupBox.width() - 250, self.ui.molGroupBox.height() - 250)
        Path(os.path.join(self.jsmoldir.name, "./jsmol.htm")).write_text(data=content, encoding="utf-8",
                                                                         errors='ignore')
        self.view.reload()

    def init_webview(self):
        """
        Initializes a QWebengine to view the molecule.
        """
        try:
            # Otherwise, the views accumulate:
            self.view.close()
            self.view = QWebEngineView()
        except AttributeError:
            self.view = QWebEngineView()
        self.jsmoldir = TemporaryDirectory()
        self.view.load(QUrl.fromLocalFile(os.path.join(self.jsmoldir.name, "./jsmol.htm")))
        # This is a bit hacky, but it works fast:
        copy2(os.path.join(str(Path(displaymol.__file__).parent), 'jquery.min.js'), self.jsmoldir.name)
        copy2(os.path.join(str(Path(displaymol.__file__).parent), 'JSmol_dk.nojq.lite.js'), self.jsmoldir.name)
        self.ui.moleculeLayout.addWidget(self.view)
        self.view.heightForWidth(1)
        self.view.loadFinished.connect(self.onWebviewLoadFinished)

    def onWebviewLoadFinished(self):
        self.view.show()

    def redraw_molecule(self):
        try:
            self.view_molecule()
        except Exception as e:
            print(e, ", unable to display molecule")
            if DEBUG:
                raise
            # self.write_empty_molfile()
            self.view.reload()

    @staticmethod
    def unable_to_open_message(filepath: Path, not_ok: Exception) -> None:
        """
        Shows a message if the current cif file can not be opened.
        """
        info = QMessageBox()
        info.setIcon(QMessageBox.Information)
        print('Output from gemmi:', not_ok)
        try:
            line = str(not_ok)[4:].split(':')[1]
        except IndexError:
            line = None
        if line:
            try:
                int(line)
                info.setText('This cif file is not readable!\n'
                             'Please check line {} in\n{}'.format(line, filepath.name))
            except ValueError:
                info.setText('This cif file is not readable! "{}"\n{}'.format(filepath.name, not_ok))
        else:
            info.setText('This cif file is not readable! "{}"\n{}'.format(filepath.name, not_ok))
        info.show()
        info.exec()
        return

    def test_checksums(self) -> None:
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

    def show_checksum_warning(self, res=True) -> None:
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

    def show_general_warning(self, warn_text: str = '') -> None:
        """
        A message box to display if the checksums do not agree.
        """
        if not warn_text:
            return
        box = QMessageBox(self)
        box.setTextFormat(Qt.AutoText)
        box.setWindowTitle(" ")
        box.setTextInteractionFlags(Qt.TextBrowserInteraction)
        box.setText(warn_text)
        box.exec()

    def check_Z(self) -> None:
        """
        Crude check if Z is much too high e.h. a SEHLXT solution with "C H N O" sum formula.
        """
        Z = to_float(self.cif['_cell_formula_units_Z'])
        density = to_float(self.cif['_exptl_crystal_density_diffrn'])
        csystem = self.cif.crystal_system
        bad = False
        ntypes = len(self.cif['_chemical_formula_sum'].split())
        # if all([ntypes, density]):
        #    if ntypes > 3.0 and density < 0.6 or density > 4.0:
        #        bad = True
        if Z and Z > 20.0 and (csystem == 'tricilinic' or csystem == 'monoclinic'):
            bad = True
        if Z and Z > 32.0 and (csystem == 'orthorhombic' or csystem == 'tetragonal' or csystem == 'trigonal'
                               or csystem == 'hexagonal' or csystem == 'cubic'):
            bad = True
        if bad:
            zinfo = QMessageBox()
            zinfo.setIcon(QMessageBox.Information)
            zinfo.setText('The number of formula units Z={:.0f} is probably wrong.'
                          '\nYou may restart refinement with a correct value.'.format(Z))
            zinfo.show()
            zinfo.exec()

    def set_pair(self, key: str, value: str) -> None:
        """
        Start a new cif key/data pair and add it to the main table.
        """
        self.missing_data.append(key)
        self.cif.block.set_pair(key, value)
        self.ui.cif_main_table.insertRow(0)
        tab_cif = MyTableWidgetItem('?')
        tab_cif.setUneditable()
        tab_data = MyTableWidgetItem(value)
        tab_data.setUneditable()
        self.ui.cif_main_table.vheaderitems.insert(0, key)
        head_item_key = MyTableWidgetItem(key)
        self.ui.cif_main_table.setItem(0, COL_DATA, tab_data)
        self.ui.cif_main_table.setItem(0, COL_CIF, tab_cif)
        self.ui.cif_main_table.setVerticalHeaderItem(0, head_item_key)
        self.ui.cif_main_table.setBackground(key, COL_DATA, light_green)

    def get_data_sources(self) -> None:
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.
        """
        self.check_Z()
        if self.manufacturer == 'bruker':
            self.sources = BrukerData(self, self.cif).sources
        if self.manufacturer == 'rigaku':
            self.sources = self.rigakucif.sources
        vheadlist = []
        for num in range(self.ui.cif_main_table.model().rowCount()):
            vheadlist.append(self.ui.cif_main_table.model().headerData(num, Qt.Vertical))
        for src in self.sources:
            if not self.sources[src]:
                continue
            if src in vheadlist:
                continue
            if src and src not in self.missing_data:
                self.set_pair(src, '?')
        # Build a dictionary of cif keys and row number values in order to fill the first column
        # of cif_main_table with cif values:
        for num in range(self.ui.cif_main_table.model().rowCount()):
            vhead = self.ui.cif_main_table.model().headerData(num, Qt.Vertical)
            if not vhead in self.ui.cif_main_table.vheaderitems:
                self.ui.cif_main_table.vheaderitems.append(vhead)
                # adding comboboxes:
                if vhead in combobox_fields:
                    self.add_property_combobox(combobox_fields[vhead], num)
                elif vhead in self.settings.load_property_keys():
                    self.add_property_combobox(self.settings.load_property_by_key(vhead), num)
        # get missing items from sources and put them into the corresponding rows:
        # missing items will even be used if under the blue separation line:
        self.missing_data.append('_publ_section_references')
        for miss_data in self.missing_data:
            # add missing item to data sources column:
            try:
                row_num = self.ui.cif_main_table.vheaderitems.index(miss_data)
            except ValueError:
                continue
            tab_item = MyTableWidgetItem()
            try:
                # sources are lower case!
                txt = str(self.sources[miss_data][0])
                if miss_data in text_field_keys:
                    # only text fields:
                    tab_item = MyQPlainTextEdit(self.ui.cif_main_table)
                    tab_item.setReadOnly(True)
                    self.ui.cif_main_table.setCellWidget(row_num, COL_DATA, tab_item)
                    tab_item.setPlainText(txt)
                    # first_col = self.ui.cif_main_table.text(row_num, COL_CIF)
                    if row_num < self.complete_data_row:
                        if txt and txt != '?':  # or txt == first_col:
                            tab_item.setBackground(light_green)
                        else:
                            tab_item.setBackground(yellow)
                    tab_item.setToolTip(str(self.sources[miss_data][1]))
                else:
                    # regular linedit fields:
                    self.ui.cif_main_table.setItem(row_num, COL_DATA, tab_item)
                    tab_item.setText(txt)  # has to be string
                    if row_num < self.complete_data_row:
                        if txt and txt != '?':
                            tab_item.setBackground(light_green)
                        else:
                            tab_item.setBackground(yellow)
                tab_item.setToolTip(str(self.sources[miss_data][1]))
            except (KeyError, TypeError) as e:
                # TypeError my originate from incomplete self.missing_data list!
                # print(e, '##', miss_data)
                pass
            # items from data sources should not be editable
            if not miss_data in text_field_keys:
                tab_item.setUneditable()

    def add_property_combobox(self, data: str, row_num: int) -> None:
        """
        Adds a QComboBox to the cif_main_table with the content of special_fields or property templates.
        """
        combobox = MyComboBox(self.ui.cif_main_table)
        # print('special:', row_num, miss_data)
        self.ui.cif_main_table.setCellWidget(row_num, COL_EDIT, combobox)
        self.ui.cif_main_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        for num, value in data:
            try:
                combobox.addItem(value, num)
            except TypeError:
                print('Bad value in property:', value)
                if DEBUG:
                    raise
                continue
        combobox.setCurrentIndex(0)

    def fill_cif_table(self) -> None:
        """
        Adds the cif content to the main table. also add reference to FinalCif.
        """
        for key, value in self.cif.key_value_pairs():
            if not value or value == '?' or value == "'?'":
                self.missing_data.append(key)
                value = '?'
            self.add_row(key, value)
            # print(key, value)
        self.test_checksums()
        self.get_data_sources()
        self.erase_disabled_items()
        # self.ui.cif_main_table.resizeRowsToContents()

    def add_row(self, key: str, value: str, at_start=False) -> None:
        """
        Create a empty row at bottom of cif_main_table. This method only fills cif data in the
        first column. Not the data from external sources!
        """
        if at_start:
            row_num = 0
        else:
            row_num = self.ui.cif_main_table.rowCount()
        self.ui.cif_main_table.insertRow(row_num)
        # Add cif key and value to the row:
        head_item_key = MyTableWidgetItem(key)
        if value is None:
            strval = '?'
        else:
            strval = str(value).strip(" ").strip("'").strip(';\n').strip('\r\n')  # or '?')
        if not key:
            strval = ''
        if key in text_field_keys:
            # All textedit fields
            # print(key, strval)
            tab_cif = MyQPlainTextEdit(self.ui.cif_main_table)
            tab_cif.setPlainText(retranslate_delimiter(strval))
            tab_data = MyQPlainTextEdit(self.ui.cif_main_table)
            tab_edit = MyQPlainTextEdit(self.ui.cif_main_table)
            self.ui.cif_main_table.setCellWidget(row_num, COL_CIF, tab_cif)
            self.ui.cif_main_table.setCellWidget(row_num, COL_DATA, tab_data)
            self.ui.cif_main_table.setCellWidget(row_num, COL_EDIT, tab_edit)
            tab_cif.setReadOnly(True)
            tab_data.setReadOnly(True)
            # Make QPlainTextEdit fields a bit higher than the rest
            self.ui.cif_main_table.setRowHeight(row_num, 90)
        else:
            # All regular linedit fields:
            tab_cif = MyTableWidgetItem(retranslate_delimiter(strval))
            if key == "These below are already in:":
                self.add_separation_line(row_num)
                self.complete_data_row = row_num
            else:
                tab_data = MyTableWidgetItem()
                self.ui.cif_main_table.setItem(row_num, COL_CIF, tab_cif)
                self.ui.cif_main_table.setItem(row_num, COL_DATA, tab_data)
                if key == '_audit_creation_method':
                    tab_data.setText(
                        'FinalCif by Daniel Kratzert, Freiburg 2019, https://github.com/dkratzert/FinalCif')
                tab_cif.setUneditable()
                tab_data.setUneditable()
                self.ui.cif_main_table.resizeRowToContents(row_num)
        self.ui.cif_main_table.setVerticalHeaderItem(row_num, head_item_key)

    def add_separation_line(self, row_num: int) -> None:
        """
        Adds a blue separation line between cif content and empty cif keywords.
        """
        # The blue line in the table:
        item1 = MyTableWidgetItem('')
        item2 = MyTableWidgetItem('')
        item3 = MyTableWidgetItem('')
        diag = QBrush(blue)
        diag.setStyle(Qt.DiagCrossPattern)
        item1.setBackground(diag)
        item1.setUneditable()
        item2.setBackground(diag)
        item2.setUneditable()
        item3.setBackground(diag)
        item3.setUneditable()
        self.ui.cif_main_table.setItem(row_num, COL_CIF, item1)
        self.ui.cif_main_table.setItem(row_num, COL_DATA, item2)
        self.ui.cif_main_table.setItem(row_num, COL_EDIT, item3)
        self.ui.cif_main_table.resizeRowToContents(row_num)
        # Not working:
        # AttributeError: 'NoneType' object has no attribute 'setFont'
        # itemFont = QFont()
        # itemFont.setBold(True)
        # self.ui.cif_main_table.verticalHeaderItem(row_num).setFont(itemFont)


if __name__ == '__main__':
    def my_exception_hook(exctype, value, error_traceback):
        """
        Hooks into Exceptions to create debug reports.
        """
        errortext = 'FinalCif crash report\n\n'
        errortext += 'Python ' + sys.version + '\n'
        errortext += sys.platform + '\n'
        errortext += time.asctime(time.localtime(time.time())) + '\n'
        errortext += "Finalcif crashed during the following operation:" + '\n'
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


    if not DEBUG:
        sys.excepthook = my_exception_hook

    app = QApplication(sys.argv)
    w = AppWindow()
    app.setWindowIcon(QIcon(os.path.join(application_path, r'icon/finalcif2.png')))
    w.setWindowTitle('FinalCif v{}'.format(VERSION))
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
