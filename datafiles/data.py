#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from cif.cif_file_io import CifContainer
from datafiles.shelxt import SHELXTlistfile


class WorkDataMixin():
    """
    A class to hold data from work folder etc.
    """

    def __init__(self):
        self.sources = {'_cell_measurement_reflns_used'          : None,
                        '_cell_measurement_theta_min'            : None,
                        '_cell_measurement_theta_max'            : None,
                        '_computing_data_collection'             : None,
                        '_computing_cell_refinement'             : None,
                        '_computing_data_reduction'              : None,
                        '_exptl_absorpt_correction_type'         : None,
                        '_exptl_absorpt_correction_T_min'        : None,
                        '_exptl_absorpt_correction_T_max'        : None,
                        '_diffrn_reflns_av_R_equivalents'        : None,
                        '_cell_measurement_temperature'          : None,
                        '_diffrn_ambient_temperature'            : None,
                        '_exptl_absorpt_process_details'         : None,
                        '_exptl_crystal_colour'                  : None,
                        '_exptl_crystal_description'             : None,
                        '_exptl_crystal_size_min'                : None,
                        '_exptl_crystal_size_mid'                : None,
                        '_exptl_crystal_size_max'                : None,
                        '_computing_structure_solution'          : None,
                        '_atom_sites_solution_primary'           : None,
                        '_diffrn_source_voltage'                 : None,
                        '_diffrn_source_current'                 : None,
                        '_chemical_formula_moiety'               : None,
                        '_publ_section_references'               : None,
                        '_refine_special_details'                : None,
                        '_exptl_crystal_recrystallization_method': None,
                        '_chemical_absolute_configuration'       : None,
                        '_space_group_name_H-M_alt'              : None,
                        '_space_group_name_Hall'                 : None,
                        '_space_group_IT_number'                 : None,
                        '_space_group_crystal_system'            : None,
                        '_twin_individual_twin_matrix_11'        : None,
                        '_twin_individual_twin_matrix_12'        : None,
                        '_twin_individual_twin_matrix_13'        : None,
                        '_twin_individual_twin_matrix_21'        : None,
                        '_twin_individual_twin_matrix_22'        : None,
                        '_twin_individual_twin_matrix_23'        : None,
                        '_twin_individual_twin_matrix_31'        : None,
                        '_twin_individual_twin_matrix_32'        : None,
                        '_twin_individual_twin_matrix_33'        : None,
                        '_twin_individual_id'                    : None,
                        '_twin_special_details'                  : (
                            'The data was integrated as a 2-component twin.', ''),
                        }


class SolutionProgram(object):
    """Handles the solution program: _computing_structure_solution"""

    def __init__(self, cif: CifContainer):
        self.cif_key = '_computing_structure_solution'
        self.cif = cif
        self.basename = cif.fileobj.stem.split('_0m')[0]
        self.method = ''

    def get_solution_program(self):
        """
        Tries to figure out which program was used for structure solution.
        TODO: figure out more solution programs.
        """
        p = self.cif.fileobj.parent
        xt_files = p.glob(self.basename + '*.lxt')
        try:
            res = self.cif.block.find_pair('_shelx_res_file')[1]
        except (TypeError, AttributeError):
            res = ''
        byxt = res.find('REM SHELXT solution in')
        for x in xt_files:
            shelxt = SHELXTlistfile(x.as_posix())
            if shelxt.version and byxt:
                self.method = 'direct'
                return shelxt
        if byxt > 0:
            xt = SHELXTlistfile('')
            xt.version = "SHELXT (G. Sheldrick)"
            self.method = 'direct'
            return xt
        xt = SHELXTlistfile('')
        xt.version = "SHELXS (G. Sheldrick)"
        self.method = 'direct'
        return xt

    def __repr__(self):
        return self.get_solution_program().version