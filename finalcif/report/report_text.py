import os

import gemmi
from docx.oxml.xmlchemy import BaseOxmlElement
from lxml import etree
from lxml.etree import XSLTAccessControl

from finalcif.app_path import application_path
from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.text import retranslate_delimiter, string_to_utf8
from finalcif.tools.misc import angstrom, remove_line_endings


def math_to_word(eq: str) -> BaseOxmlElement:
    """Transform a sympy equation to be printed in word document."""
    tree = etree.fromstring(eq)
    xslt = etree.parse(os.path.join(application_path, 'template/mathml2omml.xsl'))
    acess_control = XSLTAccessControl(read_network=False, write_network=False)
    transform = etree.XSLT(xslt, access_control=acess_control)
    new_dom = transform(tree)
    return new_dom.getroot()


def clean_string(string: str) -> str:
    """
    Removes control characters from a string.
    """
    repl = string.replace('\t', ' ') \
        .replace('\f', ' ') \
        .replace('\0', ' ') \
        .strip(' ') \
        .strip('.')
    return remove_line_endings(repl)


def gstr(string: str) -> str:
    """
    Turn a string into a gemmi string and remove control characters.
    """
    return clean_string(gemmi.cif.as_string(string))


def _get_cooling_device(cif: CifContainer) -> str:
    olx = gstr(cif['_olex2_diffrn_ambient_temperature_device'])
    iucr = gstr(cif['_diffrn_measurement_ambient_temperature_device_make'])
    if olx and iucr:
        return iucr
    if olx:
        return olx
    elif iucr:
        return iucr
    else:
        return ''


def get_inf_article(next_word: str) -> str:
    if not next_word:
        return 'a'
    voc = 'aeiou'
    return 'an' if next_word[0].lower() in voc else 'a'


def get_distance_unit(picometers: bool) -> str:
    if picometers:
        return 'pm'
    else:
        return angstrom


def get_volume_unit(picometers: bool) -> str:
    if picometers:
        return 'nm'
    else:
        return angstrom


def format_float_with_decimal_places(number: float, places=2) -> str:
    try:
        fnum = float(number)
        return f'{fnum:.{places}f}'
    except ValueError:
        return f'{number}'


def utf8(text: str) -> str:
    """A Jinja2 filter for CIF to utf8"""
    return string_to_utf8(text)


def format_radiation(radiation_type: str) -> list:
    radtype = list(radiation_type.partition("K"))
    if len(radtype) > 2:
        radtype[2] = retranslate_delimiter(radtype[2])
        return radtype
    else:
        return radtype
