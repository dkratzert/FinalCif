#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import subprocess
import sys
import threading
import time
from contextlib import suppress
from datetime import datetime
from math import sin, radians
from pathlib import Path, WindowsPath

import warnings

from finalcif.gui.vzs_viewer import VZSImageViewer

warnings.filterwarnings("ignore", category=RuntimeWarning, module="shibokensupport.signature.parser")

import gemmi

if hasattr(gemmi, 'set_leak_warnings'):
    gemmi.set_leak_warnings(False)

import requests
from qtpy import QtCore, QtGui, QtWebEngineWidgets, QtWidgets, compat
from qtpy.QtCore import Qt, QEvent
from qtpy.QtWidgets import (QMainWindow, QCheckBox, QListWidgetItem, QApplication,
                            QPlainTextEdit, QMessageBox, QScrollBar)
from gemmi import cif

from finalcif import VERSION
from finalcif.app_path import application_path
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
from finalcif.gui.import_selector import ImportSelector
from finalcif.gui.loop_creator import LoopCreator
from finalcif.gui.loops import Loop, LoopTableModel, MyQTableView
from finalcif.gui.plaintextedit import MyQPlainTextEdit
from finalcif.gui.text_value_editor import MyTextTemplateEdit, TextEditItem
from finalcif.gui.vrf_classes import MyVRFContainer, VREF
from finalcif.report.templated_report import ReportFormat
from finalcif.template.templates import ReportTemplates
from finalcif.tools.download import MyDownloader
from finalcif.tools.dsrmath import my_isnumeric
from finalcif.tools.misc import (next_path, celltxt, to_float, cif_to_header_label, grouper, is_database_number,
                                 open_file, strip_finalcif_of_name, file_age_in_days)
from finalcif.tools.options import Options
from finalcif.tools.platon import PlatonRunner
from finalcif.tools.settings import FinalCifSettings
from finalcif.tools.shred import ShredCIF
from finalcif.tools.space_groups import SpaceGroups
from finalcif.tools.spgr_format import spgrps
from finalcif.tools.statusbar import StatusBar
from finalcif.tools.sumformula import formula_str_to_dict, sum_formula_to_html

DEBUG = False
app = QApplication.instance()
if app is None:
    app = QApplication([])
app.setStyle("windowsvista")
with suppress(ImportError):
    import qtawesome as qta


class AppWindow(QMainWindow):

    def __init__(self, file: Path | None = None):
        super().__init__()
        self.thread_download = None
        self.ckf = None
        self.thread_version = None
        self.worker = None
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        # This prevents some things to happen during unit tests:
        # Open of target dir of shred cif,
        # open report doc,
        # get check.def from platon server
        self.sources: dict[str, tuple[str, str | None]] | None = None
        self.cif: CifContainer | None = None
        self.report_picture_path: Path | None = None
        self.loopcreate: LoopCreator | None = None
        self.checkdef: list[str] = []
        self.changes_answer: int = 0
        self.validation_response_forms_list = []
        self.checkdef_file: Path = Path.home().joinpath('check.def')
        self.missing_data: set = set()
        self.temperature_warning_displayed = False
        # True if line with "these are already in" reached:
        self.complete_data_row = -1
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self)
        self.ui.page_MainTable.setParent(self.ui.MainStackedWidget)
        self.settings = FinalCifSettings()
        self.load_fontsize_from_settings()
        self.options = Options(self.ui, self.settings)
        self.deposit = CODdeposit(self.ui, self.cif, self.options)
        self.equipment = Equipment(app=self, settings=self.settings)
        self.properties = Properties(parent=self, settings=self.settings)
        self.status_bar = StatusBar(ui=self.ui)
        self.status_bar.show_message(f'FinalCif version {VERSION}')
        self.authors: AuthorLoops | None = None
        self.ui.cifOrderWidget.settings = self.settings
        self.ui.cifOrderWidget.set_order_from_settings(self.settings)
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
        self.video = VZSImageViewer(self)
        self.ui.video_vLayout.addWidget(self.video)
        if file:
            self.load_cif_file(file)
        self.load_recent_cifs_list()
        self.ui.CheckcifPlaintextEdit.insertPlainText(
            "\n"
            "  Offline CheckCIF uses PLATON from Anthony L. Spek, Utrecht University, The Netherlands."
            "\n"
            "  https://platonsoft.nl\n"
            "  \n"
            "  Please cite PLATON in your publication if you use it.\n"
            "  \n"
            "  - PLATON References : \n"
            "            Spek, A.L. (2003). J. Appl. Cryst. 36, 7-13.\n"
            "            Spek, A.L. (2009). Acta Cryst. D65, 148-155.\n"
            "            Spek, A.L. (2015). Acta Cryst. C71, 9-18.\n"
            "            Spek, A.L. (2018). Inorg. Chim. Acta, 470, 232-237.\n"
            "            Spek, A.L. (2020). Acta Cryst. E76, 1-11.\n"
            "  \n"
            "  \n"
            "  - Recent versions of PLATON may be obtained from: https://platonsoft.nl/xraysoft\n"
            "  "
        )
        self.set_checkcif_output_font(self.ui.CheckcifPlaintextEdit)
        # To make file drag&drop working:
        self.setAcceptDrops(True)
        self.show()
        self.templates = ReportTemplates(self, self.settings)
        if not self.running_inside_unit_test:
            self.check_for_update_version()
        self.textedit = MyTextTemplateEdit(parent=self)
        self.ui.page_textTemplate.layout().addWidget(self.textedit)
        self.connect_signals_and_slots()
        with suppress(Exception):
            self.make_button_icons()
        # self.set_font_sizes()

    def load_fontsize_from_settings(self):
        fontsize = self.settings.load_value_of_key('global_font_size')
        if fontsize is not None and fontsize >= 8:
            self.set_global_font(fontsize)
            self.ui.textSizeSpinBox.setValue(fontsize)
        else:
            self.ui.textSizeSpinBox.setValue(0)

    @property
    def running_inside_unit_test(self):
        if "RUNNING_TEST" in os.environ:
            if DEBUG:
                print(f'pytest process running: {os.environ["PYTEST_CURRENT_TEST"]}')
            return True
        return False

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
        self.ui.ImportCifPushButton.setDisabled(True)
        self.ui.CODpushButton.setDisabled(True)
        self.ui.CCDCpushButton.setDisabled(True)
        self.ui.ShredCifButton.setDisabled(True)
        self.ui.LoopsPushButton.setDisabled(True)
        self.ui.OptionsPushButton.setDisabled(True)
        self.ui.AuthorEditPushButton.setDisabled(True)

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
        self.ui.AuthorEditPushButton.setEnabled(True)
        if self.cif.is_multi_cif:
            self.ui.CODpushButton.setDisabled(True)
        else:
            self.ui.CODpushButton.setEnabled(True)

    def set_global_font(self, size: int) -> None:
        if size >= 8:
            self.settings.save_key_value('global_font_size', size)
            font: QtGui.QFont = app.font()
            font.setPointSize(size)
            app.setFont(font)
        else:
            self.settings.save_key_value('global_font_size', 0)

    def set_font_sizes(self) -> None:
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
        self.setTextEditSizes()

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
        self.ui.SelectCif_PushButton.setIcon(qta.icon('ph.file-text', options=[{'color': 'darkgreen'}]))
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
            self.ui.OptionsPushButton.setIcon(qta.icon('msc.gear'))
        try:
            self.ui.ShredCifButton.setIcon(qta.icon('ph.files-bold'))
        except Exception:
            pass
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
            pass
        self.textedit.ui.exportTextPushButton.setIcon(qta.icon('mdi.export'))
        self.textedit.ui.savePushButton.setIcon(qta.icon('mdi.content-save'))
        self.textedit.ui.deletePushButton.setIcon(qta.icon('mdi.playlist-minus'))
        self.textedit.ui.importPushButton.setIcon(qta.icon('mdi.import'))
        try:
            self.ui.SaveAuthorLoopToTemplateButton.setIcon(qta.icon('mdi.badge-account-outline'))
        except Exception:
            pass
        try:
            self.ui.AddThisAuthorToLoopPushButton.setIcon(qta.icon('mdi.folder-table-outline'))
        except Exception:
            self.ui.AddThisAuthorToLoopPushButton.setIcon(qta.icon('mdi.file-table-outline'))
        with suppress(Exception):
            self.ui.DeleteLoopAuthorTemplateButton.setIcon(qta.icon('mdi.delete-forever-outline'))
        with suppress(Exception):
            self.ui.cifOrderWidget.ui.deleteKeyPushButton.setIcon(qta.icon('mdi.delete-forever-outline'))
        with suppress(Exception):
            self.ui.cifOrderWidget.ui.moveUpPushButton.setIcon(qta.icon('mdi.chevron-up'))
            self.ui.cifOrderWidget.ui.moveDownPushButton.setIcon(qta.icon('mdi.chevron-down'))
            self.ui.cifOrderWidget.ui.saveSettingPushButton.setIcon(qta.icon('mdi.content-save'))
            self.ui.cifOrderWidget.ui.addKeyPushButton.setIcon(qta.icon('mdi.plus'))

    def connect_signals_and_slots(self) -> None:
        """
        this method connects all signals to slots. Only a few mighjt be defined elsewere.
        """
        self.ui.datanameComboBox.currentIndexChanged.connect(self._load_block)
        self.ui.datanameComboBox.delete_signal.connect(self._delete_current_block)
        ## main
        self.ui.BackPushButton.clicked.connect(self.back_to_main)
        self.ui.BackFromDepositPushButton.clicked.connect(self.back_to_main)
        self.ui.ExploreDirButton.clicked.connect(self.explore_current_dir)
        self.ui.LoopsPushButton.clicked.connect(self._on_go_to_loops_page)
        self.ui.LoopsPushButton.clicked.connect(
            lambda x: self.ui.LoopsTabWidget.setCurrentIndex(1) if self.ui.LoopsTabWidget.count() > 0 else None)
        self.ui.LoopsPushButton.clicked.connect(lambda x: self.ui.TemplatesStackedWidget.setCurrentIndex(1))
        self.ui.AuthorEditPushButton.clicked.connect(self._on_go_to_loops_page)
        self.ui.AuthorEditPushButton.clicked.connect(lambda x: self.ui.TemplatesStackedWidget.setCurrentIndex(1))
        self.ui.AuthorEditPushButton.clicked.connect(lambda x: self.ui.LoopsTabWidget.setCurrentIndex(0))
        # checkcif
        self.ui.CheckcifStartButton.clicked.connect(self.open_checkcif_page)
        self.ui.CheckcifButton.clicked.connect(self.do_offline_checkcif)
        self.ui.CheckcifHTMLOnlineButton.clicked.connect(self.do_html_checkcif)
        self.ui.CheckcifPDFOnlineButton.clicked.connect(self.do_pdf_checkcif)
        self.ui.BackFromPlatonPushButton.clicked.connect(self.back_to_main_noload)
        self.ui.SavePushButton.clicked.connect(self.save_responses)
        # open, import
        self.ui.SelectCif_PushButton.clicked.connect(self.load_cif_file)
        self.ui.SaveCifButton.clicked.connect(self.save_cif_and_display)
        self.ui.ImportCifPushButton.clicked.connect(self.import_additional_cif)
        # report
        self.ui.SaveFullReportButton.clicked.connect(self.make_report_tables)
        self.ui.RecentComboBox.currentIndexChanged.connect(self.load_recent_file)
        self.ui.cif_main_table.row_deleted.connect(self._deleted_row)
        self.ui.CODpushButton.clicked.connect(self.open_cod_page)
        self.ui.CCDCpushButton.clicked.connect(self._ccdc_deposit)
        self.ui.newLoopPushButton.clicked.connect(self._go_to_new_loop_page)
        self.ui.deleteLoopButton.clicked.connect(self._on_delete_current_loop)
        save_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.save_current_cif_file)
        save_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+H'), self)
        save_shortcut.activated.connect(self.do_html_checkcif)
        save_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+P'), self)
        save_shortcut.activated.connect(self.do_pdf_checkcif)
        self.ui.DetailsPushButton.clicked.connect(self.show_residuals)
        self.ui.BackpushButtonDetails.clicked.connect(self.back_to_main_noload)
        self.ui.growCheckBox.toggled.connect(self.redraw_molecule)
        self.ui.labelsCheckBox.toggled.connect(self.show_labels)
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
        self.ui.cif_main_table.textTemplate.connect(self.ui.MainStackedWidget.go_to_text_template_page)
        # value has to be '?', because otherwise it adds a key without a value:
        self.ui.cif_main_table.new_key.connect(lambda x: self.add_row(key=x, value='?', at_start=True))
        self.ui.appendCifPushButton.clicked.connect(self.append_cif)
        self.ui.drawImagePushButton.clicked.connect(self.draw_image)
        self.ui.ExportAllTemplatesPushButton.clicked.connect(self.export_all_templates)
        self.ui.ImportAllTemplatesPushButton.clicked.connect(self.import_all_templates)
        self.ui.searchMainTableLineEdit.textChanged.connect(self.ui.cif_main_table.search)
        self.ui.textSizeSpinBox.valueChanged.connect(self.set_global_font)

    @property
    def finalcif_changes_filename(self):
        return self.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif_changes.cif', force_strip=True)

    def _on_go_to_loops_page(self) -> None:
        self.make_loops_tables()
        self.ui.MainStackedWidget.go_to_loops_page()

    def export_all_templates(self, filename: Path | None = None):
        import pickle
        if not filename:
            filename, _ = compat.getsavefilename(parent=self,
                                                 basedir=str(Path(self.get_last_workdir()).joinpath(
                                                     f'finalcif_templates_{time.strftime("%Y-%m-%d")}.dat')),
                                                 selectedfilter="Template File (*.dat)",
                                                 filters="Template File (*.dat)",
                                                 caption='Save templates')
        if not filename:
            return
        templates = {'text'               : self.export_raw_text_templates(),
                     'equipment'          : self.equipment.export_raw_data(),
                     'properties'         : self.properties.export_raw_data(),
                     'authors'            : self.authors.export_raw_data(),
                     'cif_order'          : self.ui.cifOrderWidget.order_keys,
                     'cif_order_essential': self.ui.cifOrderWidget.order_essentials,
                     }
        try:
            with open(filename, "wb") as f:
                pickle.dump(templates, f)
        except pickle.PickleError as e:
            self.status_bar.show_message(f'Saving templates failed: {e!s}')

    def import_all_templates(self, filename: Path | None = None):
        import pickle
        if not filename:
            filename, _ = compat.getopenfilename(parent=self,
                                                 basedir=self.get_last_workdir(),
                                                 selectedfilter="Template File (*.dat)",
                                                 filters="Template File (*.dat)",
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
        self.ui.cifOrderWidget.save_in_settings(templates.get('cif_order'), templates.get('cif_order_essential'))
        self.ui.cifOrderWidget.set_order_from_settings(self.settings)

    def draw_image(self):
        image_filename = self.cif.finalcif_file_prefixed(prefix='', suffix='-finalcif.png')
        self.ui.render_widget.save_image(image_filename)
        self.status_bar.show_message(f'Image saved to {image_filename}', timeout=20)
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
        filename = cif_file_open_dialog(parent=self)
        if not filename:
            return
        try:
            doc = read_document_from_cif_file(filename)
            block: gemmi.cif.Block = doc.sole_block()
        except Exception:
            show_general_warning(self, 'This file is not readable.')
            return
        text_list = []
        for i in block:
            if i.loop is not None:
                if len(i.loop.tags) > 0:
                    loop_column_name = i.loop.tags[0]
                    self.textedit.ui.cifKeyLineEdit.setText(loop_column_name)
                for n in range(i.loop.length()):
                    value = i.loop[n, 0]
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
            show_general_warning(self, f'"{blockname}" is not a valid cif keyword.')
            return
        for value in textlist:
            if value:
                loop.add_row([cif.quote(utf8_to_str(value))])
        filename = cif_file_save_dialog(blockname + '_template.cif')
        if not filename.strip():
            return
        try:
            write_options = cif.WriteOptions(cif.Style.Indent35)
            doc.write_file(filename, options=write_options)
            # Path(filename).write_text(doc.as_string(cif.Style.Indent35))
        except PermissionError:
            if Path(filename).is_dir():
                return
            show_general_warning(self, f'No permission to write file to {Path(filename).resolve()}')
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

    def export_raw_text_templates(self) -> list[dict]:
        templates_list = []
        for cif_key in self.settings.list_saved_items('text_templates'):
            template = self.settings.load_settings_list('text_templates', cif_key)
            templates_list.append({'cif_key': cif_key, 'data': template})
        return templates_list

    def import_raw_text_templates(self, templates_list: list[dict]):
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
        self.ui.MainStackedWidget.got_to_cod_page()

    def event(self, event: QtCore.QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            event: QtGui.QKeyEvent
            if event.key() == QtCore.Qt.Key.Key_Escape and self.ui.searchMainTableLineEdit.hasFocus():
                self.ui.searchMainTableLineEdit.clear()
        return super().event(event)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """It called when the main window resizes."""
        with suppress(AttributeError):
            self._savesize()
        # main_width = self.ui.Mainwidget.width()
        # left_frame = main_width * 0.22
        # left_frame = max(300, left_frame)
        # self.ui.LeftFrame.setMinimumWidth(int(left_frame))
        # Not necessary here, it is done in MyCifTable
        # threading.Thread(target=self.ui.cif_main_table.resizeRowsToContents).start()
        # QtCore.QTimer(self).singleShot(0, self.ui.cif_main_table.resizeRowsToContents)
        self.setTextEditSizes()
        super().resizeEvent(a0)

    def setTextEditSizes(self):
        for ui in [self.ui.Spacegroup_top_LineEdit, self.ui.CCDCNumLineEdit, self.ui.SumFormMainLineEdit]:
            ui.setFixedHeight(self.ui.appendCifPushButton.height())
            vScrollBar = ui.verticalScrollBar()
            # Scroll down a bit, or text will not be in the vertical center:
            vScrollBar.triggerAction(QScrollBar.SliderAction.SliderSingleStepAdd)

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        """Is called when the main window moves."""
        super().moveEvent(a0)
        with suppress(AttributeError):
            self._savesize()

    def changeEvent(self, event: QtCore.QEvent) -> None:
        """Is called when the main window changes its state."""
        if event.type() == QtCore.QEvent.Type.WindowStateChange:
            with suppress(AttributeError):
                self._savesize()

    def _savesize(self) -> None:
        """Saves the main window size nd position."""
        x, y = self.pos().x(), self.pos().y()
        self.settings.save_window_position(QtCore.QPoint(x, y), self.size(), self.isMaximized())

    def show_help(self) -> None:
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://dkratzert.de/files/finalcif/docs/'))

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
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://www.ccdc.cam.ac.uk/deposit'))
        self.explore_current_dir()

    def _deleted_row(self, key: str) -> None:
        """
        Deletes a row of the main table.
        """
        del self.cif[key]
        # Only delete from changes cif if changes were loaded:
        if self.options.track_changes and self.changes_answer == QMessageBox.StandardButton.Yes:
            self.delete_key_from_changes_cif(key)

    def delete_key_from_changes_cif(self, key: str) -> None:
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
        # parent must be None, otherwise it can't be moved to a thread:
        self.worker = MyDownloader(mainurl, parent=None)
        self.worker.loaded.connect(self.is_update_necessary)
        self.thread_version = threading.Thread(target=self.worker.download)
        self.thread_version.start()

    def is_update_necessary(self, content: bytes) -> None:
        """
        Reads the reply from the server and displays a warning in case of an old version.
        """
        remote_version = 0
        with suppress(Exception):
            remote_version = int(content.decode('ascii', errors='ignore'))
        if remote_version > VERSION:
            print(f'Version {VERSION} is outdated (actual is {remote_version}).')
            show_update_warning(self, remote_version)
        else:
            print(f'Version {VERSION} is up-to-date.')

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
        self.worker = MyDownloader(url, parent=None)
        self.worker.loaded.connect(self._save_checkdef)
        self.thread_download = threading.Thread(target=self.worker.download)
        self.thread_download.start()

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

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        """
        Allow drag of files to the main window
        """
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QtGui.QDropEvent):
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
        self._show_loop_buttons()

    def back_to_main_noload(self) -> None:
        """
        Get back to the main table. Without loading a new cif file.
        """
        self.status_bar.show_message('')
        self.ui.TemplatesStackedWidget.setCurrentIndex(0)
        self.ui.MainStackedWidget.got_to_main_page()
        self._show_loop_buttons()

    def _show_loop_buttons(self) -> None:
        self.ui.revertLoopsPushButton.show()
        self.ui.newLoopPushButton.show()
        self.ui.deleteLoopButton.show()

    def _checkcif_failed(self, txt: str) -> None:
        self.ui.CheckCifLogPlainTextEdit.appendHtml(f'<b>{txt}</b>')

    def _ckf_progress(self, txt: str) -> None:
        self.ui.CheckCifLogPlainTextEdit.appendPlainText(txt)

    def _checkcif_finished(self) -> None:
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
        self.checkcif_browser.setHtml(self.htmlfile.resolve().read_text('utf-8', 'ignore'))
        self.ui.ResponsesTabWidget.setCurrentIndex(0)
        threading.Thread(target=self._display_structure_factor_report, args=(parser,)).start()
        # The picture file linked in the html file:
        threading.Thread(target=parser.save_image, args=(self.cif.finalcif_file.with_suffix('.gif'),)).start()
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

    def _display_structure_factor_report(self, parser: MyHTMLParser) -> None:
        self.ui.ckf_textedit.setPlainText(parser.get_ckf())

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
            app.processEvents()
        except Exception as e:
            if DEBUG:
                print('Browser not removed:')
                print(e)
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(1)
        self.ui.CheckCifLogPlainTextEdit.appendPlainText(
            f'Sending html report request to {self.options.checkcif_url} ...')
        if not self.save_current_cif_file():
            self.ui.CheckCifLogPlainTextEdit.appendHtml('<b>Unable to save CIF file. Aborting action...</b>')
            return None
        self.load_cif_file(self.cif.finalcif_file, block=current_block, load_changes=False)
        self.htmlfile = self.cif.finalcif_file_prefixed(prefix='checkcif-', suffix='-finalcif.html')
        try:
            self.htmlfile.unlink()
        except (FileNotFoundError, PermissionError):
            pass
        self.ckf = CheckCif(parent=self, cif=self.cif, outfile=self.htmlfile,
                            hkl_upload=(not self.ui.structfactCheckBox.isChecked()), pdf=False,
                            url=self.options.checkcif_url,
                            full_iucr=self.ui.fullIucrCheckBox.isChecked(),
                            check_duplicates=self.ui.checkDuplicatesCheckBox.isChecked())
        self.ckf.progress.connect(self._ckf_progress)
        self.ckf.failed.connect(self._checkcif_failed)
        self.ckf.finished.connect(self._checkcif_finished)
        self.ui.CheckcifHTMLOnlineButton.setDisabled(True)
        self.ui.CheckcifPDFOnlineButton.setDisabled(True)
        self.ckf.start()

    def _get_check_def(self) -> None:
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
            f'Sending pdf report request to {self.options.checkcif_url} ...')
        self.ckf = CheckCif(parent=self, cif=self.cif, outfile=htmlfile,
                            hkl_upload=(not self.ui.structfactCheckBox.isChecked()),
                            pdf=True, url=self.options.checkcif_url,
                            full_iucr=self.ui.fullIucrCheckBox.isChecked(),
                            check_duplicates=self.ui.checkDuplicatesCheckBox.isChecked())
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

    def do_offline_checkcif(self) -> None:
        self.ui.CheckcifButton.setDisabled(True)
        app.processEvents()
        self.ui.CheckCifLogPlainTextEdit.clear()
        self.ui.MainStackedWidget.go_to_checkcif_page()
        self.ui.CheckCIFResultsTabWidget.setCurrentIndex(0)
        self.ui.CheckcifPlaintextEdit.clear()
        self.ui.CheckCifLogPlainTextEdit.appendPlainText("Running Checkcif locally. Please wait...\n")
        self.ui.cif_main_table.setCurrentItem(None)
        if not self.save_current_cif_file():
            self.ui.CheckCifLogPlainTextEdit.appendPlainText('Unable to save CIF file. Aborting action...')
            return None
        self.load_cif_file(self.cif.finalcif_file, block=self.ui.datanameComboBox.currentIndex(), load_changes=False)
        self.ui.MainStackedWidget.go_to_checkcif_page()
        runner = PlatonRunner(parent=self,
                              log_widget=self.ui.CheckCifLogPlainTextEdit,
                              output_widget=self.ui.CheckcifPlaintextEdit,
                              cif_file=self.cif.fileobj)
        if runner.platon_exe is not None and not Path(runner.platon_exe).exists():
            self.ui.CheckCifLogPlainTextEdit.setPlainText('\nPlaton executable not found!')
            self.ui.CheckCifLogPlainTextEdit.appendPlainText(
                'You can download Platon at http://www.platonsoft.nl/platon/\n')
        runner.tick.connect(self.append_to_ciflog_without_newline)
        runner.finished.connect(lambda: self.ui.CheckcifButton.setEnabled(True))
        runner.run_process()
        runner.formula.connect(self.add_moiety_furmula)
        return None

    def add_moiety_furmula(self, formula_moiety):
        moiety = self.ui.cif_main_table.getTextFromKey(key='_chemical_formula_moiety', col=Column.CIF)
        if formula_moiety and moiety in ['', '?'] and not self.cif.is_multi_cif:
            self.ui.cif_main_table.setText(key='_chemical_formula_moiety', txt=formula_moiety, column=Column.EDIT)

    def append_to_ciflog_without_newline(self, text: str = '') -> None:
        self.ui.CheckCifLogPlainTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.ui.CheckCifLogPlainTextEdit.insertPlainText(text)
        self.ui.CheckCifLogPlainTextEdit.moveCursor(QtGui.QTextCursor.MoveOperation.End)
        self.ui.CheckCifLogPlainTextEdit.unsetCursor()

    def set_checkcif_output_font(self, ccpe: 'QPlainTextEdit') -> None:
        doc = ccpe.document()
        font = doc.defaultFont()
        font.setFamily("Courier New")
        font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
        # app.processEvents()
        # font.setPointSize(14)
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
            filename, _ = compat.getopenfilename(parent=self,
                                                 filters="Image Files (*.png *.jpg *.jpeg *.bmp "
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
            pass

    def get_checked_templates_list_text(self) -> str | None:
        for index in range(self.ui.docxTemplatesListWidget.count()):
            item = self.ui.docxTemplatesListWidget.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                if self.templates.report_from_default_template():
                    return str(application_path / 'template/report_default.docx')
                else:
                    return item.text()
        return None

    def make_report_tables(self) -> None:
        """
        Generates a report document.
        """
        from finalcif.report.tables import make_multi_tables
        from finalcif.report.templated_report import TemplatedReport
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
        self.cif.picometer = self.options.use_picometers
        # The picture after the header:
        if self.report_picture_path:
            picfile = self.report_picture_path
        else:
            picfile = self.cif.finalcif_file.with_suffix('.gif')
        try:
            print('Report with templates')
            template_path = Path(self.get_checked_templates_list_text())
            ok = False
            if template_path.suffix in ('.docx',):
                t = TemplatedReport(format=ReportFormat.RICHTEXT, options=self.options, cif=self.cif)
                ok = t.make_templated_docx_report(output_filename=str(report_filename),
                                                  picfile=picfile,
                                                  template_path=Path(self.get_checked_templates_list_text()))
                if self.cif.is_multi_cif and self.cif.doc[0].name != 'global':
                    make_multi_tables(cif=self.cif, output_filename=str(multi_table_document))
            elif template_path.suffix in ('.html', '.tmpl'):
                t = TemplatedReport(format=ReportFormat.HTML, options=self.options, cif=self.cif)
                report_filename = report_filename.with_suffix('.html')
                ok = t.make_templated_html_report(output_filename=str(report_filename),
                                                  picfile=picfile,
                                                  template_path=template_path.parent,
                                                  template_file=template_path.name)
            if not ok:
                return None
        except FileNotFoundError as e:
            if DEBUG:
                raise
            print('Unable to make report from cif file.')
            not_ok = e
            show_general_warning(self, "The report templates could not be found:\n" + str(not_ok))
            return
        except PermissionError:
            if DEBUG:
                raise
            print('Unable to open cif file')
            show_general_warning(self, f'The report document {report_filename.name} could not be opened.\n'
                                       'Is the file already opened?')
            return
        if not self.running_inside_unit_test:
            self.open_report_document(report_filename, multi_table_document)
            # Save report and other files to a zip file:
            self.zip_report(report_filename)

    def zip_report(self, report_filename: Path) -> None:
        from finalcif.report.archive_report import ArchiveReport
        zipfile = self.cif.finalcif_file.with_suffix('.zip')
        if zipfile.exists():
            zipname = next_path(str(zipfile.parent / Path(zipfile.stem + '-%s.zip')))
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
        with suppress(Exception):
            prp_list = self.cif.finalcif_file.parent.glob('*.prp')
            sorted_prp = sorted(prp_list, key=lambda x: x.stat().st_mtime)
            arc.zip.write(filename=sorted_prp[-1], arcname=sorted_prp[-1].name)

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

    def save_current_cif_file(self) -> bool | None:
        """
        Saves the current cif file and stores the information of the third column.
        """
        if not self.cif:
            # No file is opened
            return None
        if not self.cif.is_multi_cif:
            self.cif.rename_data_name(''.join(self.ui.datanameComboBox.currentText().split(' ')))
        self.store_data_from_table_rows()
        self.save_ccdc_number()
        self.cif.set_order_keys(self.ui.cifOrderWidget.order_keys)
        try:
            self.cif.save()
            self.status_bar.show_message(f'  File Saved:  {self.cif.finalcif_file}', 10)
            if DEBUG:
                print('File saved ...')
            return True
        except Exception as e:
            print('Unable to save file:')
            print(e)
            show_general_warning(self, 'Can not save file: ' + str(e))
            return False

    def store_data_from_table_rows(self) -> None:
        """
        Stores the data from the main table in the cif object.
        """
        changes_cif: CifContainer | None = None
        if self.options.track_changes:
            try:
                changes_cif = self.get_changes_cif(self.finalcif_changes_filename)
            except Exception as e:
                print('Unable to create changes CIF:', e)
                unable_to_open_message(parent=self, filepath=self.finalcif_changes_filename, not_ok=e)
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
                if self.cif[vhead] != col_edit and changes_cif and vhead != '_audit_creation_method':
                    changes_cif[vhead] = col_edit
                try:
                    self.cif[vhead] = col_edit
                except (OSError, RuntimeError, ValueError) as e:
                    print('Can not take cif info from table:', e)
            elif changes_cif:
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
        if (changes_cif.fileobj.exists() and changes_cif.fileobj.stat().st_size == 0) or changes_cif.is_empty():
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
                    changes_cif.add_loop_to_cif(loop_tags=loop.tags, row_values=loop.values)
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
                self.add_row(key=key, value=value)
                self.ui.cif_main_table.setText(key=key, column=Column.EDIT, color=None, txt=value)
        for loop in changes.loops:
            self.cif.add_loop_to_cif(loop_tags=loop.tags, row_values=loop.values)
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
        font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
        # increases the pont size every time a bit more :)
        # size = font.pointSize()
        # font.setPointSize(14)
        doc.setDefaultFont(font)
        final_textedit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        final_textedit.setPlainText(self.cif.finalcif_file.read_text(encoding='utf-8', errors='ignore'))

    def import_additional_cif(self, filename: str):
        """
        Import an additional cif file to the main table.
        """
        imp_cif: CifContainer | None = None
        if not filename:
            filename = cif_file_open_dialog(parent=self, filter="CIF file (*.cif *.pcf *.cif_od *.cfx *.sqf)")
        if not filename:
            return
        try:
            imp_cif = CifContainer(Path(filename))
        except RuntimeError as e:
            show_general_warning(self, f'Could not import {filename}:\n' + str(e))
            return
        except GemmiError as e:
            warning = f'Problems parsing file: {filename}:\n' + str(e)
            if 'data_' in str(e):
                warning = warning + "\n\nA CIF needs to start with 'data_[some_name]'."
                show_general_warning(self, warning)
                return
            unable_to_open_message(self, Path(self.cif.filename), e)
            return
        except OSError as e:
            show_general_warning(self, f'Unable to open file {filename}:\n' + str(e))
            return
        self.check_cif_for_missing_values_before_really_open_it()
        self.import_selector = ImportSelector(self, import_cif=imp_cif, target_cif=self.cif, settings=self.settings)
        self.import_selector.show_import_window()
        self.import_selector.import_clicked.connect(self._do_import_cif_after_selection)

    def _do_import_cif_after_selection(self, keys: list[str], loops: list[list[str]]) -> None:
        self._import_key_value_pairs(keys)
        self._import_loops(loops)
        self.add_audit_creation_method()
        self.import_selector.deleteLater()
        self.import_selector.close()

    def _import_key_value_pairs(self, keys: list[str]) -> None:
        for key in keys:
            value = self.import_selector.import_cif[key]
            if key in self.ui.cif_main_table.vheaderitems:
                self.ui.cif_main_table.setText(key=key, column=Column.EDIT, txt=value, color=light_green)
            else:
                self.add_row(key, value, at_start=True)

    def _import_loops(self, loops: list[list[str]]) -> None:
        for loop in loops:
            new_loop = self.cif.block.init_loop('', loop)
            for row in self.import_selector.import_cif.block.find(loop):
                new_loop.add_row(list(row))

    def load_cif_file(self, filepath: Path, block=0, load_changes: bool = True) -> None:
        """
        Opens the cif file and fills information into the main table.
        """
        self.ui.datanameComboBox.blockSignals(True)
        if not filepath:
            filepath = Path(cif_file_open_dialog(parent=self, last_dir=self.get_last_workdir()))
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
            unable_to_open_message(self, filepath, not_ok)
            return None
        if not self.cif.is_valid_structure_cif and not self.cif.doc.find_block('global'):
            show_general_warning(self, "The CIF file you are about to open contains no structure.\n\n"
                                       "Use the Import button below to import metadata.")
            return None
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
            self._flash_block_combobox()
        self.cif.set_order_keys(self.ui.cifOrderWidget.order_keys)
        # Enable to find widgets without parent:
        # QtCore.QTimer(self).singleShot(1000, self.find_widgets_without_parent)

    def find_widgets_without_parent(self) -> None:
        print('Finding parents...')
        all_widgets = app.allWidgets()
        no_parent_widgets = [widget for widget in all_widgets if widget.parent is None]
        print(f"Found {len(no_parent_widgets)} widget(s) out of {len(all_widgets)} without parent:")
        for widget in no_parent_widgets:
            print(widget, widget.objectName())

    def _flash_block_combobox(self) -> None:
        orig_pal = self.ui.datanameComboBox.palette()
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.ColorRole.Base, light_blue)
        self.ui.datanameComboBox.setAutoFillBackground(True)
        # short after start, because window size is not finished before:
        QtCore.QTimer(self).singleShot(1500, lambda: self.ui.datanameComboBox.setPalette(pal))
        QtCore.QTimer(self).singleShot(2600, lambda: self.ui.datanameComboBox.setPalette(orig_pal))

    def add_data_names_to_combobox(self) -> None:
        self.ui.datanameComboBox.clear()
        for block in self.cif.doc:
            self.ui.datanameComboBox.addItem(block.name)

    def _clear_state_before_block_load(self) -> None:
        self.status_bar.show_message('')
        self.ui.ckf_textedit.clear()
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
            show_general_warning(parent=self, window_title='Unable to open file',
                                 warn_text='Invalid characters in file!',
                                 info_text=f'The file "{Path(self.cif.doc.source)}" has invalid '
                                           f'characters in line(s)'
                                           f' {", ".join([str(x + 1) for x in nums])}.'
                                           '\n\nOnly ascii characters are allowed.')
        except Exception as e:
            not_ok = e
            print(e)
            # if DEBUG:
            raise
            # unable_to_open_message(Path(self.cif.filename), not_ok)
        self.load_recent_cifs_list()
        self.set_vertical_header_width()
        if self.options.track_changes and load_changes:
            changes_exist = False
            if self.changes_cif_has_zero_size():
                self.finalcif_changes_filename.unlink(missing_ok=True)
            elif self.finalcif_changes_filename.exists() and self.changes_cif_has_values():
                changes_exist = True
            if changes_exist and not self.running_inside_unit_test and self.changes_answer == 0 and not self.cif.is_multi_cif:
                self.changes_answer = QMessageBox.question(self, 'Previous changes found',
                                                           f'Previous changes from a former FinalCif session '
                                                           f'were found in\n{self.finalcif_changes_filename.name}.\n\n'
                                                           'Do you wish to reload them?',
                                                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if self.changes_answer == QMessageBox.StandardButton.Yes:
                try:
                    self.load_changes_cif()
                except GemmiError as e:
                    unable_to_open_message(parent=self, filepath=self.finalcif_changes_filename, not_ok=e)
            if self.running_inside_unit_test and changes_exist:
                self.load_changes_cif()
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
            if not (self.ui.MainStackedWidget.on_checkcif_page() or self.ui.MainStackedWidget.on_info_page()):
                self.ui.MainStackedWidget.got_to_main_page()
            self.deposit.cif = self.cif
            # self.ui.cif_main_table.resizeRowsToContents()
            self.ui.cif_main_table.vheaderitems.clear()
            for row_number in range(self.ui.cif_main_table.model().rowCount()):
                vhead_key = self.get_key_by_row_number(row_number)
                self.ui.cif_main_table.vheaderitems.insert(row_number, vhead_key)
            if self.ui.MainStackedWidget.on_info_page():
                self.show_residuals()
                self.redraw_molecule()
            t = QtCore.QTimer(self)
            t.singleShot(1000, self.check_cecksums)

    def _delete_current_block(self, index: int) -> None:
        self.cif.delete_block(index)
        self.add_data_names_to_combobox()
        self.ui.datanameComboBox.setCurrentIndex(0)

    def set_vertical_header_width(self):
        """
        Sets the width of the vertical header to the length of the longest string in the list.
        """
        vheader: QtWidgets.QHeaderView = self.ui.cif_main_table.verticalHeader()
        fm = QtGui.QFontMetrics(vheader.font(), self)
        try:
            # noinspection PyTypeChecker
            longest_string: str = max(self.ui.cif_main_table.vheaderitems, key=len)
        except ValueError:
            longest_string = '_chemical_formula_sum_foo'
        vheader.setMaximumWidth(fm.horizontalAdvance(longest_string + 'O'))

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
            txt = (f'<body style="">{SpaceGroups().to_html(self.cif.space_group)} '
                   f'&thinsp;({spgrps[self.cif.space_group][1].get("itnumber")})</body>')
            self.ui.Spacegroup_top_LineEdit.setText(txt)
        except Exception as e:
            print('Space group error:', str(e))
            self.ui.Spacegroup_top_LineEdit.setText(self.cif.space_group)

    def set_shredcif_state(self) -> None:
        if ShredCIF(cif=self.cif, statusbar=self.status_bar).cif_has_hkl_or_res_file():
            self.ui.ShredCifButton.setEnabled(True)
        else:
            self.ui.ShredCifButton.setDisabled(True)

    def append_cif(self, cif_file: Path):
        if not cif_file:
            cif_file = self.get_file_from_dialog()
        if not cif_file:
            return
        cif2 = CifContainer(cif_file)
        if cif2.is_multi_cif:
            show_general_warning(self, 'Can add single data CIFs only!')
            return
        if cif2.block.name in [x.name for x in self.cif.doc]:
            show_general_warning(self, warn_text='Duplicate block',
                                 info_text=f'Data block name "<b>{cif2.block.name}</b>" '
                                           f'already present in current CIF!')
            return
        self.cif.save()
        self.load_cif_file(filepath=self.cif.finalcif_file, load_changes=False)
        self.cif.doc.add_copied_block(block=cif2.block, pos=-1)
        self.cif.save()
        self.load_cif_file(filepath=self.cif.fileobj, load_changes=False)

    def get_file_from_dialog(self) -> Path | None:
        fp = cif_file_open_dialog(parent=self, last_dir=self.get_last_workdir())
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
                show_general_warning(self, f"Attention in CIF line {errlist[1]}:\n"
                                           f"'{errlist[2].split()[0]}' has no value.")

    def get_last_workdir(self) -> str:
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
            show_general_warning(self, "The file you tried to open does not exist!")
            return False
        if filepath.stat().st_size == 0:
            show_general_warning(self, 'This file has zero byte size!')
            return False
        return True

    def warn_about_bad_cif(self):
        show_general_warning(self, "You have non-ascii characters like umlauts in the SHELX file "
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
        self.ui.dataReflnsLineEdit.setText(f"{dat_param:<5.1f}")
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
        self.ui.dLineEdit.setText(f"{d:5.3f}")
        try:
            compl = float(self.cif['_diffrn_measured_fraction_theta_max']) * 100
            if not compl:
                compl = 0.0
        except (TypeError, ValueError):
            compl = 0.0
        try:
            self.ui.completeLineEdit.setText(f"{compl:<5.1f}")
        except ValueError:
            pass
        self.ui.wavelengthLineEdit.setText(f"{wavelen}")
        self.ui.reflTotalLineEdit.setText(self.cif['_diffrn_reflns_number'])
        self.ui.uniqReflLineEdit.setText(self.cif['_refine_ls_number_reflns'])
        self.ui.refl2sigmaLineEdit.setText(self.cif['_reflns_number_gt'])
        peak = self.cif['_refine_diff_density_max']
        if peak:
            self.ui.peakLineEdit.setText("{} / {}".format(peak, self.cif['_refine_diff_density_min']))
        self._show_shelx_file()
        try:
            QtCore.QTimer(self).singleShot(0, self.view_molecule)
            # threading.Thread(target=self.view_molecule).start()
        except Exception:
            print('Molecule view crashed!')

    def _show_shelx_file(self) -> None:
        if self.cif.res_file_data:
            self.ui.shelx_warn_TextEdit.clear()
            if hasattr(self.cif.shx, 'restraint_errors') and self.cif.shx.restraint_errors:
                self.ui.shelx_warn_TextEdit.show()
                self.ui.shelx_warn_TextEdit.setPlainText('Errors were found in the SHELX file:\n')
                self.ui.shelx_warn_TextEdit.appendPlainText('\n'.join(self.cif.shx.restraint_errors))
                vScrollBar = self.ui.shelx_warn_TextEdit.verticalScrollBar()
                vScrollBar.triggerAction(QScrollBar.SliderAction.SliderToMinimum)
            else:
                self.ui.shelx_warn_TextEdit.hide()
            self.ui.shelx_TextEdit.setPlainText(cif.as_string(self.cif.res_file_data))
        else:
            self.ui.shelx_TextEdit.setPlainText("No Shelx file available")
            self.ui.shelx_warn_TextEdit.hide()

    def view_molecule(self) -> None:
        if self.ui.growCheckBox.isChecked():
            self.ui.molGroupBox.setTitle('Completed Molecule')
            self.grow_molecule()
        else:
            self.ui.molGroupBox.setTitle('Asymmetric Unit')
            with suppress(Exception):
                self.ui.render_widget.open_molecule(list(self.cif.atoms_orth),
                                                    labels=self.ui.labelsCheckBox.isChecked())

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
        if Z and Z > 20.0 and (csystem in {'tricilinic', 'monoclinic'}):
            bad = True
        if Z and Z > 32.0 and (csystem in {'orthorhombic', 'tetragonal', 'trigonal', 'hexagonal', 'cubic'}):
            bad = True
        if bad:
            bad_z_message(self, Z)

    def get_data_sources(self) -> None:
        """
        Tries to determine the sources of missing data in the cif file, e.g. Tmin/Tmax from SADABS.
        """
        self.check_Z()
        self.sources = BrukerData(self, self.cif).sources
        if self.sources:
            # Add the CCDC number in case we have a deposition mail lying around:
            self.add_ccdc_number()
            if self.cif.shx and self.cif.shx.abin and not self.cif['_platon_squeeze_void_probe_radius']:
                show_general_warning(self, "A SQUEEZE refinement was detected.\n"
                                           "Please import the corresponding .sqf file\n"
                                           "from PLATON and complete the _platon_squeeze_void_content information "
                                           "in the 'Platon SQUEEZE voids' loop.")
        vheadlist = []
        for row_number in range(self.ui.cif_main_table.model().rowCount()):
            vheadlist.append(self.ui.cif_main_table.model().headerData(row_number, QtCore.Qt.Orientation.Vertical))
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
                elif txt and txt != '?':
                    self.ui.cif_main_table.setText(key=miss_key, column=Column.DATA, txt=txt, color=light_green)
                else:
                    self.ui.cif_main_table.setText(key=miss_key, column=Column.DATA, txt=txt, color=yellow)
            except (KeyError, TypeError):
                # TypeError my originate from incomplete self.missing_data list!
                # print(e, '##', miss_key)
                pass

    def add_ccdc_number(self):
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
        vhead_key = self.ui.cif_main_table.model().headerData(row_number, QtCore.Qt.Orientation.Vertical)
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
        self.cif.set_essential_keys(self.ui.cifOrderWidget.essential_keys)
        for key, value in self.cif.key_value_pairs():
            if not value or value in {'?', "'?'"}:
                self.missing_data.add(key)
                value = '?'
            self.add_row(key, value)
            if key == '_audit_creation_method':
                self.add_audit_creation_method(key)
                # QtCore.QTimer(self).singleShot(200, self.ui.cif_main_table.resizeRowsToContents)
            # print(key, value)
        if self.cif.is_multi_cif:
            self.refresh_combo_boxes()
        else:
            self.get_data_sources()
        self.erase_disabled_items()
        self.ui.cif_main_table.setCurrentItem(None)

    def check_cecksums(self):
        if "RUNNING_TEST" in os.environ:
            return
        if not self.cif.test_res_checksum():
            show_res_checksum_warning(parent=self)
        if not self.cif.test_hkl_checksum():
            show_hkl_checksum_warning(parent=self)

    def add_audit_creation_method(self, key: str = '_audit_creation_method') -> None:
        txt = 'FinalCif V{} by Daniel Kratzert, Freiburg {}, https://dkratzert.de/finalcif.html'
        strval = txt.format(VERSION, datetime.now().year)
        self.ui.cif_main_table.setText(key=key, column=Column.DATA, txt=strval)
        self.ui.cif_main_table.setText(key=key, column=Column.EDIT, txt=strval)

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
        # do_not_display = ('_diffrn_refln_index_h')
        for num, loop in enumerate(self.cif.loops):
            tags = loop.tags
            if not tags or len(tags) < 1:
                continue
            # if tags[0] in do_not_display:
            #    continue
            self.new_loop_tab(loop, num, tags)
        if self.cif.res_file_data:
            self.add_res_file_to_loops()

    def new_loop_tab(self, loop: gemmi.cif.Loop, num: int, tags: list[str]):
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
        font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
        # font.setPointSize(14)
        doc.setDefaultFont(font)
        textedit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        textedit.setReadOnly(True)

    def _go_to_new_loop_page(self) -> None:
        self.loopcreate = LoopCreator(parent=self, cif=self.cif)
        self.ui.LoopsTabWidget.addTab(self.loopcreate, 'Create Loops')
        self.ui.LoopsTabWidget.setCurrentIndex(self.ui.LoopsTabWidget.count() - 1)
        self.ui.revertLoopsPushButton.hide()
        self.ui.newLoopPushButton.hide()
        self.ui.deleteLoopButton.hide()
        self.loopcreate.saveLoopPushButton.clicked.connect(self.save_new_loop_to_cif)

    def _on_delete_current_loop(self) -> None:
        current_tab_index = self.ui.LoopsTabWidget.currentIndex()
        current_table_view: MyQTableView = self.ui.LoopsTabWidget.widget(current_tab_index)
        try:
            header_model: LoopTableModel | QtCore.QAbstractItemModel = current_table_view.horizontalHeader().model()
        except AttributeError:
            # Not a QTableView
            return
        header_item = header_model._header[0]
        loop: gemmi.cif.Loop = self.cif.block.find_loop(header_item).get_loop()
        table: gemmi.cif.Table = self.cif.block.find(loop.tags)
        table.erase()
        self.ui.LoopsTabWidget.removeTab(current_tab_index)

    def save_new_loop_to_cif(self):
        if self.loopcreate:
            loop = self.loopcreate.save_new_loop_to_cif()
            self.new_loop_tab(loop=loop, num=self.ui.LoopsTabWidget.count(), tags=self.loopcreate.tags)
            self.ui.LoopsTabWidget.removeTab(self.ui.LoopsTabWidget.count() - 2)
            self.loopcreate.deleteLater()
            self.ui.LoopsTabWidget.setCurrentIndex(self.ui.LoopsTabWidget.count() - 1)

    def add_row(self, key: str, value: str, at_start=False, position: int | None = None) -> None:
        """
        Create a empty row at bottom of cif_main_table. This method only fills cif data in the
        first column. Not the data from external sources!
        """
        if at_start:
            row_num = 0
        elif position and position > 0:
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
            strval = gemmi.cif.as_string(value).strip('\n\r\t')
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
