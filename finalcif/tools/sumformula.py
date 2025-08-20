from finalcif.tools import chemparse


def formula_str_to_dict(sumform: str | bytes) -> dict[str, float]:
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
