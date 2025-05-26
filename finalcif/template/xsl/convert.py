from docxtpl import RichText
from lxml import etree

from finalcif.app_path import application_path


def xml_to_html(xml_string: str | RichText) -> str:
    """
    Transforms XML to HTML using XSLT.
    """
    xslt_file = application_path / 'template/xsl/xmltohtml.xsl'
    xml_string = (fr'''
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        {xml_string}
    </w:document>
    ''')

    with open(xslt_file, 'rb') as f:
        xslt_data = f.read()

    xml_doc = etree.fromstring(xml_string)
    xslt_doc = etree.fromstring(xslt_data)

    transform = etree.XSLT(xslt_doc)
    result = str(transform(xml_doc)).splitlines()
    return ''.join(result[1:-1]).strip()


def xml_to_latex(xml_string: str | RichText) -> str:
    """
    Transforms XML to HTML using XSLT.
    """
    xslt_file = application_path / 'template/xsl/xmltolatex.xsl'
    xml_string = (fr'''
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        {xml_string}
    </w:document>
    ''')

    with open(xslt_file, 'rb') as f:
        xslt_data = f.read()

    xml_doc = etree.fromstring(xml_string)
    xslt_doc = etree.fromstring(xslt_data)

    transform = etree.XSLT(xslt_doc)
    result = str(transform(xml_doc)).splitlines()
    return ''.join(result[1:-1]).strip()

if __name__ == '__main__':
    xml_string = (
        '<w:r><w:t xml:space="preserve">All hydrogen atoms were refined isotropic </w:t></w:r><w:r><w:t '
        'xml:space="preserve">on calculated positions using a riding model with their </w:t></w:r><w:r><w:rPr>'
        '<w:i/></w:rPr><w:t xml:space="preserve">U</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/>'
        '</w:rPr><w:t xml:space="preserve">iso</w:t></w:r><w:r><w:t xml:space="preserve"> values constrained to '
        '1.5 times the </w:t></w:r><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">U</w:t></w:r><w:r><w:rPr>'
        '<w:vertAlign w:val="subscript"/></w:rPr><w:t xml:space="preserve">eq</w:t></w:r><w:r><w:t '
        'xml:space="preserve"> of their pivot atoms for terminal sp</w:t></w:r><w:r><w:rPr><w:vertAlign '
        'w:val="superscript"/></w:rPr><w:t xml:space="preserve">3</w:t></w:r><w:r><w:t xml:space="preserve"> '
        'carbon atoms and 1.2 times for all other carbon atoms.</w:t></w:r>')
    #print(xml_to_html(xml_string))
    print(xml_to_latex(xml_string))
