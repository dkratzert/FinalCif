#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import re
import textwrap
from html import unescape

import gemmi

from finalcif.template.unicode2latex.u2l import uni2tex


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
    '—'     : r'--',
    '±'     : r'+-',
    '×'     : r'\\times',  # noqa: RUF001
    '≠'     : r'\\neq',
    '→'     : r'\\rightarrow',
    '←'     : r'\\leftarrow',
    '∞'     : r'\\infty',
    '≃'     : r'\\simeq',
    '≈'     : r'\\sim',
    'ß'     : r'\&s',
    'ü'     : r'\"u',
    'Ü'     : r'\"U',
    'ö'     : r'\"o',  # 'LATIN SMALL LETTER O WITH DIAERESIS'
    'Ö'     : r'\"O',
    'ä'     : r'\"a',
    'Ä'     : r'\"A',
    'é'     : r"\'e",
    'É'     : r"\'E",
    'è'     : r'\`e',
    'È'     : r'\`E',
    'ì'     : r'\`i',
    'Ì'     : r'\`I',
    'í'     : r'\'i',
    'Í'     : r'\'I',
    'ó'     : r"\'o",
    'Ó'     : r"\'O",
    'ò'     : r'\`o',
    'Ò'     : r'\`O',
    'ȯ'     : r'\.o',
    'ø'     : r'\/o',
    'á'     : r'\'a',
    'Á'     : r'\'A',
    'à'     : r'\`a',
    'À'     : r'\`A',
    'â'     : r'\^a',
    'Â'     : r'\^A',
    'å'     : r'\%a',
    'ê'     : r'\^e',
    'î'     : r'\^i',
    'Î'     : r'\^I',
    'ô'     : r'\^o',
    'Ô'     : r'\^O',
    'û'     : r'\^u',
    'Û'     : r'\^U',
    'ç'     : r'\,c',
    'ñ'     : r'\~n',
    'ł'     : r'\/l',
    'đ'     : r'\/d',
    'Å'     : r'\%A',  # 'LATIN CAPITAL LETTER A WITH RING ABOVE'
    'Å'     : r'\%A',  # unicodedata.name('Å'): 'ANGSTROM SIGN'
    '\u2079': r'^9^',
    '\u2078': r'^8^',
    '\u2077': r'^7^',
    '\u2076': r'^6^',
    '\u2075': r'^5^',
    '\u2074': r'^4^',
    '\u00B3': r'^3^',
    '\u00B2': r'^2^',
    '\u2081': r'~1~',
    '\u2082': r'~2~',
    '\u2083': r'~3~',
    '\u2084': r'~4~',
    '\u2085': r'~5~',
    '\u2086': r'~6~',
    '\u2087': r'~7~',
    '\u2088': r'~8~',
    '\u2089': r'~9~',
    '\u1D62': r'~i~',
    '\u1D63': r'~r~',
    '\u1D64': r'~u~',
    '\u1D65': r'~v~',
    '\u208A': r'~+~',
    '\u208B': r'~-~',
    '\u2090': r'~a~',
    '\u2091': r'~e~',
    '\u2095': r'~h~',
    '\u2096': r'~k~',
    '\u2097': r'~l~',
    '\u2098': r'~m~',
    '\u2099': r'~n~',
    '\u209A': r'~p~',
    '\u209B': r'~s~',
    '\u209C': r'~t~',
    '\u2C7C': r'~j~',
    '\u00BC': r'^1/4^',
    '\u00BD': r'^1/2^',
    '\u00BE': r'^3/4^',
    '\u2153': r'^1/3^',
    '\u2155': r'^1/5^',
    '\u2154': r'^2/3^',
    '\u2156': r'^2/5^',
    '\u2157': r'^3/5^',
    '\u2158': r'^4/5^',
    '\u2159': r'^1/6^',
    '\u215A': r'^5/6^',
    '\u0131': r'\?i',
    "\u03B1": r'\a',  # alpha
    "\u03B2": r'\b',  # beta
    "\u03B3": r'\g',  # ...
    "\u03B4": r'\d',
    "\u03B5": r'\e',
    "\u03B6": r'\z',
    "\u03B7": r'\h',
    "\u03B8": r'\q',
    "\u03B9": r'\i',
    "\u03BA": r'\k',
    "\u03BB": r'\l',
    "\u03BC": r'\m',
    "\u03BD": r'\n',
    "\u03BE": r'\x',
    "\u03BF": r'\o',
    "\u03C0": r'\p',
    "\u03C1": r'\r',
    "\u03C3": r'\s',
    "\u03C4": r'\t',
    "\u03C5": r'\u',
    "\u03C6": r'\F',
    "\u03C9": r'\w',
    "\u03A9": r'\W',
    "\u03D5": r'\f',
    "\u00B0": r"\%",
    '·'     : r"{middle dot}",
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


def invert_dict(inp: dict) -> dict:
    return {v: k for k, v in inp.items()}


inverted_characters_map = invert_dict(characters)

# Compiled regex that matches any CIF delimiter sequence in a single pass.
# Patterns are sorted longest-first so that e.g. '\\times' is tried before '\t'.
_delimiter_pattern = re.compile(
    '|'.join(re.escape(k) for k in sorted(inverted_characters_map, key=len, reverse=True))
)

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


def string_to_latex(cif_string: str) -> str:
    utf8_string = string_to_utf8(cif_string)
    return uni2tex(utf8_string, add_font_modifiers=False, prefer_unicode_math=False, convert_accents=True)


def utf8_to_latex(utf8_string: str) -> str:
    return uni2tex(utf8_string, add_font_modifiers=False, prefer_unicode_math=False, convert_accents=True)


def retranslate_delimiter(txt: str, no_html_unescape: bool = False) -> str:
    """
    Translates delimited cif characters back to Unicode characters.

    Uses a single compiled regex pass instead of 121 sequential str.replace
    calls, which is significantly faster for long strings (e.g. HKL files).
    """
    txt = _delimiter_pattern.sub(lambda m: inverted_characters_map[m.group()], txt)
    if no_html_unescape:
        return txt
    else:
        return html_ascii_to_utf8(txt)


def utf8_to_html_ascii(text: str) -> str:
    return text.encode('ascii', 'xmlcharrefreplace').decode()


def html_ascii_to_utf8(text: str) -> str:
    return unescape(text)


def escape_for_latex(text: str) -> str:
    """
    Escapes special characters in text so that it can be safely used in LaTeX.
    """
    latex_special_chars = {
        '\\': r'\textbackslash{}',
        '{' : r'\{',
        '}' : r'\}',
        '$' : r'\$',
        '&' : r'\&',
        '#' : r'\#',
        '_' : r'\_',
        '%' : r'\%',
        '~' : r'\textasciitilde{}',
        '^' : r'\textasciicircum{}',
        '[' : r'\[',
        ']' : r'\]',
    }
    regex = re.compile('|'.join(re.escape(key) for key in latex_special_chars))
    escaped_text = regex.sub(lambda match: latex_special_chars[match.group()], text)
    return string_to_latex(escaped_text)
