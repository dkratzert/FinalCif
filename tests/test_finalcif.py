import doctest
import sys
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qtpy.QtTest import QTest

import finalcif
import report
from datafiles import bruker_data, bruker_frame, p4p_reader, platon, rigaku_data, sadabs, saint, shelx, utils
from finalcif import AppWindow
from report import mtools, report_text, symm, tables
from tools import misc
from tools.version import VERSION


@unittest.skip
class DoctestsTest(unittest.TestCase):
    def testrun_doctest(self):
        for name in [finalcif, symm, tables, mtools, report_text, report, bruker_data, bruker_frame,
                     p4p_reader, platon, rigaku_data, sadabs, saint, shelx, utils, misc]:
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
        self.assertEqual(0, self.myapp.ui.cif_main_table.rowCount())
        self.myapp.load_cif_file(r'tests/examples/1979688.cif')
        # Size of table:
        self.assertEqual(131, self.myapp.ui.cif_main_table.rowCount())
        # The 17th row in the first column:
        self.assertEqual('geom', self.myapp.ui.cif_main_table.item(16, 0).text())
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        # QTest.mouseClick(self.myapp.ui.EquipmentTemplatesListWidget.item(2), Qt.LeftButton, delay=-1)
        self.myapp.ui.EquipmentTemplatesListWidget.item(2).setSelected(True)
        # make sure contact author is selected
        self.assertEqual('CCDC number', self.myapp.ui.EquipmentTemplatesListWidget.item(1).text())
        # have to find a better way to select the author row:
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        # A random empty item in the main table:
        self.assertEqual('?', self.myapp.ui.cif_main_table.item(3, 0).text())
        # This can only work if I have inserted the email adress manually:
        # I have to click on it with QtClick
        QTest.mouseClick(self.myapp.ui.EquipmentTemplatesListWidget, Qt.LeftButton, Qt.NoModifier)
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 0).text())
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 1).text())
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 2).text())
        # Test if it really selects the row:
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentRow(1)
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 1).text())

    @unittest.skip('does not really work')
    def test_export_template(self):
        widget = self.myapp.ui.EquipmentTemplatesListWidget
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        #item = widget.findItems('D8 VENTURE', Qt.MatchExactly)[0]
        #widget.setCurrentItem(item)
        item = widget.item(3)
        widget.setCurrentItem(item)
        rect = widget.visualItemRect(item)
        QTest.mouseClick(widget, Qt.LeftButton, Qt.NoModifier, rect.center())
        self.myapp.export_equipment_template('tests/unittest_export_template2.cif')
        self.assertEqual(['_diffrn_radiation_monochromator', 'mirror optics'],
                         Path('./tests/unittest_export_template2.cif').read_text().splitlines(keepends=False))

    @unittest.skip('test_load_equipment Is tested in gui_simpl')
    def test_load_equipment(self):
        self.myapp.load_cif_file(r'test-data/DK_zucker2_0m.cif')
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()
