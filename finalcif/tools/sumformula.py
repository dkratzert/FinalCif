from typing import Union, Dict

from finalcif.tools import chemparse


def formula_str_to_dict(sumform: Union[str, bytes]) -> Dict[str, float]:
    """
    converts an atom name like C12 to the element symbol C
    Use this code to find the atoms while going through the character astream of a sumformula
    e.g. C12H6O3Mn7
    Find two-char atoms, them one-char, and see if numbers are in between.
    """
    chemical_formula = chemparse.parse_formula(sumform.replace(" ", ""))
    return chemical_formula


def sum_formula_to_html(sumform: Dict[str, float | int], break_after: int = 99) -> str:
    """
    Makes html formatted sum formula from dictionary.
    """
    if not sumform:
        return ''
    l = ['<html><body>']
    num = 0
    for el in sumform:
        if sumform[el] == 0 or sumform[el] is None:
            continue
        try:
            times = round(float(sumform[el]), 1)
        except (TypeError, ValueError):
            times = 1
        if num > 3 and num % break_after == 0:
            l.append("<br>")
        if times == 1:
            l.append('{}'.format(el))
        else:
            l.append("{}<sub>{:g}</sub>".format(el, times))
        num += 1
    l.append('</body></html>')
    formula = "".join(l)
    return formula
