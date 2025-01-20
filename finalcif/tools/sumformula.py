from typing import Union, Dict

from finalcif.tools import chemparse


def formula_str_to_dict(sumform: Union[str, bytes]) -> Dict[str, float]:
    chemical_formula = chemparse.parse_formula(sumform.replace(" ", ""))
    return chemical_formula


def sum_formula_to_html(sumform: Dict[str, float | int], break_after: int = 99) -> str:
    """
    Makes html formatted sum formula from a dictionary.
    """
    if not sumform:
        return ''
    formula_list = ['<html><body>']
    num = 0
    for el in sumform:
        if sumform[el] == 0 or sumform[el] is None:
            continue
        try:
            times = round(float(sumform[el]), 1)
        except (TypeError, ValueError):
            times = 1
        if num > 3 and num % break_after == 0:
            formula_list.append("<br>")
        if times == 1:
            formula_list.append('{}'.format(el))
        else:
            formula_list.append("{}<sub>{:g}</sub>".format(el, times))
        num += 1
    formula_list.append('</body></html>')
    formula = "".join(formula_list)
    return formula
