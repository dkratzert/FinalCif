#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

from pathlib import Path

from cif.file_reader import CifContainer
from datafiles.bruker_frame import BrukerFrameHeader
from datafiles.p4p_reader import P4PFile
from datafiles.sadabs import Sadabs
from datafiles.saint import SaintListFile
from datafiles.shelxt import SHELXTlistfile
from datafiles.utils import DSRFind


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
        solution_program = self.get_solution_program()
        solution_version = solution_program.version or ''
        # This creates more problems than it solves:
        # try:
        #    self.plat = Platon(self.cif.filename)
        # except Exception as e:
        #    print(e)
        #    self.app.ui.CheckcifButton.setDisabled(True)
        #    self.plat = None
        solution_primary = ''
        resdata = cif.block.find_value('_shelx_res_file')
        shelx = 'Sheldrick, G.M. (2015). Acta Cryst. A71, 3-8.\nSheldrick, G.M. (2015). Acta Cryst. C71, 3-8.\n'
        dsr = ''
        d = DSRFind(resdata)
        if resdata:
            if d.dsr_used:
                dsr = 'The program DSR was used for model building:\n' \
                      'D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934. doi: 10.1107/S1600576718004508'
                shelx += dsr
        if solution_program and 'XT' in solution_program.version:
            solution_primary = 'direct'
        # TODO: determine the correct dataset number:
        dataset_num = 1
        abstype = '?'
        t_min = '?'
        t_max = '?'
        # Going back from last dataset:
        for n in range(1, len(self.sadabs.datasets) + 1):
            try:
                abstype = 'multi-scan' if not self.sadabs.dataset(-n).numerical else 'numerical'
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
        # try:
        #    moiety = self.plat.formula_moiety
        # except Exception as e:
        #    print('Could not make moiety formula:', e)
        #    moiety = ''
        # try:
        #    chk_file = self.plat.chk_filename
        # except Exception as e:
        #    chk_file = ''
        temp2 = self.p4p.temperature
        temperature = round(min([temp1, temp2]), 1)
        # TODO: make a Sources class that returns either the parser object itself or the respective value from the key
        #                                              data                         tooltip
        sources = {'_cell_measurement_reflns_used'          : (saint_data.cell_reflections, saint_data.filename.name),
                   '_cell_measurement_theta_min'            : (saint_data.cell_res_min_theta, saint_data.filename.name),
                   '_cell_measurement_theta_max'            : (saint_data.cell_res_max_theta, saint_data.filename.name),
                   '_computing_data_collection'             : (
                       saint_first_ls.aquire_software, saint_data.filename.name),
                   '_computing_cell_refinement'             : (saint_data.version, saint_data.filename.name),
                   '_computing_data_reduction'              : (saint_data.version, saint_data.filename.name),
                   '_exptl_absorpt_correction_type'         : (abstype, self.sadabs.filename.name),
                   '_exptl_absorpt_correction_T_min'        : (str(t_min), self.sadabs.filename.name),
                   '_exptl_absorpt_correction_T_max'        : (str(t_max), self.sadabs.filename.name),
                   '_diffrn_reflns_av_R_equivalents'        : (self.sadabs.Rint, self.sadabs.filename.name),
                   '_cell_measurement_temperature'          : (temperature, self.p4p.filename.name),
                   '_diffrn_ambient_temperature'            : (temperature, self.p4p.filename.name),
                   '_exptl_absorpt_process_details'         : (self.sadabs.version, self.sadabs.filename.name),
                   '_exptl_crystal_colour'                  : (self.p4p.crystal_color, self.p4p.filename.name),
                   '_exptl_crystal_description'             : (self.p4p.morphology, self.p4p.filename.name),
                   '_exptl_crystal_size_min'                : (self.p4p.crystal_size[0] or '', self.p4p.filename.name),
                   '_exptl_crystal_size_mid'                : (self.p4p.crystal_size[1] or '', self.p4p.filename.name),
                   '_exptl_crystal_size_max'                : (self.p4p.crystal_size[2] or '', self.p4p.filename.name),
                   '_computing_structure_solution'          : (solution_version, ''),
                   '_atom_sites_solution_primary'           : (solution_primary, ''),
                   '_diffrn_source_voltage'                 : (kilovolt or '', frame_name),
                   '_diffrn_source_current'                 : (milliamps or '', frame_name),
                   '_chemical_formula_moiety'               : ('', ''),
                   '_publ_section_references'               : (shelx, ''),
                   '_refine_special_details'                : ('', ''),
                   '_exptl_crystal_recrystallization_method': ('', ''),
                   }
        self.sources = dict((k.lower(), v) for k, v in sources.items())

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
            if shelxt and byxt:
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
        sad = Sadabs(self.basename)
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
