import re
from typing import NamedTuple

from finalcif.tools import chemparse

# Element symbol, number, charge sign, whitespace or any other character.
_PART_RE = re.compile(
    r'(?P<element>[A-Z][a-z]?)|(?P<number>\d+(?:\.\d+)?)|(?P<sign>[+-])'
    r'|(?P<space>\s+)|(?P<other>.)'
)

NORMAL = 'normal'
SUBSCRIPT = 'subscript'
SUPERSCRIPT = 'superscript'


class FormulaPart(NamedTuple):
    """One display fragment of a chemical formula and how to render it."""

    text: str
    style: str


def formula_parts(formula: str) -> list[FormulaPart]:
    """Split a CIF chemical formula into parts ready for rich-text rendering.

    Element counts become subscripts and ionic charges become superscripts, so
    that an IUCr moiety formula such as ``'C9 H9 Br Cl N2 1+, B F4 1-'`` renders
    as ``C9H9BrClN2(1+), BF4(1-)`` with the counts lowered and the charges
    raised.  Whitespace is used to tell a charge from a count but is not part of
    the output; a comma is followed by a single space.

    Examples::

        >>> formula_parts('H2 O')
        [FormulaPart(text='H', style='normal'), FormulaPart(text='2', style='subscript'), \
FormulaPart(text='O', style='normal')]
        >>> [p.style for p in formula_parts('B F4 1-')][-1]
        'superscript'
    """
    matches = list(_PART_RE.finditer(formula))
    parts: list[FormulaPart] = []
    previous_is_element = False
    index = 0
    while index < len(matches):
        match = matches[index]
        kind = match.lastgroup
        text = match.group()
        index += 1
        if kind == 'space':
            previous_is_element = False
            continue
        if kind == 'element':
            parts.append(FormulaPart(text, NORMAL))
            previous_is_element = True
            continue
        if kind == 'number':
            sign_index = _next_sign(matches, index)
            if sign_index is not None:
                parts.append(FormulaPart(text + matches[sign_index].group(), SUPERSCRIPT))
                index = sign_index + 1
            elif previous_is_element:
                parts.append(FormulaPart(text, SUBSCRIPT))
            else:
                # A pre-multiplier written without parentheses ('2 B F4') needs the
                # space kept, otherwise it reads as part of the element count.
                separator = ' ' if _next_is_element(matches, index) else ''
                parts.append(FormulaPart(text + separator, NORMAL))
            previous_is_element = False
            continue
        if kind == 'sign':
            parts.append(FormulaPart(text, SUPERSCRIPT))
            previous_is_element = False
            continue
        parts.append(FormulaPart(f'{text} ' if text == ',' else text, NORMAL))
        previous_is_element = False
    return parts


def _next_is_element(matches: list, index: int) -> bool:
    """Return ``True`` when the next non-space token is an element symbol."""
    while index < len(matches) and matches[index].lastgroup == 'space':
        index += 1
    return index < len(matches) and matches[index].lastgroup == 'element'


def _next_sign(matches: list, index: int) -> int | None:
    """Return the index of a charge sign directly following *index*, or ``None``.

    Only whitespace may separate the number from its sign, and the sign must end
    the moiety (i.e. be followed by whitespace, a comma, a bracket or the end).
    """
    while index < len(matches) and matches[index].lastgroup == 'space':
        index += 1
    if index >= len(matches) or matches[index].lastgroup != 'sign':
        return None
    following = matches[index + 1] if index + 1 < len(matches) else None
    if following is None or following.lastgroup in ('space', 'other'):
        return index
    return None


def formula_to_html(formula: str) -> str:
    """Render a CIF chemical formula string as HTML with sub- and superscripts.

    Unlike :func:`sum_formula_to_html` this keeps the structure of the string,
    so a moiety formula such as ``'C9 H9 Br Cl N2 1+, B F4 1-'`` survives with
    its moiety separators, multipliers and charges intact.  Returns an empty
    string for missing values (``''``, ``'?'``, ``'.'``).
    """
    text = formula.strip(" '\"")
    if not text or text in {'?', '.'}:
        return ''
    pieces: list[str] = []
    for part, style in formula_parts(text):
        if style == SUBSCRIPT:
            pieces.append(f'<sub>{part}</sub>')
        elif style == SUPERSCRIPT:
            pieces.append(f'<sup>{part}</sup>')
        else:
            pieces.append(part)
    return f'<html><body>{"".join(pieces)}</body></html>'


def formula_str_to_dict(sumform: str) -> dict[str, float]:
    chemical_formula = chemparse.parse_formula(sumform.replace(" ", ""))
    return chemical_formula


def sum_formula_to_html(sumform: dict[str, float | int], break_after: int = 99) -> str:
    """
    Makes html formatted sum formula from a dictionary.
    """
    if not sumform:
        return ''
    formula_list = ['<html><body>']
    num = 0
    for el, count in sumform.items():
        if count == 0 or count is None:
            continue
        try:
            times = round(float(count), 1)
        except (TypeError, ValueError):
            times = 1
        if num > 3 and num % break_after == 0:
            formula_list.append("<br>")
        if times == 1:
            formula_list.append(f'{el}')
        else:
            formula_list.append(f"{el}<sub>{times:g}</sub>")
        num += 1
    formula_list.append('</body></html>')
    formula = "".join(formula_list)
    return formula
