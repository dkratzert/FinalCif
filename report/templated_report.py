import itertools
import os
import subprocess
from math import sin, radians
from pathlib import Path

import jinja2
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Cm
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate, RichText, InlineImage, Subdoc

from cif.cif_file_io import CifContainer
from cif.text import retranslate_delimiter
from report.report_text import math_to_word, gstr, format_radiation, get_inf_article
from report.spgrps import SpaceGroups
from tests.helpers import remove_line_endings
from tools.misc import isnumeric, this_or_quest, timessym, angstrom, protected_space, less_or_equal


def format_sum_formula(sum_formula: str) -> RichText:
    sum_formula_group = [''.join(x[1]) for x in itertools.groupby(sum_formula, lambda x: x.isalpha())]
    richtext = RichText('')
    if sum_formula_group:
        for _, word in enumerate(sum_formula_group):
            if isnumeric(word):
                richtext.add(word, subscript=True)
            else:
                richtext.add(word)
        return richtext
    else:
        return RichText('No sum formula')


def space_group_subdoc(tpl_doc: DocxTemplate, cif: CifContainer) -> Subdoc:
    """
    Generates a Subdoc subdocument with the xml code for a math element in MSWord.
    """
    s = SpaceGroups()
    spgrxml = s.iucrNumberToMathml(cif['_space_group_IT_number'])
    spgr_word = math_to_word(spgrxml)
    # I have to create a subdocument in order to add the xml:
    sd = tpl_doc.new_subdoc()
    p: Paragraph = sd.add_paragraph()
    p.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    p._element.append(spgr_word)
    p.add_run(' ({})'.format(cif['_space_group_IT_number']))
    return sd


def get_from_to_theta_range() -> str:
    theta_min = cif['_diffrn_reflns_theta_min']
    theta_max = cif['_diffrn_reflns_theta_max']
    radiation_wavelength = cif['_diffrn_radiation_wavelength']
    try:
        d_max = ' ({:.2f}{}{})'.format(float(radiation_wavelength) / (2 * sin(radians(float(theta_max)))),
                                       protected_space,
                                       angstrom)
        # 2theta range:
        return "{:.2f} to {:.2f}{}".format(2 * float(theta_min), 2 * float(theta_max), d_max)
    except ValueError:
        return '? to ?'


def hkl_index_limits() -> str:
    limit_h_min = cif['_diffrn_reflns_limit_h_min']
    limit_h_max = cif['_diffrn_reflns_limit_h_max']
    limit_k_min = cif['_diffrn_reflns_limit_k_min']
    limit_k_max = cif['_diffrn_reflns_limit_k_max']
    limit_l_min = cif['_diffrn_reflns_limit_l_min']
    limit_l_max = cif['_diffrn_reflns_limit_l_max']
    return limit_h_min + ' {} h {} '.format(less_or_equal, less_or_equal) + limit_h_max + '\n' \
           + limit_k_min + ' {} k {} '.format(less_or_equal, less_or_equal) + limit_k_max + '\n' \
           + limit_l_min + ' {} l {} '.format(less_or_equal, less_or_equal) + limit_l_max


def get_radiation(cif):
    rad_element, radtype, radline = format_radiation(cif['_diffrn_radiation_type'])
    radiation = RichText(rad_element)
    radiation.add(radtype, italic=True)
    radiation.add(radline, italic=True, subscript=True)
    return radiation


def get_completeness(cif: CifContainer):
    try:
        completeness = "{0:.1f} %".format(round(float(cif['_diffrn_measured_fraction_theta_full']) * 100, 1))
    except ValueError:
        completeness = '?'
    return completeness


def get_diff_density_min():
    try:
        diff_density_min = "{0:.2f}".format(round(float(cif['_refine_diff_density_min']), 2))
    except ValueError:
        diff_density_min = '?'
    return diff_density_min


def get_diff_density_max():
    try:
        diff_density_max = "{0:.2f}".format(round(float(cif['_refine_diff_density_max']), 2))
    except ValueError:
        diff_density_max = '?'
    return diff_density_max


def get_exti():
    exti = cif['_refine_ls_extinction_coef']
    if exti not in ['.', "'.'", '?', '']:
        return exti
    else:
        return ''


def make_report(cif: CifContainer, options: 'Options' = None):
    tpl_doc = DocxTemplate("./template/template_text.docx")
    context = {'options'               : options,
               'cif'                   : cif,
               'space_group'           : space_group_subdoc(tpl_doc, cif),
               'bold_italic_F'         : RichText('F', italic=True, bold=True),
               'crystal_table_header'  : RichText('Crystal data and structure refinement for {}'
                                                  .format(cif.block.name), style='Heading_2'),
               'data_name_header'      : RichText('{}'.format(cif.block.name), style='Heading_2'),
               'structure_figure'      : InlineImage(tpl_doc,
                                                     r'D:\frames\guest\DK_IK_Cy5_PF6\DK_IK_Cy5_PF6\mo_DK_IK_Cy5_PF6_0m_a-finalcif.gif',
                                                     width=Cm(7.5)),
               'crystallization_method': remove_line_endings(retranslate_delimiter(
                   cif['_exptl_crystal_recrystallization_method'])) or '[No crystallization method given!]',
               'atomic_coordinates'    : cif.atoms(without_h=False),
               'sum_formula'           : format_sum_formula(cif['_chemical_formula_sum'].replace(" ", "")),
               'itnum'                 : cif['_space_group_IT_number'],
               'crystal_size'          : this_or_quest(cif['_exptl_crystal_size_min']) + timessym +
                                         this_or_quest(cif['_exptl_crystal_size_mid']) + timessym +
                                         this_or_quest(cif['_exptl_crystal_size_max']),
               'radiation'             : get_radiation(cif),
               'wavelength'            : cif['_diffrn_radiation_wavelength'],
               'theta_range'           : get_from_to_theta_range(),
               'diffr_type'            : gstr(cif['_diffrn_measurement_device_type'])
                                         or '[No measurement device type given]',
               'diffr_device'          : gstr(cif['_diffrn_measurement_device'])
                                         or '[No measurement device given]',
               'diffr_source'          : gstr(cif['_diffrn_source']).strip('\n\r')
                                         or '[No radiation source given]',
               'monochromator'         : gstr(cif['_diffrn_radiation_monochromator']) \
                                         or '[No monochromator type given]',
               'detector'              : gstr(cif['_diffrn_detector_type']) \
                                         or '[No detector type given]',
               'lowtemp_dev'           : gstr(cif['_olex2_diffrn_ambient_temperature_device']) \
                                         or '',
               'index_ranges'          : hkl_index_limits(),
               'indepentent_refl'      : this_or_quest(cif['_reflns_number_total']),
               'r_int'                 : this_or_quest(cif['_diffrn_reflns_av_R_equivalents']),
               'r_sigma'               : this_or_quest(cif['_diffrn_reflns_av_unetI/netI']),
               'completeness'          : get_completeness(cif),
               'theta_full'            : cif['_diffrn_reflns_theta_full'],
               'data'                  : this_or_quest(cif['_refine_ls_number_reflns']),
               'restraints'            : this_or_quest(cif['_refine_ls_number_restraints']),
               'parameters'            : this_or_quest(cif['_refine_ls_number_parameters']),
               'goof'                  : this_or_quest(cif['_refine_ls_goodness_of_fit_ref']),
               'ls_R_factor_gt'        : this_or_quest(cif['_refine_ls_R_factor_gt']),
               'ls_wR_factor_gt'       : this_or_quest(cif['_refine_ls_wR_factor_gt']),
               'ls_R_factor_all'       : this_or_quest(cif['_refine_ls_R_factor_all']),
               'ls_wR_factor_ref'      : this_or_quest(cif['_refine_ls_wR_factor_ref']),
               'diff_dens_min'         : get_diff_density_min(),
               'diff_dens_max'         : get_diff_density_max(),
               'exti'                  : get_exti(),
               }
    # Filter definition for {{foobar|filter}} things:
    jinja_env = jinja2.Environment()
    jinja_env.filters['inv_article'] = get_inf_article
    tpl_doc.render(context, jinja_env=jinja_env, autoescape=True)
    tpl_doc.save("generated_doc.docx")


if __name__ == '__main__':
    cif = CifContainer(Path(r'D:\frames\guest\DK_IK_Cy5_PF6\DK_IK_Cy5_PF6\mo_DK_IK_Cy5_PF6_0m_a-finalcif.cif'))
    make_report(cif)
    output_filename = "generated_doc.docx"
    if os.name == 'nt':
        subprocess.call(['cmd', '/C', Path(output_filename).absolute()])
    else:
        subprocess.call(['open', Path(output_filename).absolute()])
