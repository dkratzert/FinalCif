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
from typing import Union, Dict, Tuple, List, Optional

import gemmi.cif
import qtawesome as qta
import requests
from PyQt5 import QtCore, QtGui, QtWebEngineWidgets
from PyQt5.QtCore import QThread, QTimer, Qt, QEvent
from PyQt5.QtWidgets import QMainWindow, QShortcut, QCheckBox, QListWidgetItem, QApplication, \
    QPlainTextEdit, QFileDialog, QMessageBox
from gemmi import cif
from qtpy.QtGui import QDesktopServices

from finalcif import VERSION
from finalcif.cif.checkcif.checkcif import MyHTMLParser, AlertHelp, CheckCif
from finalcif.cif.cif_file_io import CifContainer, GemmiError
from finalcif.cif.cod.deposit import CODdeposit
from finalcif.cif.text import utf8_to_str, quote
from finalcif.datafiles.bruker_data import BrukerData
from finalcif.datafiles.ccdc_mail import CCDCMail
from finalcif.displaymol.sdm import SDM
from finalcif.equip_property.author_loop_templates import AuthorLoops
from finalcif.equip_property.equipment import Equipment
from finalcif.equip_property.properties import Properties
from finalcif.equip_property.tools import read_document_from_cif_file
from finalcif.gui.custom_classes import Column, MyTableWidgetItem, light_green, yellow, light_blue, \
    white
from finalcif.gui.dialogs import show_update_warning, unable_to_open_message, show_general_warning, \
    cif_file_open_dialog, \
    bad_z_message, show_res_checksum_warning, show_hkl_checksum_warning, cif_file_save_dialog, show_yes_now_question
from finalcif.gui.finalcif_gui_ui import Ui_FinalCifWindow
from finalcif.gui.loop_creator import LoopCreator
from finalcif.gui.loops import Loop
from finalcif.gui.plaintextedit import MyQPlainTextEdit
from finalcif.gui.text_value_editor import MyTextTemplateEdit, TextEditItem
from finalcif.gui.vrf_classes import MyVRFContainer, VREF
from finalcif.report.archive_report import ArchiveReport
from finalcif.report.tables import make_report_from, make_multi_tables
from finalcif.report.templated_report import TemplatedReport
from finalcif.template.templates import ReportTemplates
from finalcif.tools.download import MyDownloader, start_worker
from finalcif.tools.dsrmath import my_isnumeric
from finalcif.tools.misc import next_path, do_not_import_keys, celltxt, to_float, do_not_import_from_stoe_cfx, \
    cif_to_header_label, grouper, is_database_number, file_age_in_days, open_file, \
    strip_finalcif_of_name
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

    def __init__(self, file: Optional[Path] = None, unit_test: bool = False):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # This prevents some things to happen during unit tests:
        # Open of target dir of shred cif,
        # open report doc,
        # get check.def from platon server
        self.running_inside_unit_test = unit_test
        self.sources: Optional[Dict[str, Tuple[Optional[str]]]] = None
        self.cif: Optional[CifContainer] = None
        self.report_picture_path: Optional[Path] = None
        self.loopcreate: Optional[LoopCreator] = None
        self.checkdef = []
        self.changes_answer: int = 0
        self.validation_response_forms_list = []
        self.checkdef_file: Path = Path.home().joinpath('check.def')
        self.missing_data: set = set()
        self.temperature_warning_displayed = False
        self.threadpool = []
        # True if line with "these are already in" reached:
        self.complete_data_row = -1
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.ui.page_MainTable.setParent(self.ui.MainStackedWidget)
        self.settings = FinalCifSettings()
        self.options = Options(self.ui, self.settings)
        self.deposit = CODdeposit(self.ui, self.cif, self.options)
        self.equipment = Equipment(app=self, settings=self.settings)
        self.properties = Properties(app=self, settings=self.settings)
        self.status_bar = StatusBar(ui=self.ui)
        self.status_bar.show_message('FinalCif version {}'.format(VERSION))
        self.authors: Optional[AuthorLoops] = None
        self.set_window_size_and_position()
        self.ui.cif_main_table.installEventFilter(self)
        # Sorting desynchronized header and columns:
        self.ui.cif_main_table.setSortingEnabled(False)
        self.ui.cif_main_table.distribute_cif_main_table_columns_evenly()
        # Make sure the start page is shown and not the edit page:
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(0)
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)
        self.ui.MainStackedWidget.got_to_main_page()
        self.set_initial_button_states()
        if len(sys.argv) > 1 and not file:
            self.load_cif_file(Path(sys.argv[1]))
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
        self.textedit = MyTextTemplateEdit(parent=self)
        self.ui.page_textTemplate.layout().addWidget(self.textedit)
        #
        self.connect_signals_and_slots()
        with suppress(Exception):
            self.make_button_icons()
        self.format_report_button()
        self.set_font_sizes()

    def set_initial_button_states(self) -> None:
        self.ui.appendCifPushButton.setDisabled(True)
        self.ui.PictureWidthDoubleSpinBox.setRange(0.0, 25)
        self.ui.PictureWidthDoubleSpinBox.setSingleStep(0.5)
        # Just too slow for large structures:
        self.ui.growCheckBox.setChecked(False)
        self.ui.CheckcifButton.setDisabled(True)
        self.ui.CheckcifStartButton.setDisabled(True)
        self.ui.ReportPicPushButton.setDisabled(True)
        self.ui.SaveFullReportButton.setDisabled(True)
        self.ui.CheckcifHTMLOnlineButton.setDisabled(True)
        self.ui.CheckcifPDFOnlineButton.setDisabled(True)
        self.ui.SaveCifButton.setDisabled(True)
        self.ui.ExploreDirButton.setDisabled(True)
        self.ui.DetailsPushButton.setDisabled(True)
        self.ui.SourcesPushButton.setDisabled(True)
        self.ui.OptionsPushButton.setEnabled(True)
        self.ui.ImportCifPushButton.setDisabled(True)
        self.ui.CODpushButton.setDisabled(True)
        self.ui.CCDCpushButton.setDisabled(True)
        self.ui.ShredCifButton.setDisabled(True)
        self.ui.LoopsPushButton.setDisabled(True)

    def enable_buttons(self):
        self.ui.appendCifPushButton.setEnabled(True)
        self.ui.CheckcifButton.setEnabled(True)
        self.ui.CheckcifStartButton.setEnabled(True)
        self.ui.ReportPicPushButton.setEnabled(True)
        self.ui.SaveFullReportButton.setEnabled(True)
        self.ui.CheckcifHTMLOnlineButton.setEnabled(True)
        self.ui.CheckcifPDFOnlineButton.setEnabled(True)
        self.ui.SaveCifButton.setEnabled(True)
        self.ui.ExploreDirButton.setEnabled(True)
        self.ui.DetailsPushButton.setEnabled(True)
        self.ui.SourcesPushButton.setEnabled(True)
        self.ui.OptionsPushButton.setEnabled(True)
        self.ui.ImportCifPushButton.setEnabled(True)
        self.ui.CODpushButton.setEnabled(True)
        self.ui.CCDCpushButton.setEnabled(True)
        self.ui.LoopsPushButton.setEnabled(True)
        if self.cif.is_multi_cif:
            self.ui.CODpushButton.setDisabled(True)
        else:
            self.ui.CODpushButton.setEnabled(True)

    def set_font_sizes(self):
        large_font = QtGui.QFont()
        ps = large_font.pointSize()
        large_font.setPointSize(int(ps + ps * 0.38))
        mid_font = QtGui.QFont()
        ps = mid_font.pointSize()
        mid_font.setPointSize(int(ps + ps * 0.3))
        if sys.platform.startswith('win'):
            self.ui.datanameComboBox.setFont(large_font)
            self.ui.Spacegroup_top_LineEdit.setFont(large_font)
            self.ui.CCDCNumLineEdit.setFont(large_font)
            self.ui.SumFormMainLineEdit.setFont(large_font)
            self.ui.EquipmentTemplatesListWidget.setFont(mid_font)
            self.ui.docxTemplatesListWidget.setFont(mid_font)
            self.ui.PropertiesTemplatesListWidget.setFont(mid_font)
            self.ui.depositOutputTextBrowser.setFont(mid_font)

    def format_report_button(self):
        if self.report_without_template():
            self.ui.SaveFullReportButton.setText('Make Report')
        else:
            self.ui.SaveFullReportButton.setText('Make Report from Template')

    def set_window_size_and_position(self) -> None:
        wsettings = self.settings.load_window_position()
        with suppress(TypeError):
            self.resize(wsettings['size'])
        with suppress(TypeError):
            self.move(wsettings['position'])
        if wsettings['maximized']:
            self.showMaximized()

    def make_button_icons(self) -> None:
        self.ui.CheckcifButton.setIcon(qta.icon('mdi.file-document-outline'))
        self.ui.CheckcifStartButton.setIcon(qta.icon('mdi.file-document-outline'))
        self.ui.LoopsPushButton.setIcon(qta.icon('mdi.table'))
        self.ui.CheckcifHTMLOnlineButton.setIcon(qta.icon('mdi.comment-check-outline'))
        self.ui.CheckcifPDFOnlineButton.setIcon(qta.icon('mdi.comment-check'))
        with suppress(Exception):
            self.ui.SaveFullReportButton.setIcon(qta.icon('mdi.file-table-outline'))
        try:
            self.ui.ExploreDirButton.setIcon(qta.icon('ph.folder-open'))
        except Exception:
            self.ui.ExploreDirButton.setIcon(qta.icon('mdi.folder-open-outline'))
        self.ui.SaveCifButton.setIcon(qta.icon('fa5.save'))
        self.ui.SelectCif_PushButton.setIcon(qta.icon('fa.file-text-o', options=[{'color': 'darkgreen'}]))
        try:
            self.ui.AuthorEditPushButton.setIcon(qta.icon('ph.users-three-bold'))
        except Exception:
            self.ui.AuthorEditPushButton.setIcon(qta.icon('fa5s.users'))
        try:
            self.ui.SourcesPushButton.setIcon(qta.icon('ph.list-bullets-bold'))
        except Exception:
            self.ui.SourcesPushButton.setIcon(qta.icon('fa5s.list-ul'))
        try:
            self.ui.OptionsPushButton.setIcon(qta.icon('ph.gear'))
        except Exception:
            self.ui.OptionsPushButton.setIcon(qta.icon('fa.gear'))
        try:
            self.ui.ShredCifButton.setIcon(qta.icon('ph.files-bold'))
        except Exception:
            self.ui.ShredCifButton.setIcon(qta.icon('fa.files-o'))
        try:
            self.ui.DetailsPushButton.setIcon(qta.icon('ph.bird-bold'))
        except Exception:
            self.ui.DetailsPushButton.setIcon(qta.icon('fa5s.kiwi-bird'))
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
        try:
            self.ui.CCDCpushButton.setIcon(qta.icon('ph.upload-simple-bold'))
        except Exception:
            self.ui.CCDCpushButton.setIcon(qta.icon('fa5s.cloud-upload-alt'))
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
        self.textedit.ui.cancelTextPushButton.setIcon(qta.icon('mdi.keyboard-backspace'))
        try:
            self.textedit.ui.applyTextPushButton.setIcon(qta.icon('ph.check-bold'))
        except Exception:
            self.textedit.ui.applyTextPushButton.setIcon(qta.icon('fa.check'))
        self.textedit.ui.exportTextPushButton.setIcon(qta.icon('mdi.export'))
        self.textedit.ui.savePushButton.setIcon(qta.icon('mdi.content-save'))
        self.textedit.ui.deletePushButton.setIcon(qta.icon('mdi.playlist-minus'))
        self.textedit.ui.importPushButton.setIcon(qta.icon('mdi.import'))
        #
        try:
            self.ui.SaveAuthorLoopToTemplateButton.setIcon(qta.icon('mdi.badge-account-outline'))
        except Exception:
            self.ui.SaveAuthorLoopToTemplateButton.setIcon(qta.icon('fa.id-badge'))
        try:
            self.ui.AddThisAuthorToLoopPushButton.setIcon(qta.icon('mdi.folder-table-outline'))
        except Exception:
            self.ui.AddThisAuthorToLoopPushButton.setIcon(qta.icon('mdi.file-table-outline'))
        with suppress(Exception):
            self.ui.DeleteLoopAuthorTemplateButton.setIcon(qta.icon('mdi.delete-forever-outline'))

    def connect_signals_and_slots(self) -> None:
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        self.ui.datanameComboBox.currentIndexChanged.connect(self._load_block)
        ## main
        self.ui.BackPushButton.clicked.connect(self.back_to_main)
        self.ui.BackFromDepositPushButton.clicked.connect(self.back_to_main)
        self.ui.ExploreDirButton.clicked.connect(self.explore_current_dir)
        self.ui.LoopsPushButton.clicked.connect(self.ui.MainStackedWidget.go_to_loops_page)
        self.ui.LoopsPushButton.clicked.connect(
            lambda x: self.ui.LoopsTabWidget.setCurrentIndex(1) if self.ui.LoopsTabWidget.count() > 0 else None)
        self.ui.LoopsPushButton.clicked.connect(lambda x: self.ui.TemplatesStackedWidget.setCurrentIndex(1))
        self.ui.AuthorEditPushButton.clicked.connect(self.ui.MainStackedWidget.go_to_loops_page)
        self.ui.AuthorEditPushButton.clicked.connect(lambda x: self.ui.TemplatesStackedWidget.setCurrentIndex(1))
        self.ui.AuthorEditPushButton.clicked.connect(lambda x: self.ui.LoopsTabWidget.setCurrentIndex(0))
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
        self.ui.CCDCpushButton.clicked.connect(self._ccdc_deposit)
        self.ui.newLoopPushButton.clicked.connect(self._go_to_new_loop_page)
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
        self.ui.labelsCheckBox.toggled.connect(self.show_labels)
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
        self.ui.ReportPicPushButton.clicked.connect(self.select_report_picture)
        # brings the html checkcif in from in order to avoid confusion of an "empty" checkcif report page:
        self.ui.CheckCIFResultsTabWidget.currentChanged.connect(lambda: self.ui.ResponsesTabWidget.setCurrentIndex(0))
        ##
        self.ui.SelectCif_LineEdit.returnPressed.connect(self.check_if_file_field_contains_database_number)
        self.ui.fullIucrCheckBox.clicked.connect(self.toggle_hkl_option)
        self.ui.structfactCheckBox.clicked.connect(self.toggle_iucr_option)
        # text templates
        self.textedit.ui.cancelTextPushButton.clicked.connect(self.back_to_main_noload)
        self.textedit.ui.applyTextPushButton.clicked.connect(self.apply_text_template)
        self.textedit.ui.exportTextPushButton.clicked.connect(self.export_text_template)
        self.textedit.ui.savePushButton.clicked.connect(self.save_text_template)
        self.textedit.ui.deletePushButton.clicked.connect(self.delete_text_template)
        self.textedit.ui.importPushButton.clicked.connect(self.import_text_template)
        self.ui.cif_main_table.textTemplate.connect(self.on_text_template_open)
        # value has to be '?', because otherwise it adds a key without a value:
        self.ui.cif_main_table.new_key.connect(lambda x: self.add_row(key=x, value='?', at_start=True))
        #
        self.ui.appendCifPushButton.clicked.connect(self.append_cif)
        self.ui.drawImagePushButton.clicked.connect(self.draw_image)
        #
        self.ui.ExportAllTemplatesPushButton.clicked.connect(self.export_all_templates)
        self.ui.ImportAllTemplatesPushButton.clicked.connect(self.import_all_templates)
        #
        self.ui.searchMainTableLineEdit.textChanged.connect(self.ui.cif_main_table.search)

    @property
    def finalcif_changes_filename(self):
        return self.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif_changes.cif', force_strip=True)

    def export_all_templates(self, filename: Path = None):
        import pickle
        if not filename:
            filename, _ = QFileDialog.getSaveFileName(directory=str(Path(self.get_last_workdir()).joinpath(
                f'finalcif_templates_{time.strftime("%Y-%m-%d")}.dat')),
                initialFilter="Template File (*.dat)",
                filter="Template File (*.dat)",
                caption='Save templates')
        if not filename:
            return
        templates = {'text'      : self.export_raw_text_templates(),
                     'equipment' : self.equipment.export_raw_data(),
                     'properties': self.properties.export_raw_data(),
                     'authors'   : self.authors.export_raw_data(),
                     }
        try:
            pickle.dump(templates, open(filename, "wb"))
        except pickle.PickleError as e:
            self.status_bar.show_message(f'Saving templates failed: {str(e)}')

    def import_all_templates(self, filename: Path = None):
        import pickle
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(directory=self.get_last_workdir(),
                                                      initialFilter="Template File (*.dat)",
                                                      filter="Template File (*.dat)",
                                                      caption='Save templates')
        if not filename:
            return
        try:
            templates = pickle.load(open(filename, "rb"))
        except pickle.PickleError:
            return
        self.import_raw_text_templates(templates.get('text'))
        self.equipment.import_raw_data(templates.get('equipment'))
        self.properties.import_raw_data(templates.get('properties'))
        self.authors.import_raw_data(templates.get('authors'))
        self.status_bar.show_message('Template import successful.')

    def draw_image(self):
        image_filename = self.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif.png')
        self.ui.render_widget.save_image(image_filename)
        self.status_bar.show_message('Image saved to {}'.format(image_filename), timeout=20)
        self.set_report_picture_path(str(image_filename))

    def on_text_template_open(self, row: int):
        self.ui.cif_main_table.setCurrentCell(row, Column.EDIT)
        cif_key = self.ui.cif_main_table.vheaderitems[row]
        self.textedit.cif_key = cif_key
        if cif_key.startswith('_vrf_'):
            # _vrf_DIFF003_cifname
            self.textedit.ui.cifKeyLineEdit.setText(self.get_vrf_errortype(cif_key))
            self.textedit.add_textfields(
                self.settings.load_settings_list('text_templates', self.get_vrf_errortype(cif_key)))
            self.textedit.ui.plainTextEdit.setPlainText(self.ui.cif_main_table.getText(row, Column.CIF))
        else:
            self.textedit.ui.cifKeyLineEdit.setText(cif_key)
            self.textedit.add_textfields(self.settings.load_settings_list('text_templates', cif_key))
        edit_text = self.ui.cif_main_table.getText(row, Column.EDIT)
        if not self.textedit.ui.plainTextEdit.toPlainText():
            self.textedit.ui.plainTextEdit.setPlainText(edit_text)

    @staticmethod
    def get_vrf_errortype(cif_key: str) -> str:
        if cif_key.startswith('_vrf_'):
            splitkey = cif_key.split('_')
            if len(splitkey) > 2:
                return '_'.join(splitkey[:3])
            return cif_key
        else:
            return cif_key

    def import_text_template(self):
        """
        Imports a text template from a CIF file.
        """
        filename = cif_file_open_dialog()
        if not filename:
            return
        try:
            doc = read_document_from_cif_file(filename)
            block: gemmi.cif.Block = doc.sole_block()
        except Exception:
            show_general_warning('This file is not readable.')
            return
        text_list = []
        for i in block:
            if i.loop is not None:
                if len(i.loop.tags) > 0:
                    loop_column_name = i.loop.tags[0]
                    self.textedit.ui.cifKeyLineEdit.setText(loop_column_name)
                for n in range(i.loop.length()):
                    value = i.loop.val(n, 0)
                    text_list.append(gemmi.cif.as_string(value))
        self.textedit.add_textfields(text_list)

    def export_text_template(self) -> None:
        """
        Use texts from self.textedit.ui.listWidget and save in a CIF as loop.
        """
        textlist = self.textedit.get_template_texts()
        doc = cif.Document()
        blockname = self.textedit.ui.cifKeyLineEdit.text()
        block = doc.add_new_block(blockname)
        try:
            loop = block.init_loop(blockname, [''])
        except RuntimeError:
            # Not a valid loop key
            show_general_warning('"{}" is not a valid cif keyword.'.format(blockname))
            return
        for value in textlist:
            if value:
                loop.add_row([cif.quote(utf8_to_str(value))])
        filename = cif_file_save_dialog(blockname + '_template.cif')
        if not filename.strip():
            return
        try:
            doc.write_file(filename, style=cif.Style.Indent35)
            # Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning('No permission to write file to {}'.format(Path(filename).resolve()))
        self.status_bar.show_message(f'Template exported to {filename}.', timeout=10)

    def delete_text_template(self) -> None:
        """
        Delete template from settings.
        """
        cif_key = self.get_vrf_errortype(self.textedit.cif_key)
        txt = f'Do you really want to delete all template texts for {cif_key}?'
        answer = show_yes_now_question(title='Delete templates', question=txt, parent=self)
        if not answer:
            return
        self.settings.delete_template('text_templates/', cif_key)
        self.back_to_main_noload()
        TextEditItem._num = 1
        self.status_bar.show_message(f'Template for {cif_key} deleted.', timeout=10)
        self.textedit.clear_fields()
        self.refresh_color_background_from_templates()

    def save_text_template(self) -> None:
        """
        Save template in settings.
        """
        cif_key = self.get_vrf_errortype(self.textedit.cif_key)
        table_data = self.textedit.get_template_texts()
        self.settings.save_settings_list(property='text_templates', name=cif_key, items=table_data)
        self.status_bar.show_message(f'Template for {cif_key} saved.', timeout=10)
        self.refresh_color_background_from_templates()

    def export_raw_text_templates(self) -> List[Dict]:
        templates_list = []
        for cif_key in self.settings.list_saved_items('text_templates'):
            template = self.settings.load_settings_list('text_templates', cif_key)
            templates_list.append({'cif_key': cif_key, 'data': template})
        return templates_list

    def import_raw_text_templates(self, templates_list: List[Dict]):
        for template in templates_list:
            self.settings.save_settings_list(property='text_templates', name=template.get("cif_key"),
                                             items=template.get("data"))
        self.refresh_color_background_from_templates()

    def apply_text_template(self) -> None:
        """
        Use text from self.textedit.ui.plainTextEdit and fill it into current cell. Then go back to
        main table. And scroll to changed row.
        """
        text = self.textedit.ui.plainTextEdit.toPlainText()
        if text:
            TextEditItem._num = 1
            self.ui.cif_main_table.setText(key=self.textedit.cif_key, column=Column.EDIT, txt=text)
            self.ui.MainStackedWidget.got_to_main_page()
            self.textedit.clear_fields()
        else:
            self.status_bar.show_message('No combined text to apply.')

    def toggle_hkl_option(self, iucr_is_checked: bool) -> None:
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
            self.status_bar.show_message('Request sent to COD...')
            r = requests.get(f'{self.deposit.main_url}{input_txt}.cif', timeout=8)
            self.status_bar.show_message('Got a result.')
            if r.status_code == 200:
                filename = cif_file_save_dialog(f'{input_txt}.cif')
                Path(filename).write_bytes(r.content)
                r.close()
                self.load_cif_file(Path(filename))
            else:
                # self.ui.SelectCif_LineEdit.setText('')
                self.status_bar.show_message(f'No COD entry for {input_txt} found.')
        else:
            self.status_bar.show_message('Not a valid COD number. It must be seven digits.')

    @property
    def current_block(self) -> int:
        return self.ui.datanameComboBox.currentIndex()

    def open_cod_page(self) -> None:
        self.save_current_cif_file()
        self.load_cif_file(self.cif.finalcif_file, self.current_block, load_changes=False)
        self.deposit.cif = self.cif
        self.ui.MainStackedWidget.setCurrentIndex(7)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Escape and self.ui.searchMainTableLineEdit.hasFocus():
                self.ui.searchMainTableLineEdit.clear()
        return super().event(event)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """It called when the main window resizes."""
        super(AppWindow, self).resizeEvent(a0)
        with suppress(AttributeError):
            self._savesize()
        main_width = self.ui.Mainwidget.width()
        left_frame = main_width * 0.22
        if left_frame <= 300:
            left_frame = 300
        self.ui.LeftFrame.setMinimumWidth(int(left_frame))
        QtCore.QTimer.singleShot(0, self.ui.cif_main_table.resizeRowsToContents)

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        """Is called when the main window moves."""
        super(AppWindow, self).moveEvent(a0)
        with suppress(AttributeError):
            self._savesize()

    def changeEvent(self, event: QtCore.QEvent) -> None:
        """Is called when the main window changes its state."""
        if event.type() == QtCore.QEvent.WindowStateChange:
            with suppress(AttributeError):
                self._savesize()

    def _savesize(self) -> None:
        """Saves the main window size nd position."""
        x, y = self.pos().x(), self.pos().y()
        self.settings.save_window_position(QtCore.QPoint(x, y), self.size(), self.isMaximized())

    def show_help(self) -> None:
        QDesktopServices.openUrl(QtCore.QUrl('https://dkratzert.de/files/finalcif/docs/'))

    def do_shred_cif(self):
        shred = ShredCIF(cif=self.cif, statusbar=self.status_bar)
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
        Deletes a row of the main table.
        """
        del self.cif[key]
        # Only delete from changes cif if changes were loaded:
        if self.options.track_changes and self.changes_answer == QMessageBox.Yes:
            self.delete_key_from_changes_cif(key)

    def delete_key_from_changes_cif(self, key):
        changes_cif = self.get_changes_cif(self.finalcif_changes_filename)
        del changes_cif[key]
        if changes_cif.is_empty():
            changes_cif.fileobj.unlink(missing_ok=True)
            return
        changes_cif.save(self.finalcif_changes_filename)

    def check_for_update_version(self) -> None:
        if os.environ.get('NO_NETWORK'):
            print('Skipping version.txt download because NO_NETWORK variable is set.')
            return
        mainurl = "https://dkratzert.de/files/finalcif/version.txt"
        self.upd = MyDownloader(mainurl, parent=None)
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
                self.cif.block.set_pair(cifkey, '?')
                self.ui.cif_main_table.setText(key=cifkey, column=Column.CIF, txt='?')
                self.ui.cif_main_table.setText(key=cifkey, column=Column.DATA, txt='?')

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
        self.updc = MyDownloader(url, parent=None)
        checkdef_thread = QThread(parent=self)
        self.threadpool.append(checkdef_thread)
        start_worker(self.updc, checkdef_thread, onload=self._save_checkdef)

    def _save_checkdef(self, reply: bytes) -> None:
        """
        Is called by the finished signal from the downloader.
        """
        with suppress(Exception):
            self.checkdef_file.write_bytes(reply)
        self.checkdef = reply.decode('ascii', errors='ignore').splitlines(keepends=False)

    def explore_current_dir(self) -> None:
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
        if ending.lower() == '.cif':
            self.load_cif_file(Path(final_path))

    def back_to_main(self):
        """
        Get back to the main table and load the new cif file.
        """
        self.load_cif_file(filepath=self.cif.finalcif_file, load_changes=False)
        self.ui.MainStackedWidget.got_to_main_page()
        self.ui.cif_main_table.scrollToTop()
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)
        self.ui.cif_main_table.resizeRowsToContents()
        self.ui.revertLoopsPushButton.show()
        self.ui.newLoopPushButton.show()

    def back_to_main_noload(self) -> None:
        """
        Get back to the main table. Without loading a new cif file.
        """
        self.status_bar.show_message('')
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)
        self.ui.MainStackedWidget.got_to_main_page()
        self.format_report_button()
        self.ui.revertLoopsPushButton.show()
        self.ui.newLoopPushButton.show()

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
        imageobj = self.cif.finalcif_file.with_suffix('.gif')
        gif = parser.get_image()
        self.ui.CheckCifLogPlainTextEdit.appendPlainText('CheckCIF Report finished.')
        forms = parser.response_forms
        # makes all gray:
        # self.ui.responseFormsListWidget.setStyleSheet("background: 'gray';")
        a = AlertHelp(self.checkdef)
        self.validation_response_forms_list = []
        self.ui.responseFormsListWidget.clear()
        for form in forms:
            vrf = MyVRFContainer(form, a.get_help(form['alert_num']), parent=self, is_multi_cif=self.cif.is_multi_cif)
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
        current_block = self.ui.datanameComboBox.currentIndex()
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
        self.load_cif_file(self.cif.finalcif_file, block=current_block, load_changes=False)
        self.htmlfile = self.cif.finalcif_file_prefixed(prefix='checkcif-', suffix='-finalcif.html')
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
        current_block = self.ui.datanameComboBox.currentIndex()
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
            v.data_name = response_row.form['data_name']
            for block in self.cif.doc:
                if block.name == v.data_name:
                    block.set_pair(v.key, quote(utf8_to_str(v.value)))
        self.save_current_cif_file()
        self.load_cif_file(self.cif.finalcif_file, current_block, load_changes=False)
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
        current_block = self.ui.datanameComboBox.currentIndex()
        self.ui.CheckCifLogPlainTextEdit.clear()
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(2)
        if not self.save_current_cif_file():
            self.ui.CheckCifLogPlainTextEdit.appendHtml('<b>Unable to save CIF file. Aborting action...</b>')
            return None
        self.load_cif_file(self.cif.finalcif_file, current_block, load_changes=False)
        htmlfile = self.cif.finalcif_file_prefixed(prefix='checkpdf-', suffix='.html')
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
        current_block = self.ui.datanameComboBox.currentIndex()
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
        self.load_cif_file(self.cif.finalcif_file, block=current_block, load_changes=False)
        self.ui.MainStackedWidget.go_to_checkcif_page()
        QApplication.processEvents()
        timeout = 350
        try:
            p = Platon(self.cif.fileobj.resolve(), timeout, '-u')
        except Exception as e:
            print(e)
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
            vrf_txt = self.cif.finalcif_file.with_suffix('.vrf').read_text()
        if p.chk_file_text:
            with suppress(AttributeError):
                checkcif_out.appendPlainText(p.chk_file_text)
                checkcif_out.appendPlainText('\n' + '#' * 27 + ' Validation Response Forms ' + '#' * 26 + '\n')
                checkcif_out.appendPlainText(vrf_txt)
        checkcif_out.verticalScrollBar().setValue(0)
        moiety = self.ui.cif_main_table.getTextFromKey(key='_chemical_formula_moiety', col=0)
        if p.formula_moiety and moiety in ['', '?'] and not self.cif.is_multi_cif:
            self.ui.cif_main_table.setText(key='_chemical_formula_moiety', txt=p.formula_moiety, column=Column.EDIT)
        print('Killing platon!')
        p.kill()
        p.delete_orphaned_files()

    def wait_for_chk_file(self, p) -> bool:
        time.sleep(2)
        stop = 0
        while not p.chkfile.exists():
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
        if not self.cif.finalcif_file.with_suffix('.chk').exists():
            self.ui.CheckCifLogPlainTextEdit.appendPlainText('Platon returned no output.')
            QApplication.processEvents()
            return
        with suppress(FileNotFoundError):
            while self.cif.finalcif_file.with_suffix('.chk').stat().st_size < 200:
                self.append_to_ciflog_without_newline('*')
                QApplication.processEvents()
                if stop == timeout:
                    self.ui.CheckcifPlaintextEdit.appendPlainText('PLATON timed out')
                    break
                time.sleep(1)
                stop += 1
            time.sleep(0.5)

    def set_checkcif_output_font(self, ccpe: 'QPlainTextEdit') -> None:
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

    def select_report_picture(self, file: Path) -> None:
        """Sets the picture of the report document."""
        if file:
            self.report_picture_path = Path(file)
        else:
            filename, _ = QFileDialog.getOpenFileName(filter="Image Files (*.png *.jpg *.jpeg *.bmp "
                                                             "*.gif *.tif *.tiff *.eps *.emf *.wmf)",
                                                      caption='Open a Report Picture')
            self.set_report_picture_path(filename)

    def set_report_picture_path(self, filename: str):
        with suppress(Exception):
            self.report_picture_path = Path(filename)
        if self.report_picture_path.exists() and self.report_picture_path.is_file():
            with suppress(Exception):
                self.set_picture_button_icon()

    def set_picture_button_icon(self):
        try:
            self.ui.ReportPicPushButton.setIcon(qta.icon('ph.image-bold'))
        except Exception:
            self.ui.ReportPicPushButton.setIcon(qta.icon('fa.image'))

    def get_checked_templates_list_text(self) -> str:
        for index in range(self.ui.docxTemplatesListWidget.count()):
            item = self.ui.docxTemplatesListWidget.item(index)
            if item.checkState() == Qt.Checked:
                return item.text()

    def make_report_tables(self) -> None:
        """
        Generates a report document.
        """
        current_block = self.ui.datanameComboBox.currentIndex()
        if self.cif.doc[current_block].name == 'global':
            return
        not_ok = None
        if not self.cif:
            return None
        if not self.save_current_cif_file():
            return None
        self.load_cif_file(self.cif.finalcif_file, block=current_block, load_changes=False)
        report_filename = self.cif.finalcif_file_prefixed(prefix='report_', suffix='-finalcif.docx')
        multi_table_document = self.cif.finalcif_file_prefixed(prefix='', suffix='-multitable.docx')
        # The picture after the header:
        if self.report_picture_path:
            picfile = self.report_picture_path
        else:
            picfile = self.cif.finalcif_file.with_suffix('.gif')
        try:
            if self.report_without_template():
                print('Report without templates')
                make_report_from(options=self.options, cif=self.cif,
                                 output_filename=str(report_filename), picfile=picfile)
            else:
                print('Report with templates')
                t = TemplatedReport()
                t.make_templated_report(options=self.options, cif=self.cif,
                                        output_filename=str(report_filename), picfile=picfile,
                                        template_path=Path(self.get_checked_templates_list_text()))
            if self.cif.is_multi_cif and self.cif.doc[0].name != 'global':
                make_multi_tables(cif=self.cif, output_filename=str(multi_table_document))
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
                                 'Is the file already opened?'.format(report_filename.name))
            return
        if not self.running_inside_unit_test:
            self.open_report_document(report_filename, multi_table_document)
        # Save report and other files to a zip file:
        self.zip_report(report_filename)

    def report_without_template(self) -> bool:
        """Check whether the report is generated from a template or hard-coded"""
        return self.ui.docxTemplatesListWidget.item(0).checkState() == Qt.CheckState.Checked \
            or not self.ui.docxTemplatesListWidget.currentItem()

    def zip_report(self, report_filename: Path) -> None:
        zipfile = self.cif.finalcif_file.with_suffix('.zip')
        if zipfile.exists():
            zipname = next_path(zipfile.stem + '-%s.zip')
            zipfile = zipfile.parent.joinpath(zipname)
        with suppress(Exception):
            arc = ArchiveReport(zipfile)
        with suppress(Exception):
            arc.zip.write(filename=report_filename, arcname=report_filename.name)
        with suppress(Exception):
            arc.zip.write(filename=self.cif.finalcif_file, arcname=self.cif.finalcif_file.name)
        with suppress(Exception):
            pdfname = self.cif.finalcif_file_prefixed(prefix='checkcif-', suffix='-finalcif.pdf')
            arc.zip.write(filename=pdfname, arcname=pdfname.name)
        with suppress(Exception):
            multitable = self.cif.finalcif_file_prefixed(prefix='', suffix='-multitable.docx')
            arc.zip.write(filename=multitable, arcname=multitable.name)

    def open_report_document(self, report_filename: Path, multi_table_document: Path) -> None:
        if self.cif.is_multi_cif:
            open_file(multi_table_document)
        open_file(report_filename)

    def save_current_recent_files_list(self, filename: Path) -> None:
        """
        Saves the list of the recently opened files. Non-existent files are removed.
        """
        if os.name == 'nt':
            # Use path with backslash for Windows systems:
            filename: str = str(WindowsPath(filename.resolve()).absolute())
        else:
            filename: str = str(Path(filename.resolve()).absolute())
        recent = list(self.settings.settings.value('recent_files', type=list))
        # delete possible previous occurrence of new file:
        while filename in recent:
            recent.remove(filename)
        # file has to be str not Path():
        recent.insert(0, filename)
        recent = recent[:10]
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

    def save_current_cif_file(self) -> Union[bool, None]:
        """
        Saves the current cif file and stores the information of the third column.
        """
        if not self.cif:
            # No file is opened
            return None
        self.cif.rename_data_name(''.join(self.ui.datanameComboBox.currentText().split(' ')))
        self.store_data_from_table_rows()
        self.save_ccdc_number()
        try:
            self.cif.save()
            self.status_bar.show_message('  File Saved:  {}'.format(self.cif.finalcif_file), 10)
            print('File saved ...')
            return True
        except Exception as e:
            print('Unable to save file:')
            print(e)
            show_general_warning('Can not save file: ' + str(e))
            return False

    def store_data_from_table_rows(self) -> None:
        """
        Stores the data from the main table in the cif object.
        """
        changes_cif: Optional[CifContainer] = None
        if self.options.track_changes:
            try:
                changes_cif = self.get_changes_cif(self.finalcif_changes_filename)
            except Exception as e:
                print('Unable to create changes CIF:', e)
                unable_to_open_message(filepath=self.finalcif_changes_filename, not_ok=e)
                changes_cif = None
        # makes sure also the currently edited item is saved:
        self.ui.cif_main_table.setCurrentItem(None)
        for row in range(self.ui.cif_main_table.rows_count):
            vhead = self.ui.cif_main_table.vheader_text(row)
            if not self.is_row_a_cif_item(vhead):
                continue
            col_data = self.ui.cif_main_table.text(row, Column.DATA)
            col_edit = self.ui.cif_main_table.text(row, Column.EDIT)
            if col_data and not col_edit and col_data != '?':
                self.cif[vhead] = col_data
            if col_edit:
                if self.cif[vhead] != col_edit and changes_cif:
                    changes_cif[vhead] = col_edit
                try:
                    self.cif[vhead] = col_edit
                except (RuntimeError, ValueError, IOError) as e:
                    print('Can not take cif info from table:', e)
            else:
                if changes_cif:
                    del changes_cif[vhead]
        if self.options.track_changes and changes_cif and changes_cif.file_is_there_and_writable():
            self.save_keys_and_loops_to_changes_cif(changes_cif)

    def save_keys_and_loops_to_changes_cif(self, changes_cif: CifContainer) -> None:
        self.save_changed_loops(changes_cif)
        try:
            changes_cif.save(filename=self.finalcif_changes_filename)
        except Exception as e:
            print(f'Unable to save changes file: {e}')
            # del changes_cif
            # self.finalcif_changes_filename.unlink(missing_ok=True)
            return
        if changes_cif.fileobj.exists() and changes_cif.fileobj.stat().st_size == 0 or changes_cif.is_empty():
            print('Changes file has no content. Deleting it ...')
            with suppress(Exception):
                changes_cif.fileobj.unlink(missing_ok=True)

    def save_changed_loops(self, changes_cif: CifContainer) -> None:
        """
        previous_cif is the original unchanged cif that gets 'previous_cif'-finalcif.cif after saving.
        previous_values contains its loops.
        """
        previous_cif_path = Path(strip_finalcif_of_name(self.cif.finalcif_file,
                                                        till_name_ends=True)).with_suffix('.cif')
        if previous_cif_path.exists():
            previous_cif = CifContainer(previous_cif_path)
            previous_values = []
            for loop2 in previous_cif.loops:
                previous_values.append(loop2.values)
            for loop in self.cif.loops:
                if loop.values not in previous_values:
                    changes_cif.add_loop_to_cif(loop_tags=loop.tags, loop_values=loop.values)
            changes_cif.save(filename=self.finalcif_changes_filename)

    def get_changes_cif(self, finalcif_changes_filename: Path) -> CifContainer:
        if self.changes_cif_has_zero_size():
            finalcif_changes_filename.unlink()
        block_name = self.cif.current_block if self.cif.current_block else self.cif.block.name
        block_name = block_name + '_changes'
        changes_cif = CifContainer(file=finalcif_changes_filename,
                                   new_block=block_name if not finalcif_changes_filename.exists() else '')
        # new block of added cif is not loaded:
        if block_name in [x.name for x in changes_cif.doc]:
            changes_cif.load_block_by_name(block_name)
        changes_cif.fileobj.touch(exist_ok=True)
        return changes_cif

    def changes_cif_has_zero_size(self) -> bool:
        return self.finalcif_changes_filename.exists() and self.finalcif_changes_filename.stat().st_size == 0

    def load_changes_cif(self) -> bool:
        changes = self.get_changes_cif(self.finalcif_changes_filename)
        for item in changes.block:
            if item.pair is not None:
                key, value = item.pair
                value = gemmi.cif.as_string(value).strip()
                self.ui.cif_main_table.setText(key=key, column=Column.EDIT, color=None, txt=value)
        for loop in changes.loops:
            self.cif.add_loop_to_cif(loop_tags=loop.tags, loop_values=loop.values)
        return True

    def is_row_a_cif_item(self, vhead: str) -> bool:
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
        final_textedit.setPlainText(self.cif.finalcif_file.read_text(encoding='utf-8', errors='ignore'))

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
        self.check_cif_for_missing_values_before_really_open_it()
        try:
            self.import_key_value_pairs(imp_cif)
            self.import_loops(imp_cif)
        except Exception as e:
            print(e)
            unable_to_open_message(Path(self.cif.filename), e)
        # I think I leave the user possibilities to change the imported values:
        # self.save_current_cif_file()
        # self.load_cif_file(str(self.cif.finalcif_file))

    def import_loops(self, imp_cif: 'CifContainer'):
        """
        Import all loops from the CifContainer imp_cif to the current block.
        """
        for loop in imp_cif.loops:
            if self.ui.importOnlyNewDataCheckBox.isChecked() and self.cif.block.find(loop.tags):
                # Import only new loops
                continue
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
                if self.ui.importOnlyNewDataCheckBox.isChecked() and self.cif[key]:
                    # Import only new key/values
                    continue
                value = cif.as_string(value)
                if key in self.ui.cif_main_table.vheaderitems:
                    self.ui.cif_main_table.setText(key=key, column=Column.EDIT, txt=value, color=light_green)
                else:
                    self.add_row(key, value)  # , column =Column.EDIT

    def do_not_import_this_key(self, key: str, value: str, cif: 'CifContainer') -> bool:
        if value == '?' or value.strip() == '':
            return True
        if key in do_not_import_keys:
            return True
        if key in do_not_import_from_stoe_cfx and cif.fileobj.suffix == '.cfx':
            return True
        return False

    def load_cif_file(self, filepath: Path, block=0, load_changes: bool = True) -> None:
        """
        Opens the cif file and fills information into the main table.
        """
        self.ui.datanameComboBox.blockSignals(True)
        # Is also done in block load method
        self._clear_state_before_block_load()
        if not filepath:
            filepath = Path(cif_file_open_dialog(last_dir=self.get_last_workdir()))
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
        except GemmiError as e:
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
        # Do this only when sure we can load the file:
        self.save_current_recent_files_list(filepath)
        self._load_block(block, load_changes=load_changes)
        self.add_data_names_to_combobox()
        self.ui.datanameComboBox.setCurrentIndex(block)
        self.ui.cif_main_table.resizeRowsToContents()
        self.ui.datanameComboBox.blockSignals(False)
        if self.cif.is_multi_cif:
            # short after start, because window size is not finished
            QTimer.singleShot(1000, self.ui.datanameComboBox.showPopup)

    def add_data_names_to_combobox(self) -> None:
        self.ui.datanameComboBox.clear()
        for block in self.cif.doc:
            self.ui.datanameComboBox.addItem(block.name)

    def _clear_state_before_block_load(self) -> None:
        self.status_bar.show_message('')
        # Set to empty state before loading:
        self.missing_data = set()
        # clean table and vheader before loading:
        self.ui.cif_main_table.delete_content()

    def _load_block(self, index: int, load_changes: bool = True) -> None:
        if not self.cif:
            return
        self._clear_state_before_block_load()
        self.cif.load_this_block(index)
        self.check_cif_for_missing_values_before_really_open_it()
        try:
            self.fill_cif_table()
        except UnicodeDecodeError:
            nums = self.cif.get_line_numbers_of_bad_characters(Path(self.cif.doc.source))
            show_general_warning(window_title='Unable to open file',
                                 warn_text='Invalid characters in file!',
                                 info_text=f'The file "{Path(self.cif.doc.source)}" has invalid '
                                           f'characters in line(s)'
                                           f' {", ".join([str(x + 1) for x in nums])}.'
                                           '\n\nOnly ascii characters are allowed.')
        except Exception as e:
            not_ok = e
            print(e)
            if DEBUG:
                raise
            unable_to_open_message(Path(self.cif.filename), not_ok)
        self.load_recent_cifs_list()
        if self.options.track_changes and load_changes:
            changes_exist = False
            if self.changes_cif_has_zero_size():
                self.finalcif_changes_filename.unlink(missing_ok=True)
            elif self.finalcif_changes_filename.exists() and self.changes_cif_has_values():
                changes_exist = True
            if changes_exist and not self.running_inside_unit_test and self.changes_answer == 0:
                self.changes_answer = QMessageBox.question(self, 'Previous changes found',
                                                           f'Previous changes from a former FinalCif session '
                                                           f'were found in\n{self.finalcif_changes_filename.name}.\n\n'
                                                           'Do you wish to reload them?',
                                                           QMessageBox.Yes | QMessageBox.No)
            if self.changes_answer == QMessageBox.Yes:
                try:
                    self.load_changes_cif()
                except Exception as e:
                    unable_to_open_message(filepath=self.finalcif_changes_filename, not_ok=e)
            if self.running_inside_unit_test and changes_exist:
                self.load_changes_cif()
        self.make_loops_tables()
        if self.cif:
            self.set_shredcif_state()
            # saving current cif dir as last working directory:
            self.settings.save_current_dir(str(self.cif.path_base))
            self.enable_buttons()
            self.fill_space_group_lineedit()
            self.fill_sum_formula_lineedit()
            self.ui.CCDCNumLineEdit.setText(self.cif['_database_code_depnum_ccdc_archive'])
            self.ui.CheckcifPlaintextEdit.clear()
            self.ui.TemplatesStackedWidget.setCurrentIndex(0)
            self.authors = AuthorLoops(ui=self.ui, cif=self.cif, app=self)
            if not self.ui.MainStackedWidget.on_checkcif_page():
                self.ui.MainStackedWidget.got_to_main_page()
            self.deposit.cif = self.cif
            # self.ui.cif_main_table.resizeRowsToContents()
            self.ui.cif_main_table.vheaderitems.clear()
            for row_number in range(self.ui.cif_main_table.model().rowCount()):
                vhead_key = self.get_key_by_row_number(row_number)
                self.ui.cif_main_table.vheaderitems.insert(row_number, vhead_key)

    def changes_cif_has_values(self) -> bool:
        try:
            return not self.get_changes_cif(self.finalcif_changes_filename).is_empty()
        except IndexError:
            return False

    def fill_sum_formula_lineedit(self) -> None:
        try:
            self.ui.SumFormMainLineEdit.setText(sum_formula_to_html(formula_str_to_dict(
                self.cif['_chemical_formula_sum'].strip(" '"))))
        except Exception:
            self.ui.SumFormMainLineEdit.setText(self.cif['_chemical_formula_sum'].strip(" '"))

    def fill_space_group_lineedit(self) -> None:
        try:
            self.ui.Spacegroup_top_LineEdit.setText(
                SpaceGroups().to_html(self.cif.space_group))
        except Exception as e:
            print('Space group error:', str(e))
            self.ui.Spacegroup_top_LineEdit.setText(self.cif.space_group)

    def set_shredcif_state(self) -> None:
        if ShredCIF(cif=self.cif, statusbar=self.status_bar).cif_has_hkl_or_res_file():
            self.ui.ShredCifButton.setEnabled(True)
        else:
            self.ui.ShredCifButton.setDisabled(True)

    def append_cif(self):
        self.cif.save()
        self.load_cif_file(filepath=self.cif.finalcif_file, load_changes=False)
        cif_file = self.get_file_from_dialog()
        if not cif_file:
            return
        cif2 = CifContainer(cif_file)
        if cif2.is_multi_cif:
            show_general_warning('Can add single data CIFs only!')
        if cif2.block.name in [x.name for x in self.cif.doc]:
            show_general_warning(warn_text='Duplicate block', info_text='Data block name "<b>{}</b>" already present '
                                                                        'in current CIF!'.format(self.cif.block.name))
            return
        self.cif.doc.add_copied_block(block=cif2.block, pos=-1)
        self.cif.save()
        self.load_cif_file(filepath=self.cif.fileobj, load_changes=False)

    def get_file_from_dialog(self) -> Union[Path, None]:
        fp = cif_file_open_dialog(last_dir=self.get_last_workdir())
        if not fp:
            return None
        filepath = Path(fp)
        # if change_into_workdir:
        # The warning about inconsistent temperature:
        self.temperature_warning_displayed = False
        return filepath

    def check_cif_for_missing_values_before_really_open_it(self) -> None:
        try:
            # Will not stop reading if only the value is missing and ends with newline:
            self.cif.doc.check_for_missing_values()
        except (RuntimeError, ValueError) as e:
            print('Missing value:')
            print(str(e))
            errlist = str(e).split(':')
            if len(errlist) > 1:
                show_general_warning(
                    f"Attention in CIF line {errlist[1]}:\n'{errlist[2].split()[0]}' has no value.")

    def get_last_workdir(self):
        try:
            # loading last working directory:
            last = self.settings.load_last_workdir()
        except TypeError:
            last = ''
        if last and Path(last).exists():
            return last
        return ''

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
        if self.cif.res_file_data:
            self.ui.shelx_TextEdit.setPlainText(cif.as_string(self.cif.res_file_data))
        try:
            QTimer.singleShot(0, self.view_molecule)
        except Exception:
            print('Molecule view crashed!')

    def view_molecule(self) -> None:
        if self.ui.growCheckBox.isChecked():
            self.ui.molGroupBox.setTitle('Completed Molecule')
            self.grow_molecule()
        else:
            self.ui.molGroupBox.setTitle('Asymmetric Unit')
            with suppress(Exception):
                atoms = [x for x in self.cif.atoms_orth]
                self.ui.render_widget.open_molecule(atoms, labels=self.ui.labelsCheckBox.isChecked())

    def grow_molecule(self):
        atoms = tuple(self.cif.atoms_fract)
        if atoms:
            sdm = SDM(atoms, self.cif.symmops, self.cif.cell[:6], centric=self.cif.is_centrosymm)
            with suppress(Exception):
                needsymm = sdm.calc_sdm()
                atoms = sdm.packer(sdm, needsymm)
                self.ui.render_widget.open_molecule(atoms, labels=self.ui.labelsCheckBox.isChecked())

    def redraw_molecule(self) -> None:
        try:
            self.view_molecule()
        except Exception:
            print('Molecule view crashed!!')

    def show_labels(self, value: bool):
        self.ui.render_widget.show_labels(value)

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
                if '_database_code_depnum_ccdc_archive' not in self.ui.cif_main_table.vheaderitems:
                    # self.ui.cif_main_table.vheaderitems.insert(0, '_database_code_depnum_ccdc_archive')
                    self.add_row('_database_code_depnum_ccdc_archive', '', at_start=True)
                txt = self.ui.cif_main_table.getTextFromKey('_database_code_depnum_ccdc_archive', Column.EDIT).strip()
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
                # Makes sure data is loaded on first load and not only after saving:
                self.missing_data.add(src)
        self.refresh_combo_boxes()
        # Get missing items from sources and put them into the corresponding rows:
        # missing items will even be used if under the blue separation line:
        for miss_key in self.missing_data:
            # add missing item to data sources column:
            row_num = self.ui.cif_main_table.vheaderitems.index(miss_key)
            try:
                txt = str(self.sources[miss_key][0])
                if row_num > self.complete_data_row:
                    self.ui.cif_main_table.setText(key=miss_key, column=Column.DATA, txt=txt)
                else:
                    if txt and txt != '?':
                        self.ui.cif_main_table.setText(key=miss_key, column=Column.DATA, txt=txt, color=light_green)
                    else:
                        self.ui.cif_main_table.setText(key=miss_key, column=Column.DATA, txt=txt, color=yellow)
            except (KeyError, TypeError):
                # TypeError my originate from incomplete self.missing_data list!
                # print(e, '##', miss_key)
                pass

    def refresh_combo_boxes(self) -> None:
        combos_from_settings = self.settings.load_cif_keys_of_properties()
        for row_number in range(self.ui.cif_main_table.model().rowCount()):
            vhead_key = self.get_key_by_row_number(row_number)
            if vhead_key not in self.ui.cif_main_table.vheaderitems:
                self.ui.cif_main_table.vheaderitems.insert(row_number, vhead_key)
            # adding comboboxes:
            if vhead_key in combos_from_settings:
                # First add self-made properties:
                self.add_combobox(row_number, vhead_key)

    def refresh_color_background_from_templates(self):
        for row_number in range(self.ui.cif_main_table.model().rowCount()):
            vhead_key = self.get_key_by_row_number(row_number)
            vhead_key = self.get_vrf_errortype(vhead_key)
            widget = self.ui.cif_main_table.cellWidget(row_number, Column.EDIT)
            if isinstance(widget, MyQPlainTextEdit):
                if self.settings.load_settings_list('text_templates', vhead_key):
                    widget.setBackground(light_blue)
                else:
                    widget.setBackground(white)

    def get_key_by_row_number(self, row_number: int) -> str:
        vhead_key = self.ui.cif_main_table.model().headerData(row_number, QtCore.Qt.Vertical)
        return vhead_key

    def add_combobox(self, row: int, vhead_key: str) -> None:
        """
        :param row: row number
        :param vhead_key: CIF keyword for combobox
        """
        properties_list = self.settings.load_property_values_by_key(vhead_key)
        if properties_list:
            self.ui.cif_main_table.add_property_combobox(properties_list, row, vhead_key)

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
                self.ui.cif_main_table.setText(key=key, column=Column.DATA, txt=strval)
                QTimer.singleShot(200, self.ui.cif_main_table.resizeRowsToContents)
            # print(key, value)
        if not self.cif.test_res_checksum():
            show_res_checksum_warning()
        if not self.cif.test_hkl_checksum():
            show_hkl_checksum_warning()
        if self.cif.is_multi_cif:
            self.refresh_combo_boxes()
        else:
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
        do_not_display = ('_diffrn_refln_index_h')
        for num, loop in enumerate(self.cif.loops):
            tags = loop.tags
            if not tags or len(tags) < 1:
                continue
            if tags[0] in do_not_display:
                continue
            self.new_loop_tab(loop, num, tags)
        if self.cif.res_file_data:
            self.add_res_file_to_loops()

    def new_loop_tab(self, loop: gemmi.cif.Loop, num: int, tags: List[str]):
        loop = Loop(tags, values=grouper(loop.values, loop.width()),
                    parent=self.ui.LoopsTabWidget, block=self.cif.block)
        self.add_loop_widget(loop, first_tag=tags[0])
        self.ui.LoopsTabWidget.setTabToolTip(num + 1, tags[0])
        self.ui.revertLoopsPushButton.clicked.connect(loop.model.revert)

    def add_loop_widget(self, loop: Loop, first_tag: str) -> None:
        self.ui.LoopsTabWidget.addTab(loop.tableview, cif_to_header_label.get(first_tag) or first_tag)

    def add_res_file_to_loops(self) -> None:
        textedit = QPlainTextEdit()
        self.ui.LoopsTabWidget.addTab(textedit, 'SHELX res file')
        textedit.setPlainText(self.cif.res_file_data[1:-1])
        doc = textedit.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setPointSize(14)
        doc.setDefaultFont(font)
        textedit.setLineWrapMode(QPlainTextEdit.NoWrap)
        textedit.setReadOnly(True)

    def _go_to_new_loop_page(self):
        self.loopcreate = LoopCreator(cif=self.cif)
        self.ui.LoopsTabWidget.addTab(self.loopcreate, 'Create Loops')
        self.ui.LoopsTabWidget.setCurrentIndex(self.ui.LoopsTabWidget.count() - 1)
        self.ui.revertLoopsPushButton.hide()
        self.ui.newLoopPushButton.hide()
        self.loopcreate.saveLoopPushButton.clicked.connect(self.save_new_loop_to_cif)

    def save_new_loop_to_cif(self):
        if self.loopcreate:
            loop = self.loopcreate.save_new_loop_to_cif()
            self.new_loop_tab(loop=loop, num=self.ui.LoopsTabWidget.count(), tags=self.loopcreate.tags)
            self.ui.LoopsTabWidget.removeTab(self.ui.LoopsTabWidget.count() - 2)
            self.loopcreate.deleteLater()
            self.ui.LoopsTabWidget.setCurrentIndex(self.ui.LoopsTabWidget.count() - 1)

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
        if key not in self.ui.cif_main_table.vheaderitems:
            self.ui.cif_main_table.vheaderitems.insert(row_num, key)
        else:
            print(f'The key {key} is already present.')
            return
        self.ui.cif_main_table.insertRow(row_num)
        if value is None or value == '?':
            strval = '?'
        else:
            strval = gemmi.cif.as_string(value).strip()
        if not key:
            strval = ''
        # All regular linedit fields:
        if key == "These below are already in:":
            self.ui.cif_main_table.add_separation_line(row_num)
            self.complete_data_row = row_num
        else:
            color = None
            load_key = key
            load_key = self.get_vrf_errortype(load_key)
            if load_key in self.settings.list_saved_items('text_templates'):
                color = light_blue
            self.ui.cif_main_table.setText(row=row_num, key=key, column=Column.CIF,
                                           txt='?' if at_start else strval)
            self.ui.cif_main_table.setText(row=row_num, key=key, column=Column.DATA, txt='')
            self.ui.cif_main_table.setText(row=row_num, key=key, column=Column.EDIT, color=color,
                                           txt=strval if at_start else '')
        head_item_key = MyTableWidgetItem(key)
        if key != "These below are already in:":
            self.ui.cif_main_table.setVerticalHeaderItem(row_num, head_item_key)
        if not key.startswith('_'):
            return
        if key not in self.cif.order:
            self.cif.order.insert(row_num, key)
        if not self.cif.block.find_value(key):
            self.cif[key] = value
