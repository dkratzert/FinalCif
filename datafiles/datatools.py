from pathlib import Path

from cif.file_reader import CifContainer
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

    def __init__(self, cif: CifContainer):
        self.cif = cif
        saint_data = self.get_saint()
        p4p = self.get_p4p()
        saint_first_ls = self.get_saint('*_01._ls')
        sadabs_data = self.get_sadabs()
        frame_header = self.get_frame()
        solution_program = self.get_solution_program()
        solution_version = solution_program.version or ''
        solution_primary = ''
        if solution_program and 'XT' in solution_program.version:
            solution_primary = 'direct'
        # TODO: determine the correct dataset number:
        dataset_num = -1
        try:
            abstype = 'multi-scan' if not sadabs_data.dataset(-1).numerical else 'numerical'
            t_min = min(sadabs_data.dataset(dataset_num).transmission)
            t_max = max(sadabs_data.dataset(dataset_num).transmission)
        except (KeyError, AttributeError):
            # no abs file found
            print('no abs file found')
            abstype = '?'
            t_min = '?'
            t_max = '?'
        # the lower temp is more likely:
        temp1 = frame_header.temperature
        temp2 = p4p.temperature
        temperature = round(min([temp1, temp2]), 1)
        # TODO: make a Sources class that returns either the parser object itself or the respective value from the key:
        sources = {'_cell_measurement_reflns_used'  : saint_data.cell_reflections,
                   '_cell_measurement_theta_min'    : saint_data.cell_res_min_theta,
                   '_cell_measurement_theta_max'    : saint_data.cell_res_max_theta,
                   '_computing_data_collection'     : saint_first_ls.aquire_software,
                   '_computing_cell_refinement'     : saint_data.version,
                   '_computing_data_reduction'      : saint_data.version,
                   '_exptl_absorpt_correction_type' : abstype,
                   '_exptl_absorpt_correction_T_min': str(t_min),
                   '_exptl_absorpt_correction_T_max': str(t_max),
                   '_diffrn_reflns_av_R_equivalents': sadabs_data.Rint,
                   '_cell_measurement_temperature'  : temperature,
                   '_diffrn_ambient_temperature'    : temperature,
                   '_exptl_absorpt_process_details' : sadabs_data.version,
                   '_exptl_crystal_colour'          : p4p.crystal_color,
                   '_exptl_crystal_description'     : p4p.morphology,
                   '_exptl_crystal_size_min'        : p4p.crystal_size[0] or '',
                   '_exptl_crystal_size_mid'        : p4p.crystal_size[1] or '',
                   '_exptl_crystal_size_max'        : p4p.crystal_size[2] or '',
                   '_computing_structure_solution'  : solution_version,
                   '_atom_sites_solution_primary'   : solution_primary,
                   '_diffrn_source_current': frame_header.kilovolts or '',
                   '_diffrn_source_voltage': frame_header.milliwatt or '',
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
        xt_files = p.glob('*.lxt')
        try:
            res = self.cif.block.find_pair('_shelx_res_file')[1]
        except TypeError:
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

    def get_saint(self, name_patt='*_0m._ls'):
        """
        returns a saint parser object from the ._ls file.
        """
        p = Path('./')
        saintfiles = p.rglob(name_patt)
        saint = None
        for s in saintfiles:
            saint = SaintListFile(s.as_posix())
            if saint:
                # TODO: This is a relly stupid approach!
                return saint
        return saint

    def get_sadabs(self):
        p = Path('./')
        sadfiles = p.rglob('*.abs')
        sadabs = None
        for s in sadfiles:
            sadabs = Sadabs(s.as_posix())
            if sadabs:
                return sadabs
        return sadabs

    def get_frame(self):
        p = Path('./')
        frames = p.rglob('*.sfrm')
        header = None
        for fr in frames:
            header = BrukerFrameHeader(fr.as_posix())
            if header:
                return header
        return header

    def get_p4p(self):
        p = Path('./')
        p4p_files = p.rglob('*.p4p')
        p4p = None
        for p in p4p_files:
            p4p = P4PFile(p.as_posix())
            if p4p:
                return p4p
        return p4p
