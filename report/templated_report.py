import os
import subprocess
from pathlib import Path

from docx.shared import Cm
from docxtpl import DocxTemplate, RichText, R, InlineImage


def make_report():
    doc = DocxTemplate("template/template2.docx")
    context = {'company_name' : "World company",
               'table_content': [{'eins': 'foo',
                                  'zwei': 'bar',
                                  'drei': 123},

                                 {'eins': 'even',
                                  'zwei': 'more',
                                  'drei': 'content'},
                                 ],
               'bold_italic_F': RichText('F', italic=True, bold=True),
               # R is alternative for Richtext:
               'tableheader'  : R('This is a header', style='Heading_2'),
               'mytable'      : True,  # disables the table
               'an_image'     : InlineImage(doc, 'icon/finalcif2.png', width=Cm(5)),
               }
    doc.render(context)
    doc.save("generated_doc.docx")


if __name__ == '__main__':
    make_report()
    output_filename = "generated_doc.docx"
    if os.name == 'nt':
        subprocess.call(['cmd', '/C', Path(output_filename).absolute()])
    else:
        subprocess.call(['open', Path(output_filename).absolute()])
