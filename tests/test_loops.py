#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import os
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget
from gemmi.cif import as_string

from finalcif.appwindow import AppWindow
from finalcif.cif.cif_file_io import CifContainer
from tests.helpers import unify_line_endings


class TestLoops(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).resolve().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').resolve()
        self.myapp = AppWindow(self.testcif, unit_test=True)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()  # For full screen view
        self.myapp.ui.LoopsPushButton.click()

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)
        self.myapp.close()

    def get_index_of(self, loopkey: str = ''):
        tabw: QTabWidget = self.myapp.ui.LoopsTabWidget
        tab = -1
        for tab in range(tabw.count()):
            if tabw.tabText(tab).startswith(loopkey):
                break
            else:
                tab = -1
        return tab

    def test_get_index_of_tab(self):
        self.assertEqual(2, self.get_index_of('CIF Author'))

    def test_loop_data(self):
        index = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('Citations')).model().index(0, 1)
        self.assertEqual('10.1021/acs.orglett.0c01078', index.data())

    def test_loop_data_atoms_aniso(self):
        index = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('Displacement Para')).model().index(0, 1)
        self.assertEqual('0.0161(10)', index.data())

    def test_loop_audit_author_name(self):
        index = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('CIF Author')).model().index(0, 0)
        self.assertEqual('Daniel Kratzert', index.data())

    def test_loop_audit_author_address(self):
        index = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('CIF Author')).model().index(0, 1)
        self.assertEqual(unify_line_endings('University of Freiburg\nGermany'), unify_line_endings(index.data()))

    def test_loop_dots(self):
        index = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('Bonds')).model().index(1, 3)
        self.assertEqual('.', index.data())

    def test_loop_question_marks(self):
        index = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('Bonds')).model().index(1, 4)
        self.assertEqual('?', index.data())

    def test_loop_no_edit(self):
        self.myapp.ui.SaveCifButton.click()
        c = CifContainer(self.myapp.final_cif_file_name)
        self.assertEqual('0.0181', c.loops[3].val(0, 2))

    def test_loop_edit_one_single_field(self):
        model = self.myapp.ui.LoopsTabWidget.widget(self.get_index_of('Scattering')).model()
        print(self.myapp.ui.LoopsTabWidget.tabText(4))
        model.setData(model.index(0, 2), 'foo bar', role=Qt.EditRole)
        self.myapp.ui.SaveCifButton.click()
        c = CifContainer(self.myapp.final_cif_file_name)
        self.assertEqual('foo bar', as_string(c.loops[3].val(0, 2)))
