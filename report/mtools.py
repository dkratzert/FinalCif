import itertools as it
import re

from docx.table import Table
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from cif.cif_file_io import CifContainer
from report.report_text import math_to_word
from report.spgrps import SpaceGroups

cif_keywords_list = (
    ['_chemical_formula_weight', 1],
    ['_diffrn_ambient_temperature', 2],
    ['_space_group_crystal_system', 3],
    # ['_space_group_name_H-M_alt', 4],
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
    # ['_exptl_crystal_size_max', 16],
    # ['_exptl_crystal_size_mid', 16],
    # ['_exptl_crystal_size_min', 16],
    ['_exptl_crystal_colour', 17],
    ['_exptl_crystal_description', 18],
    # ['_diffrn_radiation_type', 19],
    # ['_diffrn_radiation_wavelength', 19],
    ['_diffrn_reflns_theta_min', 20],
    ['_diffrn_reflns_theta_max', 20],
    # ['_diffrn_reflns_limit_h_min', 21],
    # ['_diffrn_reflns_limit_h_max', 21],
    # ['_diffrn_reflns_limit_k_min', 21],
    # ['_diffrn_reflns_limit_k_max', 21],
    # ['_diffrn_reflns_limit_l_min', 21],
    # ['_diffrn_reflns_limit_l_max', 21],
    ['_diffrn_reflns_number', 22],
    # ['_reflns_number_total', 23],
    # ['_diffrn_reflns_av_R_equivalents', 23],
    # ['_diffrn_reflns_av_unetI/netI', 23],
    # ['_refine_ls_number_reflns', 24],
    # ['_refine_ls_number_restraints', 24],
    # ['_refine_ls_number_parameters', 24],
    ['_refine_ls_goodness_of_fit_ref', 25],
    # ['_refine_ls_R_factor_gt', 26],
    # ['_refine_ls_wR_factor_gt', 26],
    # ['_refine_ls_R_factor_all', 27],
    # ['_refine_ls_wR_factor_ref', 27],
    # ['_refine_diff_density_max', 28],
    # ['_refine_diff_density_min', 28],
    # ['_refine_ls_abs_structure_Flack', 29]

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


def format_space_group(table: Table, cif: CifContainer) -> None:
    """
    Sets formating of the space group symbol in row 6.
    """
    space_group = cif['_space_group_name_H-M_alt'].strip("'")
    it_number = cif['_space_group_IT_number']
    paragraph = table.cell(5, 1).paragraphs[0]
    try:
        # The HM space group symbol
        s = SpaceGroups()
        spgrxml = s.iucrNumberToMathml(it_number)
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        paragraph._element.append(math_to_word(spgrxml))
        paragraph.add_run(' (' + it_number + ')')
    except Exception:
        # Use fallback:
        if space_group:
            if len(space_group) > 4:  # don't modify P 1
                space_group = re.sub(r'\s1', '', space_group)  # remove extra Hall "1" for mono and tric
            space_group = re.sub(r'\s', '', space_group)  # remove all remaining whitespace
            # space_group = re.sub(r'-1', u'\u0031\u0305', space_group)  # exchange -1 with 1bar
            space_group_formated_text = [char for char in space_group]  # ???)
            is_sub = False
            for k, char in enumerate(space_group_formated_text):
                sgrunsub = paragraph.add_run(char)
                if not char.isdigit():
                    sgrunsub.font.italic = True
                else:
                    if space_group_formated_text[k - 1].isdigit() and not is_sub:
                        is_sub = True
                        sgrunsub.font.subscript = True  # lowercase the second digit if previous is also digit
                    else:
                        is_sub = False  # only every second number as subscript for P212121 etc.
            if it_number:
                paragraph.add_run(' (' + it_number + ')')
        else:
            paragraph.add_run('?')
