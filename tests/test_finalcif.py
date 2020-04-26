import sys
import time
import unittest
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication
from qtpy.QtTest import QTest

from finalcif import AppWindow
from gui.custom_classes import yellow, light_green
from tools.version import VERSION

export_templ_data = ['data_D8__VENTURE',
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

addr = """Albert-Ludwigs-Universität Freiburg
Institut für Anorganische und Analytische Chemie
Albertstraße 21
Freiburg i. Br.
79104
Germany"""

export_prop_data = r"""data_Molecular__Graphics
loop_
_computing_molecular_graphics
'Olex2 (Dolomanov et al., 2009)'
'ShelXle (Hu\"bschle 2011)'
'ORTEP Farrujia 2012'
'Bruker SHELXTL, XP (G. Sheldrick)'
'Mercury CSD, C. F. Macrae et al. 2008'
'PLATON (A.L.Spek, 2019)'
"""

app = QApplication(sys.argv)


class TestApplication(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow([x for x in Path('.').rglob('1979688.cif')][0].absolute())
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.hide()  # For full screen view
        # self.myapp.setBaseSize(1200, 780)
        # I have to load any cif file in order to have vheaderitems in the main table:
        # self.myapp.load_cif_file(r'tests/examples/1979688.cif')

    def tearDown(self) -> None:
        super(TestApplication, self).tearDown()

    # @unittest.skip("foo")
    def test_gui_simpl(self):
        # self.assertEqual(0, self.myapp.ui.cif_main_table.rowCount())
        # self.myapp.load_cif_file(r'tests/examples/1979688.cif')
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

    # @unittest.skip('')
    def test_export_template(self):
        widget = self.myapp.ui.EquipmentTemplatesListWidget
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = widget.findItems('D8 VENTURE', Qt.MatchStartsWith)[0]
        # widget.setCurrentItem(item)
        # item = widget.item(3)
        widget.setCurrentItem(item)
        # rect = widget.visualItemRect(item)
        # QTest.mouseDClick(widget.viewport(), Qt.LeftButton, Qt.NoModifier, rect.center())
        # Why is this not called by the signal?
        self.myapp.edit_equipment_template()
        self.myapp.export_equipment_template('unittest_export_template2.cif')
        outfile = Path('unittest_export_template2.cif')
        self.assertEqual(export_templ_data, outfile.read_text().splitlines(keepends=False))
        outfile.unlink()

    # @unittest.skip('')
    def test_load_equipment(self):
        # self.myapp.load_cif_file(r'test-data/DK_zucker2_0m.cif')
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author name and address',
                                                                    Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()
        self.assertEqual('daniel.kratzert@ac.uni-freiburg.de', self.myapp.ui.cif_main_table.item(19, 1).text())

    def test_properties(self):
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = self.myapp.ui.PropertiesTemplatesListWidget.findItems('Crystal Color', Qt.MatchStartsWith)
        self.myapp.ui.PropertiesTemplatesListWidget.setCurrentItem(item[0])
        self.myapp.edit_property_template()
        self.assertEqual('_exptl_crystal_colour', self.myapp.ui.cifKeywordLineEdit.text())
        self.assertEqual('', self.myapp.ui.PropertiesEditTableWidget.item(0, 0).text())
        self.assertEqual('colourless', self.myapp.ui.PropertiesEditTableWidget.item(1, 0).text())
        self.assertEqual('white', self.myapp.ui.PropertiesEditTableWidget.item(2, 0).text())
        # Testing export:
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = self.myapp.ui.PropertiesTemplatesListWidget.findItems('Molecular Graph', Qt.MatchStartsWith)
        self.myapp.ui.PropertiesTemplatesListWidget.setCurrentItem(item[0])
        self.myapp.edit_property_template()
        self.assertEqual('ShelXle (Hübschle 2011)', self.myapp.ui.PropertiesEditTableWidget.item(2, 0).text())
        self.myapp.export_property_template('test_prop_export.cif')
        self.assertEqual(export_prop_data, Path('test_prop_export.cif').read_text())
        Path('test_prop_export.cif').unlink()
        # Testing import:
        data = """data_Fooo__Baar\nloop_\n_foo\n'bar baz'"""
        file = Path('test_prop_import.cif')
        file.write_text(data)
        self.myapp.import_property_from_file(file.name)
        item = self.myapp.ui.PropertiesTemplatesListWidget.findItems('Fooo Baar', Qt.MatchStartsWith)
        self.myapp.ui.PropertiesTemplatesListWidget.setCurrentItem(item[0])
        self.myapp.edit_property_template()
        self.assertEqual('_foo', self.myapp.ui.cifKeywordLineEdit.text())
        self.assertEqual('bar baz', self.myapp.ui.PropertiesEditTableWidget.item(1, 0).text())
        self.myapp.ui.DeletePropertiesButton.click()
        file.unlink()

    def test_dropdown_widgets(self):
        """
        Testing if comboboxes are there and fields have the correct type
        """
        self.assertEqual('direct', self.myapp.ui.cif_main_table.item(17, 0).text())
        self.assertEqual('', self.myapp.ui.cif_main_table.item(17, 1).text())
        self.assertEqual("<class 'gui.custom_classes.MyTableWidgetItem'>",
                         str(self.myapp.ui.cif_main_table.item(17, 1).__class__))
        self.assertEqual("<class 'NoneType'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(17, 1).__class__))
        # The type of the _atom_sites_solution_primary combobox:
        self.assertEqual("<class 'gui.custom_classes.MyComboBox'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(17, 2).__class__))
        # The first item of the _atom_sites_solution_primary combobox:
        self.assertEqual('direct', self.myapp.ui.cif_main_table.cellWidget(17, 2).itemText(1))
        self.assertEqual("<class 'gui.custom_classes.MyQPlainTextEdit'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(18, 0).__class__))
        self.assertEqual(addr, self.myapp.ui.cif_main_table.cellWidget(18, 0).toPlainText())
        ###
        # Now the above with MyCifTable methods:
        self.assertEqual('direct', self.myapp.ui.cif_main_table.text(17, 0))
        self.assertEqual('', self.myapp.ui.cif_main_table.text(17, 1))
        self.assertEqual('', self.myapp.ui.cif_main_table.text(17, 2))
        # Click on vertical header in order to see the help text:
        self.myapp.ui.cif_main_table.vheader_section_click(17)
        text = self.myapp.ui.cif_main_table.verticalHeaderItem(17).text()
        self.assertEqual('Codes which identify the methods used to locate the initial atom sites', text)
        # Click again to see the original text:
        self.myapp.ui.cif_main_table.vheader_section_click(17)
        text2 = self.myapp.ui.cif_main_table.verticalHeaderItem(17).text()
        self.assertEqual('_atom_sites_solution_primary', text2)
        # Test if table has unicode characters instead of ascii:
        self.assertEqual('ω and ϕ scans', self.myapp.ui.cif_main_table.getTextFromKey('_diffrn_measurement_method', 0))

    def test_set_text(self):
        # A combobox
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_primary', txt='foobar', column=2)
        self.assertEqual('foobar', self.myapp.ui.cif_main_table.text(17, 2))
        # A MyPlaintextedit
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_address', txt='foobar', column=2)
        self.assertEqual('foobar', self.myapp.ui.cif_main_table.text(18, 2))
        # A empty table cell
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_email', txt='foobar', column=2)
        self.assertEqual('foobar', self.myapp.ui.cif_main_table.text(19, 2))
        # A cell with item
        self.myapp.ui.cif_main_table.setText(key='_audit_creation_method', txt='foobar', column=1)
        self.assertEqual('foobar', self.myapp.ui.cif_main_table.text(22, 1))

    def test_info_fields(self):
        self.assertEqual('CCDC 1979688', self.myapp.ui.CCDCNumLineEdit.text())
        self.assertEqual('cu_BruecknerJK_153F40_0m', self.myapp.ui.datnameLineEdit.text())
        self.assertEqual('P 21 21 2', self.myapp.ui.spacegroupLineEdit.text())

    def test_cif_container(self):
        self.assertEqual('direct', self.myapp.cif['_atom_sites_solution_primary'])
        self.assertEqual('0.9288', self.myapp.cif.absorpt_correction_T_max)
        self.assertEqual('0.7697', self.myapp.cif.absorpt_correction_T_min)
        self.assertEqual(('O1', 'C1', 'C14', '105.9(2)', '.', '.'), [i for i in self.myapp.cif.angles()][0])
        self.assertEqual(('C1', 'C', '0.00232(11)', '0.37061(7)', '0.3615(5)', '.', '1', '0.0240(5)'),
                         [i for i in self.myapp.cif.atoms()][0])
        self.assertEqual(
            ['C1', 'C', 0.0023200000000000004, 0.37061000000000005, 0.36150000000000004, 0, 1.0, 0.024000000000000004],
            [i for i in self.myapp.cif.atoms_fract][0])
        self.assertEqual(
            ['C1', 'C', 0.04565296000000001, 13.721056969000005, 1.7250780000000003, 0, 1.0, 0.024000000000000004],
            [i for i in self.myapp.cif.atoms_orth][0])
        self.assertEqual((19.678, 37.02290000000001, 4.772, 90.0, 90.0, 90.0, 3476.576780226401), self.myapp.cif.cell)
        self.assertEqual(True, self.myapp.cif.chars_ok)
        self.assertEqual('P 2 2ab', self.myapp.cif.hall_symbol)
        self.assertEqual(20714, self.myapp.cif.hkl_checksum_calcd)
        self.assertEqual(17612, self.myapp.cif.res_checksum_calcd)
        self.assertEqual(179, self.myapp.cif.nangles())
        self.assertEqual(4.0, self.myapp.cif.Z_value)
        self.assertEqual(['x, y, z', '-x, -y, z', '-x+1/2, y+1/2, -z', 'x+1/2, -y+1/2, -z'], self.myapp.cif.symmops)
        self.assertEqual('SHELXL-2018/3 (Sheldrick, 2018)', self.myapp.cif['_computing_structure_refinement'])
        del self.myapp.cif['_computing_structure_refinement']
        self.assertEqual('', self.myapp.cif['_computing_structure_refinement'])
        self.assertEqual('<gemmi.UnitCell(19.678, 37.0229, 4.772, 90, 90, 90)>', str(self.myapp.cif.atomic_struct.cell))
        self.assertFalse(self.myapp.cif.ishydrogen('C1'))
        self.assertTrue(self.myapp.cif.ishydrogen('H1'))
        self.myapp.cif.add_to_cif('_computing_structure_refinement', 'foobar')
        self.assertEqual('foobar', self.myapp.cif['_computing_structure_refinement'])


class TestWorkfolder(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        self.myapp = AppWindow([x for x in Path('.').rglob('cu_BruecknerJK_153F40_0m.cif')][0].absolute())
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.hide()  # For full screen view
        # self.myapp.setBaseSize(1200, 780)
        # I have to load any cif file in order to have vheaderitems in the main table:
        # self.myapp.load_cif_file(r'tests/examples/1979688.cif')

    def tearDown(self) -> None:
        super().tearDown()

    def testDataColumn(self):
        '_computing_structure_solution:'
        self.assertEqual('SHELXT (G. Sheldrick)', self.myapp.ui.cif_main_table.text(19, 1))
        self.assertEqual('direct',
                         self.myapp.ui.cif_main_table.getTextFromKey('_atom_sites_solution_primary', 1))
        self.assertEqual('9624',
                         self.myapp.ui.cif_main_table.getTextFromKey('_cell_measurement_reflns_used', 1))
        self.assertEqual('78.8605',
                         self.myapp.ui.cif_main_table.getTextFromKey('_cell_measurement_theta_max', 1))
        self.assertEqual('2.547',
                         self.myapp.ui.cif_main_table.getTextFromKey('_cell_measurement_theta_min', 1))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_absolute_configuration', 1))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_absolute_configuration', 2))
        self.assertEqual("<class 'gui.custom_classes.MyComboBox'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(9, 2).__class__))
        self.assertEqual('?',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_formula_moiety', 0))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_formula_moiety', 1))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_formula_moiety', 2))
        # Test for background color:
        self.assertEqual(light_green, self.myapp.ui.cif_main_table.item(8, 1).background().color())
        self.assertEqual(yellow, self.myapp.ui.cif_main_table.item(9, 1).background().color())
        with self.assertRaises(AttributeError):
            self.myapp.ui.cif_main_table.item(8, 2).background().color()
        # Test for auto-fill data:
        self.assertEqual('SAINT V8.40A',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_cell_refinement', 1))
        self.assertEqual('?',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_cell_refinement', 0))
        self.assertEqual('Bruker BIS V6.2.12/2019-08-12',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_data_collection', 1))
        self.assertEqual(light_green, self.myapp.ui.cif_main_table.item(14, 1).background().color())
        self.assertEqual(light_green, self.myapp.ui.cif_main_table.item(15, 1).background().color())
        self.assertEqual(light_green, self.myapp.ui.cif_main_table.item(16, 1).background().color())
        self.assertEqual(QColor(0, 0, 0, 255), self.myapp.ui.cif_main_table.item(17, 1).background().color())
        self.assertEqual('SHELXT (G. Sheldrick)',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_structure_solution', 1))
        self.assertEqual('1.1',
                         self.myapp.ui.cif_main_table.getTextFromKey('_diffrn_source_current', 1))
        self.assertEqual('50.0',
                         self.myapp.ui.cif_main_table.getTextFromKey('_diffrn_source_voltage', 1))
        self.assertEqual('colourless',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_colour', 1))
        self.assertEqual('plate',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_description', 1))
        # _exptl_crystal_recrystallization_method Yellow:
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_recrystallization_method', 1))
        self.assertEqual('QPlainTextEdit {background-color: #faf796;}',
                         self.myapp.ui.cif_main_table.cellWidget(40, 1).styleSheet())
        self.assertEqual('0.220',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_size_max', 1))
        self.assertEqual('0.100',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_size_mid', 1))
        self.assertEqual('0.040',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_size_min', 1))
        self.assertEqual(
            """Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.\n""",
            self.myapp.ui.cif_main_table.getTextFromKey('_publ_section_references', 1))
        self.assertEqual('geom', self.myapp.ui.cif_main_table.getTextFromKey('_atom_sites_solution_hydrogens', 0))
        self.assertEqual('', self.myapp.ui.cif_main_table.getTextFromKey('_atom_sites_solution_hydrogens', 1))
        self.assertEqual(
            """FinalCif V{} by Daniel Kratzert, Freiburg 2019, https://github.com/dkratzert/FinalCif""".format(VERSION),
            self.myapp.ui.cif_main_table.getTextFromKey('_audit_creation_method', 1))
        self.assertEqual('18', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_IT_number', 0))
        self.assertEqual('orthorhombic', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_crystal_system', 0))
        self.assertEqual('P 21 21 2', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_name_H-M_alt', 0))
        self.assertEqual('P 2 2ab', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_name_Hall', 0))

    def allrows_test_key(self, key: str = '', results: list = None):
        for n, r in enumerate(results):
            self.assertEqual(r, self.myapp.ui.cif_main_table.getTextFromKey(key, n))

    def test_equipment_click(self):
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('APEX2 QUAZAR', Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()
        self.allrows_test_key('_diffrn_measurement_method', ['?', 'ω and ϕ scans', 'ω and ϕ scans'])
        self.allrows_test_key('_diffrn_measurement_specimen_support', ['?', 'MiTeGen micromount', 'MiTeGen micromount'])
        self.allrows_test_key('_olex2_diffrn_ambient_temperature_device',
                              ['?', 'Oxford Cryostream 800', 'Oxford Cryostream 800'])

    def test_edit_values_and_save(self):
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_primary', column=2, txt='test1')
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_secondary', column=2, txt='test2')
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_address', column=2, txt='test3')
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_email', column=2, txt='test4')
        cif = Path('testcif_file.cif')
        self.myapp.save_current_cif_file(cif.name)
        self.myapp.ui.cif_main_table.setRowCount(0)
        self.myapp.load_cif_file(cif.name)
        # test if data is still the same:
        self.assertEqual('test1',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_atom_sites_solution_primary', col=0))
        self.assertEqual('test2',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_atom_sites_solution_secondary', col=0))
        self.assertEqual('test3',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_audit_contact_author_address', col=0))
        self.assertEqual('test4',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_audit_contact_author_email', col=0))
        cif.unlink()

    def test_checkcif_html(self):
        self.maxDiff = None
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('D8 VENTURE', Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact author', Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.load_selected_equipment()
        self.myapp.ui.structfactCheckBox.setChecked(True)
        QTest.mouseClick(self.myapp.ui.CheckcifHTMLOnlineButton, Qt.LeftButton, Qt.NoModifier)
        time.sleep(5)
        html = Path('checkcif-' + self.myapp.cif.fileobj.stem[:-len('-finalcif')] + '-test.html')
        htmlfile = html.read_text().splitlines()
        # Filter out changing links:
        htmlfile = [x for x in htmlfile if not x.startswith(' <a href="http://checkcif.iucr.org')]
        resobj = Path('checkcif-' + self.myapp.cif.fileobj.stem[:-len('-finalcif')] + '-finalcif.html')
        result = resobj.read_text().splitlines()
        result = [x for x in result if not x.startswith(' <a href="http://checkcif.iucr.org')]
        self.assertEqual(htmlfile, result)
        resobj.unlink()
        self.myapp.cif.fileobj.unlink()
