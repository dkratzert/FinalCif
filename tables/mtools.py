import itertools as it

cif_keywords_list = (
    ['_chemical_formula_weight', 1],
    ['_diffrn_ambient_temperature', 2],
    ['_space_group_crystal_system', 3],
    #['_space_group_name_H-M_alt', 4],
    ['_cell_length_a', 5],
    ['_cell_length_b', 6],
    ['_cell_length_c', 7],
    ['_cell_angle_alpha', 8],
    ['_cell_angle_beta', 9],
    ['_cell_angle_gamma', 10],
    ['_cell_volume', 11],
    ['_cell_formula_units_Z', 12],
    ['_exptl_crystal_density_diffrn', 13],
    ['_exptl_absorpt_coefficient_mu', 14],
    ['_exptl_crystal_F_000', 15],
    #['_exptl_crystal_size_max', 16],
    #['_exptl_crystal_size_mid', 16],
    #['_exptl_crystal_size_min', 16],
    ['_exptl_crystal_colour', 17],
    ['_exptl_crystal_description', 18],
    #['_diffrn_radiation_type', 19],
    #['_diffrn_radiation_wavelength', 19],
    ['_diffrn_reflns_theta_min', 20],
    ['_diffrn_reflns_theta_max', 20],
    #['_diffrn_reflns_limit_h_min', 21],
    #['_diffrn_reflns_limit_h_max', 21],
    #['_diffrn_reflns_limit_k_min', 21],
    #['_diffrn_reflns_limit_k_max', 21],
    #['_diffrn_reflns_limit_l_min', 21],
    #['_diffrn_reflns_limit_l_max', 21],
    ['_diffrn_reflns_number', 22],
    #['_reflns_number_total', 23],
    #['_diffrn_reflns_av_R_equivalents', 23],
    #['_diffrn_reflns_av_unetI/netI', 23],
    #['_refine_ls_number_reflns', 24],
    #['_refine_ls_number_restraints', 24],
    #['_refine_ls_number_parameters', 24],
    ['_refine_ls_goodness_of_fit_ref', 25],
    #['_refine_ls_R_factor_gt', 26],
    #['_refine_ls_wR_factor_gt', 26],
    #['_refine_ls_R_factor_all', 27],
    #['_refine_ls_wR_factor_ref', 27],
    #['_refine_diff_density_max', 28],
    #['_refine_diff_density_min', 28],
    #['_refine_ls_abs_structure_Flack', 29]

)


def grouper(inputs, n, fillvalue=None):
    iters = [iter(inputs)] * n
    return it.zip_longest(*iters, fillvalue=fillvalue)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def this_or_quest(value):
    """
    Returns the value or a question mark if the value is None.
    """
    return value if value else '?'
