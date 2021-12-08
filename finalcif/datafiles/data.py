#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------


class WorkDataMixin():
    """
    A class to hold data from work folder etc.
    """

    def __init__(self):
        self.sources = {'_atom_sites_solution_primary'           : None,
                        '_cell_measurement_reflns_used'          : None,
                        '_cell_measurement_temperature'          : None,
                        '_cell_measurement_theta_min'            : None,
                        '_cell_measurement_theta_max'            : None,
                        '_chemical_absolute_configuration'       : None,
                        '_chemical_formula_moiety'               : None,
                        '_computing_data_collection'             : None,
                        '_computing_cell_refinement'             : None,
                        '_computing_data_reduction'              : None,
                        '_computing_structure_solution'          : None,
                        '_database_code_depnum_ccdc_archive'     : None,
                        '_diffrn_ambient_temperature'            : None,
                        '_diffrn_reflns_av_R_equivalents'        : None,
                        '_diffrn_source_voltage'                 : None,
                        '_diffrn_source_current'                 : None,
                        '_exptl_absorpt_correction_type'         : None,
                        '_exptl_absorpt_correction_T_min'        : None,
                        '_exptl_absorpt_correction_T_max'        : None,
                        '_exptl_absorpt_process_details'         : None,
                        '_exptl_crystal_colour'                  : None,
                        '_exptl_crystal_description'             : None,
                        '_exptl_crystal_recrystallization_method': None,
                        '_exptl_crystal_size_min'                : None,
                        '_exptl_crystal_size_mid'                : None,
                        '_exptl_crystal_size_max'                : None,
                        '_publ_section_references'               : None,
                        '_refine_special_details'                : None,
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
                        '_twin_special_details'                  : None,
                        }
