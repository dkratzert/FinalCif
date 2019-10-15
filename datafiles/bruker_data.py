#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from contextlib import suppress
from pathlib import Path

from gemmi import cif as gcif

from cif.cif_file_io import CifContainer
from datafiles.bruker_frame import BrukerFrameHeader
from datafiles.p4p_reader import P4PFile
from datafiles.sadabs import Sadabs
from datafiles.saint import SaintListFile
from datafiles.shelxt import SHELXTlistfile


class MissingCifData():
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value


class BrukerData(object):

    def __init__(self, app: 'AppWindow', cif: CifContainer):
        self.cif = cif
        self.app = app
        self.basename = cif.fileobj.stem.split('_0m')[0]
        saint_data = self.saint_log('*_0m._ls')
        saint_first_ls = self.saint_log('*_01._ls')
        sp = self.get_solution_program()
        solution_primary = ''
        if 'shelx' in self.cif.block.find_value('_audit_creation_method').lower():
            shelx = 'Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.\n'
        else:
            shelx = ''
        if cif.resdata:
            if cif.dsr_used:
                dsr = 'The program DSR was used for model building:\n' \
                      'D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934. doi: 10.1107/S1600576718004508'
                shelx += dsr
        if sp and 'XT' in sp.version:
            solution_primary = 'direct'
        solution_program = (sp.version, sp.filename)
        abstype = '?'
        t_min = '?'
        t_max = '?'
        # Going back from last dataset:
        for n in range(1, len(self.sadabs.datasets) + 1):
            try:
                abstype = 'numerical' if self.sadabs.dataset(-n).numerical else 'multi-scan'
                t_min = min(self.sadabs.dataset(-n).transmission)
                t_max = max(self.sadabs.dataset(-n).transmission)
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
        except (FileNotFoundError):
            frame_name = ''
        if self.cif.solution_program_details:
            solution_program = (self.cif.solution_program_details, self.cif.fileobj.name)
        if self.cif['_computing_structure_solution']:
            solution_program = (gcif.as_string(self.cif['_computing_structure_solution']), self.cif.fileobj.name)
        if self.cif.absorpt_process_details:
            absdetails = (self.cif.absorpt_process_details, self.cif.fileobj.name)
        else:
            absdetails = (self.sadabs.version, self.sadabs.filename.name)
        if self.cif.absorpt_correction_type:
            abscorrtype = (self.cif.absorpt_correction_type, self.cif.fileobj.name)
        else:
            abscorrtype = (abstype, self.sadabs.filename.name)
        if self.cif.absorpt_correction_T_max:
            abs_tmax = (self.cif.absorpt_correction_T_max, self.cif.fileobj.name)
        else:
            abs_tmax = (str(t_max), self.sadabs.filename.name)
        if self.cif.absorpt_correction_T_min:
            abs_tmin = (self.cif.absorpt_correction_T_min, self.cif.fileobj.name)
        else:
            abs_tmin = (str(t_min), self.sadabs.filename.name)

        if self.sadabs.Rint:
            rint = (self.sadabs.Rint, self.sadabs.filename.name)
        else:
            rint = ('', '')
        temp2 = self.p4p.temperature
        temperature = round(min([temp1, temp2]), 1)
        if temperature < 0.01:
            temperature = '?'
        # TODO: refrator space group things into a general method:
        spgr = '?'
        if not self.cif['_space_group_name_H-M_alt']:
            try:
                spgr = self.cif.space_group()
            except AttributeError:
                pass
        hallsym = '?'
        if not self.cif['_space_group_name_Hall']:
            with suppress(AttributeError):
                hallsym = self.cif.hall_symbol()
        spgrnum = '?'
        if not self.cif['_space_group_IT_number']:
            with suppress(AttributeError):
                spgrnum = self.cif.spgr_number_from_symmops()
        csystem = '?'
        if not self.cif['_space_group_crystal_system']:
            with suppress(AttributeError):
                csystem = self.cif.crystal_system()
        """
        #TODO: symmops are missing, need loops for that
        if not self.symmops:
            for x in reversed(self.symmops_from_spgr()):
                self.add_to_cif(cif_as_list, key=x, value='')
            self.add_to_cif(cif_as_list, key='_space_group_symop_operation_xyz', value='')
            self.add_to_cif(cif_as_list, key='_loop', value='')"""
        # All sources that are not filled with data will be yellow in the main table
        #                          data                         tooltip
        sources = {'_cell_measurement_reflns_used'          : (saint_data.cell_reflections, saint_data.filename.name),
                   '_cell_measurement_theta_min'            : (saint_data.cell_res_min_theta, saint_data.filename.name),
                   '_cell_measurement_theta_max'            : (saint_data.cell_res_max_theta, saint_data.filename.name),
                   '_computing_data_collection'             : (
                       saint_first_ls.aquire_software, saint_data.filename.name),
                   '_computing_cell_refinement'             : (saint_data.version, saint_data.filename.name),
                   '_computing_data_reduction'              : (saint_data.version, saint_data.filename.name),
                   '_exptl_absorpt_correction_type'         : abscorrtype,
                   '_exptl_absorpt_correction_T_min'        : abs_tmin,
                   '_exptl_absorpt_correction_T_max'        : abs_tmax,
                   '_diffrn_reflns_av_R_equivalents'        : rint,
                   '_cell_measurement_temperature'          : (temperature, self.p4p.filename.name),
                   '_diffrn_ambient_temperature'            : (temperature, self.p4p.filename.name),
                   '_exptl_absorpt_process_details'         : absdetails,
                   '_exptl_crystal_colour'                  : (self.p4p.crystal_color, self.p4p.filename.name),
                   '_exptl_crystal_description'             : (self.p4p.morphology, self.p4p.filename.name),
                   '_exptl_crystal_size_min'                : (self.p4p.crystal_size[0] or '', self.p4p.filename.name),
                   '_exptl_crystal_size_mid'                : (self.p4p.crystal_size[1] or '', self.p4p.filename.name),
                   '_exptl_crystal_size_max'                : (self.p4p.crystal_size[2] or '', self.p4p.filename.name),
                   '_computing_structure_solution'          : solution_program,
                   '_atom_sites_solution_primary'           : (solution_primary, ''),
                   '_diffrn_source_voltage'                 : (kilovolt or '', frame_name),
                   '_diffrn_source_current'                 : (milliamps or '', frame_name),
                   '_chemical_formula_moiety'               : ('', ''),
                   '_publ_section_references'               : (shelx, ''),
                   '_refine_special_details'                : ('', ''),
                   '_exptl_crystal_recrystallization_method': ('', ''),
                   '_chemical_absolute_configuration'       : ('', ''),
                   '_space_group_name_H-M_alt'              : (spgr, 'calculated by gemmi'),
                   '_space_group_name_Hall'                 : (hallsym, 'calculated by gemmi'),
                   '_space_group_IT_number'                 : (spgrnum, 'calculated by gemmi'),
                   '_space_group_crystal_system'            : (csystem, 'calculated by gemmi'),
                   }
        self.sources = sources  # dict((k.lower(), v) for k, v in sources.items())

    def get_solution_program(self):
        """
        Tries to figure out which program was used for structure solution.
        TODO: figure out more solution programs.
        """
        p = Path('./')
        # for line in cif._ciftext:
        #    if line.startswith('REM SHELXT solution in'):
        xt_files = p.glob(self.basename + '*.lxt')
        try:
            res = self.cif.block.find_pair('_shelx_res_file')[1]
        except (TypeError, AttributeError):
            res = ''
        byxt = res.find('REM SHELXT solution in')
        for x in xt_files:
            shelxt = SHELXTlistfile(x.as_posix())
            if shelxt.version and byxt:
                return shelxt
        if byxt > 0:
            xt = SHELXTlistfile('')
            xt.version = "SHELXT (G. Sheldrick)"
            return xt
        xt = SHELXTlistfile('')
        xt.version = "SHELXS (G. Sheldrick)"
        return xt

    def saint_log(self, name_patt='*_0m._ls'):
        """
        returns a saint parser object from the ._ls files.
        """
        return SaintListFile(name_patt)

    @property
    def sadabs(self):
        sad = Sadabs(basename='*.abs')
        # self.sad_fileLE, button = self.app.add_new_datafile(0, 'SADABS', 'add specific .abs file here, if needed...')
        # self.sad_fileLE.setText(str(sad.filename.absolute()))
        # button.clicked.connect(self.app.get_cif_file_block)
        # I have to run self.app.get_cif_file_block but data sources for abs file should be updated
        return sad

    @property
    def frame_header(self):
        return BrukerFrameHeader(self.basename)

    @property
    def p4p(self):
        return P4PFile(self.basename)
