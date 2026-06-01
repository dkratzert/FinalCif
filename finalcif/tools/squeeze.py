#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   Dr. Daniel Kratzert
#   ----------------------------------------------------------------------------
"""
Helper utilities for handling PLATON SQUEEZE structures.
"""
from __future__ import annotations

import re
from typing import Literal

from finalcif.tools.chemparse import parse_formula, ChemparseError

# Atomic numbers (= electron count for neutral atoms) for elements common in crystallography.
ATOMIC_NUMBERS: dict[str, int] = {
    'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
    'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18,
    'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26,
    'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34,
    'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42,
    'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50,
    'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58,
    'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66,
    'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74,
    'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81, 'Pb': 82,
    'Bi': 83, 'Th': 90, 'U': 92,
}


def _normalize_squeeze_formula(formula_str: str) -> str:
    """
    Convert leading-multiplier notation to trailing-multiplier notation so
    that ``chemparse.parse_formula`` can handle it.

    SQUEEZE content strings use the crystallographic convention where the
    multiplier precedes the parenthesised group, e.g. ``2(H2O)``.
    ``chemparse`` expects the multiplier to follow the closing parenthesis,
    i.e. ``(H2O)2``.

    Olex2/SMTBX void content strings may also use a space-separated format
    where the multiplier precedes the formula without parentheses, e.g.
    ``1 PF6-`` or ``2 H2O``.

    This function handles both notations:

    * ``N(fragment)`` → ``(fragment)N``
    * ``N fragment``  → ``(fragment)N``  (space-separated, no parentheses)

    Charge indicators (trailing ``+`` or ``-``) are harmless because they are
    treated as unknown elements contributing 0 electrons.

    Args:
        formula_str: Raw formula such as ``'2(H2O)'``, ``'C4H8O'``, or ``'1 PF6-'``.

    Returns:
        Normalised formula string accepted by ``chemparse.parse_formula``.
    """
    formula_str = formula_str.strip()

    # Handle space-separated leading multiplier without parentheses: "2 H2O" → "(H2O)2"
    m = re.match(r'^(\d+(?:\.\d+)?)\s+(.+)$', formula_str)
    if m:
        multiplier, fragment = m.group(1), m.group(2)
        formula_str = f'({fragment}){multiplier}'

    # Handle leading multiplier directly before an element symbol: "2C6H5CH(CH3)2" → "(C6H5CH(CH3)2)2"
    if not m:
        m2 = re.match(r'^(\d+(?:\.\d+)?)([A-Z].*)$', formula_str)
        if m2:
            multiplier, fragment = m2.group(1), m2.group(2)
            formula_str = f'({fragment}){multiplier}'

    # Handle leading multiplier directly before parentheses: "2(H2O)" → "(H2O)2"
    def _swap(match: re.Match) -> str:
        return f'{match.group(1)}({match.group(3)}){match.group(2)}'

    formula_str = re.sub(r'(^|(?<=\s))(\d+(?:\.\d+)?)\(([^()]*)\)', _swap, formula_str)

    # Remove remaining spaces — chemparse requires concatenated symbols (e.g. "Os S O F" → "OsSOF")
    return formula_str.replace(' ', '')


def electrons_from_formula(formula_str: str) -> int:
    """
    Returns the total electron count for a chemical formula string.

    Supports standard crystallographic formulae such as 'C4H8O', '2(H2O)', 'CHCl3'.
    Unknown elements contribute 0 electrons.  Returns 0 for empty / placeholder strings.

    Args:
        formula_str: Chemical formula, e.g. '2(C4H8O)' or 'H2O'.

    Returns:
        Integer electron count, or 0 when the formula cannot be parsed.
    """
    if not formula_str or formula_str.strip() in ('?', '.', ''):
        return 0
    try:
        normalised = _normalize_squeeze_formula(formula_str.strip())
        atom_dict = parse_formula(normalised)
        return round(sum(ATOMIC_NUMBERS.get(el, 0) * count for el, count in atom_dict.items()))
    except ChemparseError:
        return 0
    except (TypeError, ValueError, KeyError, AttributeError):
        # Unexpected formula format — return 0 to avoid crashing the UI
        return 0


def build_details_text(void_rows: list[dict], method: Literal['squeeze', 'smtbx'] = 'squeeze') -> str:
    """
    Auto-generates a draft details text from void data.

    Each entry in *void_rows* is expected to have the keys:
    ``nr``, ``volume``, ``electrons_platon``, ``formula``.
    Voids without a formula are skipped.

    For PLATON SQUEEZE (*method='squeeze'*) the generated style mirrors the
    example text in ``all_cif_dicts.py``:

        "The C4H8O solvent molecule (42 electrons) disordered in a void of
        248.3 A**3 was treated by SQUEEZE."

    For Olex2/SMTBX solvent masks (*method='smtbx'*) a parallel sentence is
    generated that references the SMTBX mask procedure instead.

    Args:
        void_rows: List of dicts with void metadata and user-provided formula.
        method: Treatment method - ``'squeeze'`` (default) or ``'smtbx'``.

    Returns:
        Multi-sentence details string, or empty string when no formulae are set.
    """
    sentences: list[str] = []
    for row in void_rows:
        formula = (row.get('formula') or '').strip()
        if not formula or formula == '?':
            continue
        volume = row.get('volume', '?')
        calc_e = electrons_from_formula(formula)
        if method == 'smtbx':
            sentences.append(
                f'The {formula} molecule ({calc_e} electrons) '
                f'in a void of {volume} \u212b\u00b3 was treated by the Olex2/SMTBX '
                f'solvent mask procedure.'
            )
        else:
            sentences.append(
                f'The {formula} molecule ({calc_e} electrons) '
                f'in a void of {volume} \u212b\u00b3 was treated by SQUEEZE.'
            )
    return '\n'.join(sentences)
