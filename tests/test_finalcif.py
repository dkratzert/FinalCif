import doctest
import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

import finalcif
import report
from datafiles import bruker_data, bruker_frame, p4p_reader, platon, rigaku_data, sadabs, saint, shelxt, utils
from finalcif import AppWindow
from report import symm, tables, mtools, report_text
from tools import misc
from tools.version import VERSION
from gui.finalcif_gui import Ui_FinalCifWindow


@unittest.skip
class DoctestsTest(unittest.TestCase):
    def testrun_doctest(self):
        for name in [finalcif, symm, tables, mtools, report_text, report, bruker_data, bruker_frame,
                     p4p_reader, platon, rigaku_data, sadabs, saint, shelxt, utils, misc]:
            failed, attempted = doctest.testmod(name)  # , verbose=True)
            if failed == 0:
                print('passed all {} tests in {}!'.format(attempted, name.__name__))
            else:
                msg = '!!!!!!!!!!!!!!!! {} of {} tests failed in {}  !!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(failed,
                                                                                                         attempted,
                                                                                                         name.__name__)
                self.assertFalse(failed, msg)

app = QApplication(sys.argv)


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow()
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        # w.showMaximized()  # For full screen view
        self.myapp.setBaseSize(1200, 780)

    def tearDown(self) -> None:
        super(TestApplication, self).tearDown()

    # @unittest.skip("foo")
    def test_gui_simpl(self):
        self.assertEqual(0, self.myapp.ui.CifItemsTable.rowCount())
        self.myapp.load_cif_file(r'test-data/DK_zucker2_0m.cif')
        self.assertEqual(107, self.myapp.ui.CifItemsTable.rowCount())
        self.assertEqual('_audit_contact_author_email', self.myapp.ui.CifItemsTable.verticalHeaderItem(1).text())
        #TODO: test for value in _audit_contact_author_email
        #TODO: test for value in _audit_creation_method, bith in all columns
        #QTest.mouseClick(self.myapp.ui.CifItemsTable.verticalHeaderItem(1).setFlags(), Qt.LeftButton, delay=1)
