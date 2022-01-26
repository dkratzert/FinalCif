#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import subprocess
import sys
import time
from contextlib import suppress
from datetime import datetime
from math import sin, radians
from pathlib import Path, WindowsPath
from shutil import copy2
from tempfile import TemporaryDirectory
from typing import Union, Dict, Tuple

import qtawesome as qta
import requests
from PyQt5 import QtCore, QtGui, QtWebEngineWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QShortcut, QCheckBox, QListWidgetItem, QApplication, \
    QPlainTextEdit, QFileDialog, QLabel
from gemmi import cif
from qtpy.QtGui import QDesktopServices

import finalcif
from finalcif import VERSION
from finalcif.cif.checkcif.checkcif import MyHTMLParser, AlertHelp, CheckCif
from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.cod.deposit import CODdeposit
from finalcif.cif.text import retranslate_delimiter
from finalcif.datafiles.bruker_data import BrukerData
from finalcif.datafiles.ccdc_mail import CCDCMail
from finalcif.displaymol import mol_file_writer
from finalcif.displaymol.sdm import SDM
from finalcif.displaymol.write_html import write
from finalcif.equip_property.author_loop_templates import AuthorLoops
from finalcif.equip_property.equipment import Equipment
from finalcif.equip_property.properties import Properties
from finalcif.gui.custom_classes import COL_CIF, COL_DATA, COL_EDIT, MyTableWidgetItem, light_green, yellow, MyCifTable
from finalcif.gui.dialogs import show_update_warning, unable_to_open_message, show_general_warning, \
    cif_file_open_dialog, \
    bad_z_message, show_res_checksum_warning, show_hkl_checksum_warning
from finalcif.gui.finalcif_gui import Ui_FinalCifWindow
from finalcif.gui.loops import Loop
from finalcif.gui.text_value_editor import MyTextTemplateEdit, txts
from finalcif.gui.vrf_classes import MyVRFContainer, VREF
from finalcif.report.archive_report import ArchiveReport
from finalcif.report.tables import make_report_from
from finalcif.report.templated_report import TemplatedReport
from finalcif.template.templates import ReportTemplates
from finalcif.tools.download import MyDownloader, start_worker
from finalcif.tools.dsrmath import my_isnumeric
from finalcif.tools.misc import strip_finalcif_of_name, next_path, do_not_import_keys, celltxt, to_float, \
    combobox_fields, \
    do_not_import_from_stoe_cfx, cif_to_header_label, grouper, is_database_number, file_age_in_days
from finalcif.tools.options import Options
from finalcif.tools.platon import Platon
from finalcif.tools.settings import FinalCifSettings
from finalcif.tools.shred import ShredCIF
from finalcif.tools.space_groups import SpaceGroups
from finalcif.tools.statusbar import StatusBar
from finalcif.tools.sumformula import formula_str_to_dict, sum_formula_to_html

DEBUG = False
app = QApplication(sys.argv)


class AppWindow(QMainWindow):

    def __init__(self, file=None, unit_test: bool = False):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # This prevents some things to happen during unit tests:
        # Open of target dir of shred cif,
        # open report doc,
        # get check.def from platon server
        self.running_inside_unit_test = unit_test
        self.sources: Union[None, Dict[str, Tuple[Union[str, None]]]] = None
        self.cif: Union[CifContainer, None] = None
        self.view: Union[QtWebEngineWidgets.QWebEngineView, None] = None
        self.report_picture_path: Union[Path, None] = None
        self.checkdef = []
        self.checkdef_file: Path = Path.home().joinpath('check.def')
        self.final_cif_file_name = Path()
        self.missing_data: set = set()
        self.temperature_warning_displayed = False
        self.threadpool = []
        # True if line with "these are already in" reached:
        self.complete_data_row = -1
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.settings = FinalCifSettings()
        self.options = Options(self.ui, self.settings)
        self.deposit = CODdeposit(self.ui, self.cif, self.options)
        self.equipment = Equipment(app=self, settings=self.settings)
        self.properties = Properties(app=self, settings=self.settings)
        self.status_bar = StatusBar(ui=self.ui)
        self.status_bar.show_message('FinalCif version {}'.format(VERSION))
        self.authors: Union[AuthorLoops, None] = None
        self.set_window_size_and_position()
        self.ui.cif_main_table.installEventFilter(self)
        # Sorting desynchronized header and columns:
        self.ui.cif_main_table.setSortingEnabled(False)
        self.distribute_cif_main_table_columns_evenly()
        # Make sure the start page is shown and not the edit page:
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(0)
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)
        self.ui.MainStackedWidget.got_to_main_page()
        self.set_initial_button_states()
        if len(sys.argv) > 1:
            self.load_cif_file(Path(sys.argv[1]) if sys.argv[1] != 'compile_ui' else Path())
        elif file:
            self.load_cif_file(file)
        self.load_recent_cifs_list()
        self.set_checkcif_output_font(self.ui.CheckcifPlaintextEdit)
        # To make file drag&drop working:
        self.setAcceptDrops(True)
        self.show()
        self.templates = ReportTemplates(self, self.settings)
        if not self.running_inside_unit_test:
            self.check_for_update_version()
        #self.ui.MainStackedWidget.go_to_text_template_page()
        self.txtedit = MyTextTemplateEdit(parent=self)
        self.txtedit.add_textfields(txts)
        self.ui.page_textTemplate.layout().addWidget(self.txtedit)
        #
        self.connect_signals_and_slots()
        self.make_button_icons()

    def distribute_cif_main_table_columns_evenly(self):
        hheader = self.ui.cif_main_table.horizontalHeader()
        hheader.setSectionResizeMode(COL_CIF, QHeaderView.Stretch)
        hheader.setSectionResizeMode(COL_DATA, QHeaderView.Stretch)
        hheader.setSectionResizeMode(COL_EDIT, QHeaderView.Stretch)
        hheader.setAlternatingRowColors(True)
        self.ui.cif_main_table.verticalHeader().setAlternatingRowColors(True)

    def set_initial_button_states(self):
        self.ui.PictureWidthDoubleSpinBox.setRange(0.0, 25)
        self.ui.PictureWidthDoubleSpinBox.setSingleStep(0.5)
        # Just too slow for large structures:
        self.ui.growCheckBox.setChecked(False)
        self.ui.CheckcifButton.setDisabled(True)
        self.ui.CheckcifHTMLOnlineButton.setDisabled(True)
        self.ui.CheckcifPDFOnlineButton.setDisabled(True)
        self.ui.SaveCifButton.setDisabled(True)
        self.ui.ExploreDirButton.setDisabled(True)
        self.ui.DetailsPushButton.setDisabled(True)
        self.ui.SourcesPushButton.setDisabled(True)
        self.ui.OptionsPushButton.setDisabled(True)
        self.ui.ImportCifPushButton.setDisabled(True)
        self.ui.CODpushButton.setDisabled(True)
        self.ui.CCDCpushButton.setDisabled(True)
        self.ui.ShredCifButton.setDisabled(True)
        self.ui.LoopsPushButton.setDisabled(True)

    def set_window_size_and_position(self):
        wsettings = self.settings.load_window_position()
        with suppress(TypeError):
            self.resize(wsettings['size'])
        with suppress(TypeError):
            self.move(wsettings['position'])
        if wsettings['maximized']:
            self.showMaximized()

    def make_button_icons(self):
        self.ui.CheckcifButton.setIcon(qta.icon('mdi.file-document-outline'))
        self.ui.CheckcifStartButton.setIcon(qta.icon('mdi.file-document-outline'))
        self.ui.LoopsPushButton.setIcon(qta.icon('mdi.table'))
        self.ui.CheckcifHTMLOnlineButton.setIcon(qta.icon('mdi.comment-check-outline'))
        self.ui.CheckcifPDFOnlineButton.setIcon(qta.icon('mdi.comment-check'))
        self.ui.SaveFullReportButton.setIcon(qta.icon('mdi.file-table-outline'))
        self.ui.ExploreDirButton.setIcon(qta.icon('fa5.folder-open'))
        self.ui.SaveCifButton.setIcon(qta.icon('fa5.save'))
        self.ui.SelectCif_PushButton.setIcon(qta.icon('fa5.file-alt', options=[{'color': 'darkgreen'}]))
        # self.ui.SelectCif_PushButton.setIcon(qta.icon('fa5s.spinner', color='red',
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
        self.ui.CCDCpushButton.setIcon(qta.icon('fa5s.upload'))
        self.ui.CODpushButton.setIcon(qta.icon('mdi.upload'))
        self.ui.SavePushButton.setIcon(qta.icon('mdi.content-save'))
        self.ui.revertLoopsPushButton.setIcon(qta.icon('mdi.backup-restore'))
        # Backbuttons:
        self.ui.BackpushButtonDetails.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackFromDepositPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackSourcesPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackFromOptionspPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackFromLoopsPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.ui.BackFromPlatonPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        self.txtedit.ui.backToCIFfromTextButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        #
        self.ui.SaveAuthorLoopToTemplateButton.setIcon(qta.icon('mdi.badge-account-outline'))
        self.ui.AddThisAuthorToLoopPushButton.setIcon(qta.icon('mdi.folder-table-outline'))
        self.ui.DeleteLoopAuthorTemplateButton.setIcon(qta.icon('mdi.delete-forever-outline'))

    def connect_signals_and_slots(self):
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        ## main
        self.ui.BackPushButton.clicked.connect(self.back_to_main)
        self.ui.BackFromDepositPushButton.clicked.connect(self.back_to_main)
        self.ui.ExploreDirButton.clicked.connect(self.explore_current_dir)
        self.ui.LoopsPushButton.clicked.connect(self.ui.MainStackedWidget.go_to_loops_page)
        self.ui.LoopsPushButton.clicked.connect(lambda: self.ui.TemplatesStackedWidget.setCurrentIndex(1))
        ## checkcif
        self.ui.CheckcifStartButton.clicked.connect(self.open_checkcif_page)
        self.ui.CheckcifButton.clicked.connect(self.do_offline_checkcif)
        self.ui.CheckcifHTMLOnlineButton.clicked.connect(self.do_html_checkcif)
        self.ui.CheckcifPDFOnlineButton.clicked.connect(self.do_pdf_checkcif)
        self.ui.BackFromPlatonPushButton.clicked.connect(self.back_to_main_noload)
        self.ui.SavePushButton.clicked.connect(self.save_responses)
        ## open, import
        self.ui.SelectCif_PushButton.clicked.connect(self.load_cif_file)
        self.ui.SaveCifButton.clicked.connect(self.save_cif_and_display)
        self.ui.ImportCifPushButton.clicked.connect(self.import_additional_cif)
        ## report
        self.ui.SaveFullReportButton.clicked.connect(self.make_report_tables)
        self.ui.RecentComboBox.currentIndexChanged.connect(self.load_recent_file)
        #
        self.ui.cif_main_table.row_deleted.connect(self._deleted_row)
        #
        self.ui.CODpushButton.clicked.connect(self.open_cod_page)
        self.ui.BackToCODPushButton.clicked.connect(self.open_cod_page)
        self.ui.CCDCpushButton.clicked.connect(self._ccdc_deposit)
        #
        save_shortcut = QShortcut(QtGui.QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.save_current_cif_file)
        save_shortcut = QShortcut(QtGui.QKeySequence('Ctrl+H'), self)
        save_shortcut.activated.connect(self.do_html_checkcif)
        save_shortcut = QShortcut(QtGui.QKeySequence('Ctrl+P'), self)
        save_shortcut.activated.connect(self.do_pdf_checkcif)
        #
        self.ui.DetailsPushButton.clicked.connect(self.show_residuals)
        self.ui.BackpushButtonDetails.clicked.connect(self.back_to_main_noload)
        self.ui.growCheckBox.toggled.connect(self.redraw_molecule)
        #
        self.ui.SourcesPushButton.clicked.connect(self.show_sources)
        self.ui.BackSourcesPushButton.clicked.connect(self.back_to_main_noload)
        self.ui.BackFromOptionspPushButton.clicked.connect(self.back_to_main_noload)
        self.ui.BackFromLoopsPushButton.clicked.connect(self.back_to_main_noload)
        # Shred Cif
        self.ui.ShredCifButton.clicked.connect(self.do_shred_cif)
        self.ui.OptionsPushButton.clicked.connect(self.options.show_options)
        # help
        self.ui.HelpPushButton.clicked.connect(self.show_help)
        self.ui.ReportPicPushButton.clicked.connect(self.set_report_picture)
        # brings the html checkcif in from in order to avoid confusion of an "empty" checkcif report page:
        self.ui.CheckCIFResultsTabWidget.currentChanged.connect(lambda: self.ui.ResponsesTabWidget.setCurrentIndex(0))
        ##
        self.ui.SelectCif_LineEdit.returnPressed.connect(self.check_if_file_field_contains_database_number)
        self.ui.fullIucrCheckBox.clicked.connect(self.toggle_hkl_option)
        self.ui.structfactCheckBox.clicked.connect(self.toggle_iucr_option)
        # text templates
        self.txtedit.ui.backToCIFfromTextButton.clicked.connect(self.back_to_main_noload)

    def toggle_hkl_option(self, iucr_is_checked: bool):
        if iucr_is_checked:
            self.ui.structfactCheckBox.setChecked(False)

    def toggle_iucr_option(self, hkl_is_checked: bool):
        if hkl_is_checked:
            self.ui.fullIucrCheckBox.setChecked(False)

    def check_if_file_field_contains_database_number(self):
        """
        Downloads a CIF file from the COD with the corresponding deposition number entered into the file field.
        """
        input_txt = self.ui.SelectCif_LineEdit.text().strip()
        if is_database_number(input_txt):
            file = '{}.cif'.format(input_txt)
            r = requests.get(self.deposit.main_url + '{}.cif'.format(input_txt))
            if r.status_code == 200:
                Path(file).write_bytes(r.content)
                r.close()
                self.load_cif_file(Path(file))
            else:
                self.ui.SelectCif_LineEdit.setText('')

    def open_cod_page(self):
        self.save_current_cif_file()
        self.load_cif_file(self.final_cif_file_name)
        self.deposit.cif = self.cif
        self.ui.MainStackedWidget.setCurrentIndex(7)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """It called when the main window resizes."""
        super(AppWindow, self).resizeEvent(a0)
        with suppress(AttributeError):
            self.view.reload()
        with suppress(AttributeError):
            self._savesize()

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        """Is called when the main window moves."""
        super(AppWindow, self).moveEvent(a0)
        with suppress(AttributeError):
            self._savesize()

    def changeEvent(self, event):
        """Is called when the main window changes its state."""
        if event.type() == QtCore.QEvent.WindowStateChange:
            with suppress(AttributeError):
                self._savesize()

    def _savesize(self):
        """Saves the main window size nd position."""
        x, y = self.pos().x(), self.pos().y()
        self.settings.save_window_position(QtCore.QPoint(x, y), self.size(), self.isMaximized())

    def show_help(self):
        QDesktopServices.openUrl(QtCore.QUrl('https://dkratzert.de/files/finalcif/docs/'))

    def do_shred_cif(self):
        shred = ShredCIF(cif=self.cif, ui=self.ui)
        shred.shred_cif()
        if not self.running_inside_unit_test:
            self.explore_current_dir()

    def open_checkcif_page(self):
        """
        Opens the checkcif stackwidget page and therein the html report page
        """
        self.ui.MainStackedWidget.go_to_checkcif_page()

    def _ccdc_deposit(self) -> None:
        """
        Open the CCDC deposit web page.
        """
        QDesktopServices.openUrl(QtCore.QUrl('https://www.ccdc.cam.ac.uk/deposit'))
        self.explore_current_dir()

    def _deleted_row(self, key: str) -> None:
        """
        Deletes a row of the main table and reloads the cif file.
        """
        if self.cif.block.find_pair(key):
            self.cif.block.find([key]).erase()
            if key in self.missing_data:
                self.missing_data.discard(key)
                # del self.missing_data[self.missing_data.index(key)]
            self.save_current_cif_file()
            self.load_cif_file(self.final_cif_file_name)

    def check_for_update_version(self) -> None:
        if os.environ.get('NO_NETWORK'):
            print('Skipping version.txt download because NO_NETWORK variable is set.')
            return
        mainurl = "https://dkratzert.de/files/finalcif/version.txt"
        self.upd = MyDownloader(mainurl)
        version_thread = QThread()
        self.threadpool.append(version_thread)
        start_worker(self.upd, version_thread, onload=self.is_update_necessary)

    def is_update_necessary(self, content: bytes) -> None:
        """
        Reads the reply from the server and displays a warning in case of an old version.
        """
        remote_version = 0
        with suppress(Exception):
            remote_version = int(content.decode('ascii', errors='ignore'))
        if remote_version > VERSION:
            print('Version {} is outdated (actual is {}).'.format(VERSION, remote_version))
            show_update_warning(remote_version)
        else:
            print('Version {} is up-to-date.'.format(VERSION))

    def erase_disabled_items(self) -> None:
        """
        Items that got disabled in the sources list are set to ? here.
        """
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

    def show_sources(self) -> None:
        """
        Shows data sources in the SourcesTableWidget.
        """
        COL_key = 1
        COL_source_data = 2
        if not self.sources:
            return
        table = self.ui.SourcesTableWidget
        table.setRowCount(0)
        rownum = 0
        for s in self.sources:
            if not self.sources[s]:
                continue
            table.insertRow(rownum)
            box = QCheckBox(self)
            box.clicked.connect(self.erase_disabled_items)
            table.setCellWidget(rownum, 0, box)
            box.setChecked(True)
            box.setStyleSheet("margin-left:10%; margin-right:0%;")
            source_item = MyTableWidgetItem(s)
            source_item.setUneditable()
            data_item = MyTableWidgetItem(self.sources[s][1])
            data_item.setUneditable()
            table.setItem(rownum, COL_key, source_item)
            table.setItem(rownum, COL_source_data, data_item)
            rownum += 1
        table.resizeColumnToContents(0)
        table.resizeColumnToContents(1)
        table.resizeColumnToContents(2)
        self.ui.MainStackedWidget.go_to_data_sources_page()

    def get_checkdef_for_response_forms(self) -> None:
        """
        Sends a get request to the platon server in order to get the current check.def file.
        """
        if os.environ.get('NO_NETWORK'):
            print('Skipping check.def download because NO_NETWORK variable is set.')
            return
        url = 'http://www.platonsoft.nl/xraysoft/unix/platon/check.def'
        self.updc = MyDownloader(url)
        checkdef_thread = QThread()
        self.threadpool.append(checkdef_thread)
        start_worker(self.updc, checkdef_thread, onload=self._save_checkdef)

    def _save_checkdef(self, reply: bytes) -> None:
        """
        Is called by the finished signal from the downloader.
        """
        with suppress(Exception):
            self.checkdef_file.write_bytes(reply)
        self.checkdef = reply.decode('ascii', errors='ignore').splitlines(keepends=False)

    def explore_current_dir(self):
        """
        Opens the file checkcif_browser for the current directory.
        """
        try:
            curdir = self.cif.fileobj.resolve().parent
        except AttributeError:
            return
        if sys.platform == "win" or sys.platform == "win32":
            subprocess.Popen(['explorer', str(curdir)], shell=True)
        if sys.platform == 'darwin':
            subprocess.call(['open', curdir])
        if sys.platform == 'linux':
            subprocess.call(['xdg-open', curdir])

    def dragEnterEvent(self, e: QtCore.QEvent):
        """
        Allow drag of files to the main window
        """
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QtCore.QEvent):
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
            self.load_cif_file(Path(final_path))

    def back_to_main(self):
        """
        Get back to the main table and load the new cif file.
        """
        self.load_cif_file(self.final_cif_file_name.resolve())
        self.ui.MainStackedWidget.got_to_main_page()
        self.ui.cif_main_table.scrollToTop()
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)

    def back_to_main_noload(self):
        """
        Get back to the main table. Without loading a new cif file.
        """
        self.status_bar.show_message('')
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)
        self.ui.MainStackedWidget.got_to_main_page()
        if self.view:
            self.ui.moleculeLayout.removeWidget(self.view)

    def _checkcif_failed(self, txt: str):
        self.ui.CheckCifLogPlainTextEdit.appendHtml('<b>{}</b>'.format(txt))

    def _ckf_progress(self, txt: str):
        self.ui.CheckCifLogPlainTextEdit.appendPlainText(txt)

    def _checkcif_finished(self):
        """
        Loads the html checkcif results and displays them in a checkcif_browser window.
        """
        self.ui.CheckcifHTMLOnlineButton.setEnabled(True)
        self.ui.CheckcifPDFOnlineButton.setEnabled(True)
        try:
            parser = MyHTMLParser(self.htmlfile.read_text())
        except FileNotFoundError:
            # happens if checkcif fails, e.g. takes too much time.
            self.ui.CheckCifLogPlainTextEdit.appendHtml('<b>CheckCIF failed to finish. '
                                                        'Please try it at https://checkcif.iucr.org/ instead.</b>')
            return
        self.checkcif_browser = QtWebEngineWidgets.QWebEngineView(self.ui.htmlTabwidgetPage)
        self.ui.htmlCHeckCifGridLayout.addWidget(self.checkcif_browser)
        url = QtCore.QUrl.fromLocalFile(str(self.htmlfile.resolve()))
        self.ui.MainStackedWidget.go_to_checkcif_page()
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(1)  # Index 1 is html page
        self.checkcif_browser.load(url)
        self.ui.ResponsesTabWidget.setCurrentIndex(0)
        # The picture file linked in the html file:
        imageobj = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.gif')
        gif = parser.get_image()
        self.ui.CheckCifLogPlainTextEdit.appendPlainText('CheckCIF Report finished.')
        forms = parser.response_forms
        # makes all gray:
        # self.ui.responseFormsListWidget.setStyleSheet("background: 'gray';")
        a = AlertHelp(self.checkdef)
        self.validation_response_forms_list = []
        self.ui.responseFormsListWidget.clear()
        for form in forms:
            vrf = MyVRFContainer(form, a.get_help(form['alert_num']), parent=self)
            self.validation_response_forms_list.append(vrf)
            item = QListWidgetItem()
            item.setSizeHint(vrf.sizeHint())
            self.ui.responseFormsListWidget.addItem(item)
            self.ui.responseFormsListWidget.setItemWidget(item, vrf)
        if not forms:
            iteme = QListWidgetItem(' ')
            item = QListWidgetItem(' No level A, B or C alerts to explain.')
            self.ui.responseFormsListWidget.addItem(iteme)
            self.ui.responseFormsListWidget.addItem(item)
        if gif:
            imageobj.write_bytes(gif)

    def do_html_checkcif(self) -> None:
        """
        Performs an online checkcif via checkcif.iucr.org.
        """
        self._get_check_def()
        self.ui.CheckCifLogPlainTextEdit.clear()
        try:
            self.checkcif_browser.close()
            self.ui.htmlCHeckCifGridLayout.removeWidget(self.checkcif_browser)
            QApplication.processEvents()
        except Exception as e:
            if DEBUG:
                print('Browser not removed:')
                print(e)
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(1)
        self.ui.CheckCifLogPlainTextEdit.appendPlainText(
            'Sending html report request to {} ...'.format(self.options.checkcif_url))
        if not self.save_current_cif_file():
            self.ui.CheckCifLogPlainTextEdit.appendHtml('<b>Unable to save CIF file. Aborting action...</b>')
            return None
        self.load_cif_file(self.final_cif_file_name)
        self.htmlfile = Path(strip_finalcif_of_name('checkcif-' + self.cif.fileobj.stem) + '-finalcif.html')
        try:
            self.htmlfile.unlink()
        except (FileNotFoundError, PermissionError):
            pass
        self.ckf = CheckCif(cif=self.cif, outfile=self.htmlfile,
                            hkl_upload=(not self.ui.structfactCheckBox.isChecked()), pdf=False,
                            url=self.options.checkcif_url,
                            full_iucr=self.ui.fullIucrCheckBox.isChecked())
        self.ckf.progress.connect(self._ckf_progress)
        self.ckf.failed.connect(self._checkcif_failed)
        # noinspection PyUnresolvedReferences
        self.ckf.finished.connect(self._checkcif_finished)
        self.ui.CheckcifHTMLOnlineButton.setDisabled(True)
        self.ui.CheckcifPDFOnlineButton.setDisabled(True)
        self.ckf.start()

    def _get_check_def(self):
        if self.checkdef_file.exists() and file_age_in_days(self.checkdef_file) < 60:
            self.checkdef = self.checkdef_file.read_text().splitlines(keepends=False)
        else:
            self.get_checkdef_for_response_forms()

    def save_responses(self) -> None:
        """
        Saves the validation response form text to _vrf_ CIF entries.
        :return: None
        """
        if not self.validation_response_forms_list:
            return
        n = 0
        for response_row in self.validation_response_forms_list:
            response_txt = response_row.response_text_edit.toPlainText()
            if not response_txt:
                # No response was written
                continue
            n += 1
            v = VREF()
            v.key = response_row.form['name']
            v.problem = response_row.form['problem']
            v.response = response_txt
            self.add_row(v.key, v.value, at_start=True)
        self.save_current_cif_file()
        if n:
            self.ui.CheckCifLogPlainTextEdit.appendPlainText('Forms saved')
        else:
            self.ui.CheckCifLogPlainTextEdit.appendPlainText('No forms were filled in.')

    def _switch_to_report(self) -> None:
        self.ui.ResponsesTabWidget.setCurrentIndex(0)

    def _pdf_checkcif_finished(self) -> None:
        self.ui.CheckcifPDFOnlineButton.setEnabled(True)
        self.ui.CheckcifHTMLOnlineButton.setEnabled(True)
        self.ckf.show_pdf_report()

    def do_pdf_checkcif(self) -> None:
        """
        Performs an online checkcif and shows the result as pdf.
        """
        self.ui.CheckCifLogPlainTextEdit.clear()
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(2)
        if not self.save_current_cif_file():
            self.ui.CheckCifLogPlainTextEdit.appendHtml('<b>Unable to save CIF file. Aborting action...</b>')
            return None
        self.load_cif_file(self.final_cif_file_name)
        htmlfile = Path('checkpdf-' + self.cif.fileobj.stem + '.html')
        try:
            htmlfile.unlink()
        except (FileNotFoundError, PermissionError):
            pass
        self.ui.CheckCifLogPlainTextEdit.appendPlainText(
            'Sending pdf report request to {} ...'.format(self.options.checkcif_url))
        self.ckf = CheckCif(cif=self.cif, outfile=htmlfile, hkl_upload=(not self.ui.structfactCheckBox.isChecked()),
                            pdf=True, url=self.options.checkcif_url,
                            full_iucr=self.ui.fullIucrCheckBox.isChecked())
        self.ckf.failed.connect(self._checkcif_failed)
        # noinspection PyUnresolvedReferences
        self.ckf.finished.connect(self._pdf_checkcif_finished)
        self.ckf.progress.connect(self._ckf_progress)
        self.ui.CheckcifPDFOnlineButton.setDisabled(True)
        self.ui.CheckcifHTMLOnlineButton.setDisabled(True)
        self.ckf.start()
        self.ui.CheckCifLogPlainTextEdit.appendPlainText('PDF Checkcif report finished.')
        try:
            htmlfile.unlink()
        except (FileNotFoundError, PermissionError):
            pass

    def append_to_ciflog_without_newline(self, text: str = '') -> None:
        self.ui.CheckCifLogPlainTextEdit.moveCursor(QtGui.QTextCursor.End)
        self.ui.CheckCifLogPlainTextEdit.insertPlainText(text)
        self.ui.CheckCifLogPlainTextEdit.moveCursor(QtGui.QTextCursor.End)

    def do_offline_checkcif(self) -> None:
        """
        Performs a checkcif with platon and displays it in the text editor of the MainStackedWidget.
        """
        self.ui.CheckCifLogPlainTextEdit.clear()
        self.ui.MainStackedWidget.go_to_checkcif_page()
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(0)
        self.ui.CheckCifLogPlainTextEdit.appendPlainText("Running Checkcif locally. Please wait...\n")
        QApplication.processEvents()
        # makes sure also the currently edited item is saved:
        self.ui.cif_main_table.setCurrentItem(None)
        self.ui.CheckcifPlaintextEdit.clear()
        if not self.save_current_cif_file():
            self.ui.CheckCifLogPlainTextEdit.appendPlainText('Unable to save CIF file. Aborting action...')
            return None
        self.load_cif_file(self.final_cif_file_name)
        self.ui.MainStackedWidget.go_to_checkcif_page()
        QApplication.processEvents()
        timeout = 350
        try:
            p = Platon(self.final_cif_file_name, timeout, '-u')
        except Exception as e:
            print(e)
            # self.ui.CheckcifButton.setDisabled(True)
            return
        checkcif_out = self.ui.CheckcifPlaintextEdit
        checkcif_out.setPlainText('Platon output: \nThis might not be the same as the IUCr CheckCIF!')
        QApplication.processEvents()
        p.start()
        if not self.wait_for_chk_file(p):
            checkcif_out.appendPlainText('Platon did not start. No .chk file from Platon found!')
            checkcif_out.appendPlainText(p.platon_output)
            p.kill()
            p.delete_orphaned_files()
            return
        checkcif_out.appendPlainText('\n' + '#' * 80)
        checkcif_out.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.wait_until_platon_finished(timeout)
        checkcif_out.appendPlainText(p.platon_output)
        p.parse_chk_file()
        vrf_txt = ''
        with suppress(FileNotFoundError):
            vrf_txt = Path(self.cif.fileobj.stem + '.vrf').read_text()
        if p.chk_file_text:
            with suppress(AttributeError):
                checkcif_out.appendPlainText(p.chk_file_text)
                checkcif_out.appendPlainText('\n' + '#' * 27 + ' Validation Response Forms ' + '#' * 26 + '\n')
                checkcif_out.appendPlainText(vrf_txt)
        checkcif_out.verticalScrollBar().setValue(0)
        moiety = self.ui.cif_main_table.getTextFromKey(key='_chemical_formula_moiety', col=0)
        if p.formula_moiety and moiety in ['', '?']:
            self.ui.cif_main_table.setText(key='_chemical_formula_moiety', txt=p.formula_moiety, column=COL_EDIT)
        print('Killing platon!')
        p.kill()
        p.delete_orphaned_files()

    def wait_for_chk_file(self, p) -> bool:
        time.sleep(2)
        stop = 0
        while not Path(self.cif.fileobj.stem + '.chk').exists():
            self.append_to_ciflog_without_newline('.')
            QApplication.processEvents()
            time.sleep(2)
            if not p.plat:
                self.append_to_ciflog_without_newline('aborted here')
                self.append_to_ciflog_without_newline(p.platon_output)
                return False
            stop += 1
            if stop == 8:
                return False
        return True

    def wait_until_platon_finished(self, timeout: int = 300):
        stop = 0
        if not Path(self.cif.fileobj.stem + '.chk').exists():
            self.ui.CheckCifLogPlainTextEdit.appendPlainText('Platon returned no output.')
            QApplication.processEvents()
            return
        with suppress(FileNotFoundError):
            while Path(self.cif.fileobj.stem + '.chk').stat().st_size < 200:
                self.append_to_ciflog_without_newline('*')
                QApplication.processEvents()
                if stop == timeout:
                    self.ui.CheckcifPlaintextEdit.appendPlainText('PLATON timed out')
                    break
                time.sleep(1)
                stop += 1
            time.sleep(0.5)

    def set_checkcif_output_font(self, ccpe):
        doc = ccpe.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        font.setStyleHint(QtGui.QFont.Monospace)
        QApplication.processEvents()
        font.setPointSize(14)
        doc.setDefaultFont(font)

    def load_recent_file(self, file_index: int) -> None:
        """
        Loads the currently slected file in the recent combobox.
        :param file_index: index in the combobox
        :return: None
        """
        combo = self.ui.RecentComboBox
        if file_index > 0:
            txt = combo.itemText(file_index)
            self.load_cif_file(Path(txt))

    def set_report_picture(self, file: Path) -> None:
        """Sets the picture of the report document."""
        if file:
            self.report_picture_path = Path(file)
        else:
            filename, _ = QFileDialog.getOpenFileName(filter="Image Files (*.png *.jpg *.jpeg *.bmp "
                                                             "*.gif *.tif *.tiff *.eps *.emf *.wmf)",
                                                      caption='Open a Report Picture')
            with suppress(Exception):
                self.report_picture_path = Path(filename)
            if self.report_picture_path.exists() and self.report_picture_path.is_file():
                self.ui.ReportPicPushButton.setIcon(qta.icon('fa5.image'))
                self.ui.ReportPicPushButton.setText('')

    def make_report_tables(self) -> None:
        """
        Generates a report document.
        """
        not_ok = None
        if not self.cif:
            return None
        if not self.save_current_cif_file():
            return None
        self.load_cif_file(self.final_cif_file_name)
        report_filename = strip_finalcif_of_name('report_{}'.format(self.cif.fileobj.stem)) + '-finalcif.docx'
        # The picture after the header:
        if self.report_picture_path:
            picfile = self.report_picture_path
        else:
            picfile = Path(self.final_cif_file_name.stem + '.gif')
        try:
            if self.ui.TemplatesListWidget.currentRow() == 0 or not self.ui.TemplatesListWidget.currentItem():
                make_report_from(options=self.options, file_obj=self.final_cif_file_name,
                                 output_filename=report_filename, picfile=picfile)
            else:
                t = TemplatedReport()
                t.make_templated_report(options=self.options, file_obj=self.final_cif_file_name,
                                        output_filename=report_filename, picfile=picfile,
                                        template_path=Path(self.ui.TemplatesListWidget.currentItem().text()))
        except FileNotFoundError as e:
            if DEBUG:
                raise
            print('Unable to make report from cif file.')
            not_ok = e
            show_general_warning("The report templates could not be found:\n" + str(not_ok))
            return
        except PermissionError:
            if DEBUG:
                raise
            print('Unable to open cif file')
            show_general_warning('The report document {} could not be opened.\n'
                                 'Is the file already opened?'.format(report_filename))
            return
        if not self.running_inside_unit_test:
            self.open_report_document(report_filename)
        # Save report and other files to a zip file:
        self.zip_report(report_filename)

    def zip_report(self, report_filename):
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

    def open_report_document(self, report_filename: str):
        if Path(report_filename).resolve().exists():
            if os.name == 'nt':
                os.startfile(Path(report_filename).resolve())
            if sys.platform == 'darwin':
                subprocess.call(['open', Path(report_filename).resolve()])

    def save_current_recent_files_list(self, file: Path) -> None:
        """
        Saves the list of the recently opened files. Non-existent files are removed.
        """
        if os.name == 'nt':
            # Used path with backslash for windows systems:
            file: str = str(WindowsPath(file.resolve()).absolute())
        else:
            file: str = str(Path(file.resolve()).absolute())
        recent = list(self.settings.settings.value('recent_files', type=list))
        # delete possible previous occurence of new file:
        while file in recent:
            recent.remove(file)
        # file has to be str not Path():
        recent.insert(0, file)
        recent = recent[:8]
        self.settings.settings.setValue('recent_files', recent)

    def load_recent_cifs_list(self) -> None:
        self.ui.RecentComboBox.clear()
        recent = list(self.settings.settings.value('recent_files', type=list))
        self.ui.RecentComboBox.addItem('Recent Files')
        for n, file in enumerate(recent):
            if not isinstance(file, str):
                del recent[n]
            self.ui.RecentComboBox.addItem(file, n)

    def save_cif_and_display(self) -> None:
        saved = self.save_current_cif_file()
        if saved:
            self.display_cif_text()

    def save_current_cif_file(self, filename: Union[str, None] = None) -> Union[bool, None]:
        """
        Saves the current cif file and stores the information of the third column.
        """
        if not self.cif:
            # No file is opened
            return None
        self.cif.rename_data_name(''.join(self.ui.datnameLineEdit.text().split(' ')))
        # restore header, otherwise item is not saved:
        table = self.ui.cif_main_table
        table.setCurrentItem(None)  # makes sure also the currently edited item is saved
        self.store_data_from_table_rows(table)
        self.save_ccdc_number()
        if not filename:
            self.final_cif_file_name = self.cif.fileobj.parent.joinpath(
                strip_finalcif_of_name(self.cif.fileobj.stem) + '-finalcif.cif')
        else:
            self.final_cif_file_name = Path(filename)
        try:
            self.cif.save(str(self.final_cif_file_name.resolve()))
            self.status_bar.show_message('  File Saved:  {}'.format(self.final_cif_file_name.name), 10)
            print('File saved ...')
            return True
        except Exception as e:
            print('Unable to save file:')
            print(e)
            show_general_warning('Can not save file: ' + str(e))
            return False

    def store_data_from_table_rows(self, table: MyCifTable) -> None:
        """
        Stores the data from the main table in the cif object.
        """
        for row in range(self.ui.cif_main_table.rows_count):
            vhead = self.ui.cif_main_table.vheader_text(row)
            if not self.is_row_a_cif_item(vhead):
                continue
            col_data = table.text(row, COL_DATA)
            col_edit = table.text(row, COL_EDIT)
            if col_data and not col_edit and col_data != '?':
                self.cif[vhead] = col_data
            if col_edit:
                try:
                    self.cif[vhead] = col_edit
                except (RuntimeError, ValueError, IOError) as e:
                    print('Can not take cif info from table:', e)

    def is_row_a_cif_item(self, vhead):
        is_cif = False
        # vertical header item is a cif keyword:
        if vhead.startswith('_'):
            is_cif = True
        return is_cif

    def save_ccdc_number(self) -> None:
        ccdc_number = self.ui.CCDCNumLineEdit.toPlainText().split(' ')
        if len(ccdc_number) > 1 and my_isnumeric(ccdc_number[1]):
            ccdc_number = ccdc_number[1]
        else:
            ccdc_number = ccdc_number[0]
        if ccdc_number:
            self.cif.set_pair_delimited('_database_code_depnum_ccdc_archive', ccdc_number)

    def display_cif_text(self) -> None:
        """
        Displays the saved cif file into a textfield.
        """
        self.ui.MainStackedWidget.go_to_cif_text_page()
        final_textedit = self.ui.FinalCifFilePlainTextEdit
        doc = final_textedit.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        font.setStyleHint(QtGui.QFont.Monospace)
        # increases the pont size every time a bit more :)
        # size = font.pointSize()
        font.setPointSize(14)
        doc.setDefaultFont(font)
        final_textedit.setLineWrapMode(QPlainTextEdit.NoWrap)
        final_textedit.setPlainText(self.final_cif_file_name.read_text(encoding='utf-8', errors='ignore'))

    def import_additional_cif(self, filename: str):
        """
        Import an additional cif file to the main table.
        """
        imp_cif: Union[CifContainer, None] = None
        if not filename:
            filename = cif_file_open_dialog(filter="CIF file (*.cif *.pcf *.cif_od *.cfx *.sqf)")
        if not filename:
            return
        try:
            imp_cif = CifContainer(Path(filename))
        except RuntimeError as e:
            show_general_warning('Could not import {}:\n'.format(filename) + str(e))
            return
        except ValueError as e:
            warning = 'Problems parsing file: {}:\n'.format(filename) + str(e)
            if 'data_' in str(e):
                warning = warning + "\n\nA CIF needs to start with 'data_[some_name]'."
            show_general_warning(warning)
            return
        except IOError as e:
            show_general_warning('Unable to open file {}:\n'.format(filename) + str(e))
            return
        self.import_key_value_pairs(imp_cif)
        self.import_loops(imp_cif)
        # I think I leave the user possibilities to change the imported values:
        # self.save_current_cif_file()
        # self.load_cif_file(str(self.final_cif_file_name))

    def import_loops(self, imp_cif: 'CifContainer'):
        """
        Import all loops from the CifContainer imp_cif to the current block.
        """
        for loop in imp_cif.loops:
            new_loop = self.cif.block.init_loop('', loop.tags)
            for row in imp_cif.block.find(loop.tags):
                new_loop.add_row(row)

    def import_key_value_pairs(self, imp_cif: CifContainer) -> None:
        for item in imp_cif.block:
            if item.pair is not None:
                key, value = item.pair
                # leave out unit cell etc.:
                if self.do_not_import_this_key(key, value, imp_cif):
                    continue
                value = cif.as_string(value)
                if key in self.ui.cif_main_table.vheaderitems:
                    self.ui.cif_main_table.setText(key=key, column=COL_EDIT, txt=value, color=light_green)
                else:
                    self.add_row(key, value)  # , column=COL_EDIT

    def do_not_import_this_key(self, key: str, value: str, cif: CifContainer) -> bool:
        if value == '?' or value.strip() == '':
            return True
        if key in do_not_import_keys:
            return True
        if key in do_not_import_from_stoe_cfx and cif.fileobj.suffix == '.cfx':
            return True
        return False

    def load_cif_file(self, filepath: Path) -> None:
        """
        Opens the cif file and fills information into the main table.
        """
        self.status_bar.show_message('')
        with suppress(AttributeError):
            self.ui.moleculeLayout.removeWidget(self.view)
        # Set to empty state before loading:
        self.missing_data = set()
        # clean table and vheader before loading:
        self.ui.cif_main_table.delete_content()
        if not filepath:
            filepath = self.get_file_from_dialog()
            if not filepath.is_file():
                return
        self.set_path_display_in_file_selector(str(filepath))
        try:
            if not self.able_to_open(filepath):
                return
        except (OSError, IndexError):
            print('Something failed during cif file opening...')
            if DEBUG:
                raise
            return
        not_ok = None
        try:
            e = None
            self.cif = CifContainer(filepath)
        except (RuntimeError, IndexError, ValueError) as e:
            print('Unable to open cif file...')
            if DEBUG:
                raise
            print(e)
            not_ok = e
        if not_ok:
            unable_to_open_message(filepath, not_ok)
            return
        if not self.cif.chars_ok:
            self.warn_about_bad_cif()
        self.check_cif_for_missing_values_before_really_open_it()
        self.go_into_cifs_directory(filepath)
        self.final_cif_file_name = Path(strip_finalcif_of_name(str(self.cif.fileobj.stem)) + '-finalcif.cif')
        try:
            self.fill_cif_table()
        except Exception as e:
            not_ok = e
            # raise
            unable_to_open_message(filepath, not_ok)
            raise
        # Do this only when sure we can load the file:
        self.save_current_recent_files_list(filepath)
        self.load_recent_cifs_list()
        self.make_loops_tables()
        # Initial button states:
        self.ui.CheckcifButton.setEnabled(True)
        self.ui.CheckcifHTMLOnlineButton.setEnabled(True)
        self.ui.CheckcifPDFOnlineButton.setEnabled(True)
        self.ui.SaveCifButton.setEnabled(True)
        self.ui.ExploreDirButton.setEnabled(True)
        if self.cif:
            if ShredCIF(cif=self.cif, ui=self.ui).cif_has_hkl_or_res_file():
                self.ui.ShredCifButton.setEnabled(True)
            else:
                self.ui.ShredCifButton.setDisabled(True)
            curdir = str(self.cif.fileobj.resolve().parent)
            # saving current cif dir as last working directory:
            self.settings.save_current_dir(curdir)
            self.enable_buttons()
            self.ui.datnameLineEdit.setText(self.cif.block.name)
            try:
                self.ui.Spacegroup_top_LineEdit.setText(
                    SpaceGroups().to_html(self.cif.space_group))
            except Exception as e:
                print('Space group error:', str(e))
                self.ui.Spacegroup_top_LineEdit.setText(self.cif.space_group)
            try:
                self.ui.SumFormMainLineEdit.setText(sum_formula_to_html(formula_str_to_dict(
                    self.cif['_chemical_formula_sum'].strip(" '"))))
            except Exception:
                self.ui.SumFormMainLineEdit.setText(self.cif['_chemical_formula_sum'].strip(" '"))
            self.ui.CCDCNumLineEdit.setText(self.cif['_database_code_depnum_ccdc_archive'])
            self.ui.CheckcifPlaintextEdit.clear()
            self.ui.TemplatesStackedWidget.setCurrentIndex(0)
            self.authors = AuthorLoops(ui=self.ui, cif=self.cif, app=self)
            if not self.ui.MainStackedWidget.on_checkcif_page():
                self.ui.MainStackedWidget.got_to_main_page()
            self.deposit.cif = self.cif

    def enable_buttons(self):
        self.ui.DetailsPushButton.setEnabled(True)
        self.ui.SourcesPushButton.setEnabled(True)
        self.ui.OptionsPushButton.setEnabled(True)
        self.ui.ImportCifPushButton.setEnabled(True)
        self.ui.CODpushButton.setEnabled(True)
        self.ui.CCDCpushButton.setEnabled(True)
        self.ui.ShredCifButton.setEnabled(True)
        self.ui.LoopsPushButton.setEnabled(True)

    def get_file_from_dialog(self, change_into_workdir=True) -> Union[Path, None]:
        if change_into_workdir:
            self.set_last_workdir()
        fp = cif_file_open_dialog()
        filepath = Path(fp)
        if change_into_workdir:
            # The warning about inconsistent temperature:
            self.temperature_warning_displayed = False
        return filepath

    def go_into_cifs_directory(self, filepath):
        try:
            # Change the current working Directory
            os.chdir(filepath.resolve().parent)
        except OSError:
            print("Can't change the Current Working Directory")

    def check_cif_for_missing_values_before_really_open_it(self):
        try:
            # Will not stop reading if only the value is missing and ends with newline:
            self.cif.doc.check_for_missing_values()
        except (RuntimeError, ValueError) as e:
            print('Missing value:')
            print(str(e))
            errlist = str(e).split(':')
            if len(errlist) > 1:
                show_general_warning(
                    "Attention CIF line {}: '{}' has no value.".format(errlist[1], errlist[2].split()[0]))

    def set_last_workdir(self):
        try:
            # loading last working directory:
            last = self.settings.load_last_workdir()
        except TypeError:
            last = ''
        if last and Path(last).exists():
            os.chdir(last)

    def set_path_display_in_file_selector(self, fname: str) -> None:
        if os.name == 'nt':
            self.ui.SelectCif_LineEdit.setText(str(WindowsPath(fname).resolve()))
        else:
            self.ui.SelectCif_LineEdit.setText(str(fname))

    def able_to_open(self, filepath: Path) -> bool:
        if not filepath.exists():
            show_general_warning("The file you tried to open does not exist!")
            return False
        if filepath.stat().st_size == 0:
            show_general_warning('This file has zero byte size!')
            return False
        return True

    def warn_about_bad_cif(self):
        show_general_warning("You have non-ascii characters like umlauts in the SHELX file "
                             "attached to this CIF.\n\n"
                             "FinalCif tries to convert them, but be warned "
                             "(they are not allowed in CIF1 files anyway).\n")

    def show_residuals(self) -> None:
        """
        show residuals of the cif file an a special page.
        """
        try:
            self.cif.fileobj
        except AttributeError:
            return
        self.ui.MainStackedWidget.go_to_info_page()
        self.ui.cellField.setText(celltxt.format(*self.cif.cell, self.cif['_space_group_centring_type']))
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
        if 'darwin' in sys.platform:
            self.ui.moleculeLayout.addWidget(QLabel('FinalCif is currently unable to draw molecules in MACOS'))
            print('Do not draw molecule on MACOS')
            # Currently, the QWebEngineView doesn't work  on macos due to pyinstaller issues.
            return None
        try:
            self.init_webview()
        except Exception as e:
            print(e, '###')
        # because this is fast with small structures and slow with large:
        self.view_molecule()

    def view_molecule(self) -> None:
        if self.ui.growCheckBox.isChecked():
            self.ui.molGroupBox.setTitle('Completed Molecule')
            atoms = list(self.cif.atoms_fract)
            if atoms:
                sdm = SDM(atoms, self.cif.symmops, self.cif.cell[:6], centric=self.cif.is_centrosymm)
                try:
                    needsymm = sdm.calc_sdm()
                    atoms = sdm.packer(sdm, needsymm)
                except Exception:
                    if DEBUG:
                        raise
                    atoms = []
        else:
            self.ui.molGroupBox.setTitle('Asymmetric Unit')
            atoms = self.cif.atoms_orth
        try:
            mol = ' '
            if atoms:
                mol = mol_file_writer.MolFile(atoms)
                mol = mol.make_mol()
        except (TypeError, KeyError):
            print("Error while writing mol file.")
            mol = ' '
            if DEBUG:
                raise
        content = write(mol, self.ui.molGroupBox.width() - 250,
                        self.ui.molGroupBox.height() - 250)
        Path(os.path.join(self.jsmoldir.name, "./jsmol.htm")).write_text(data=content, encoding="utf-8",
                                                                         errors='ignore')
        self.view.reload()

    def init_webview(self) -> None:
        """
        Initializes a QWebengine to view the molecule.
        """
        try:
            # Otherwise, the views accumulate:
            self.view.close()
            self.view = QtWebEngineWidgets.QWebEngineView(parent=self)
        except AttributeError:
            self.view = QtWebEngineWidgets.QWebEngineView(parent=self)
        self.jsmoldir = TemporaryDirectory()
        self.view.load(QtCore.QUrl.fromLocalFile(os.path.join(self.jsmoldir.name, "./jsmol.htm")))
        # This is a bit hacky, but it works fast:
        copy2(Path(finalcif.displaymol.__file__).parent.joinpath('jquery.min.js'), self.jsmoldir.name)
        copy2(Path(finalcif.displaymol.__file__).parent.joinpath('JSmol_dk.nojq.lite.js'), self.jsmoldir.name)
        self.ui.moleculeLayout.addWidget(self.view)
        self.view.heightForWidth(1)
        # noinspection PyUnresolvedReferences
        self.view.loadFinished.connect(self.on_webview_load_finished)

    def on_webview_load_finished(self) -> None:
        self.view.show()

    def redraw_molecule(self) -> None:
        if 'darwin' in sys.platform:
            print('Do not draw molecule on MACOS')
            # Currently, the QWebEngineView doesn't work  on macos due to pyinstaller issues.
            return None
        try:
            self.view_molecule()
        except Exception as e:
            print(e, ", unable to display molecule")
            if DEBUG:
                raise
            # self.write_empty_molfile()
            self.view.reload()

    def check_Z(self) -> None:
        """
        A crude check if Z is much too high e.g. a SEHLXT solution with "C H N O" sum formula.
        """
        Z = to_float(self.cif['_cell_formula_units_Z'])
        if not Z:
            Z = 1
        csystem = self.cif.crystal_system
        bad = False
        if Z and Z > 20.0 and (csystem == 'tricilinic' or csystem == 'monoclinic'):
            bad = True
        if Z and Z > 32.0 and (csystem == 'orthorhombic' or csystem == 'tetragonal' or csystem == 'trigonal'
                               or csystem == 'hexagonal' or csystem == 'cubic'):
            bad = True
        if bad:
            bad_z_message(Z)

    def get_data_sources(self) -> None:
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.
        """
        self.check_Z()
        self.sources = BrukerData(self, self.cif).sources
        if self.sources:
            # Add the CCDC number in case we have a deposition mail lying around:
            ccdc = CCDCMail(self.cif)
            if ccdc.depnum > 0:
                # The next line is necessary, otherwise reopening of a cif would not add the CCDC number:
                if not '_database_code_depnum_ccdc_archive' in self.ui.cif_main_table.vheaderitems:
                    # self.ui.cif_main_table.vheaderitems.insert(0, '_database_code_depnum_ccdc_archive')
                    self.add_row('_database_code_depnum_ccdc_archive', '', at_start=True)
                txt = self.ui.cif_main_table.getTextFromKey('_database_code_depnum_ccdc_archive', COL_EDIT).strip()
                if not txt or (txt == '?'):
                    self.sources['_database_code_depnum_ccdc_archive'] = (str(ccdc.depnum), str(ccdc.emlfile.name))
                    self.missing_data.add('_database_code_depnum_ccdc_archive')
        vheadlist = []
        for row_number in range(self.ui.cif_main_table.model().rowCount()):
            vheadlist.append(self.ui.cif_main_table.model().headerData(row_number, QtCore.Qt.Vertical))
        for src in self.sources:
            if not self.sources[src]:
                continue
            if src in vheadlist:
                # do not add keys twice
                continue
            if src and src not in self.missing_data:
                self.add_row(src, '?')
        self.refresh_combo_boxes()
        # Get missing items from sources and put them into the corresponding rows:
        # missing items will even be used if under the blue separation line:
        for miss_key in self.missing_data:
            # add missing item to data sources column:
            row_num = self.ui.cif_main_table.vheaderitems.index(miss_key)
            try:
                txt = str(self.sources[miss_key][0])
                if row_num > self.complete_data_row:
                    self.ui.cif_main_table.setText(key=miss_key, column=COL_DATA, txt=txt)
                else:
                    if txt and txt != '?':
                        self.ui.cif_main_table.setText(key=miss_key, column=COL_DATA, txt=txt, color=light_green)
                    else:
                        self.ui.cif_main_table.setText(key=miss_key, column=COL_DATA, txt=txt, color=yellow)
            except (KeyError, TypeError) as e:
                # TypeError my originate from incomplete self.missing_data list!
                # print(e, '##', miss_key)
                pass

    def refresh_combo_boxes(self):
        for row_number in range(self.ui.cif_main_table.model().rowCount()):
            vhead_key = self.ui.cif_main_table.model().headerData(row_number, QtCore.Qt.Vertical)
            if not vhead_key in self.ui.cif_main_table.vheaderitems:
                self.ui.cif_main_table.vheaderitems.append(vhead_key)
            # adding comboboxes:
            if vhead_key in self.settings.load_cif_keys_of_properties():
                # First add self-made properties:
                self.add_combobox(row_number, vhead_key)
            elif vhead_key in combobox_fields:
                # Then the pre-defined:
                self.ui.cif_main_table.add_property_combobox(combobox_fields[vhead_key], row_number)

    def add_combobox(self, num: int, vhead_key: str):
        """
        :param num: row number
        :param vhead_key: CIF keyword for combobox
        """
        properties_list = self.settings.load_property_values_by_key(vhead_key)
        if properties_list:
            self.ui.cif_main_table.add_property_combobox(properties_list, num)

    def fill_cif_table(self) -> None:
        """
        Adds the cif content to the main table. also add reference to FinalCif.
        """
        for key, value in self.cif.key_value_pairs():
            if not value or value == '?' or value == "'?'":
                self.missing_data.add(key)
                value = '?'
            self.add_row(key, value)
            if key == '_audit_creation_method':
                txt = 'FinalCif V{} by Daniel Kratzert, Freiburg {}, https://dkratzert.de/finalcif.html'
                strval = txt.format(VERSION, datetime.now().year)
                self.ui.cif_main_table.setText(key=key, column=COL_DATA, txt=strval)
            # print(key, value)
        if not self.cif.test_res_checksum():
            show_res_checksum_warning()
        if not self.cif.test_hkl_checksum():
            show_hkl_checksum_warning()
        self.get_data_sources()
        self.erase_disabled_items()
        self.ui.cif_main_table.setCurrentItem(None)

    def make_loops_tables(self) -> None:
        for _ in range(self.ui.LoopsTabWidget.count()):
            # I use this, so that always the first tab stays.
            self.ui.LoopsTabWidget.removeTab(1)
        if self.cif and self.cif.loops:
            self.add_loops_tables()

    def add_loops_tables(self) -> None:
        """
        Generates a list of tables containing the cif loops.
        """
        for num, loop in enumerate(self.cif.loops):
            tags = loop.tags
            if not tags or len(tags) < 1:
                continue
            loop = Loop(tags, values=grouper(loop.values, loop.width()),
                        parent=self.ui.LoopsTabWidget, block=self.cif.block)
            self.ui.LoopsTabWidget.addTab(loop.tableview, cif_to_header_label.get(tags[0]) or tags[0])
            self.ui.LoopsTabWidget.setTabToolTip(num + 1, tags[0])
            self.ui.revertLoopsPushButton.clicked.connect(loop.model.revert)
        if self.cif.res_file_data:
            self.add_res_file_to_loops()

    def add_res_file_to_loops(self):
        textedit = QPlainTextEdit()
        self.ui.LoopsTabWidget.addTab(textedit, 'SHELX res file')
        textedit.setPlainText(self.cif.res_file_data[1:-1])
        doc = textedit.document()
        font = doc.defaultFont()
        font.setFamily("Courier")
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setPointSize(14)
        doc.setDefaultFont(font)
        textedit.setLineWrapMode(QPlainTextEdit.NoWrap)
        textedit.setReadOnly(True)

    def add_row(self, key: str, value: str, at_start=False, position: Union[int, None] = None) -> None:
        """
        Create a empty row at bottom of cif_main_table. This method only fills cif data in the
        first column. Not the data from external sources!
        """
        if at_start:
            row_num = 0
        else:
            if position and position > 0:
                row_num = position
            else:
                row_num = self.ui.cif_main_table.rowCount()
        self.ui.cif_main_table.insertRow(row_num)
        if value is None:
            strval = '?'
        else:
            strval = str(value).strip(" ").strip("'").strip(';\n').strip('\r\n')  # or '?')
        if not key:
            strval = ''
        # All regular linedit fields:
        if key == "These below are already in:":
            self.ui.cif_main_table.add_separation_line(row_num)
            self.complete_data_row = row_num
        else:
            # Cif text is set here:
            self.ui.cif_main_table.setText(row=row_num, key=key, column=COL_CIF,
                                           txt='?' if at_start else retranslate_delimiter(strval))
            # This is to have COL_DATA at a defined state:
            self.ui.cif_main_table.setText(row=row_num, key=key, column=COL_DATA, txt='')
            self.ui.cif_main_table.setText(row=row_num, key=key, column=COL_EDIT,
                                           txt=retranslate_delimiter(strval) if at_start else '')
        head_item_key = MyTableWidgetItem(key)
        if not key == "These below are already in:":
            self.ui.cif_main_table.setVerticalHeaderItem(row_num, head_item_key)
        if not key in self.ui.cif_main_table.vheaderitems:
            self.ui.cif_main_table.vheaderitems.insert(row_num, key)
        if not key.startswith('_'):
            return
        if key not in self.cif.order:
            self.cif.order.insert(row_num, key)
        if not self.cif.block.find_value(key):
            self.cif[key] = value
