#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import textwrap
from html import unescape

import gemmi


def quote(string: str, wrapping=80) -> str:
    """
    Quotes a cif string and wraps it. The shorter strings are directly handled by cif.quote().
    """
    if len(string) < 80:
        return gemmi.cif.quote(string)
    lines = ''
    for line in string.split('\n'):
        if len(line) > wrapping:
            line = textwrap.fill(line, width=wrapping, drop_whitespace=False)
        lines += f'{line}\n'
    quoted = gemmi.cif.quote(lines.rstrip('\n'))
    return quoted


characters = {
    '—'      : r'--',
    '±'      : r'+-',
    '×'      : r'\\times',
    '≠'      : r'\\neq',
    '→'      : r'\\rightarrow',
    '←'      : r'\\leftarrow',
    '∞'      : r'\\infty',
    '≃'      : r'\\simeq',
    '≈'      : r'\\sim',
    'ß'      : r'\&s',
    'ü'      : r'\"u',
    'Ü'      : r'\"U',
    'ö'      : r'\"o',  # 'LATIN SMALL LETTER O WITH DIAERESIS'
    'Ö'      : r'\"O',
    'ä'      : r'\"a',
    'Ä'      : r'\"A',
    'é'      : r"\'e",
    'É'      : r"\'E",
    'è'      : r'\`e',
    'È'      : r'\`E',
    'ì'      : r'\`i',
    'Ì'      : r'\`I',
    'í'      : r'\'i',
    'Í'      : r'\'I',
    'ó'      : r"\'o",
    'Ó'      : r"\'O",
    'ò'      : r'\`o',
    'Ò'      : r'\`O',
    'ȯ'      : r'\.o',
    'ø'      : r'\/o',
    'á'      : r'\'a',
    'Á'      : r'\'A',
    'à'      : r'\`a',
    'À'      : r'\`A',
    'â'      : r'\^a',
    'Â'      : r'\^A',
    'å'      : r'\%a',
    'ê'      : r'\^e',
    'î'      : r'\^i',
    'Î'      : r'\^I',
    'ô'      : r'\^o',
    'Ô'      : r'\^O',
    'û'      : r'\^u',
    'Û'      : r'\^U',
    'ç'      : r'\,c',
    'ñ'      : r'\~n',
    'ł'      : r'\/l',
    'đ'      : r'\/d',
    'Å'      : r'\%A',  # 'LATIN CAPITAL LETTER A WITH RING ABOVE'
    'Å'      : r'\%A',  # unicodedata.name('Å'): 'ANGSTROM SIGN'
    u'\u2079': r'^9^',
    u'\u2078': r'^8^',
    u'\u2077': r'^7^',
    u'\u2076': r'^6^',
    u'\u2075': r'^5^',
    u'\u2074': r'^4^',
    u'\u00B3': r'^3^',
    u'\u00B2': r'^2^',
    u'\u2081': r'~1~',
    u'\u2082': r'~2~',
    u'\u2083': r'~3~',
    u'\u2084': r'~4~',
    u'\u2085': r'~5~',
    u'\u2086': r'~6~',
    u'\u2087': r'~7~',
    u'\u2088': r'~8~',
    u'\u2089': r'~9~',
    u'\u1D62': r'~i~',
    u'\u1D63': r'~r~',
    u'\u1D64': r'~u~',
    u'\u1D65': r'~v~',
    u'\u208A': r'~+~',
    u'\u208B': r'~-~',
    u'\u2090': r'~a~',
    u'\u2091': r'~e~',
    u'\u2095': r'~h~',
    u'\u2096': r'~k~',
    u'\u2097': r'~l~',
    u'\u2098': r'~m~',
    u'\u2099': r'~n~',
    u'\u209A': r'~p~',
    u'\u209B': r'~s~',
    u'\u209C': r'~t~',
    u'\u2C7C': r'~j~',
    u'\u00BC': r'^1/4^',
    u'\u00BD': r'^1/2^',
    u'\u00BE': r'^3/4^',
    u'\u2153': r'^1/3^',
    u'\u2155': r'^1/5^',
    u'\u2154': r'^2/3^',
    u'\u2156': r'^2/5^',
    u'\u2157': r'^3/5^',
    u'\u2158': r'^4/5^',
    u'\u2159': r'^1/6^',
    u'\u215A': r'^5/6^',
    u'\u0131': r'\?i',
    u"\u03B1": r'\a',  # alpha
    u"\u03B2": r'\b',  # beta
    u"\u03B3": r'\g',  # ...
    u"\u03B4": r'\d',
    u"\u03B5": r'\e',
    u"\u03B6": r'\z',
    u"\u03B7": r'\h',
    u"\u03B8": r'\q',
    u"\u03B9": r'\i',
    u"\u03BA": r'\k',
    u"\u03BB": r'\l',
    u"\u03BC": r'\m',
    u"\u03BD": r'\n',
    u"\u03BE": r'\x',
    u"\u03BF": r'\o',
    u"\u03C0": r'\p',
    u"\u03C1": r'\r',
    u"\u03C3": r'\s',
    u"\u03C4": r'\t',
    u"\u03C5": r'\u',
    u"\u03C6": r'\F',
    u"\u03C9": r'\w',
    u"\u03A9": r'\W',
    u"\u03D5": r'\f',
    u"\u00B0": r"\%",
    '·'      : r"{middle dot}",
    # "1̄": r'\=1',  # Does not work in QT?
}

false_characters_map = {
    # Fix for wrong characters in FinalCif prior to version 96:
    # Removing it from 110, because there are no v96 users left.
    'ü': r'u\"',
    'Ü': r'U\"',
    'ö': r'o\"',
    'Ö': r'O\"',
    'ä': r'a\"',
    'Ä': r'A\"',
}


def invert_dict(input: dict) -> dict:
    return {v: k for k, v in input.items()}


inverted_characters_map = invert_dict(characters)

# Removed, because it became obsolete
# inverted_characters_map.update(invert_dict(false_characters_map))


def utf8_to_str(txt: str) -> str:
    """
    Translates an utf-8 text to a CIF ascii string.
    """
    for char in txt:
        if char in characters:
            txt = txt.replace(char, characters[char])
    return utf8_to_html_ascii(txt)


def delimit_string(txt: str) -> str:
    return utf8_to_str(txt)


def string_to_utf8(txt: str) -> str:
    return retranslate_delimiter(txt)


def retranslate_delimiter(txt: str, no_html_unescape: bool = False) -> str:
    """
    Translates delimited cif characters back to unicode characters.
    """
    for char in inverted_characters_map.keys():
        txt = txt.replace(char, inverted_characters_map[char])
    if no_html_unescape:
        return txt
    else:
        return html_ascii_to_utf8(txt)


def utf8_to_html_ascii(text: str) -> str:
    return text.encode('ascii', 'xmlcharrefreplace').decode()


def html_ascii_to_utf8(text: str) -> str:
    return unescape(text)
