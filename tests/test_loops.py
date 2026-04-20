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

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QTabWidget

from gemmi.cif import as_string

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.loops import LoopsPage
from finalcif.tools.misc import unify_line_endings

app = QApplication.instance()
if app is None:
    app = QApplication([])

data = Path('tests')


class TestLoops(unittest.TestCase):

    def setUp(self) -> None:
        self.testcif = (data / 'examples/1979688_small.cif').resolve()
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

    def test_delete_loop(self):
        self.assertEqual(9, len(self.cif.loops))
        self.loops_page.on_delete_current_loop()
        self.assertEqual(8, len(self.cif.loops))

    def test_get_index_of_tab(self):
        self.assertEqual(1, self.get_index_of('CIF Author'))

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


# noinspection PyMissingTypeHints
class TestLoopsMove(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        self.testcif = (data / 'examples/1979688_small.cif').resolve()
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
