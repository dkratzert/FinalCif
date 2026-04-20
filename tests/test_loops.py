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

from qtpy.QtCore import Qt, QModelIndex
from qtpy.QtWidgets import QApplication, QTabWidget, QPlainTextEdit

from gemmi.cif import as_string

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.custom_classes import light_blue, light_red
from finalcif.gui.loops import LoopsPage, LoopTableModel, MyQTableView
from finalcif.tools.misc import unify_line_endings

app = QApplication.instance()
if app is None:
    app = QApplication([])

data = Path('tests')
SMALL_CIF = data / 'examples/1979688_small.cif'
FULL_CIF = data / 'examples/1979688.cif'  # has res_file_data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_model(header=None, rows=None) -> LoopTableModel:
    """Build a LoopTableModel directly without a CIF file."""
    if header is None:
        header = ['_col_a', '_col_b', '_col_c']
    if rows is None:
        rows = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    return LoopTableModel(header, rows)


def _make_view_with_model(header=None, rows=None) -> MyQTableView:
    model = _make_model(header, rows)
    view = MyQTableView(parent=None)
    view.setModel(model)
    return view


# ---------------------------------------------------------------------------
# LoopTableModel unit tests (no CIF file needed)
# ---------------------------------------------------------------------------

class TestLoopTableModel(unittest.TestCase):

    def setUp(self):
        self.model = _make_model()

    # --- structural properties ---

    def test_header_property(self):
        self.assertEqual(['_col_a', '_col_b', '_col_c'], self.model.header)

    def test_loop_data_property(self):
        self.assertEqual([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']], self.model.loop_data)

    def test_row_count(self):
        self.assertEqual(3, self.model.rowCount())

    def test_column_count(self):
        self.assertEqual(3, self.model.columnCount())

    def test_column_count_empty_data(self):
        m = LoopTableModel(['_a'], [])
        self.assertEqual(0, m.columnCount())

    def test_header_data_display_role(self):
        result = self.model.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        self.assertEqual('_col_b', result)

    def test_header_data_out_of_range_returns_empty(self):
        result = self.model.headerData(99, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        self.assertEqual('', result)

    # --- flags ---

    def test_flags_valid_index(self):
        idx = self.model.index(0, 0)
        flags = self.model.flags(idx)
        self.assertTrue(flags & Qt.ItemFlag.ItemIsEditable)
        self.assertTrue(flags & Qt.ItemFlag.ItemIsEnabled)
        self.assertTrue(flags & Qt.ItemFlag.ItemIsSelectable)

    def test_flags_invalid_index_returns_none(self):
        self.assertIsNone(self.model.flags(QModelIndex()))

    # --- data roles ---

    def test_data_display_role(self):
        idx = self.model.index(0, 0)
        self.assertEqual('1', self.model.data(idx, Qt.ItemDataRole.DisplayRole))

    def test_data_edit_role(self):
        idx = self.model.index(1, 2)
        self.assertEqual('6', self.model.data(idx, Qt.ItemDataRole.EditRole))

    def test_data_size_hint_role(self):
        from qtpy.QtCore import QSize
        idx = self.model.index(0, 0)
        result = self.model.data(idx, Qt.ItemDataRole.SizeHintRole)
        self.assertEqual(QSize(120, 50), result)

    def test_data_background_role_unmodified_valid_returns_none(self):
        idx = self.model.index(0, 0)
        result = self.model.data(idx, Qt.ItemDataRole.BackgroundRole)
        self.assertIsNone(result)

    def test_data_background_role_modified_valid_returns_light_blue(self):
        idx = self.model.index(0, 0)
        self.model.setData(idx, '99', Qt.ItemDataRole.EditRole)
        result = self.model.data(idx, Qt.ItemDataRole.BackgroundRole)
        self.assertEqual(light_blue, result)

    def test_data_background_role_invalid_value_returns_light_red(self):
        # Use a header key that has a float validator
        m = LoopTableModel(['_cell_length_a'], [['not_a_number']])
        idx = m.index(0, 0)
        result = m.data(idx, Qt.ItemDataRole.BackgroundRole)
        self.assertEqual(light_red, result)

    def test_data_tooltip_role_with_validator(self):
        m = LoopTableModel(['_cell_length_a'], [['5.0']])
        idx = m.index(0, 0)
        tip = m.data(idx, Qt.ItemDataRole.ToolTipRole)
        self.assertIsNotNone(tip)
        self.assertIsInstance(tip, str)

    def test_data_tooltip_role_no_validator_returns_none(self):
        idx = self.model.index(0, 0)
        self.assertIsNone(self.model.data(idx, Qt.ItemDataRole.ToolTipRole))

    # --- setData ---

    def test_set_data_updates_value(self):
        idx = self.model.index(0, 0)
        self.model.setData(idx, 'new', Qt.ItemDataRole.EditRole)
        self.assertEqual('new', self.model.loop_data[0][0])

    def test_set_data_records_modification(self):
        idx = self.model.index(1, 2)
        self.model.setData(idx, 'changed', Qt.ItemDataRole.EditRole)
        self.assertEqual(1, len(self.model.modified))
        entry = self.model.modified[0]
        self.assertEqual(1, entry['row'])
        self.assertEqual(2, entry['column'])
        self.assertEqual('6', entry['previous'])

    def test_set_data_wrong_role_returns_false(self):
        idx = self.model.index(0, 0)
        result = self.model.setData(idx, 'x', Qt.ItemDataRole.DisplayRole)
        self.assertFalse(result)

    # --- removeRow ---

    def test_remove_row(self):
        self.model.removeRow(1)
        self.assertEqual(2, self.model.rowCount())
        self.assertEqual(['7', '8', '9'], self.model.loop_data[1])

    def test_remove_row_emits_row_deleted(self):
        emitted = []
        self.model.rowDeleted.connect(lambda h, r: emitted.append((h, r)))
        self.model.removeRow(0)
        self.assertEqual(1, len(emitted))
        self.assertEqual(0, emitted[0][1])

    def test_remove_row_from_empty_model_returns_false(self):
        m = LoopTableModel(['_a'], [])
        self.assertFalse(m.removeRow(0))

    # --- add_empty_row ---

    def test_add_empty_row_increases_row_count(self):
        self.model.add_empty_row()
        self.assertEqual(4, self.model.rowCount())
        self.assertEqual(['', '', ''], self.model.loop_data[3])

    def test_add_empty_row_on_empty_model_is_noop(self):
        m = LoopTableModel(['_a', '_b'], [])
        m.add_empty_row()
        self.assertEqual(0, m.rowCount())

    # --- move_row_down ---

    def test_move_row_down_returns_true(self):
        self.assertTrue(self.model.move_row_down(0))

    def test_move_row_down_changes_order(self):
        self.model.move_row_down(0)
        self.assertEqual(['4', '5', '6'], self.model.loop_data[0])
        self.assertEqual(['1', '2', '3'], self.model.loop_data[1])

    def test_move_row_down_at_last_row_returns_false(self):
        self.assertFalse(self.model.move_row_down(2))

    def test_move_row_down_single_row_returns_false(self):
        m = LoopTableModel(['_a'], [['x']])
        self.assertFalse(m.move_row_down(0))

    # --- move_row_up ---

    def test_move_row_up_returns_true(self):
        self.assertTrue(self.model.move_row_up(1))

    def test_move_row_up_changes_order(self):
        self.model.move_row_up(2)
        self.assertEqual(['7', '8', '9'], self.model.loop_data[1])
        self.assertEqual(['4', '5', '6'], self.model.loop_data[2])

    def test_move_row_up_at_first_row_returns_false(self):
        self.assertFalse(self.model.move_row_up(0))

    def test_move_row_up_single_row_returns_false(self):
        m = LoopTableModel(['_a'], [['x']])
        self.assertFalse(m.move_row_up(0))

    # --- revert ---

    def test_revert_restores_original_values(self):
        idx = self.model.index(0, 0)
        self.model.setData(idx, 'changed', Qt.ItemDataRole.EditRole)
        self.assertEqual('changed', self.model.loop_data[0][0])
        self.model.revert()
        self.assertEqual('1', self.model.loop_data[0][0])

    def test_revert_clears_modified_list(self):
        idx = self.model.index(0, 0)
        self.model.setData(idx, 'changed', Qt.ItemDataRole.EditRole)
        self.model.revert()
        self.assertEqual([], self.model.modified)

    def test_revert_with_no_changes_is_safe(self):
        self.model.revert()  # must not raise
        self.assertEqual('1', self.model.loop_data[0][0])

    # --- validate_text ---

    def test_validate_text_no_validator_always_true(self):
        self.assertTrue(self.model.validate_text('anything', 0))

    def test_validate_text_valid_float(self):
        m = LoopTableModel(['_cell_length_a'], [['5.5']])
        self.assertTrue(m.validate_text('5.5', 0))

    def test_validate_text_invalid_float(self):
        m = LoopTableModel(['_cell_length_a'], [['abc']])
        self.assertFalse(m.validate_text('abc', 0))

    def test_validate_text_question_mark_is_valid(self):
        m = LoopTableModel(['_cell_length_a'], [['?']])
        self.assertTrue(m.validate_text('?', 0))


# ---------------------------------------------------------------------------
# MyQTableView unit tests
# ---------------------------------------------------------------------------

class TestMyQTableView(unittest.TestCase):

    def setUp(self):
        self.view = _make_view_with_model()

    def test_is_last_row_middle(self):
        self.assertTrue(self.view.is_last_row(1))

    def test_is_last_row_last(self):
        self.assertFalse(self.view.is_last_row(2))

    def test_get_index_of_row(self):
        idx = self.view.get_index_of_row(1)
        self.assertEqual(1, idx.row())
        self.assertEqual(0, idx.column())

    def test_add_row_increases_row_count(self):
        self.view._add_row(None)
        self.assertEqual(4, self.view.model().rowCount())
        self.assertEqual(['', '', ''], self.view.model().loop_data[3])

    def test_delete_row_decreases_row_count(self):
        idx = self.view.model().index(1, 0)
        self.view.setCurrentIndex(idx)
        self.view._delete_row(None)
        self.assertEqual(2, self.view.model().rowCount())

    def test_row_down_via_view_updates_selection(self):
        idx = self.view.model().index(0, 0)
        self.view.setCurrentIndex(idx)
        self.view._row_down(None)
        self.assertEqual(1, self.view.currentIndex().row())

    def test_row_up_via_view_updates_selection(self):
        idx = self.view.model().index(2, 0)
        self.view.setCurrentIndex(idx)
        self.view._row_up(None)
        self.assertEqual(1, self.view.currentIndex().row())

    def test_row_down_at_last_row_does_not_move(self):
        idx = self.view.model().index(2, 0)
        self.view.setCurrentIndex(idx)
        self.view._row_down(None)
        # selection unchanged
        self.assertEqual(2, self.view.currentIndex().row())
        # data unchanged
        self.assertEqual(['7', '8', '9'], self.view.model().loop_data[2])

    def test_row_up_at_first_row_does_not_move(self):
        idx = self.view.model().index(0, 0)
        self.view.setCurrentIndex(idx)
        self.view._row_up(None)
        self.assertEqual(0, self.view.currentIndex().row())
        self.assertEqual(['1', '2', '3'], self.view.model().loop_data[0])


# ---------------------------------------------------------------------------
# LoopsPage integration tests
# ---------------------------------------------------------------------------

class TestLoops(unittest.TestCase):

    def setUp(self) -> None:
        self.testcif = SMALL_CIF.resolve()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        self.cif = CifContainer(self.testcif)
        self.loops_page = LoopsPage(cif=self.cif)

    def tearDown(self) -> None:
        self.cif.finalcif_file.unlink(missing_ok=True)
        self.loops_page.deleteLater()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)

    def get_index_of(self, loopkey: str = '') -> int:
        tabw: QTabWidget = self.loops_page.tab_widget
        tab = -1
        for tab in range(tabw.count()):
            if tabw.tabText(tab).startswith(loopkey):
                break
            else:
                tab = -1
        return tab

    def test_tab_count_after_load(self):
        self.assertEqual(9, self.loops_page.tab_widget.count())

    def test_delete_loop(self):
        self.assertEqual(9, len(self.cif.loops))
        self.loops_page.on_delete_current_loop()
        self.assertEqual(8, len(self.cif.loops))

    def test_delete_loop_also_removes_tab(self):
        self.loops_page.on_delete_current_loop()
        self.assertEqual(8, self.loops_page.tab_widget.count())

    def test_get_index_of_tab(self):
        self.assertEqual(1, self.get_index_of('CIF Author'))

    def test_tab_tooltip_is_cif_key(self):
        # Tab 0 should have a tooltip equal to the first tag of the first loop
        tooltip = self.loops_page.tab_widget.tabToolTip(0)
        self.assertTrue(tooltip.startswith('_'))

    def test_loop_data(self):
        index = self.loops_page.tab_widget.widget(self.get_index_of('Citations')).model().index(0, 1)
        self.assertEqual('10.1021/acs.orglett.0c01078', index.data())

    def test_loop_data_atoms_aniso(self):
        index = self.loops_page.tab_widget.widget(self.get_index_of('Displacement Para')).model().index(0, 1)
        self.assertEqual('0.0161(10)', index.data())

    def test_loop_audit_author_name(self):
        index = self.loops_page.tab_widget.widget(self.get_index_of('CIF Author')).model().index(0, 0)
        self.assertEqual('Daniel Kratzert', index.data())

    def test_loop_audit_author_address(self):
        index = self.loops_page.tab_widget.widget(self.get_index_of('CIF Author')).model().index(0, 1)
        self.assertEqual(unify_line_endings('University of Freiburg\nGermany'), unify_line_endings(index.data()))

    def test_loop_dots(self):
        index = self.loops_page.tab_widget.widget(self.get_index_of('Bonds')).model().index(1, 3)
        self.assertEqual('.', index.data())

    def test_loop_question_marks(self):
        index = self.loops_page.tab_widget.widget(self.get_index_of('Bonds')).model().index(1, 4)
        self.assertEqual('?', index.data())

    def test_loop_no_edit(self):
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        val = c.loops[3][0, 2]
        self.assertEqual('0.0181', val)

    def test_loop_edit_one_single_field(self):
        model = self.loops_page.tab_widget.widget(self.get_index_of('Scattering')).model()
        model.setData(model.index(0, 2), 'foo bar', role=Qt.ItemDataRole.EditRole)
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        result = as_string(c.loops[3][0, 2])
        self.assertEqual('foo bar', result)

    def test_set_author_editor_tab_inserts_at_index_zero(self):
        from qtpy.QtWidgets import QWidget
        author_widget = QWidget()
        self.loops_page.set_author_editor_tab(author_widget)
        self.assertEqual('Author Editor', self.loops_page.tab_widget.tabText(0))
        # loop tabs now shift to 1..n
        self.assertEqual(10, self.loops_page.tab_widget.count())

    def test_set_author_editor_tab_sets_has_author_tab_flag(self):
        from qtpy.QtWidgets import QWidget
        self.loops_page.set_author_editor_tab(QWidget())
        self.assertTrue(self.loops_page._has_author_tab)

    def test_load_replaces_loop_tabs(self):
        # Load the same CIF a second time; tab count must be the same (not doubled)
        self.loops_page.load(self.cif)
        self.assertEqual(9, self.loops_page.tab_widget.count())

    def test_revert_all_loops_restores_values(self):
        model = self.loops_page.tab_widget.widget(self.get_index_of('Scattering')).model()
        original = model.index(0, 0).data()
        model.setData(model.index(0, 0), 'X', Qt.ItemDataRole.EditRole)
        self.assertEqual('X', model.index(0, 0).data())
        self.loops_page.revert_all_loops()
        self.assertEqual(original, model.index(0, 0).data())

    def test_new_loop_requested_signal_emitted(self):
        signals = []
        self.loops_page.new_loop_requested.connect(lambda: signals.append(True))
        self.loops_page.go_to_new_loop_page()
        self.assertEqual([True], signals)

    def test_go_to_new_loop_page_adds_creator_tab(self):
        count_before = self.loops_page.tab_widget.count()
        self.loops_page.go_to_new_loop_page()
        self.assertEqual(count_before + 1, self.loops_page.tab_widget.count())
        self.assertEqual('Create Loops', self.loops_page.tab_widget.tabText(self.loops_page.tab_widget.count() - 1))


class TestLoopsResFile(unittest.TestCase):
    """Tests that require a CIF with an embedded SHELX res file."""

    def setUp(self) -> None:
        self.testcif = FULL_CIF.resolve()
        self.cif = CifContainer(self.testcif)
        self.loops_page = LoopsPage(cif=self.cif)

    def tearDown(self) -> None:
        self.cif.finalcif_file.unlink(missing_ok=True)
        self.loops_page.deleteLater()

    def test_shelx_res_file_tab_is_added(self):
        tab_texts = [self.loops_page.tab_widget.tabText(i)
                     for i in range(self.loops_page.tab_widget.count())]
        self.assertIn('SHELX res file', tab_texts)

    def test_shelx_tab_widget_is_plain_text_edit(self):
        tab_texts = [self.loops_page.tab_widget.tabText(i)
                     for i in range(self.loops_page.tab_widget.count())]
        idx = tab_texts.index('SHELX res file')
        widget = self.loops_page.tab_widget.widget(idx)
        self.assertIsInstance(widget, QPlainTextEdit)

    def test_shelx_tab_content_is_not_empty(self):
        tab_texts = [self.loops_page.tab_widget.tabText(i)
                     for i in range(self.loops_page.tab_widget.count())]
        idx = tab_texts.index('SHELX res file')
        text = self.loops_page.tab_widget.widget(idx).toPlainText()
        self.assertTrue(len(text) > 0)

    def test_shelx_tab_is_read_only(self):
        tab_texts = [self.loops_page.tab_widget.tabText(i)
                     for i in range(self.loops_page.tab_widget.count())]
        idx = tab_texts.index('SHELX res file')
        self.assertTrue(self.loops_page.tab_widget.widget(idx).isReadOnly())


# ---------------------------------------------------------------------------
# Row-move integration tests (LoopsPage + CIF round-trip)
# ---------------------------------------------------------------------------

class TestLoopsMove(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        self.testcif = SMALL_CIF.resolve()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)
        self.cif = CifContainer(self.testcif)
        self.loops_page = LoopsPage(cif=self.cif)

    def tearDown(self) -> None:
        self.cif.finalcif_file.unlink(missing_ok=True)
        self.loops_page.deleteLater()
        (data / 'examples/1979688-finalcif_changes.cif').unlink(missing_ok=True)

    def get_index_of(self, loopkey: str = '') -> int:
        tabw: QTabWidget = self.loops_page.tab_widget
        tab = -1
        for tab in range(tabw.count()):
            if tabw.tabText(tab).startswith(loopkey):
                break
            else:
                tab = -1
        return tab

    def set_current_index_to_row_col(self, row, col, tab='Scattering'):
        view = self.loops_page.tab_widget.widget(self.get_index_of(tab))
        index = view.model().index(row, col)
        view.setCurrentIndex(index)
        return view

    def test_order_of_scattering_factors_table(self):
        view = self.loops_page.tab_widget.widget(self.get_index_of('Scattering'))
        self.assertEqual('C', view.model().index(0, 0).data())
        self.assertEqual('H', view.model().index(1, 0).data())
        self.assertEqual('O', view.model().index(2, 0).data())

    def test_row_col_selection(self):
        view = self.set_current_index_to_row_col(1, 0)
        self.assertEqual(1, view.currentIndex().row())
        self.assertEqual(0, view.currentIndex().column())

    def test_move_row_down_from_middle(self):
        view = self.set_current_index_to_row_col(1, 0)
        view._row_down(None)
        self.assertEqual('C', view.model().index(0, 0).data())
        self.assertEqual('O', view.model().index(1, 0).data())
        self.assertEqual('H', view.model().index(2, 0).data())

    def test_move_row_down_from_middle_save_and_load_again(self):
        view = self.set_current_index_to_row_col(1, 0)
        view._row_down(None)
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        try:
            self.assertEqual('C', as_string(c.loops[3].val(0, 0)))
            self.assertEqual('O', as_string(c.loops[3].val(1, 0)))
            self.assertEqual('H', as_string(c.loops[3].val(2, 0)))
        except AttributeError:
            self.assertEqual('C', as_string(c.loops[3][0, 0]))
            self.assertEqual('O', as_string(c.loops[3][1, 0]))
            self.assertEqual('H', as_string(c.loops[3][2, 0]))

    def test_move_row_down_from_middle_save_and_load_again_for_angles(self):
        view = self.set_current_index_to_row_col(1, 0, tab='Angles')
        view._row_down(None)
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        self.assertEqual("['O1', 'C1', 'C14', '105.9(2)', '.', '.', '?']", str(c.loops[7].values[:7]))

    def test_move_row_down_from_end(self):
        view = self.set_current_index_to_row_col(2, 0)
        view._row_down(None)
        self.assertEqual('C', view.model().index(0, 0).data())
        self.assertEqual('H', view.model().index(1, 0).data())
        self.assertEqual('O', view.model().index(2, 0).data())

    def test_move_row_down_from_end_save_and_load_again(self):
        view = self.set_current_index_to_row_col(2, 0)
        view._row_down(None)
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        try:
            self.assertEqual('C', as_string(c.loops[3].val(0, 0)))
            self.assertEqual('H', as_string(c.loops[3].val(1, 0)))
            self.assertEqual('O', as_string(c.loops[3].val(2, 0)))
        except AttributeError:
            self.assertEqual('C', as_string(c.loops[3][0, 0]))
            self.assertEqual('H', as_string(c.loops[3][1, 0]))
            self.assertEqual('O', as_string(c.loops[3][2, 0]))

    def test_move_row_up_from_middle(self):
        view = self.set_current_index_to_row_col(1, 0)
        view._row_up(None)
        self.assertEqual('H', view.model().index(0, 0).data())
        self.assertEqual('C', view.model().index(1, 0).data())
        self.assertEqual('O', view.model().index(2, 0).data())

    def test_move_row_up_from_middle_save_and_load_again(self):
        view = self.set_current_index_to_row_col(1, 0)
        view._row_up(None)
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        try:
            self.assertEqual('H', as_string(c.loops[3].val(0, 0)))
            self.assertEqual('C', as_string(c.loops[3].val(1, 0)))
            self.assertEqual('O', as_string(c.loops[3].val(2, 0)))
        except AttributeError:
            self.assertEqual('H', as_string(c.loops[3][0, 0]))
            self.assertEqual('C', as_string(c.loops[3][1, 0]))
            self.assertEqual('O', as_string(c.loops[3][2, 0]))

    def test_move_row_up_from_start(self):
        view = self.set_current_index_to_row_col(0, 0)
        view._row_up(None)
        self.assertEqual('C', view.model().index(0, 0).data())
        self.assertEqual('H', view.model().index(1, 0).data())
        self.assertEqual('O', view.model().index(2, 0).data())

    def test_move_row_up_from_start_save_and_load_again(self):
        view = self.set_current_index_to_row_col(0, 0)
        view._row_up(None)
        self.cif.save()
        c = CifContainer(self.cif.finalcif_file)
        try:
            self.assertEqual('C', as_string(c.loops[3].val(0, 0)))
            self.assertEqual('H', as_string(c.loops[3].val(1, 0)))
            self.assertEqual('O', as_string(c.loops[3].val(2, 0)))
        except AttributeError:
            self.assertEqual('C', as_string(c.loops[3][0, 0]))
            self.assertEqual('H', as_string(c.loops[3][1, 0]))
            self.assertEqual('O', as_string(c.loops[3][2, 0]))
