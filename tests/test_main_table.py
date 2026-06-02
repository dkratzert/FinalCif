#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
from unittest.mock import patch

os.environ["RUNNING_TEST"] = 'True'
import unittest
from tests.helpers import AppWindowTestCase
from pathlib import Path

from qtpy.QtCore import Qt, QEvent, QModelIndex
from qtpy.QtGui import QColor, QBrush, QKeyEvent
from qtpy.QtTest import QTest
from qtpy.QtWidgets import QApplication

from finalcif.appwindow import AppWindow
from finalcif.gui.cif_table_model import CifTableModel, CifRowData
from finalcif.gui.cif_table_view import CifTableView
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

    def test_pasted_existing_cif_path_opens_file(self):
        target_cif = (data.parent / 'test-data/1000006.cif').resolve()
        line_edit = self.app.ui.SelectCif_LineEdit
        line_edit.clear()
        line_edit.setFocus()
        QApplication.clipboard().setText(f'"{target_cif}"')

        with patch.object(self.app, 'load_cif_file') as mock_load:
            QTest.keyClick(line_edit, Qt.Key.Key_V, Qt.KeyboardModifier.ControlModifier)

        mock_load.assert_called_once_with(target_cif)

    def test_return_pressed_existing_cif_path_opens_file_without_cod_lookup(self):
        target_cif = (data.parent / 'test-data/1000006.cif').resolve()
        self.app.ui.SelectCif_LineEdit.setText(str(target_cif))

        with patch.object(self.app, 'load_cif_file') as mock_load, patch('finalcif.appwindow.requests.get') as mock_get:
            self.app.check_if_file_field_contains_database_number()

        mock_load.assert_called_once_with(target_cif)
        mock_get.assert_not_called()


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


# ---------------------------------------------------------------------------
# Isolated tests – no AppWindow, just CifTableModel / CifTableView directly.
# ---------------------------------------------------------------------------

class TestCifTableModelIsolated(unittest.TestCase):
    """Tests for CifTableModel that cover previously untested branches."""

    def _make_model(self) -> CifTableModel:
        model = CifTableModel()
        model.bulk_load([
            CifRowData(key='_key_a', cif_value='val_a', data_value='d_a', edit_value='e_a'),
            CifRowData(key='_key_sep', is_separator=True),
            CifRowData(key='_key_c', cif_value='val_c',
                       cif_color=QColor(255, 0, 0),
                       data_color=QColor(0, 255, 0),
                       edit_color=QColor(0, 0, 255)),
        ])
        return model

    # --- data() ---

    def test_data_invalid_index_returns_none(self):
        model = self._make_model()
        self.assertIsNone(model.data(QModelIndex(), Qt.ItemDataRole.DisplayRole))

    def test_data_separator_background_role_returns_brush(self):
        model = self._make_model()
        result = model.data(model.index(1, 0), Qt.ItemDataRole.BackgroundRole)
        self.assertIsInstance(result, QBrush)

    def test_data_separator_display_role_returns_empty_string(self):
        model = self._make_model()
        self.assertEqual('', model.data(model.index(1, 0), Qt.ItemDataRole.DisplayRole))

    def test_data_separator_edit_role_returns_empty_string(self):
        model = self._make_model()
        self.assertEqual('', model.data(model.index(1, 0), Qt.ItemDataRole.EditRole))

    def test_data_separator_other_role_returns_none(self):
        model = self._make_model()
        self.assertIsNone(model.data(model.index(1, 0), Qt.ItemDataRole.DecorationRole))

    # --- setData() ---

    def test_setdata_invalid_index_returns_false(self):
        model = self._make_model()
        self.assertFalse(model.setData(QModelIndex(), 'v', Qt.ItemDataRole.EditRole))

    def test_setdata_background_role_col0(self):
        model = self._make_model()
        color = QColor(1, 2, 3)
        self.assertTrue(model.setData(model.index(0, 0), color, Qt.ItemDataRole.BackgroundRole))
        self.assertEqual(color, model._rows[0].cif_color)

    def test_setdata_background_role_col1(self):
        model = self._make_model()
        color = QColor(4, 5, 6)
        self.assertTrue(model.setData(model.index(0, 1), color, Qt.ItemDataRole.BackgroundRole))
        self.assertEqual(color, model._rows[0].data_color)

    def test_setdata_background_role_col2(self):
        model = self._make_model()
        color = QColor(7, 8, 9)
        self.assertTrue(model.setData(model.index(0, 2), color, Qt.ItemDataRole.BackgroundRole))
        self.assertEqual(color, model._rows[0].edit_color)

    def test_setdata_unknown_role_returns_false(self):
        model = self._make_model()
        self.assertFalse(model.setData(model.index(0, 0), 'x', Qt.ItemDataRole.DecorationRole))

    # --- flags() ---

    def test_flags_invalid_index_returns_no_flags(self):
        model = self._make_model()
        self.assertEqual(Qt.ItemFlag.NoItemFlags, model.flags(QModelIndex()))

    def test_flags_separator_row_is_only_enabled(self):
        model = self._make_model()
        result = model.flags(model.index(1, 0))
        self.assertEqual(Qt.ItemFlag.ItemIsEnabled, result)

    def test_flags_regular_col0_not_editable(self):
        model = self._make_model()
        result = model.flags(model.index(0, 0))
        self.assertTrue(result & Qt.ItemFlag.ItemIsEnabled)
        self.assertTrue(result & Qt.ItemFlag.ItemIsSelectable)
        self.assertFalse(result & Qt.ItemFlag.ItemIsEditable)

    def test_flags_regular_col2_is_editable(self):
        model = self._make_model()
        result = model.flags(model.index(0, 2))
        self.assertTrue(result & Qt.ItemFlag.ItemIsEditable)

    # --- headerData() ---

    def test_header_data_vertical_background_separator_returns_brush(self):
        model = self._make_model()
        result = model.headerData(1, Qt.Orientation.Vertical, Qt.ItemDataRole.BackgroundRole)
        self.assertIsInstance(result, QBrush)

    def test_header_data_vertical_background_non_separator_returns_none(self):
        model = self._make_model()
        result = model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.BackgroundRole)
        self.assertIsNone(result)

    # --- row_from_key() ---

    def test_row_from_key_missing_raises_value_error(self):
        model = self._make_model()
        with self.assertRaises(ValueError):
            model.row_from_key('_nonexistent_key')

    # --- remove_row() ---

    def test_remove_row_out_of_range_returns_empty_string(self):
        model = self._make_model()
        self.assertEqual('', model.remove_row(999))

    def test_remove_row_negative_returns_empty_string(self):
        model = self._make_model()
        self.assertEqual('', model.remove_row(-1))

    # --- get_row_data() ---

    def test_get_row_data_out_of_bounds_returns_none(self):
        model = self._make_model()
        self.assertIsNone(model.get_row_data(999))

    def test_get_row_data_negative_returns_none(self):
        model = self._make_model()
        self.assertIsNone(model.get_row_data(-1))


class TestCifTableViewIsolated(unittest.TestCase):
    """Tests for CifTableView that cover previously untested branches."""

    def _make_view(self) -> CifTableView:
        view = CifTableView()
        view.bulk_load([
            CifRowData(key='_key_a', cif_value='val_a', data_value='d_a', edit_value='e_a'),
            CifRowData(key='_key_b', cif_value='val_b', data_value='d_b', edit_value='e_b'),
            CifRowData(key='_key_c', cif_value='val_c', data_value='d_c', edit_value='e_c'),
        ])
        return view

    def setUp(self):
        self.view = self._make_view()

    def tearDown(self):
        self.view.close()

    # --- counts ---

    def test_columns_count(self):
        self.assertEqual(3, self.view.columns_count)

    # --- delete_row variants ---

    def test_delete_row_without_argument_uses_current_index(self):
        self.view.setCurrentCell(1, 0)
        count_before = self.view.rowCount()
        self.view.delete_row()
        self.assertEqual(count_before - 1, self.view.rowCount())

    def test_delete_row_out_of_range_is_silent(self):
        count_before = self.view.rowCount()
        self.view.delete_row(999)
        self.assertEqual(count_before, self.view.rowCount())

    def test_delete_current_row_via_private_method(self):
        self.view.setCurrentCell(0, 0)
        count_before = self.view.rowCount()
        self.view._delete_current_row()
        self.assertEqual(count_before - 1, self.view.rowCount())

    # --- navigation ---

    def test_set_current_cell_and_current_row(self):
        self.view.setCurrentCell(2, 1)
        self.assertEqual(2, self.view.currentRow())

    def test_goto_template_page_emits_text_template_signal(self):
        received = []
        self.view.textTemplate.connect(lambda r: received.append(r))
        self.view.goto_template_page(1)
        self.assertEqual([1], received)

    # --- search ---

    def test_search_empty_string_unhides_all_rows(self):
        self.view.search('_key_a')  # hide non-matching rows first
        self.view.search('')
        for row in range(self.view.rowCount()):
            self.assertFalse(self.view.isRowHidden(row))

    def test_search_filters_non_matching_rows(self):
        self.view.search('_key_a')
        self.assertFalse(self.view.isRowHidden(0))  # _key_a – matches
        self.assertTrue(self.view.isRowHidden(1))   # _key_b – hidden
        self.assertTrue(self.view.isRowHidden(2))   # _key_c – hidden

    # --- clipboard ---

    def test_copy_vhead_item_puts_key_in_clipboard(self):
        self.view.setCurrentCell(0, 0)
        self.view.copy_vhead_item()
        self.assertEqual('_key_a', QApplication.clipboard().text())

    # --- _vheader_section_click ---

    def test_vheader_click_out_of_range_does_not_call_help(self):
        with patch('finalcif.gui.cif_table_view.show_keyword_help') as mock_help:
            self.view._vheader_section_click(999)
        mock_help.assert_not_called()

    def test_vheader_click_unknown_key_shows_no_help_message(self):
        with patch('finalcif.gui.cif_table_view.show_keyword_help') as mock_help:
            self.view._vheader_section_click(0)  # _key_a not in cif_all_dict
        mock_help.assert_called_once()
        self.assertIn('No help available', mock_help.call_args[0][1])

    def test_vheader_click_vrf_key_shows_vrf_help(self):
        self.view.bulk_load([CifRowData(key='_vrf_alert_A', cif_value='')])
        with patch('finalcif.gui.cif_table_view.show_keyword_help') as mock_help:
            self.view._vheader_section_click(0)
        mock_help.assert_called_once()
        self.assertIn('Validation Response Form', mock_help.call_args[0][1])

    def test_vheader_click_known_cif_key_shows_dict_help(self):
        from finalcif.cif.all_cif_dicts import cif_all_dict
        known_key = next(iter(cif_all_dict))
        self.view.bulk_load([CifRowData(key=known_key, cif_value='')])
        with patch('finalcif.gui.cif_table_view.show_keyword_help') as mock_help:
            self.view._vheader_section_click(0)
        mock_help.assert_called_once()

    # --- eventFilter ---

    def test_event_filter_tab_key_navigates_to_edit_column(self):
        self.view.setCurrentCell(0, 0)
        event = QKeyEvent(QEvent.Type.KeyRelease, Qt.Key.Key_Tab, Qt.KeyboardModifier.NoModifier)
        result = self.view.eventFilter(self.view, event)
        self.assertTrue(result)
        self.assertEqual(2, self.view.currentIndex().column())

    def test_event_filter_backtab_key_goes_to_previous_row_edit_column(self):
        self.view.setCurrentCell(2, 0)
        event = QKeyEvent(QEvent.Type.KeyRelease, Qt.Key.Key_Backtab, Qt.KeyboardModifier.NoModifier)
        result = self.view.eventFilter(self.view, event)
        self.assertTrue(result)
        self.assertEqual(1, self.view.currentIndex().row())
        self.assertEqual(2, self.view.currentIndex().column())

    def test_event_filter_non_key_event_passes_through(self):
        event = QEvent(QEvent.Type.MouseButtonPress)
        result = self.view.eventFilter(self.view, event)
        self.assertFalse(result)

    # --- add_property_combobox TypeError ---

    def test_add_property_combobox_bad_value_does_not_raise(self):
        """TypeError from retranslate_delimiter(None) is caught; bad item is skipped."""
        bad_data = [(0, None)]
        # Should not propagate the TypeError; the bad item is silently skipped.
        self.view.add_property_combobox(bad_data, 0, '_key_a')
        combobox = self.view.cellWidget(0, Column.EDIT)
        # The bad item was skipped, so the combobox has no items from bad_data.
        self.assertEqual(0, combobox.count())

    def test_add_property_combobox_good_items_added_despite_bad_ones(self):
        """Good items are still added when bad ones are interspersed."""
        mixed_data = [(0, 'good_value'), (1, None), (2, 'another_good')]
        self.view.add_property_combobox(mixed_data, 0, '_key_a')
        combobox = self.view.cellWidget(0, Column.EDIT)
        self.assertEqual(2, combobox.count())
