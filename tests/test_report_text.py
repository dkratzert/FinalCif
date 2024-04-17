import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock

from docx import Document
from docx.text.paragraph import Paragraph

from finalcif import VERSION
from finalcif.cif.cif_file_io import CifContainer
from finalcif.report.references import ReferenceList
from finalcif.report.report_text import Hydrogens, MachineType, Crystallization, CrystalSelection, DataCollection, \
    DataReduction, SolveRefine, CCDC, FinalCifreport, Disorder

data = Path('.')
statics = Path('tests/statics')


class MyMock(Mock):
    def __repr__(self):
        return 'mocked_block_name'


class CifMock:
    def __init__(self, cif=None):
        self.cif = cif
        self.block = MyMock()

    def __getitem__(self, item):
        return self.cif.get(item)


class TestMachineType(TestCase):

    def test__get_cooling_device_iucr(self):
        cif = CifContainer(statics / 'temp_device_iucr.cif')
        self.assertEqual('Oxford Cryostream 850 ', MachineType._get_cooling_device(cif))

    def test__get_cooling_device_olx(self):
        cif = CifContainer(statics / 'temp_device_olx.cif')
        self.assertEqual('Oxford Cryostream 810 ', MachineType._get_cooling_device(cif))

    def test__get_cooling_device_both(self):
        cif = CifContainer(statics / 'temp_device_both.cif')
        self.assertEqual('Oxford Cryostream 900 ', MachineType._get_cooling_device(cif))

    def test__get_no_cooling_device(self):
        cif = CifContainer(statics / 'temp_no_device.cif')
        self.assertEqual('', MachineType._get_cooling_device(cif))


class TestTextParagraphs(unittest.TestCase):

    def setUp(self) -> None:
        document = Document()
        self.paragraph: Paragraph = document.add_paragraph()
        self.reflist = ReferenceList(paragraph=self.paragraph)

    def test_crystallization(self):
        cif = {'_exptl_crystal_recrystallization_method': 'The compound was crystallized '
                                                          'from water by evaporation at 25 °C.'}
        # noinspection PyTypeChecker
        Crystallization(cif, paragraph=self.paragraph)
        self.assertEqual('The compound was crystallized from water by evaporation at 25 °C. ', self.paragraph.text)

    def test_empty_crystallization(self):
        cif = {'_exptl_crystal_recrystallization_method': ''}
        # noinspection PyTypeChecker
        Crystallization(cif, paragraph=self.paragraph)
        self.assertEqual(("[No _exptl_crystal_recrystallization_method like 'The compound was "
                          "crystallized from methanol by evaporation at 25 °C.' was given]. "), self.paragraph.text)

    def test_crystallization_with_a_newline_in_the_input(self):
        cif = {'_exptl_crystal_recrystallization_method': 'The compound was crystallized \n'
                                                          'from water by evaporation at 25 °C.'}
        # noinspection PyTypeChecker
        Crystallization(cif, paragraph=self.paragraph)
        # The formatting of gstr should always turn a newline into a space char:
        self.assertEqual('The compound was crystallized from water by evaporation at 25 °C. ', self.paragraph.text)

    def test_crystal_selection(self):
        data = {'_exptl_crystal_description'          : 'block',
                '_exptl_crystal_colour'               : 'yellow',
                '_diffrn_measurement_specimen_support': 'Nylon loop'}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A yellow, block-shaped crystal of mocked_block_name was mounted on a Nylon '
                          'loop with perfluoroether oil. '), self.paragraph.text)

    def test_crystal_selection_empty(self):
        data = {'_exptl_crystal_description'          : '',
                '_exptl_crystal_colour'               : '',
                '_diffrn_measurement_specimen_support': ''}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A crystal of mocked_block_name was mounted on the goniometer. '), self.paragraph.text)

    def test_crystal_selection_only_shape(self):
        data = {'_exptl_crystal_description'          : 'block',
                '_exptl_crystal_colour'               : '',
                '_diffrn_measurement_specimen_support': ''}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A block-shaped crystal of mocked_block_name '
                          'was mounted on the goniometer. '), self.paragraph.text)

    def test_crystal_selection_only_color(self):
        data = {'_exptl_crystal_description'          : '',
                '_exptl_crystal_colour'               : 'yellow',
                '_diffrn_measurement_specimen_support': ''}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A yellow crystal of mocked_block_name '
                          'was mounted on the goniometer. '), self.paragraph.text)

    def test_crystal_selection_only_support(self):
        data = {'_exptl_crystal_description'          : '',
                '_exptl_crystal_colour'               : '',
                '_diffrn_measurement_specimen_support': 'Mitegen micromount'}
        cif = CifMock(data)

        # noinspection PyTypeChecker
        CrystalSelection(cif, paragraph=self.paragraph)
        self.assertEqual(('A crystal of mocked_block_name was mounted on a Mitegen micromount with '
                          'perfluoroether oil. '), self.paragraph.text)

    def test_data_collection(self):
        cif = {'_diffrn_ambient_temperature': '100(2)'}
        # noinspection PyTypeChecker
        DataCollection(cif, paragraph=self.paragraph)
        self.assertEqual('Data were collected from a shock-cooled single crystal at 100(2)\xa0K', self.paragraph.text)

    def test_data_collection_empty(self):
        cif = {'_diffrn_ambient_temperature': ''}
        # noinspection PyTypeChecker
        DataCollection(cif, paragraph=self.paragraph)
        self.assertEqual(('Data were collected from a single crystal at [No _diffrn_ambient_temperature '
                          'given]\xa0K'), self.paragraph.text)

    def test_machine_type_empty(self):
        cif = {
            '_diffrn_measurement_device_type'                    : '',
            '_diffrn_measurement_device'                         : '',
            '_diffrn_source'                                     : '',
            '_diffrn_radiation_monochromator'                    : '',
            '_olex2_diffrn_ambient_temperature_device'           : '',
            '_diffrn_measurement_ambient_temperature_device_make': '',
            '_diffrn_radiation_type'                             : '',
            '_diffrn_radiation_wavelength'                       : '',
            '_diffrn_detector_type'                              : '',
        }
        # noinspection PyTypeChecker
        MachineType(cif, paragraph=self.paragraph)
        self.assertEqual(('on a [No _diffrn_measurement_device_type given] [No '
                          '_diffrn_measurement_device given] with a [No _diffrn_source given] using a '
                          '[No _diffrn_radiation_monochromator given] as monochromator and a [No '
                          '_diffrn_detector_type given] detector. The diffractometer was equipped with '
                          'a low temperature device and used [No _diffrn_radiation_type given] '
                          'radiation (λ = [No _diffrn_radiation_wavelength given]\xa0Å). '), self.paragraph.text)

    def test_machine_type_1(self):
        cif = {
            '_diffrn_measurement_device_type'                    : 'Bruker Foo Bar  ',
            '_diffrn_measurement_device'                         : 'four-circle diffractometer',
            '_diffrn_source'                                     : 'sealed X-ray tube',
            '_diffrn_radiation_monochromator'                    : 'Ge 220',
            '_olex2_diffrn_ambient_temperature_device'           : '',
            '_diffrn_measurement_ambient_temperature_device_make': 'Oxford Cryostream 800',
            '_diffrn_radiation_type'                             : 'Cu Kα',
            '_diffrn_radiation_wavelength'                       : '1.54178',
            '_diffrn_detector_type'                              : 'Photon X',
        }
        # noinspection PyTypeChecker
        MachineType(cif, paragraph=self.paragraph)
        self.assertEqual(('on a Bruker Foo Bar four-circle diffractometer with a sealed X-ray tube '
                          'using a Ge 220 as monochromator and a Photon X detector. The diffractometer '
                          'was equipped with an Oxford Cryostream 800 low temperature device and used '
                          'Cu Kα radiation (λ = 1.54178\xa0Å). '), self.paragraph.text)

    def test_machine_type_2(self):
        cif = {
            '_diffrn_measurement_device_type'                    : 'Bruker Foo Bar  ',
            '_diffrn_measurement_device'                         : 'four-circle diffractometer',
            '_diffrn_source'                                     : 'sealed X-ray tube',
            '_diffrn_radiation_monochromator'                    : 'Ge 220',
            '_olex2_diffrn_ambient_temperature_device'           : 'Oxford Cryostream 800',
            '_diffrn_measurement_ambient_temperature_device_make': '',
            '_diffrn_radiation_type'                             : 'Cu Kα',
            '_diffrn_radiation_wavelength'                       : '1.54178',
            '_diffrn_detector_type'                              : 'Photon X',
        }
        # noinspection PyTypeChecker
        MachineType(cif, paragraph=self.paragraph)
        self.assertEqual(('on a Bruker Foo Bar four-circle diffractometer with a sealed X-ray tube '
                          'using a Ge 220 as monochromator and a Photon X detector. The diffractometer '
                          'was equipped with an Oxford Cryostream 800 low temperature device and used '
                          'Cu Kα radiation (λ = 1.54178\xa0Å). '), self.paragraph.text)

    def test_data_reduction_empty(self):
        cif = {
            '_computing_data_reduction'     : '',
            '_exptl_absorpt_correction_type': '',
            '_exptl_absorpt_process_details': '',
        }
        # noinspection PyTypeChecker
        DataReduction(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('All data were integrated with [No _computing_data_reduction given] and a ?? '
                          'absorption correction using [Unknown scaling program] was applied.[1,2]'),
                         self.paragraph.text)
        self.assertEqual(('[0] Unknown Reference, please add.\n'
                          '[1] Unknown Reference, please add.'), str(self.reflist))

    def test_data_reduction(self):
        cif = {
            '_computing_data_reduction'     : 'SAINT V8.40A',
            '_exptl_absorpt_correction_type': 'multi-scan',
            '_exptl_absorpt_process_details': ("SADABS 2016/2: Krause, L., Herbst-Irmer, R., "
                                               "Sheldrick G.M. & Stalke D.,\n"
                                               " J. Appl. Cryst. 48 (2015) 3-10"),
        }
        # noinspection PyTypeChecker
        DataReduction(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('All data were integrated with SAINT and a multi-scan absorption correction '
                          'using SADABS was applied.[1,2]'), self.paragraph.text)
        self.assertEqual(("[0] Bruker, SAINT, V8.40A, Bruker AXS Inc., Madison, Wisconsin, USA.\n"
                          "[1] L. Krause, R. Herbst-Irmer, G. M. Sheldrick, D. Stalke, J. Appl. Cryst. "
                          "2015, 48, 3–10, doi:10.1107/S1600576714022985."), str(self.reflist))

    def test_solve_refine_empty(self):
        cif = {
            '_computing_structure_solution'   : '',
            '_atom_sites_solution_primary'    : '',
            '_computing_structure_refinement' : '',
            '_refine_special_details'         : '',
            '_olex2_refine_details'           : '',
            '_refine_ls_structure_factor_coef': '',
            '_computing_molecular_graphics'   : '',
        }
        # noinspection PyTypeChecker
        SolveRefine(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('The structure was solved by [No _atom_sites_solution_primary given] methods '
                          'using [No and refined by full-matrix least-squares methods against F by [No '
                          '_computing_structure_refinement given].[1,2]'), self.paragraph.text)
        self.assertEqual(('[0] Unknown Reference, please add.\n'
                          '[1] Unknown Reference, please add.'), str(self.reflist))

    def test_solve_refine_with_olex2(self):
        cif = {
            '_computing_structure_solution'   : 'SHELXT - CRYSTAL STRUCTURE SOLUTION - VERSION 2014/5',
            '_atom_sites_solution_primary'    : 'direct',
            '_computing_structure_refinement' : 'SHELXL-2018/3 (Sheldrick, 2018)',
            '_refine_special_details'         : ('The methanol molecule is disordered around a special\n'
                                                 'position and thus half occupied.'),
            '_olex2_refine_details'           : '"Olex refine details"',
            '_refine_ls_structure_factor_coef': 'Fsqd',
            '_computing_molecular_graphics'   : 'Olex2 (Dolomanov et al., 2009)',
        }
        # noinspection PyTypeChecker
        SolveRefine(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('The structure was solved by direct methods using SHELXT and refined by '
                          'full-matrix least-squares methods against F2 by SHELXL-2018/3 using '
                          'Olex2.[1-3]'), self.paragraph.text)
        self.assertEqual(('[0] G. M. Sheldrick, Acta Cryst. 2015, A71, 3–8, '
                          'doi:10.1107/S2053273314026370.\n'
                          '[1] G. M. Sheldrick, Acta Cryst. 2015, C71, 3–8, '
                          'doi:10.1107/S2053229614024218.\n'
                          '[2] O. V. Dolomanov, L. J. Bourhis, R. J. Gildea, J. A. K. Howard, H. '
                          'Puschmann, J. Appl. Cryst. 2009, 42, 339-341, doi:10.1107/S0021889808042726.'),
                         str(self.reflist))

    def test_solve_refine(self):
        cif = {
            '_computing_structure_solution'   : 'SHELXT - CRYSTAL STRUCTURE SOLUTION - VERSION 2014/5',
            '_atom_sites_solution_primary'    : 'direct',
            '_computing_structure_refinement' : 'SHELXL-2018/3 (Sheldrick, 2018)',
            '_refine_special_details'         : ('The methanol molecule is disordered around a special\n'
                                                 'position and thus half occupied.'),
            '_olex2_refine_details'           : '"Olex refine details"',
            '_refine_ls_structure_factor_coef': 'Fsqd',
            '_computing_molecular_graphics'   : 'ShelXle (Hübschle 2011)',
        }
        # noinspection PyTypeChecker
        SolveRefine(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('The structure was solved by direct methods using SHELXT and refined by '
                          'full-matrix least-squares methods against F2 by SHELXL-2018/3 using '
                          'ShelXle.[1-3]'), self.paragraph.text)
        self.assertEqual(('[0] G. M. Sheldrick, Acta Cryst. 2015, A71, 3–8, '
                          'doi:10.1107/S2053273314026370.\n'
                          '[1] G. M. Sheldrick, Acta Cryst. 2015, C71, 3–8, '
                          'doi:10.1107/S2053229614024218.\n'
                          '[2] C. B. Hübschle, G. M. Sheldrick, B. Dittrich, J. Appl. Cryst. 2011, 44, '
                          '1281–1284, doi:10.1107/S0021889811043202.'), str(self.reflist))

    def test_ccdc_empty(self):
        cif = {
            '_database_code_depnum_ccdc_archive': '',
        }
        # noinspection PyTypeChecker
        CCDC(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('Crystallographic data for the structures reported here have been '
                          'deposited with the Cambridge Crystallographic Data Centre.[1] CCDC ?????? '
                          'contain the supplementary crystallographic data for this paper. These data '
                          'can be obtained free of charge from The Cambridge Crystallographic Data '
                          'Centre via www.ccdc.cam.ac.uk/\u200bstructures.'), self.paragraph.text)
        self.assertEqual(('[0] C. R. Groom, I. J. Bruno, M. P. Lightfoot, S. C. Ward, Acta Cryst. 2016, '
                          'B72, 171–179, doi:10.1107/S2052520616003954.'), str(self.reflist))

    def test_ccdc_with_number(self):
        cif = {
            '_database_code_depnum_ccdc_archive': '123456',
        }
        # noinspection PyTypeChecker
        CCDC(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('Crystallographic data for the structures reported here have been '
                          'deposited with the Cambridge Crystallographic Data Centre.[1] CCDC 123456 '
                          'contain the supplementary crystallographic data for this paper. These data '
                          'can be obtained free of charge from The Cambridge Crystallographic Data '
                          'Centre via www.ccdc.cam.ac.uk/\u200bstructures.'), self.paragraph.text)
        self.assertEqual(('[0] C. R. Groom, I. J. Bruno, M. P. Lightfoot, S. C. Ward, Acta Cryst. 2016, '
                          'B72, 171–179, doi:10.1107/S2052520616003954.'), str(self.reflist))

    def test_ccdc_with_number_and_CCDC(self):
        cif = {
            '_database_code_depnum_ccdc_archive': 'CCDC 123456',
        }
        # noinspection PyTypeChecker
        CCDC(cif, paragraph=self.paragraph, ref=self.reflist)
        self.assertEqual(('Crystallographic data for the structures reported here have been '
                          'deposited with the Cambridge Crystallographic Data Centre.[1] CCDC 123456 '
                          'contain the supplementary crystallographic data for this paper. These data '
                          'can be obtained free of charge from The Cambridge Crystallographic Data '
                          'Centre via www.ccdc.cam.ac.uk/\u200bstructures.'), self.paragraph.text)

    def test_finalcif_report(self):
        FinalCifreport(paragraph=self.paragraph, reflist=self.reflist)
        self.assertEqual('This report and the CIF file were generated using FinalCif.[1]', self.paragraph.text)
        self.assertEqual(f'[0] D. Kratzert, FinalCif, V{VERSION}, https://dkratzert.de/finalcif.html.',
                         str(self.reflist))

    def test_hydrogens_all_free_anis(self):
        cif = CifContainer(data / 'test-data/hydrogen/all_free_free_anisotropic.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('The hydrogen atoms were refined freely with anisotropic displacement '
                          'parameters.'), self.paragraph.text)

    def test_hydrogens_all_free_iso(self):
        cif = CifContainer(data / 'test-data/hydrogen/all_free_free_isotropic.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('All hydrogen atoms were refined freely with '
                          'isotropic displacement parameters.'), self.paragraph.text)

    def test_hydrogens_all_iso_constr(self):
        cif = CifContainer(data / 'test-data/hydrogen/all_free_isotropic_constr.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('All hydrogen atoms were refined freely with their Uiso values constrained to '
                          '1.5 times the Ueq of their pivot atoms for terminal sp3 carbon atoms and 1.2 '
                          'times for all other carbon atoms.'), self.paragraph.text)

    def test_hydrogens_all_riding_anis(self):
        cif = CifContainer(data / 'test-data/hydrogen/all_riding_anisotropic.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('The hydrogen atoms were refined anisotropic on calculated positions using '
                          'a riding model with their Uiso values constrained to 1.5 times the Ueq of '
                          'their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all '
                          'other carbon atoms.'), self.paragraph.text)

    def test_hydrogens_all_riding_isotropic(self):
        cif = CifContainer(data / 'test-data/hydrogen/all_riding_isotropic.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('All C-bound hydrogen atoms were refined isotropic on calculated positions '
                          'using a riding model with their Uiso values constrained to 1.5 times the Ueq '
                          'of their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all '
                          'other carbon atoms.'), self.paragraph.text)

    def test_hydrogens_some_riding_isotropic(self):
        cif = CifContainer(data / 'test-data/hydrogen/some_riding_isotropic.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('All C-bound hydrogen atoms were refined with isotropic displacement '
                          'parameters. Some were refined freely and some on calculated positions using '
                          'a riding model with their Uiso values constrained to 1.5 times the Ueq of '
                          'their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all other '
                          'carbon atoms.'), self.paragraph.text)

    def test_hydrogens_some_riding_some_isotropic(self):
        cif = CifContainer(data / 'test-data/hydrogen/some_riding_some_isotropic.cif')
        # noinspection PyTypeChecker
        Hydrogens(cif, paragraph=self.paragraph)
        self.assertEqual(('All C-bound hydrogen atoms were refined with isotropic displacement '
                          'parameters. Some were refined freely and some on calculated positions using '
                          'a riding model with their Uiso values constrained to 1.5 times the Ueq of '
                          'their pivot atoms for terminal sp3 carbon atoms and 1.2 times for all other '
                          'carbon atoms.'), self.paragraph.text)

    def test_disorder(self):
        cif = type('CifContainer', (object,), {'dsr_used': True})()
        # noinspection PyTypeChecker
        Disorder(cif, paragraph=self.paragraph, reflist=self.reflist)
        self.assertEqual(('Disordered moieties were refined using bond lengths restraints and '
                          'displacement parameter restraints. Some parts of the disorder model were '
                          'introduced by the program DSR.[1,2] '), self.paragraph.text)
        self.assertEqual(('[0] D. Kratzert, J.J. Holstein, I. Krossing, J. Appl. Cryst. 2015, 48, '
                          '933–938, doi:10.1107/S1600576715005580.\n'
                          '[1] D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928–934, '
                          'doi:10.1107/S1600576718004508.'), str(self.reflist))

    def test_disorder_without_dsr(self):
        cif = type('CifContainer', (object,), {'dsr_used': False})()
        # noinspection PyTypeChecker
        Disorder(cif, paragraph=self.paragraph, reflist=self.reflist)
        self.assertEqual(('Disordered moieties were refined using bond lengths restraints and '
                          'displacement parameter restraints. '), self.paragraph.text)
        self.assertEqual('', str(self.reflist))
