from lxml import etree


def xml_to_html(xml_file, xslt_file):
    """
    Transforms XML to HTML using XSLT stylesheet in Python.
    """
    xml_string = '''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
    <w:r><w:t xml:space="preserve">All hydrogen atoms were refined isotropic </w:t></w:r><w:r><w:t xml:space="preserve">on calculated positions using a riding model with their </w:t></w:r><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">U</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t xml:space="preserve">iso</w:t></w:r><w:r><w:t xml:space="preserve"> values constrained to 1.5 times the </w:t></w:r><w:r><w:rPr><w:i/></w:rPr><w:t xml:space="preserve">U</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t xml:space="preserve">eq</w:t></w:r><w:r><w:t xml:space="preserve"> of their pivot atoms for terminal sp</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="superscript"/></w:rPr><w:t xml:space="preserve">3</w:t></w:r><w:r><w:t xml:space="preserve"> carbon atoms and 1.2 times for all other carbon atoms.</w:t></w:r>
    </w:document>
    '''

    with open(xslt_file, 'rb') as f:
        xslt_data = f.read()

    # Parse XML and XSLT
    xml_doc = etree.fromstring(xml_string)
    xslt_doc = etree.fromstring(xslt_data)

    transform = etree.XSLT(xslt_doc)
    result = transform(xml_doc)

    print(result)
    # Write transformed HTML to output file
    #with open(output_file, 'wb') as f:
    #    f.write(result)


# Example usage
xml_file = '/Users/daniel/Documents/GitHub/FinalCif/finalcif/template/xsl/test.xml'
xslt_file = '/Users/daniel/Documents/GitHub/FinalCif/finalcif/template/xsl/xmltohtml.xsl'
output_file = 'output.html'

if __name__ == '__main__':
    xml_to_html(xml_file, xslt_file)

    #print(f"XML transformed to HTML and saved to: {output_file}")
