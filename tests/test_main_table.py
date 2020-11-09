#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import sys
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow
from gui.custom_classes import COL_CIF, COL_DATA, COL_EDIT
from tests.helpers import unify_line_endings

app = QApplication(sys.argv)


class TestMainTableFieldBehavior(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp = AppWindow(self.testcif)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()  # For full screen view

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)

    def key_row(self, key: str) -> int:
        return self.myapp.ui.cif_main_table.row_from_key(key)

    def cell_widget(self, row: int, col: int) -> str:
        return str(self.myapp.ui.cif_main_table.cellWidget(row, col).__class__)

    def cell_text(self, key: str, col: int) -> str:
        return unify_line_endings(self.myapp.ui.cif_main_table.getTextFromKey(key, col))

    def equipment_click(self, field: str):
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems(field, Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.equipment.load_selected_equipment()

    def get_background_color(self, key: str, col: int) -> QColor:
        return self.myapp.ui.cif_main_table.itemFromKey(key, col).background().color()

    ######

    def test_rowcounts(self):
        self.assertEqual(130, self.myapp.ui.cif_main_table.rowCount())

    def test_delete_row(self):
        self.myapp.ui.cif_main_table.delete_row(self.key_row('_audit_update_record'))
        self.assertEqual(129, self.myapp.ui.cif_main_table.rowCount())

    def test_delete_and_reappear(self):
        self.myapp.ui.cif_main_table.delete_row(16)
        # cline count stays the same:
        self.assertEqual(130, self.myapp.ui.cif_main_table.rowCount())
        self.assertEqual('?', self.cell_text('_atom_sites_solution_primary', COL_CIF))
        # method comes from solution program now:
        self.assertEqual('direct', self.cell_text('_atom_sites_solution_primary', COL_DATA))
        # This is an essential key, it reappears after reload:
        self.assertEqual(0, self.key_row('_atom_sites_solution_primary'))

    def test_get_text_from_item(self):
        self.assertEqual('geom', self.myapp.ui.cif_main_table.item(15, COL_CIF).text())
        self.assertEqual('', self.myapp.ui.cif_main_table.item(15, COL_DATA).text())
        self.assertEqual('', self.myapp.ui.cif_main_table.item(15, COL_EDIT).text())

    def test_get_text_by_key(self):
        self.assertEqual('geom', self.cell_text('_atom_sites_solution_hydrogens', COL_CIF))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', COL_DATA))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', COL_EDIT))

    def test_CCDC_in_equipment_list(self):
        self.assertEqual('CCDC number', self.myapp.ui.EquipmentTemplatesListWidget.item(1).text())

    def test_load_equipment(self):
        # make sure contact author is selected
        self.equipment_click('Contact author name and')
        # It is important here, that the first column has 'daniel.kratzert@ac.uni-freiburg.de' in it:
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', COL_CIF))
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', COL_DATA))
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', COL_EDIT))

    def test_field_types(self):
        self.assertEqual("<class 'gui.custom_classes.MyTableWidgetItem'>",
                         str(self.myapp.ui.cif_main_table.itemFromKey('_atom_sites_solution_hydrogens',
                                                                      COL_CIF).__class__))
        self.assertEqual("<class 'NoneType'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_atom_sites_solution_hydrogens',
                                                                          COL_CIF).__class__))

    def test_combobox_field(self):
        self.assertEqual("<class 'gui.custom_classes.MyComboBox'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_atom_sites_solution_hydrogens',
                                                                          COL_EDIT).__class__))

    def test_plaintextedit_field(self):
        self.assertEqual("<class 'gui.custom_classes.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_audit_contact_author_address',
                                                                          COL_CIF).__class__))
        self.assertEqual("<class 'gui.custom_classes.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_audit_contact_author_address',
                                                                          COL_DATA).__class__))
        self.assertEqual("<class 'gui.custom_classes.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_audit_contact_author_address',
                                                                          COL_EDIT).__class__))
