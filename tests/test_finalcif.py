import doctest
import sys
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import finalcif
import report
from datafiles import bruker_data, bruker_frame, p4p_reader, platon, rigaku_data, sadabs, saint, shelxt, utils
from finalcif import AppWindow
from report import mtools, report_text, symm, tables
from tools import misc
from tools.version import VERSION


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
        self.assertEqual(111, self.myapp.ui.CifItemsTable.rowCount())
        self.assertEqual('_audit_contact_author_email', self.myapp.ui.CifItemsTable.verticalHeaderItem(1).text())
        self.assertEqual('', self.myapp.ui.CifItemsTable.item(1, 1).text())
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        # QTest.mouseClick(self.myapp.ui.EquipmentTemplatesListWidget.item(2), Qt.LeftButton, delay=-1)
        self.myapp.ui.EquipmentTemplatesListWidget.item(2).setSelected(True)
        # make sure contact author is selected
        self.assertEqual('Contact author name and address', self.myapp.ui.EquipmentTemplatesListWidget.item(2).text())
        # have to find a better way to select the author row:
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.assertEqual('?', self.myapp.ui.CifItemsTable.item(1, 0).text())
        # Tihs can only word if I have inserted the emeail adress manually:
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.CifItemsTable.item(1, 1).text())
        self.assertTrue(self.myapp.ui.CifItemsTable.item(1, 2))
        # Test if it really selects the row:
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentRow(0)
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.CifItemsTable.item(1, 1).text())

    def test_export_template(self):
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        #self.myapp.load_selected_equipment()
        self.myapp.edit_equipment_template()
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(1)
        self.myapp.export_equipment_template('./tests/unittest_export_template2.cif')
        self.assertEqual(Path('./tests/unittest_export_template.cif').read_text(),
                         Path('./tests/unittest_export_template2.cif').read_text())
        self.assertNotEqual('', Path('./tests/unittest_export_template.cif').read_text())
        self.assertNotEqual('', Path('./tests/unittest_export_template2.cif').read_text())
        Path('./tests/unittest_export_template2.cif').unlink()

    @unittest.skip('test_load_equipment Is tested in gui_simpl')
    def test_load_equipment(self):
        self.myapp.load_cif_file(r'test-data/DK_zucker2_0m.cif')
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()
