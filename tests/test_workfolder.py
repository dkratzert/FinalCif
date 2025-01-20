import os

os.environ['RUNNING_TEST'] = 'True'
import unittest
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget
from qtpy.QtTest import QTest

from finalcif import VERSION
from finalcif.appwindow import AppWindow
from finalcif.gui.custom_classes import Column
from finalcif.tools.misc import unify_line_endings
from tests.helpers import addr

data = Path('tests')


class TestFileIsOpened(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        self.testcif = (data / 'examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        self.myapp = AppWindow(file=self.testcif)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(True)
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        (data / 'examples/work/foo.cif').unlink(missing_ok=True)
        (data / 'examples/work/cu_BruecknerJK_153F40_0m-finalcif.cif').unlink(missing_ok=True)

    def tearDown(self) -> None:
        Path('foo.cif').unlink(missing_ok=True)
        Path('tests/examples/work/cu_BruecknerJK_153F40_0m-finalcif.cif').unlink(missing_ok=True)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)
        self.myapp.close()

    def test_save_action(self):
        self.myapp.save_current_cif_file()
        self.assertEqual(True, (data / 'examples/work/cu_BruecknerJK_153F40_0m-finalcif.cif').exists())


class TestWorkfolder(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        self.testcif = (data / 'examples/work/cu_BruecknerJK_153F40_0m.cif').resolve()
        # TODO: Adapt this to the bahavior with the changes file:
        (data / 'examples/work/cu_BruecknerJK_153F40_0m-finalcif_changes.cif').unlink(missing_ok=True)
        self.myapp = AppWindow(file=self.testcif)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(True)
        self.myapp.equipment.import_equipment_from_file(str(data.parent / 'test-data/Crystallographer_Details.cif'))
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))

    def tearDown(self) -> None:
        self.testcif.with_suffix('.ins').unlink(missing_ok=True)
        self.testcif.with_suffix('.lst').unlink(missing_ok=True)
        self.testcif.with_suffix('.2fcf').unlink(missing_ok=True)
        (data / 'testcif_file.cif').unlink(missing_ok=True)
        (data / 'examples/work/cu_BruecknerJK_153F40_0m-finalcif_changes.cif').unlink(missing_ok=True)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)
        self.myapp.close()

    def key_row(self, key: str) -> int:
        return self.myapp.ui.cif_main_table.row_from_key(key)

    def cell_widget(self, row: int, col: int) -> QWidget:
        return self.myapp.ui.cif_main_table.cellWidget(row, col)

    def cell_widget_class(self, row: int, col: int) -> str:
        try:
            return str(self.myapp.ui.cif_main_table.cellWidget(row, col).__class__)
        except Exception:
            return ''

    def get_combobox_items(self, row: int, col: int):
        widget = self.cell_widget(row, col)
        return [widget.itemText(i) for i in range(widget.count())]

    def cell_text(self, key: str, col: int) -> str:
        try:
            return unify_line_endings(self.myapp.ui.cif_main_table.getTextFromKey(key, col))
        except ValueError:
            return ''

    def equipment_click(self, field: str):
        listw = self.myapp.ui.EquipmentTemplatesListWidget
        self.myapp.ui.EquipmentTemplatesStackedWidget.setCurrentIndex(0)
        item = listw.findItems(field, Qt.MatchStartsWith)[0]
        listw.setCurrentItem(item)
        self.assertEqual(field.upper(), item.text().upper())
        rect = listw.visualItemRect(item)
        QTest.mouseDClick(listw.viewport(), Qt.LeftButton, Qt.NoModifier, rect.center())
        # This is necessary:
        self.myapp.equipment.load_selected_equipment()

    def get_background_color(self, key: str, col: int) -> QColor:
        return self.myapp.ui.cif_main_table.itemFromKey(key, col).background().color()

    def testDataColumn(self):
        self.myapp.hide()
        # test of ccdc number added from email during load:
        self.assertEqual('1979688', self.cell_text('_database_code_depnum_ccdc_archive', Column.DATA))
        # '_computing_structure_solution:'
        self.assertEqual('SHELXT 2018/2', self.cell_text('_computing_structure_solution', Column.DATA))
        self.assertEqual('direct', self.cell_text('_atom_sites_solution_primary', Column.DATA))
        self.assertEqual('9624', self.cell_text('_cell_measurement_reflns_used', Column.DATA))
        self.assertEqual('78.8605', self.cell_text('_cell_measurement_theta_max', Column.DATA))
        self.assertEqual('2.547', self.cell_text('_cell_measurement_theta_min', Column.DATA))
        # Test for auto-fill data:
        self.assertEqual('SAINT V8.40A', self.cell_text('_computing_cell_refinement', Column.DATA))
        self.assertEqual('?', self.cell_text('_computing_cell_refinement', Column.CIF))
        self.assertEqual('Bruker BIS V6.2.12/2019-08-12', self.cell_text('_computing_data_collection', Column.DATA))
        self.assertEqual('1.1', self.cell_text('_diffrn_source_current', Column.DATA))
        self.assertEqual('50.0', self.cell_text('_diffrn_source_voltage', Column.DATA))
        self.assertEqual('colourless', self.cell_text('_exptl_crystal_colour', Column.DATA))
        self.assertEqual('plate', self.cell_text('_exptl_crystal_description', Column.DATA))
        # _exptl_crystal_recrystallization_method Yellow:
        self.assertEqual('', self.cell_text('_exptl_crystal_recrystallization_method', Column.DATA))
        # self.assertEqual('QPlainTextEdit {background-color: #faf796;}',
        #                 self.myapp.ui.cif_main_table.cellWidget(41, 1).styleSheet())
        self.assertEqual(
            """Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.""",
            self.cell_text('_publ_section_references', Column.DATA))
        self.assertEqual('geom', self.cell_text('_atom_sites_solution_hydrogens', 0))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', Column.DATA))

    def test_abs_configuration_combo(self):
        self.assertEqual(6, self.key_row('_chemical_absolute_configuration'))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>", self.cell_widget_class(6, Column.CIF))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         self.cell_widget_class(6, Column.DATA))
        self.assertEqual("<class 'finalcif.gui.combobox.MyComboBox'>", self.cell_widget_class(6, Column.EDIT))

        row = self.key_row('_diffrn_radiation_type')
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         self.cell_widget_class(row, Column.CIF))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         self.cell_widget_class(row, Column.DATA))
        self.assertEqual("<class 'finalcif.gui.combobox.MyComboBox'>", self.cell_widget_class(row, Column.EDIT))

        row = self.key_row('_diffrn_ambient_temperature')
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         self.cell_widget_class(row, Column.CIF))
        self.assertEqual("<class 'finalcif.gui.plaintextedit.MyQPlainTextEdit'>",
                         self.cell_widget_class(row, Column.DATA))
        self.assertEqual("<class 'finalcif.gui.combobox.MyComboBox'>", self.cell_widget_class(row, Column.EDIT))

    def test_combo_items(self):
        row = self.key_row('_diffrn_ambient_temperature')
        self.assertEqual(
            ['', '15(1)', '80(2)', '100(2)', '110(2)', '120(2)', '130(2)', '150(2)', '200(2)', '293.15(2)', '298(2)'],
            self.get_combobox_items(row, Column.EDIT))

        row = self.key_row('_diffrn_radiation_type')
        self.assertEqual(['', 'Mo Kα', 'Cu Kα', 'Ag Kα', 'In Kα', 'Ga Kα', 'Fe Kα', 'W Kα'],
                         self.get_combobox_items(row, Column.EDIT))

        row = self.key_row('_exptl_crystal_description')
        self.assertEqual(['', 'block', 'needle', 'plate', 'prism', 'sphere'], self.get_combobox_items(row, Column.EDIT))

        row = self.key_row('_atom_sites_solution_primary')
        self.assertEqual(
            ['', 'direct', 'vecmap', 'heavy', 'difmap', 'geom', 'disper', 'isomor', 'notdet', 'dual', 'iterative',
             'other'], self.get_combobox_items(row, Column.EDIT))

        row = self.key_row('_exptl_crystal_colour')
        self.assertEqual(
            ['', 'colourless', 'white', 'black', 'yellow', 'red', 'blue', 'green', 'gray', 'pink', 'orange',
             'violet',
             'brown'], self.get_combobox_items(row, Column.EDIT))

    def test_background_color_data(self):
        self.assertEqual('background-color: #d9ffc9;',
                         self.myapp.ui.cif_main_table.widget_from_key('_computing_cell_refinement',
                                                                      Column.DATA).styleSheet())
        self.assertEqual('background-color: #d9ffc9;',
                         self.myapp.ui.cif_main_table.widget_from_key('_computing_data_collection',
                                                                      Column.DATA).styleSheet())
        self.assertEqual('background-color: #d9ffc9;',
                         self.myapp.ui.cif_main_table.widget_from_key('_computing_data_reduction',
                                                                      Column.DATA).styleSheet())

        self.assertEqual('', self.myapp.ui.cif_main_table.widget_from_key('_cell_measurement_theta_max',
                                                                          Column.CIF).styleSheet())
        self.assertEqual('background-color: #d9ffc9;',
                         self.myapp.ui.cif_main_table.widget_from_key('_cell_measurement_theta_max',
                                                                      Column.DATA).styleSheet())
        self.assertEqual('', self.myapp.ui.cif_main_table.widget_from_key('_cell_measurement_theta_max',
                                                                          Column.EDIT).styleSheet())

        self.assertEqual('', self.myapp.ui.cif_main_table.widget_from_key('_computing_molecular_graphics',
                                                                          Column.DATA).styleSheet())

    def test_exptl_crystal_size(self):
        self.assertEqual('0.220', self.cell_text('_exptl_crystal_size_max', Column.DATA))
        self.assertEqual('0.100', self.cell_text('_exptl_crystal_size_mid', Column.DATA))
        self.assertEqual('0.040', self.cell_text('_exptl_crystal_size_min', Column.DATA))

    def test_symmetry(self):
        self.assertEqual('18', self.cell_text('_space_group_IT_number', 0))
        self.assertEqual('orthorhombic', self.cell_text('_space_group_crystal_system', 0))
        self.assertEqual('P 21 21 2', self.cell_text('_space_group_name_H-M_alt', 0))
        self.assertEqual('P 2 2ab', self.cell_text('_space_group_name_Hall', 0))

    def test_abs_configuration(self):
        self.assertEqual('?', self.cell_text('_chemical_absolute_configuration', Column.CIF))
        self.assertEqual('', self.cell_text('_chemical_absolute_configuration', Column.DATA))
        self.assertEqual('', self.cell_text('_chemical_absolute_configuration', Column.EDIT))
        self.assertIn('background-color: #faf796;',
                      self.myapp.ui.cif_main_table.widget_from_key('_chemical_absolute_configuration',
                                                                   1).styleSheet())

    def allrows_test_key(self, key: str = '', results: list = None):
        # The results list is a list with three items for each data column in the main table.
        self.myapp.hide()
        for n, r in enumerate(results):
            # print(self.cell_text(key, n))
            self.assertEqual(r, self.cell_text(key, n))

    def test_equipment_click_machine(self):
        self.equipment_click('D8 VENTURE')
        self.allrows_test_key('_diffrn_measurement_method', ['?', 'ω and ϕ scans', 'ω and ϕ scans'])
        self.allrows_test_key('_diffrn_measurement_specimen_support',
                              ['?', 'MiTeGen micromount', 'MiTeGen micromount'])

    def test_addr_after_author_click_0(self):
        self.equipment_click('Crystallographer Details')
        self.assertEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', Column.EDIT))
        self.assertEqual(unify_line_endings(addr), self.cell_text('_audit_contact_author_address', Column.DATA))
        self.assertEqual('?', self.cell_text('_audit_contact_author_address', Column.CIF))

    def test_edit_values_and_save(self):
        self.myapp.hide()
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_primary', column=2, txt='test1ä')
        self.myapp.ui.cif_main_table.setText(key='_atom_sites_solution_secondary', column=2, txt='test2ö')
        # Not there anymore
        # self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_address', column=2, txt='test3ü')
        # self.myapp.ui.cif_main_table.setText(key='_audit_contact_author_email', column=2, txt='test4ß')
        self.myapp.ui.cif_main_table.setText(key='_diffrn_measurement_method', column=2, txt='test 12 Å')
        self.myapp.save_current_cif_file()
        self.myapp.ui.cif_main_table.setRowCount(0)
        self.myapp.load_cif_file(self.myapp.cif.finalcif_file)
        # test if data is still the same:
        # The character is quoted in the cif file:
        self.assertEqual(r'test 12 \%A', self.myapp.cif['_diffrn_measurement_method'])
        # And unquoted in the application:
        self.assertEqual(r'test 12 Å', self.cell_text(key='_diffrn_measurement_method', col=0))
        self.assertEqual('test1ä', self.cell_text(key='_atom_sites_solution_primary', col=0))
        self.assertEqual(r'test1\"a', self.myapp.cif['_atom_sites_solution_primary'])
        self.assertEqual('test2ö', self.cell_text(key='_atom_sites_solution_secondary', col=0))
        # Not there anymore
        # self.assertEqual('test3ü', self.cell_text(key='_audit_contact_author_address', col=0))
        # self.assertEqual('test4ß', self.cell_text(key='_audit_contact_author_email', col=0))

    def test_rename_data_tag(self):
        self.myapp.hide()
        self.myapp.ui.datanameComboBox.setEditText('foo_bar_yes')
        self.myapp.ui.SaveCifButton.click()
        self.myapp.ui.BackPushButton.click()
        pair = self.myapp.cif.block.find_pair('_vrf_PLAT307_foo_bar_yes')
        erg = ['_vrf_PLAT307_foo_bar_yes',
               ';\r\nPROBLEM: Isolated Metal Atom found in Structure (Unusual) Ga1 Check\r\nRESPONSE: foobar\r\n;']
        erg = [x.replace("\n", "").replace("\r", "") for x in erg]
        pair = [x.replace("\n", "").replace("\r", "") for x in pair]
        self.assertEqual(erg, pair)
        self.myapp.cif.finalcif_file.unlink(missing_ok=True)


class TestWorkfolderOtherCifName(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        self.testcif = (data / 'examples/work/p21c.cif').resolve()
        self.myapp = AppWindow(file=self.testcif)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(True)
        self.myapp.equipment.import_equipment_from_file(data.parent / 'test-data/Crystallographer_Details.cif')
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))

    def tearDown(self) -> None:
        self.testcif.with_suffix('.ins').unlink(missing_ok=True)
        self.testcif.with_suffix('.lst').unlink(missing_ok=True)
        self.testcif.with_suffix('.2fcf').unlink(missing_ok=True)
        (data / 'testcif_file.cif').unlink(missing_ok=True)
        self.myapp.ui.trackChangesCifCheckBox.setChecked(False)
        self.myapp.close()

    def cell_text(self, key: str, col: int) -> str:
        return unify_line_endings(self.myapp.ui.cif_main_table.getTextFromKey(key, col))

    def key_row(self, key: str) -> int:
        return self.myapp.ui.cif_main_table.row_from_key(key)

    def testDataColumn(self):
        self.myapp.hide()
        # test of ccdc number added from email during load:
        self.assertEqual('1979688', self.cell_text('_database_code_depnum_ccdc_archive', Column.DATA))
        # '_computing_structure_solution:'
        self.assertEqual('SHELXT (G. Sheldrick)', self.cell_text('_computing_structure_solution', Column.DATA))
        self.assertEqual('direct', self.cell_text('_atom_sites_solution_primary', Column.DATA))
        self.assertEqual('9624', self.cell_text('_cell_measurement_reflns_used', Column.DATA))
        self.assertEqual('78.8605', self.cell_text('_cell_measurement_theta_max', Column.DATA))
        self.assertEqual('2.547', self.cell_text('_cell_measurement_theta_min', Column.DATA))
        # Test for auto-fill data:
        self.assertEqual('SAINT V8.40A', self.cell_text('_computing_cell_refinement', Column.DATA))
        self.assertEqual('?', self.cell_text('_computing_cell_refinement', Column.CIF))
        self.assertEqual('Bruker BIS V6.2.12/2019-08-12', self.cell_text('_computing_data_collection', Column.DATA))
        self.assertEqual('1.1', self.cell_text('_diffrn_source_current', Column.DATA))
        self.assertEqual('50.0', self.cell_text('_diffrn_source_voltage', Column.DATA))
        self.assertEqual('colourless', self.cell_text('_exptl_crystal_colour', Column.DATA))
        self.assertEqual('plate', self.cell_text('_exptl_crystal_description', Column.DATA))
        # _exptl_crystal_recrystallization_method Yellow:
        self.assertEqual('', self.cell_text('_exptl_crystal_recrystallization_method', Column.DATA))
        self.assertEqual('background-color: #faf796;',
                         self.myapp.ui.cif_main_table.cellWidget(
                             self.key_row('_exptl_crystal_recrystallization_method'), 1).styleSheet())
        self.assertEqual("Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, "
                         "G.M. (2015). Acta Cryst. C71, 3-8.", self.cell_text('_publ_section_references', Column.DATA))
        self.assertEqual('geom', self.cell_text('_atom_sites_solution_hydrogens', 0))
        self.assertEqual('', self.cell_text('_atom_sites_solution_hydrogens', Column.DATA))


if __name__ == '__main__':
    unittest.main()
