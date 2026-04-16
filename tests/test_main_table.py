#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os

os.environ["RUNNING_TEST"] = 'True'
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor

from finalcif.appwindow import AppWindow
from finalcif.gui.custom_classes import Column
from finalcif.tools.misc import unify_line_endings

data = Path('tests')


# noinspection PyMissingTypeHints
class TestMainTableFieldBehavior(AppWindowTestCase):

    def setUp(self) -> None:
        self.testcif = (data / 'examples/1979688.cif').absolute()
        (data / '/examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        self.app = AppWindow(file=self.testcif)
        # self.app.show()
        self.app.settings.empty_deleted_list()
        self.app.ui.trackChangesCifCheckBox.setChecked(False)

    def tearDown(self) -> None:
        self.app.cif.finalcif_file.unlink(missing_ok=True)
        self.app.close()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        super().tearDown()

    def key_row(self, key: str) -> int:
        return self.app.ui.cif_main_table.row_from_key(key)

    def cell_widget(self, row: int, col: int) -> str:
        return str(self.app.ui.cif_main_table.cellWidget(row, col).__class__)

    def cell_text(self, key: str, col: int) -> str:
        return unify_line_endings(self.app.ui.cif_main_table.getTextFromKey(key, col))

    def equipment_click(self, field: str):
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = self.app.ui.EquipmentTemplatesListWidget.findItems(field, Qt.MatchStartsWith)[0]
        self.app.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.app.equipment.load_selected_equipment()

    ######

    def test_delete_row(self):
        rows = self.app.ui.cif_main_table.rowCount()
        self.app.ui.cif_main_table.delete_row(self.key_row('_audit_update_record'))
        self.assertEqual(rows - 1, self.app.ui.cif_main_table.rowCount())

    def test_get_text_by_key(self):
        self.assertEqual('geom', self.cell_text('_atom_sites_solution_hydrogens', Column.CIF))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', Column.DATA))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', Column.EDIT))

    def test_load_equipment(self):
        self.app.equipment.import_equipment_from_file(str(data.parent / 'test-data/Crystallographer_Details.cif'))
        # make sure contact author is selected
        self.equipment_click('Crystallographer Details')
        # It is important here, that the first column has 'dkratzert@gmx.de' in it:
        self.assertEqual('?',
                         self.app.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', Column.CIF))
        self.assertEqual('dkratzert@gmx.de',
                         self.app.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', Column.DATA))
        self.assertEqual('dkratzert@gmx.de',
                         self.app.ui.cif_main_table.getTextFromKey('_audit_contact_author_email', Column.EDIT))

    def test_field_types(self):
        # In the model/view architecture, all cells have persistent widgets (no QTableWidgetItem).
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         str(self.app.ui.cif_main_table.widget_from_key('_atom_sites_solution_hydrogens',
                                                                          Column.CIF).__class__))
        self.assertEqual("<class 'finalcif.gui.combobox.MyComboBox'>",
                         str(self.app.ui.cif_main_table.widget_from_key('_atom_sites_solution_hydrogens',
                                                                          Column.EDIT).__class__))

    def test_multicif(self):
        self.assertEqual(False, self.app.cif.is_multi_cif)
        self.assertEqual(1, len(self.app.cif.doc))
        self.app.append_cif(data.parent / 'test-data/1000006.cif')
        self.assertEqual(True, self.app.cif.is_multi_cif)
        self.assertEqual(2, len(self.app.cif.doc))


class TestMainTableRowHeights(AppWindowTestCase):
    """Tests that row heights in the main CIF table are reasonable.

    Exact pixel values vary across platforms, fonts, and DPI settings,
    so all assertions use generous range checks.
    """

    def setUp(self) -> None:
        self.testcif = (data / 'examples/1979688.cif').absolute()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        self.app = AppWindow(file=self.testcif)
        self.app.settings.empty_deleted_list()
        self.app.ui.trackChangesCifCheckBox.setChecked(False)
        self.table = self.app.ui.cif_main_table
        self.table.resizeRowsToContents()

    def tearDown(self) -> None:
        self.app.cif.finalcif_file.unlink(missing_ok=True)
        self.app.close()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        super().tearDown()

    def test_single_line_row_height(self):
        """A short single-line value like 'geom' should produce a compact row."""
        row = self.table.row_from_key('_atom_sites_solution_hydrogens')
        h = self.table.rowHeight(row)
        self.assertGreaterEqual(h, 10)
        self.assertLessEqual(h, 80)

    def test_separator_row_is_short(self):
        """The blue diagonal separator row should be very compact."""
        sep_row = self.app.complete_data_row
        self.assertGreaterEqual(sep_row, 0, 'Separator row not found')
        h = self.table.rowHeight(sep_row)
        self.assertLessEqual(h, 40)

    def test_shelx_res_file_row_height_bounded(self):
        """_shelx_res_file is truncated to MAX_DISPLAY_LINES; row should be medium height."""
        row = self.table.row_from_key('_shelx_res_file')
        h = self.table.rowHeight(row)
        self.assertGreaterEqual(h, 30)
        self.assertLessEqual(h, 500)

    def test_shelx_hkl_file_row_height_bounded(self):
        """_shelx_hkl_file is very large but truncated; row height must stay bounded."""
        row = self.table.row_from_key('_shelx_hkl_file')
        h = self.table.rowHeight(row)
        self.assertLessEqual(h, 600)

    def test_empty_value_row_stays_compact(self):
        """A row whose CIF value is '?' and has no other data should be compact."""
        row = self.table.row_from_key('_chemical_name_common')
        h = self.table.rowHeight(row)
        self.assertGreaterEqual(h, 10)
        self.assertLessEqual(h, 80)

    def test_row_height_after_equipment_load(self):
        """After loading equipment data the row should still have a reasonable height."""
        self.app.equipment.import_equipment_from_file(
            str(data.parent / 'test-data/Crystallographer_Details.cif'))
        self.app.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = self.app.ui.EquipmentTemplatesListWidget.findItems(
            'Crystallographer Details', Qt.MatchStartsWith)[0]
        self.app.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.app.equipment.load_selected_equipment()
        self.table.resizeRowsToContents()
        row = self.table.row_from_key('_audit_contact_author_email')
        h = self.table.rowHeight(row)
        self.assertLessEqual(h, 100)
