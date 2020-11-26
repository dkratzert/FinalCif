import itertools
import os
import subprocess
from pathlib import Path

from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Cm
from docx.text.paragraph import Paragraph
from docxtpl import DocxTemplate, RichText, InlineImage, Subdoc

from cif.cif_file_io import CifContainer
from cif.text import retranslate_delimiter
from report.report_text import math_to_word, gstr
from report.spgrps import SpaceGroups
from tests.helpers import remove_line_endings
from tools.misc import isnumeric, this_or_quest, timessym


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


def make_report(cif: CifContainer):
    tpl_doc = DocxTemplate("./template/template_text.docx")
    space_group_subdocument = space_group(tpl_doc, cif)
    context = {'options'               : {'report_text': True, 'atoms_table': True, 'without_h': False},
               'cif'                   : cif,
               'space_group'           : space_group_subdocument,
               'bold_italic_F'         : RichText('F', italic=True, bold=True),
               'crystal_table_header'  : RichText('Crystal data and structure refinement for {}'
                                                  .format(cif.block.name), style='Heading_2'),
               'data_name_header'      : RichText('{}'.format(cif.block.name), style='Heading_2'),
               'structure_figure'      : InlineImage(tpl_doc,
                                                     r'D:\frames\guest\DK_IK_Cy5_PF6\DK_IK_Cy5_PF6\mo_DK_IK_Cy5_PF6_0m_a-finalcif.gif',
                                                     width=Cm(7.5)),
               'crystallization_method': remove_line_endings(
                   retranslate_delimiter(cif['_exptl_crystal_recrystallization_method']))
                                         or '[No crystallization method given!]',
               'atomic_coordinates'    : cif.atoms(without_h=False),
               'sum_formula'           : format_sum_formula(cif['_chemical_formula_sum'].replace(" ", "")),
               'itnum'                 : cif['_space_group_IT_number'],
               'crystal_size'          : this_or_quest(cif['_exptl_crystal_size_min']) + timessym +
                                         this_or_quest(cif['_exptl_crystal_size_mid']) + timessym +
                                         this_or_quest(cif['_exptl_crystal_size_max']),
               'diffr_type'            : gstr(
                   cif['_diffrn_measurement_device_type']) or '[No measurement device type given]'
               }
    tpl_doc.render(context, autoescape=True)
    tpl_doc.save("generated_doc.docx")


def space_group(tpl_doc: DocxTemplate, cif: CifContainer) -> Subdoc:
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


if __name__ == '__main__':
    cif = CifContainer(Path(r'D:\frames\guest\DK_IK_Cy5_PF6\DK_IK_Cy5_PF6\mo_DK_IK_Cy5_PF6_0m_a-finalcif.cif'))
    make_report(cif)
    output_filename = "generated_doc.docx"
    if os.name == 'nt':
        subprocess.call(['cmd', '/C', Path(output_filename).absolute()])
    else:
        subprocess.call(['open', Path(output_filename).absolute()])
