import doctest
import os
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



app = QApplication(sys.argv)


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow('/Users/daniel/GitHub/FinalCif/tests/examples/1979688.cif')
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.showMaximized()  # For full screen view
        #self.myapp.setBaseSize(1200, 780)
        # I have to load any cif file in order to have vheaderitems in the main table:
        #self.myapp.load_cif_file(r'tests/examples/1979688.cif')


    def tearDown(self) -> None:
        super(TestApplication, self).tearDown()

    # @unittest.skip("foo")
    def test_gui_simpl(self):
        #self.assertEqual(0, self.myapp.ui.cif_main_table.rowCount())
        #self.myapp.load_cif_file(r'tests/examples/1979688.cif')
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
        # I have to click on it with QtClick
        QTest.mouseClick(self.myapp.ui.EquipmentTemplatesListWidget, Qt.LeftButton, Qt.NoModifier)
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 0).text())
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 1).text())
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 2).text())
        # Test if it really selects the row:
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentRow(1)
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 1).text())

    #@unittest.skip('does not really work')
    def test_export_template(self):
        widget = self.myapp.ui.EquipmentTemplatesListWidget
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = widget.findItems('D8 VENTURE', Qt.MatchStartsWith)[0]
        #widget.setCurrentItem(item)
        #item = widget.item(3)
        widget.setCurrentItem(item)
        #rect = widget.visualItemRect(item)
        #QTest.mouseDClick(widget.viewport(), Qt.LeftButton, Qt.NoModifier, rect.center())
        # Why is this not called by the signal?
        self.myapp.edit_equipment_template()
        self.myapp.export_equipment_template('unittest_export_template2.cif')
        outfile = Path('unittest_export_template2.cif')
        data = ['data_D8__VENTURE',
         "_diffrn_radiation_monochromator   'mirror optics'",
         "_diffrn_measurement_device        'three-circle diffractometer'",
         "_diffrn_measurement_device_type   'Bruker D8 VENTURE dual wavelength Mo/Cu'",
         "_diffrn_measurement_method        '\\w and \\f scans'",
         "_diffrn_source                    'microfocus sealed X-ray tube'",
         '_diffrn_detector_area_resol_mean  7.41',
         '_diffrn_detector                  CPAD',
         "_diffrn_detector_type             'Bruker PHOTON III'",
         "_diffrn_source_type               'Incoatec I\\ms'",
         '_diffrn_radiation_probe           x-ray',
         "_diffrn_measurement_specimen_support 'MiTeGen micromount'",
         "_olex2_diffrn_ambient_temperature_device 'Oxford Cryostream 800'",
         '_diffrn_ambient_environment       N~2~']
        self.assertEqual(data, outfile.read_text().splitlines(keepends=False))
        outfile.unlink()


    #@unittest.skip('test_load_equipment Is tested in gui_simpl')
    def test_load_equipment(self):
        #self.myapp.load_cif_file(r'test-data/DK_zucker2_0m.cif')
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()

@unittest.skip
class DoctestsTest(unittest.TestCase):
    def testrun_doctest(self):
        for name in [str(i.absolute()) for i in Path('.').rglob('*.py')]: #[finalcif, symm, tables, mtools, report_text, report, bruker_data, bruker_frame,
                     #p4p_reader, platon, rigaku_data, sadabs, saint, shelx, utils, misc]:
            failed, attempted = doctest.testfile(name)  # , verbose=True)
            if failed == 0:
                print('passed all {} tests in {}!'.format(attempted, name.__name__))
            else:
                msg = '!!!!!!!!!!!!!!!! {} of {} tests failed in {}  !!!!!!!!!!!!!!!!!!!!!!!!!!!'.format(failed,
                                                                                                         attempted,
                                                                                                         name.__name__)
                self.assertFalse(failed, msg)