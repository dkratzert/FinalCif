import os
import sys
import unittest
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication

from appwindow import AppWindow
from gui.custom_classes import light_green, yellow, COL_DATA, COL_CIF, COL_EDIT
from tools.version import VERSION


def unify_line_endings(text: str):
    return '\n'.join(text.splitlines())


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

addr = """Albert-Ludwigs-Universität Freiburg\r\nInstitut für Anorganische und Analytische Chemie\r\nAlbertstraße 21\r\nFreiburg i. Br.\r\n79104\r\nGermany"""

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


class TestWorkfolder(unittest.TestCase):
    """A CIF fle in a complete work folder"""

    def setUp(self) -> None:
        os.chdir(Path(__file__).absolute().parent.parent)
        self.testcif = Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').absolute()
        self.myapp = AppWindow(self.testcif)
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.hide()

    def tearDown(self) -> None:
        Path(self.testcif.stem + '.ins').unlink(missing_ok=True)
        Path(self.testcif.stem + '.lst').unlink(missing_ok=True)
        Path(self.testcif.stem + '.2fcf').unlink(missing_ok=True)
        Path('testcif_file.cif').unlink(missing_ok=True)

    def testDataColumn(self):
        self.myapp.hide()
        # test of ccdc number added from email during load:
        self.assertEqual('1979688',
                         self.myapp.ui.cif_main_table.getTextFromKey('_database_code_depnum_ccdc_archive', 1))
        # '_computing_structure_solution:'
        self.assertEqual('SHELXT (G. Sheldrick)',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_structure_solution', 1))
        self.assertEqual('direct',
                         self.myapp.ui.cif_main_table.getTextFromKey('_atom_sites_solution_primary', 1))
        self.assertEqual('9624',
                         self.myapp.ui.cif_main_table.getTextFromKey('_cell_measurement_reflns_used', 1))
        self.assertEqual('78.8605',
                         self.myapp.ui.cif_main_table.getTextFromKey('_cell_measurement_theta_max', 1))
        self.assertEqual('2.547',
                         self.myapp.ui.cif_main_table.getTextFromKey('_cell_measurement_theta_min', 1))
        self.assertEqual("<class 'gui.custom_classes.MyComboBox'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(10, 2).__class__))
        # Test for auto-fill data:
        self.assertEqual('SAINT V8.40A',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_cell_refinement', 1))
        self.assertEqual('?',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_cell_refinement', 0))
        self.assertEqual('Bruker BIS V6.2.12/2019-08-12',
                         self.myapp.ui.cif_main_table.getTextFromKey('_computing_data_collection', 1))
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
        # self.assertEqual('QPlainTextEdit {background-color: #faf796;}',
        #                 self.myapp.ui.cif_main_table.cellWidget(41, 1).styleSheet())
        self.assertEqual(
            """Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.\n""",
            self.myapp.ui.cif_main_table.getTextFromKey('_publ_section_references', 1))
        self.assertEqual('geom', self.myapp.ui.cif_main_table.getTextFromKey('_atom_sites_solution_hydrogens', 0))
        self.assertEqual('', self.myapp.ui.cif_main_table.getTextFromKey('_atom_sites_solution_hydrogens', 1))
        self.assertEqual(
            """FinalCif V{} by Daniel Kratzert, Freiburg {}, https://github.com/dkratzert/FinalCif""".format(VERSION,
                                                                                                             datetime.now().year),
            self.myapp.ui.cif_main_table.getTextFromKey('_audit_creation_method', 1))

    def test_background_data(self):
        self.assertEqual(light_green,
                         self.myapp.ui.cif_main_table.itemFromKey('_computing_cell_refinement',
                                                                  COL_DATA).background().color())
        self.assertEqual(light_green,
                         self.myapp.ui.cif_main_table.itemFromKey('_computing_data_collection',
                                                                  COL_DATA).background().color())
        self.assertEqual(light_green,
                         self.myapp.ui.cif_main_table.itemFromKey('_computing_data_reduction',
                                                                  COL_DATA).background().color())
        self.assertEqual(QColor(0, 0, 0, 255), self.myapp.ui.cif_main_table.itemFromKey('_computing_molecular_graphics',
                                                                                        COL_DATA).background().color())

    def test_chemical_formula_moiety(self):
        self.assertEqual('?',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_formula_moiety', COL_CIF))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_formula_moiety', COL_DATA))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_formula_moiety', COL_EDIT))

    def test_background_color_theta_max(self):
        self.assertEqual((0, 0, 0, 255), self.myapp.ui.cif_main_table.itemFromKey('_cell_measurement_theta_max',
                                                                                  COL_CIF).background().color().getRgb())
        self.assertEqual(light_green, self.myapp.ui.cif_main_table.itemFromKey('_cell_measurement_theta_max',
                                                                               COL_DATA).background().color())
        self.assertEqual((0, 0, 0, 255), self.myapp.ui.cif_main_table.itemFromKey('_cell_measurement_theta_max',
                                                                                  COL_EDIT).background().color().getRgb())

    def test_exptl_crystal_size(self):
        self.assertEqual('0.220',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_size_max', COL_DATA))
        self.assertEqual('0.100',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_size_mid', COL_DATA))
        self.assertEqual('0.040',
                         self.myapp.ui.cif_main_table.getTextFromKey('_exptl_crystal_size_min', COL_DATA))

    def test_symmetry(self):
        self.assertEqual('18', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_IT_number', 0))
        self.assertEqual('orthorhombic', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_crystal_system', 0))
        self.assertEqual('P 21 21 2', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_name_H-M_alt', 0))
        self.assertEqual('P 2 2ab', self.myapp.ui.cif_main_table.getTextFromKey('_space_group_name_Hall', 0))

    def test_abs_configuration(self):
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_absolute_configuration', 1))
        self.assertEqual('',
                         self.myapp.ui.cif_main_table.getTextFromKey('_chemical_absolute_configuration', 2))
        self.assertEqual(yellow, self.myapp.ui.cif_main_table.itemFromKey('_chemical_absolute_configuration',
                                                                          1).background().color())

    def allrows_test_key(self, key: str = '', results: list = None):
        self.myapp.hide()
        for n, r in enumerate(results):
            # print('##', key, n, r)
            # print(self.myapp.ui.cif_main_table.getTextFromKey(key, n))
            self.assertEqual(r, self.myapp.ui.cif_main_table.getTextFromKey(key, n))

    def test_equipment_click(self):
        self.myapp.hide()
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('APEX2 QUAZAR', Qt.MatchExactly)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.equipment.load_selected_equipment()
        self.allrows_test_key('_diffrn_measurement_method', ['?', 'ω and ϕ scans', 'ω and ϕ scans'])
        self.allrows_test_key('_diffrn_measurement_specimen_support', ['?', 'MiTeGen micromount', 'MiTeGen micromount'])
        self.allrows_test_key('_olex2_diffrn_ambient_temperature_device',
                              ['Oxford Cryostream 800', 'Oxford Cryostream 800', 'Oxford Cryostream 800'])
        # Check if click on author adds the address to second and third column:
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact Author', Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.myapp.equipment.load_selected_equipment()
        self.assertEqual('?', self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_address', 0))
        self.assertEqual(unify_line_endings(addr),
                         unify_line_endings(
                             self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_address', 1)))
        self.assertEqual(unify_line_endings(addr),
                         unify_line_endings(
                             self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_address', 2)))

    def test_contact_author_name(self):
        item = self.myapp.ui.EquipmentTemplatesListWidget.findItems('Contact Author', Qt.MatchStartsWith)[0]
        self.myapp.ui.EquipmentTemplatesListWidget.setCurrentItem(item)
        self.assertEqual('?', self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_name', 0))
        self.assertEqual('Dr. Daniel Kratzert',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_name', 1))
        self.assertEqual('Dr. Daniel Kratzert',
                         self.myapp.ui.cif_main_table.getTextFromKey('_audit_contact_author_name', 2))
        self.assertEqual(self.myapp.ui.cif_main_table.vheaderitems[5], '_audit_contact_author_name')
        self.assertEqual('Dr. Daniel Kratzert', self.myapp.ui.cif_main_table.getText(5, 1))
        self.assertEqual("<class 'NoneType'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(5, 0).__class__))
        self.assertEqual("<class 'NoneType'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(5, 1).__class__))
        self.assertEqual("<class 'NoneType'>",
                         str(self.myapp.ui.cif_main_table.cellWidget(5, 2).__class__))
        self.assertEqual(unify_line_endings(addr),
                         unify_line_endings(str(self.myapp.ui.cif_main_table.cellWidget(3, 2))))

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
        self.myapp.load_cif_file(cif.name)
        # test if data is still the same:
        # The character is quoted in the cif file:
        self.assertEqual(r'test 12 \%A', self.myapp.cif['_diffrn_measurement_method'])
        # And unquoted in the application:
        self.assertEqual(r'test 12 Å',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_diffrn_measurement_method', col=0))
        self.assertEqual('test1ä',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_atom_sites_solution_primary', col=0))
        self.assertEqual(r'test1a\"', self.myapp.cif['_atom_sites_solution_primary'])
        self.assertEqual('test2ö',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_atom_sites_solution_secondary', col=0))
        self.assertEqual('test3ü',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_audit_contact_author_address', col=0))
        self.assertEqual('test4ß',
                         self.myapp.ui.cif_main_table.getTextFromKey(key='_audit_contact_author_email', col=0))

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
