from typing import Union, Dict

from finalcif.cif.atoms import atoms


def formula_str_to_dict(sumform: Union[str, bytes]) -> Dict[str, str]:
    """
    converts an atom name like C12 to the element symbol C
    Use this code to find the atoms while going through the character astream of a sumformula
    e.g. C12H6O3Mn7
    Find two-char atoms, them one-char, and see if numbers are in between.
    """
    elements = [x.upper() for x in atoms]
    atlist = {}
    nums = []
    try:
        sumform = sumform.upper().replace(' ', '').replace('\n', '').replace('\r', '')
    except AttributeError:
        print('Error in formula_str_to_dict')
        return atlist

    def isnumber(el):
        for x in el:
            if x.isnumeric() or x == '.':
                nums.append(x)
            else:
                # end of number
                break

    while sumform:
        if sumform[0:2] in elements:  # The two-character elements
            isnumber(sumform[2:])
            atlist[sumform[0:2].capitalize()] = "".join(nums)
            sumform = sumform[2 + len(nums):]
            nums.clear()
        elif sumform[0] in elements:
            isnumber(sumform[1:])
            atlist[sumform[0]] = "".join(nums)
            sumform = sumform[1 + len(nums):]
            nums.clear()
        else:
            raise KeyError
    return atlist


def sum_formula_to_html(sumform: Dict[str, str], break_after: int = 99) -> str:
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
