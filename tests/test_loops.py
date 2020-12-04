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
from PyQt5.QtWidgets import QApplication
from gemmi.cif import as_string

from appwindow import AppWindow
from cif.cif_file_io import CifContainer
from tests.helpers import unify_line_endings

app = QApplication(sys.argv)


class TestLoops(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/1979688.cif').absolute()
        self.myapp = AppWindow(self.testcif)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()  # For full screen view
        self.myapp.ui.LoopsPushButton.click()

    def tearDown(self) -> None:
        self.myapp.final_cif_file_name.unlink(missing_ok=True)

    def test_loop_data(self):
        index = self.myapp._loop_tables[0].model.index(0, 1)
        self.assertEqual('10.1021/acs.orglett.0c01078', index.data())

    def test_loop_data_atoms_aniso(self):
        index = self.myapp._loop_tables[5].model.index(0, 1)
        self.assertEqual('0.0161(10)', index.data())

    def test_loop_audit_author_name(self):
        index = self.myapp._loop_tables[1].model.index(0, 0)
        self.assertEqual('Daniel Kratzert', index.data())

    def test_loop_audit_author_address(self):
        index = self.myapp._loop_tables[1].model.index(0, 1)
        self.assertEqual(unify_line_endings('University of Freiburg\nGermany'), unify_line_endings(index.data()))

    def test_loop_dots(self):
        index = self.myapp._loop_tables[6].model.index(1, 3)
        self.assertEqual('.', index.data())

    def test_loop_question_marks(self):
        index = self.myapp._loop_tables[6].model.index(1, 4)
        self.assertEqual('?', index.data())

    def test_loop_no_edit(self):
        self.myapp.ui.SaveCifButton.click()
        c = CifContainer(self.myapp.final_cif_file_name)
        self.assertEqual('0.0181', c.loops[3].val(0, 2))

    def test_loop_edit(self):
        index = self.myapp._loop_tables[3].model.index(0, 2)
        self.myapp._loop_tables[3].model.setData(index, 'foo bar', role=Qt.EditRole)
        self.myapp.ui.SaveCifButton.click()
        c = CifContainer(self.myapp.final_cif_file_name)
        self.assertEqual('foo bar', as_string(c.loops[3].val(0, 2)))
