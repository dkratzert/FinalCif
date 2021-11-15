from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.text.paragraph import Paragraph

from finalcif.report.report_text import math_to_word
from finalcif.tools.space_groups import SpaceGroups

cif_keywords_list = (
    ['_chemical_formula_weight', 1],
    ['_diffrn_ambient_temperature', 2],
    ['_space_group_crystal_system', 3],
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
    ['_exptl_crystal_colour', 17],
    ['_exptl_crystal_description', 18],
    ['_diffrn_reflns_theta_min', 20],
    ['_diffrn_reflns_theta_max', 20],
    ['_diffrn_reflns_number', 22],
    ['_refine_ls_goodness_of_fit_ref', 25],
)


def format_space_group(paragraph: Paragraph, space_group: str, it_number: str) -> None:
    """
    Sets formatting of the space group symbol in row 6 of the report table.
    """
    try:
        # The HM space group type
        s = SpaceGroups()
        spgrxml = s.to_mathml(space_group)
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
        paragraph._element.append(math_to_word(spgrxml))
        paragraph.add_run(' (' + it_number + ')')
    except Exception:
        paragraph.add_run(space_group)
