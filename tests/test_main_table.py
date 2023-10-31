#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from pathlib import Path

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from finalcif.appwindow import AppWindow
from finalcif.gui.custom_classes import Column
from finalcif.tools.misc import unify_line_endings

data = Path('tests')


# noinspection PyMissingTypeHints
class TestMainTableFieldBehavior(unittest.TestCase):

    def setUp(self) -> None:
        self.testcif = (data / 'examples/1979688.cif').absolute()
        (data / '/examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        self.myapp = AppWindow(file=self.testcif)
        # self.myapp.show()
        self.myapp.settings.empty_deleted_list()
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)

    def tearDown(self) -> None:
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)
        self.myapp.close()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)

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
        self.assertEqual(139, self.myapp.ui.cif_main_table.rowCount())

    def test_delete_row(self):
        self.myapp.ui.cif_main_table.delete_row(self.key_row('_audit_update_record'))
        self.assertEqual(138, self.myapp.ui.cif_main_table.rowCount())

    def test_delete_and_reappear(self):
        self.assertEqual(139, self.myapp.ui.cif_main_table.rowCount())
        self.myapp.ui.cif_main_table.delete_row(
            self.myapp.ui.cif_main_table.row_from_key('_atom_sites_solution_primary'))
        # One less than before:
        self.assertEqual(138, self.myapp.ui.cif_main_table.rowCount())
        # Line is deleted:
        self.assertFalse('_atom_sites_solution_primary' in self.myapp.ui.cif_main_table.vheaderitems)

    def test_get_text_by_key(self):
        self.assertEqual('geom', self.cell_text('_atom_sites_solution_hydrogens', Column.CIF))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', Column.DATA))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', Column.EDIT))

    def test_Crystallographer_in_equipment_list(self):
        self.assertEqual('Crystallographer Details', self.myapp.ui.EquipmentTemplatesListWidget.item(1).text())

    def test_load_equipment(self):
        self.myapp.equipment.import_equipment_from_file(str(data.parent / 'test-data/Crystallographer_Details.cif'))
        # make sure contact author is selected
        self.equipment_click('Crystallographer Details')
        # It is important here, that the first column has 'dkratzert@gmx.de' in it:
        self.assertEqual('?',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', Column.CIF))
        self.assertEqual('dkratzert@gmx.de',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', Column.DATA))
        self.assertEqual('dkratzert@gmx.de',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', Column.EDIT))

    def test_field_types(self):
        self.assertEqual("<class 'NoneType'>",
                         str(self.myapp.ui.cif_main_table.itemFromKey('_atom_sites_solution_hydrogens',
                                                                      Column.CIF).__class__))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_atom_sites_solution_hydrogens',
                                                                          Column.CIF).__class__))

    def test_combobox_field(self):
        self.assertEqual("<class 'finalcif.gui.combobox.MyComboBox'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_atom_sites_solution_hydrogens',
                                                                          Column.EDIT).__class__))

    def test_plaintextedit_field(self):
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_audit_contact_author_address',
                                                                          Column.CIF).__class__))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_audit_contact_author_address',
                                                                          Column.DATA).__class__))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.widget_from_key('_audit_contact_author_address',
                                                                          Column.EDIT).__class__))

    def test_multicif(self):
        self.assertEqual(False, self.myapp.cif.is_multi_cif)
        self.assertEqual(1, len(self.myapp.cif.doc))
        self.myapp.append_cif(data.parent / 'test-data/1000006.cif')
        self.assertEqual(True, self.myapp.cif.is_multi_cif)
        self.assertEqual(2, len(self.myapp.cif.doc))
