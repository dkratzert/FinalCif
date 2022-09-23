#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import re
from contextlib import suppress
from pathlib import Path

from gemmi import cif as gcif

from finalcif.cif.cif_file_io import CifContainer
from finalcif.datafiles.bruker_frame import BrukerFrameHeader
from finalcif.datafiles.data import WorkDataMixin
from finalcif.datafiles.p4p_reader import P4PFile
from finalcif.datafiles.sadabs import Sadabs
from finalcif.datafiles.saint import SaintListFile
from finalcif.datafiles.shelx_lst import SolutionProgram
from finalcif.gui.dialogs import show_general_warning


class MissingCifData():
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value


class BrukerData(WorkDataMixin):

    def __init__(self, app, cif: CifContainer):
        super(BrukerData, self).__init__()
        self.cif = cif
        self.app = app
        self.saint_data = SaintListFile(name_patt='*_0*m._ls', directory=self.cif.fileobj.parent.resolve())
        # Using the saint list files name as base reference for all other data containing files:
        basename = self.saint_data.filename.stem.split('_0m')[0]
        self.basename = re.sub(r'^(cu|mo|ag)_', '', basename)
        # This is only in this list file, not in the global:
        saint_first_ls = SaintListFile(name_patt='*_01._ls', directory=self.cif.fileobj.parent.resolve())
        sol = SolutionProgram(cif)
        solution_program = None
        if 'shelx' in self.cif.block.find_value('_audit_creation_method').lower():
            shelx = 'Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.\n'
        else:
            shelx = ''
        if cif.res_file_data and cif.dsr_used:
            dsr = 'The program DSR was used for model building:\n' \
                  'D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934. doi: 10.1107/S1600576718004508'
            shelx += dsr
        abstype = '?'
        t_min = '?'
        t_max = '?'
        # Going back from last dataset:
        for n in range(1, len(self.sadabs.datasets) + 1):
            try:
                abstype = 'numerical' if self.sadabs.dataset(-n).numerical else 'multi-scan'
                t_min = self.sadabs.dataset(-n).transmission.tmin
                t_max = self.sadabs.dataset(-n).transmission.tmax
                if all([abstype, t_min, t_max]):
                    break
            except (KeyError, AttributeError, TypeError):
                pass
                # print('No .abs file found.')
                # no abs file found
        # the lower temp is more likely:
        try:
            temp1 = self.frame_header.temperature
        except (AttributeError, KeyError, FileNotFoundError):
            temp1 = 293
        try:
            kilovolt = self.frame_header.kilovolts
        except (AttributeError, KeyError, FileNotFoundError):
            kilovolt = ''
        try:
            milliamps = self.frame_header.milliamps
        except (AttributeError, KeyError, FileNotFoundError):
            milliamps = ''
        try:
            frame_name = self.frame_header.filename.name
        except FileNotFoundError:
            frame_name = ''
        if not self.cif['_computing_structure_solution'] and self.cif.solution_program_details:
            solution_program = (self.cif.solution_program_details, self.cif.fileobj.name)
        if self.cif['_computing_structure_solution']:
            solution_program = (gcif.as_string(self.cif['_computing_structure_solution']), self.cif.fileobj.name)
        if not solution_program:
            solution_program = (sol.program.version, Path(sol.program.filename).name)
        if self.cif.absorpt_process_details:
            absdetails = (self.cif.absorpt_process_details, self.cif.fileobj.name)
        else:
            absdetails = (self.sadabs.version, self.sadabs.filename.name)
        if self.cif.absorpt_correction_type:
            abscorrtype = (self.cif.absorpt_correction_type, self.cif.fileobj.name)
        else:
            abscorrtype = (abstype, self.sadabs.filename.name)
        if self.cif.absorpt_correction_t_max:
            abs_tmax = (self.cif.absorpt_correction_t_max, self.cif.fileobj.name)
        else:
            abs_tmax = (str(t_max), self.sadabs.filename.name)
        if self.cif.absorpt_correction_t_min:
            abs_tmin = (self.cif.absorpt_correction_t_min, self.cif.fileobj.name)
        else:
            abs_tmin = (str(t_min), self.sadabs.filename.name)

        if self.sadabs.Rint:
            rint = (self.sadabs.Rint, self.sadabs.filename.name)
            self.sources['_diffrn_reflns_av_R_equivalents'] = rint
        temp2 = self.p4p.temperature
        temperature = round(min([temp1, temp2]), 1)
        if temperature < 0.01:
            temperature = ''
        if (self.cif['_diffrn_ambient_temperature'].split('(')[0] or
            self.cif['_cell_measurement_temperature']).split('(')[0] == '0':
            show_general_warning('<b>Warning of impossible temperature specification</b>:<br>'
                                 'You probably entered &minus;273.15 °C instead '
                                 'of &minus;173.15 °C into the SHELX instruction file.<br>'
                                 'A temperature of 0 K is likely to be wrong.')
        try:
            if abs(int(self.cif['_diffrn_ambient_temperature'].split('(')[0]) - int(temperature)) >= 2 and \
                not self.app.temperature_warning_displayed:
                self.app.temperature_warning_displayed = True
                show_general_warning('<b>Warning</b>: The temperature from the measurement and '
                                     'from SHELX differ. Please double-check for correctness.<br><br>'
                                     'SHELX says: {} K<br>'
                                     'The P4P file says: {} K<br>'
                                     'Frame header says: {} K<br><br>'
                                     'You may add a '
                                     '<a href="http://shelx.uni-goettingen.de/shelxl_html.php#TEMP">TEMP</a> '
                                     'instruction to your SHELX file (in °C).'
                                     .format(self.cif['_diffrn_ambient_temperature'].split('(')[0],
                                             round(temp2, 1),
                                             round(temp1, 1)))
        except ValueError:
            # most probably one value is '?'
            pass
        if not self.cif['_space_group_name_H-M_alt']:
            try:
                self.sources['_space_group_name_H-M_alt'] = (
                    self.cif.space_group, 'Calculated by gemmi: https://gemmi.readthedocs.io')
            except AttributeError:
                pass
        if not self.cif['_space_group_name_Hall']:
            with suppress(AttributeError):
                self.sources['_space_group_name_Hall'] = (
                    self.cif.hall_symbol, 'Calculated by gemmi: https://gemmi.readthedocs.io')
        if not self.cif['_space_group_IT_number']:
            with suppress(AttributeError):
                self.sources['_space_group_IT_number'] = (
                    self.cif.spgr_number_from_symmops, 'Calculated by gemmi: https://gemmi.readthedocs.io')
        if not self.cif['_space_group_crystal_system']:
            with suppress(AttributeError):
                csystem = self.cif.crystal_system
                self.sources['_space_group_crystal_system'] = (
                    csystem, 'calculated by gemmi: https://gemmi.readthedocs.io')
        if not self.cif.symmops and self.cif.symmops_from_spgr:
            loop = self.cif.block.init_loop('_space_group_symop_operation_', ['xyz'])
            for symmop in reversed(self.cif.symmops_from_spgr):
                loop.add_row([gcif.quote(symmop)])
        # All sources that are not filled with data will be yellow in the main table
        #                          data                         tooltip
        self.sources['_cell_measurement_reflns_used'] = (
            self.saint_data.cell_reflections, self.saint_data.filename.name)
        self.sources['_cell_measurement_theta_min'] = (
            self.saint_data.cell_res_min_theta or '', self.saint_data.filename.name)
        self.sources['_cell_measurement_theta_max'] = (
            self.saint_data.cell_res_max_theta or '', self.saint_data.filename.name)
        self.sources['_computing_data_collection'] = (saint_first_ls.aquire_software, saint_first_ls.filename.name)
        self.sources['_computing_cell_refinement'] = (self.saint_data.version, self.saint_data.filename.name)
        self.sources['_computing_data_reduction'] = (self.saint_data.version, self.saint_data.filename.name)
        self.sources['_exptl_absorpt_correction_type'] = abscorrtype
        self.sources['_exptl_absorpt_correction_T_min'] = abs_tmin
        self.sources['_exptl_absorpt_correction_T_max'] = abs_tmax
        self.sources['_exptl_absorpt_process_details'] = absdetails
        self.sources['_cell_measurement_temperature'] = (temperature, self.p4p.filename.name)
        self.sources['_diffrn_ambient_temperature'] = (temperature, self.p4p.filename.name)
        self.sources['_exptl_crystal_colour'] = (self.p4p.crystal_color, self.p4p.filename.name)
        self.sources['_exptl_crystal_description'] = (self.p4p.morphology, self.p4p.filename.name)
        self.sources['_exptl_crystal_size_min'] = (self.p4p.crystal_size[0] or '', self.p4p.filename.name)
        self.sources['_exptl_crystal_size_mid'] = (self.p4p.crystal_size[1] or '', self.p4p.filename.name)
        self.sources['_exptl_crystal_size_max'] = (self.p4p.crystal_size[2] or '', self.p4p.filename.name)
        self.sources['_computing_structure_solution'] = solution_program
        self.sources['_atom_sites_solution_primary'] = (sol.method, 'Inherited from solution program.')
        self.sources['_diffrn_source_voltage'] = (kilovolt or '', frame_name)
        self.sources['_diffrn_source_current'] = (milliamps or '', frame_name)
        self.sources['_chemical_formula_moiety'] = ('', '')
        self.sources['_publ_section_references'] = (shelx, '')
        self.sources['_refine_special_details'] = ('', '')
        self.sources['_exptl_crystal_recrystallization_method'] = ('', '')
        if not self.cif.is_centrosymm:
            self.sources['_chemical_absolute_configuration'] = ('', '')
        if self.saint_data.is_twin and self.saint_data.components_firstsample == 2:
            with suppress(Exception):
                law = self.saint_data.twinlaw[list(self.saint_data.twinlaw.keys())[0]]
                self.sources['_twin_individual_twin_matrix_11'] = (str(law[0][1]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_12'] = (str(law[0][2]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_13'] = (str(law[0][0]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_21'] = (str(law[1][1]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_22'] = (str(law[1][2]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_23'] = (str(law[1][0]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_31'] = (str(law[2][1]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_32'] = (str(law[2][2]), self.saint_data.filename.name)
                self.sources['_twin_individual_twin_matrix_33'] = (str(law[2][0]), self.saint_data.filename.name)
                self.sources['_twin_individual_id'] = (
                    str(self.saint_data.components_firstsample), self.saint_data.filename.name)
                self.sources['_twin_special_details'] = (
                    'The data was integrated as a 2-component twin.', self.saint_data.filename.name)

    @property
    def sadabs(self):
        sad = Sadabs(basename='*.abs', searchpath=self.cif.fileobj.parent)
        return sad

    @property
    def frame_header(self):
        return BrukerFrameHeader(self.basename, self.cif.fileobj.parent)

    @property
    def p4p(self):
        return P4PFile(self.basename, self.cif.fileobj.parent)
