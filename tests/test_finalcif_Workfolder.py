import os
import unittest
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget
from qtpy.QtTest import QTest

from finalcif.appwindow import AppWindow
from finalcif.gui.custom_classes import light_green, yellow, COL_DATA, COL_CIF, COL_EDIT
from tests.helpers import unify_line_endings, addr
from finalcif import VERSION


class TestNothingOpened(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.myapp = AppWindow(unit_test=True)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        Path('foo.cif').unlink(missing_ok=True)
        Path('cu_BruecknerJK_153F40_0m-finalcif.cif').unlink(missing_ok=True)

    def tearDown(self) -> None:
        self.myapp.close()

    def test_save_noting(self):
        self.myapp.save_current_cif_file()
        self.assertEqual(False, Path('cu_BruecknerJK_153F40_0m-finalcif.cif').exists())

    def test_save_file(self):
        self.myapp.save_current_cif_file('foo.cif')
        self.assertEqual(False, Path('foo.cif').exists())


class TestFileIsOpened(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        self.myapp = AppWindow(self.testcif, unit_test=True)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        Path('foo.cif').unlink(missing_ok=True)
        Path('cu_BruecknerJK_153F40_0m-finalcif.cif').unlink(missing_ok=True)

    def tearDown(self) -> None:
        Path('foo.cif').unlink(missing_ok=True)
        Path('cu_BruecknerJK_153F40_0m-finalcif.cif').unlink(missing_ok=True)
        self.myapp.close()

    def test_save_action(self):
        self.myapp.save_current_cif_file()
        self.assertEqual(True, Path('cu_BruecknerJK_153F40_0m-finalcif.cif').exists())

    def test_save_file(self):
        self.myapp.save_current_cif_file('foo.cif')
        self.assertEqual(True, Path('foo.cif').exists())


class TestWorkfolder(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        self.myapp = AppWindow(self.testcif, unit_test=True)
        self.myapp.running_inside_unit_test = True
        self.myapp.hide()
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))

    def tearDown(self) -> None:
        Path(self.testcif.stem + '.ins').unlink(missing_ok=True)
        Path(self.testcif.stem + '.lst').unlink(missing_ok=True)
        Path(self.testcif.stem + '.2fcf').unlink(missing_ok=True)
        Path('testcif_file.cif').unlink(missing_ok=True)
        self.myapp.close()

    def key_row(self, key: str) -> int:
        return self.myapp.ui.cif_main_table.row_from_key(key)

    def cell_widget(self, row: int, col: int) -> QWidget:
        return self.myapp.ui.cif_main_table.cellWidget(row, col)

    def cell_widget_class(self, row: int, col: int) -> str:
        return str(self.myapp.ui.cif_main_table.cellWidget(row, col).__class__)

    def get_combobox_items(self, row: int, col: int):
        widget = self.cell_widget(row, col)
        return [widget.itemText(i) for i in range(widget.count())]

    def cell_text(self, key: str, col: int) -> str:
        return unify_line_endings(self.myapp.ui.cif_main_table.getTextFromKey(key, col))

    def equipment_click(self, field: str):
        listw = self.myapp.ui.EquipmentTemplatesListWidget
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = listw.findItems(field, Qt.MatchStartsWith)[0]
        listw.setCurrentItem(item)
        self.assertEqual(field, item.text())
        rect = listw.visualItemRect(item)
        QTest.mouseDClick(listw.viewport(), Qt.LeftButton, Qt.NoModifier, rect.center())
        # This is necessary:
        self.myapp.equipment.load_selected_equipment()

    def get_background_color(self, key: str, col: int) -> QColor:
        return self.myapp.ui.cif_main_table.itemFromKey(key, col).background().color()

    def testDataColumn(self):
        self.myapp.hide()
        # test of ccdc number added from email during load:
        self.assertEqual('1979688', self.cell_text('_database_code_depnum_ccdc_archive', COL_DATA))
        # '_computing_structure_solution:'
        self.assertEqual('SHELXT (G. Sheldrick)', self.cell_text('_computing_structure_solution', COL_DATA))
        self.assertEqual('direct', self.cell_text('_atom_sites_solution_primary', COL_DATA))
        self.assertEqual('9624', self.cell_text('_cell_measurement_reflns_used', COL_DATA))
        self.assertEqual('78.8605', self.cell_text('_cell_measurement_theta_max', COL_DATA))
        self.assertEqual('2.547', self.cell_text('_cell_measurement_theta_min', COL_DATA))
        # Test for auto-fill data:
        self.assertEqual('SAINT V8.40A', self.cell_text('_computing_cell_refinement', COL_DATA))
        self.assertEqual('?', self.cell_text('_computing_cell_refinement', COL_CIF))
        self.assertEqual('Bruker BIS V6.2.12/2019-08-12', self.cell_text('_computing_data_collection', COL_DATA))
        self.assertEqual('SHELXT (G. Sheldrick)', self.cell_text('_computing_structure_solution', COL_DATA))
        self.assertEqual('1.1', self.cell_text('_diffrn_source_current', COL_DATA))
        self.assertEqual('50.0', self.cell_text('_diffrn_source_voltage', COL_DATA))
        self.assertEqual('colourless', self.cell_text('_exptl_crystal_colour', COL_DATA))
        self.assertEqual('plate', self.cell_text('_exptl_crystal_description', COL_DATA))
        # _exptl_crystal_recrystallization_method Yellow:
        self.assertEqual('', self.cell_text('_exptl_crystal_recrystallization_method', COL_DATA))
        # self.assertEqual('QPlainTextEdit {background-color: #faf796;}',
        #                 self.myapp.ui.cif_main_table.cellWidget(41, 1).styleSheet())
        self.assertEqual(
            """Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.""",
            self.cell_text('_publ_section_references', COL_DATA))
        self.assertEqual('geom', self.cell_text('_atom_sites_solution_hydrogens', 0))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', COL_DATA))
        self.assertEqual(
            """FinalCif V{} by Daniel Kratzert, Freiburg {}, https://dkratzert.de/finalcif.html""".format(VERSION,
                                                                                                          datetime.now().year),
            self.cell_text('_audit_creation_method', COL_DATA))

    def test_abs_configuration_combo(self):
        self.assertEqual(10, self.key_row('_chemical_absolute_configuration'))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(10, COL_CIF))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(10, COL_DATA))
        self.assertEqual("<class 'finalcif.gui.custom_classes.MyComboBox'>", self.cell_widget_class(10, COL_EDIT))

    def test_diffrn_radiation_type_combo(self):
        row = self.key_row('_diffrn_radiation_type')
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(row, COL_CIF))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(row, COL_DATA))
        self.assertEqual("<class 'finalcif.gui.custom_classes.MyComboBox'>", self.cell_widget_class(row, COL_EDIT))

    def test_diffrn_ambient_temperature_combo(self):
        row = self.key_row('_diffrn_ambient_temperature')
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(row, COL_CIF))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(row, COL_DATA))
        self.assertEqual("<class 'finalcif.gui.custom_classes.MyComboBox'>", self.cell_widget_class(row, COL_EDIT))

    def test_combo_items_ambient_temp(self):
        row = self.key_row('_diffrn_ambient_temperature')
        self.assertEqual(
            ['', '15(1)', '80(2)', '100(2)', '110(2)', '120(2)', '130(2)', '150(2)', '200(2)', '293.15(2)', '298(2)'],
            self.get_combobox_items(row, COL_EDIT))

    def test_combo_items_radiation(self):
        row = self.key_row('_diffrn_radiation_type')
        self.assertEqual(['', 'Mo Kα', 'Cu Kα', 'Ag Kα'], self.get_combobox_items(row, COL_EDIT))

    def test_ambient_conditions_combo(self):
        # Test if N~~2~ is correctly translated to N_2
        row = self.key_row('_diffrn_ambient_environment')
        self.assertEqual('N₂', self.get_combobox_items(row, COL_EDIT)[1])

    def test_combo_items_exptl_crystal_description(self):
        row = self.key_row('_exptl_crystal_description')
        self.assertEqual(['', 'block', 'needle', 'plate', 'prism', 'sphere'], self.get_combobox_items(row, COL_EDIT))

    def test_combo_items_atom_sites_solution_primary(self):
        row = self.key_row('_atom_sites_solution_primary')
        self.assertEqual(
            ['', 'direct', 'vecmap', 'heavy', 'difmap', 'geom', 'disper', 'isomor', 'notdet', 'dual', 'iterative',
             'other'], self.get_combobox_items(row, COL_EDIT))

    def test_combo_items_exptl_crystal_colour(self):
        row = self.key_row('_exptl_crystal_colour')
        self.assertEqual(
            ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue', 'green', 'gray', 'pink', 'orange',
             'violet',
             'brown'], self.get_combobox_items(row, COL_EDIT))

    def test_background_color_data(self):
        self.assertEqual(light_green, self.get_background_color('_computing_cell_refinement', COL_DATA))
        self.assertEqual(light_green, self.get_background_color('_computing_data_collection', COL_DATA))
        self.assertEqual(light_green, self.get_background_color('_computing_data_reduction', COL_DATA))
        self.assertEqual(QColor(0, 0, 0, 255), self.get_background_color('_computing_molecular_graphics', COL_DATA))

    def test_chemical_formula_moiety(self):
        self.assertEqual('?',
                         self.cell_text('_chemical_formula_moiety', COL_CIF))
        self.assertEqual('',
                         self.cell_text('_chemical_formula_moiety', COL_DATA))
        self.assertEqual('',
                         self.cell_text('_chemical_formula_moiety', COL_EDIT))

    def test_background_color_theta_max(self):
        self.assertEqual((0, 0, 0, 255), self.get_background_color('_cell_measurement_theta_max', COL_CIF).getRgb())
        self.assertEqual(light_green, self.get_background_color('_cell_measurement_theta_max', COL_DATA))
        self.assertEqual((0, 0, 0, 255),
                         self.get_background_color('_cell_measurement_theta_max', COL_EDIT).getRgb())

    def test_exptl_crystal_size(self):
        self.assertEqual('0.220', self.cell_text('_exptl_crystal_size_max', COL_DATA))
        self.assertEqual('0.100', self.cell_text('_exptl_crystal_size_mid', COL_DATA))
        self.assertEqual('0.040', self.cell_text('_exptl_crystal_size_min', COL_DATA))

    def test_symmetry(self):
        self.assertEqual('18', self.cell_text('_space_group_IT_number', 0))
        self.assertEqual('orthorhombic', self.cell_text('_space_group_crystal_system', 0))
        self.assertEqual('P 21 21 2', self.cell_text('_space_group_name_H-M_alt', 0))
        self.assertEqual('P 2 2ab', self.cell_text('_space_group_name_Hall', 0))

    def test_abs_configuration(self):
        self.assertEqual('?', self.cell_text('_chemical_absolute_configuration', COL_CIF))
        self.assertEqual('', self.cell_text('_chemical_absolute_configuration', COL_DATA))
        self.assertEqual('', self.cell_text('_chemical_absolute_configuration', COL_EDIT))
        self.assertEqual(yellow, self.myapp.ui.cif_main_table.itemFromKey('_chemical_absolute_configuration',
                                                                          1).background().color())

    def allrows_test_key(self, key: str = '', results: list = None):
        # The results list is a list with three items for each data column in the main table.
        self.myapp.hide()
        for n, r in enumerate(results):
            # print(self.cell_text(key, n))
            self.assertEqual(r, self.cell_text(key, n))

    def test_equipment_click_machine(self):
        self.equipment_click('APEX2 QUAZAR')
        self.allrows_test_key('_diffrn_measurement_method', ['?', 'ω and ϕ scans', 'ω and ϕ scans'])
        self.allrows_test_key('_diffrn_measurement_specimen_support',
                              ['?', 'MiTeGen micromount', 'MiTeGen micromount'])

    # unittest.SkipTest('')
    def test_equipment_click_machine_oxford_0(self):
        self.equipment_click('APEX2 QUAZAR')
        # We have a value which is new. So a row at start is created and only the CIF column is populated
        self.assertEqual('?', self.cell_text('_diffrn_measurement_ambient_temperature_device_make', COL_CIF))

    def test_equipment_click_machine_oxford_1(self):
        self.equipment_click('APEX2 QUAZAR')
        self.assertEqual('Oxford Cryostream 800',
                         self.cell_text('_diffrn_measurement_ambient_temperature_device_make', COL_DATA))

    def test_equipment_click_machine_oxford_2(self):
        self.equipment_click('APEX2 QUAZAR')
        self.assertEqual('Oxford Cryostream 800',
                         self.cell_text('_diffrn_measurement_ambient_temperature_device_make', COL_EDIT))

    def test_equipment_click_author_address_0(self):
        # Check if click on author adds the address to second and third column:
        self.equipment_click('Crystallographer Details')
        self.assertEqual('?', self.cell_text('_audit_contact_author_address', COL_CIF))

    def test_equipment_click_author_address_1(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', COL_DATA))

    def test_equipment_click_author_address_2(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', COL_EDIT))

    def test_contact_author_name_0(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual('?', self.cell_text('_audit_contact_author_name', COL_CIF))

    def test_contact_author_name_1(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual('Dr. Daniel Kratzert', self.cell_text('_audit_contact_author_name', COL_DATA))

    def test_contact_author_name_2(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual('Dr. Daniel Kratzert', self.cell_text('_audit_contact_author_name', COL_EDIT))

    def test_contact_author_cellwidget_bevore_click(self):
        self.assertEqual(self.myapp.ui.cif_main_table.vheaderitems[5], '_audit_contact_author_name')
        self.assertEqual('', self.myapp.ui.cif_main_table.getText(5, COL_DATA))

    def test_contact_author_cellwidget_after(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual(self.myapp.ui.cif_main_table.vheaderitems[5], '_audit_contact_author_name')
        self.assertEqual('Dr. Daniel Kratzert', self.myapp.ui.cif_main_table.getText(5, COL_DATA))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(5, COL_CIF))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(5, COL_DATA))
        self.assertEqual("<class 'NoneType'>", self.cell_widget_class(5, COL_EDIT))

    def test_addr(self):
        self.assertNotEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', COL_EDIT))

    def test_addr_after_author_click_0(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', COL_EDIT))

    def test_addr_after_author_click_1(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', COL_DATA))

    def test_addr_after_author_click_2(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual('?', self.cell_text('_audit_contact_author_address', COL_CIF))

    def test_edit_values_and_save(self):
        self.myapp.hide()
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_primary', column=2, txt='test1ä')
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_secondary', column=2, txt='test2ö')
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_address', column=2, txt='test3ü')
        self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_email', column=2, txt='test4ß')
        self.myapp.ui.cif_main_table.setText(key='_diffrn_measurement_method', column=2, txt='test 12 Å')
        cif = Path('testcif_file.cif')
        self.myapp.save_current_cif_file(cif.name)
        self.myapp.ui.cif_main_table.setRowCount(0)
        self.myapp.load_cif_file(cif)
        # test if data is still the same:
        # The character is quoted in the cif file:
        self.assertEqual(r'test 12 \%A', self.myapp.cif['_diffrn_measurement_method'])
        # And unquoted in the application:
        self.assertEqual(r'test 12 Å', self.cell_text(key='_diffrn_measurement_method', col=0))
        self.assertEqual('test1ä', self.cell_text(key='_atom_sites_solution_primary', col=0))
        self.assertEqual(r'test1\"a', self.myapp.cif['_atom_sites_solution_primary'])
        self.assertEqual('test2ö', self.cell_text(key='_atom_sites_solution_secondary', col=0))
        self.assertEqual('test3ü', self.cell_text(key='_audit_contact_author_address', col=0))
        self.assertEqual('test4ß', self.cell_text(key='_audit_contact_author_email', col=0))

    def test_rename_data_tag(self):
        self.myapp.hide()
        self.myapp.ui.datnameLineEdit.setText('foo_bar_yes')
        self.myapp.ui.SaveCifButton.click()
        self.myapp.ui.BackPushButton.click()
        pair = self.myapp.cif.block.find_pair('_vrf_PLAT307_foo_bar_yes')
        erg = ['_vrf_PLAT307_foo_bar_yes',
               ';\r\nPROBLEM: Isolated Metal Atom found in Structure (Unusual) Ga1 Check\r\nRESPONSE: foobar\r\n;']
        erg = [x.replace("\n", "").replace("\r", "") for x in erg]
        pair = [x.replace("\n", "").replace("\r", "") for x in pair]
        self.assertEqual(erg, pair)
        self.myapp.final_cif_file_name.unlink()


if __name__ == '__main__':
    unittest.main()
