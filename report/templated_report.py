import os
import subprocess
from pathlib import Path

from docx.oxml.ns import qn
from docx.shared import Cm
from docxtpl import DocxTemplate, RichText, InlineImage

from cif.cif_file_io import CifContainer
from report.report_text import math_to_word
from report.spgrps import SpaceGroups

"""
TODO: Use two different templates for report with and without text.
"""

def make_columns_section(document, columns: str = '1'):
    """
    Makes a new section (new page) which has a certain number of columns.
    available sections:
    CONTINUOUS, NEW_COLUMN, NEW_PAGE, EVEN_PAGE, ODD_PAGE
    """
    # noinspection PyUnresolvedReferences
    from docx.enum.section import WD_SECTION
    section = document.add_section(WD_SECTION.CONTINUOUS)
    sectPr = section._sectPr
    cols = sectPr.xpath('./w:cols')[0]
    cols.set(qn('w:num'), '{}'.format(columns))
    return ''


def make_report(cif: CifContainer):
    doc = DocxTemplate("./template/template3.docx")
    s = SpaceGroups()
    spgrxml = s.iucrNumberToMathml(cif['_space_group_IT_number'])
    context = {'options'             : {'report_text': True},
               'cif'                 : cif,
               'twocolumns'          : make_columns_section(document=doc, columns='2'),
               'onecolumn'           : make_columns_section(document=doc, columns='2'),
               'space_group'         : math_to_word(spgrxml),
               'bold_italic_F'       : RichText('F', italic=True, bold=True),
               'crystal_table_header': RichText('Crystal data and structure refinement for {}'.format(cif.block.name),
                                                style='Heading_2'),
               'structure_figure'    : InlineImage(doc, './test-data/P21c-final-finalcif.gif', width=Cm(8)),
               }
    doc.render(context, autoescape=True)
    doc.save("generated_doc.docx")


if __name__ == '__main__':
    cif = CifContainer(Path('./test-data/p21c.cif'))
    make_report(cif)
    output_filename = "generated_doc.docx"
    if os.name == 'nt':
        subprocess.call(['cmd', '/C', Path(output_filename).absolute()])
    else:
        subprocess.call(['open', Path(output_filename).absolute()])
