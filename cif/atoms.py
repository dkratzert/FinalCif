# /usr/bin/env python
# -*- encoding: utf-8 -*-
# möp
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <daniel.kratzert@ac.uni-freiburg.de> wrote this file. As long as you retain
# this notice you can do whatever you want with this stuff. If we meet some day,
# and you think this stuff is worth it, you can buy me a beer in return.
# Daniel Kratzert
# ----------------------------------------------------------------------------
#

import re

num2element = {
    0: 'n',
    1: 'H',
    2: 'He',
    3: 'Li',
    4: 'Be',
    5: 'B',
    6: 'C',
    7: 'N',
    8: 'O',
    9: 'F',
    10: 'Ne',
    11: 'Na',
    12: 'Mg',
    13: 'Al',
    14: 'Si',
    15: 'P',
    16: 'S',
    17: 'Cl',
    18: 'Ar',
    19: 'K',
    20: 'Ca',
    21: 'Sc',
    22: 'Ti',
    23: 'V',
    24: 'Cr',
    25: 'Mn',
    26: 'Fe',
    27: 'Co',
    28: 'Ni',
    29: 'Cu',
    30: 'Zn',
    31: 'Ga',
    32: 'Ge',
    33: 'As',
    34: 'Se',
    35: 'Br',
    36: 'Kr',
    37: 'Rb',
    38: 'Sr',
    39: 'Y',
    40: 'Zr',
    41: 'Nb',
    42: 'Mo',
    43: 'Tc',
    44: 'Ru',
    45: 'Rh',
    46: 'Pd',
    47: 'Ag',
    48: 'Cd',
    49: 'In',
    50: 'Sn',
    51: 'Sb',
    52: 'Te',
    53: 'I',
    54: 'Xe',
    55: 'Cs',
    56: 'Ba',
    57: 'La',
    58: 'Ce',
    59: 'Pr',
    60: 'Nd',
    61: 'Pm',
    62: 'Sm',
    63: 'Eu',
    64: 'Gd',
    65: 'Tb',
    66: 'Dy',
    67: 'Ho',
    68: 'Er',
    69: 'Tm',
    70: 'Yb',
    71: 'Lu',
    72: 'Hf',
    73: 'Ta',
    74: 'W',
    75: 'Re',
    76: 'Os',
    77: 'Ir',
    78: 'Pt',
    79: 'Au',
    80: 'Hg',
    81: 'Tl',
    82: 'Pb',
    83: 'Bi',
    84: 'Po',
    85: 'At',
    86: 'Rn',
    87: 'Fr',
    88: 'Ra',
    89: 'Ac',
    90: 'Th',
    91: 'Pa',
    92: 'U',
    93: 'Np',
    94: 'Pu',
    95: 'Am',
    96: 'Cm',
    97: 'Bk',
    98: 'Cf',
    99: 'Es',
    100: 'Fm',
    101: 'Md',
    102: 'No',
    103: 'Lr',
    104: 'Rf',
    105: 'Db',
    106: 'Sg',
    107: 'Bh',
    108: 'Hs',
    109: 'Mt',
    110: 'Ds',
    111: 'Rg',
    112: 'Cn',
    114: 'Uuq',
    116: 'Uuh'
}

element2num = {
    'H': 1,
    'He': 2,
    'Li': 3,
    'Be': 4,
    'B': 5,
    'C': 6,
    'N': 7,
    'O': 8,
    'F': 9,
    'Ne': 10,
    'Na': 11,
    'Mg': 12,
    'Al': 13,
    'Si': 14,
    'P': 15,
    'S': 16,
    'Cl': 17,
    'Ar': 18,
    'K': 19,
    'Ca': 20,
    'Sc': 21,
    'Ti': 22,
    'V': 23,
    'Cr': 24,
    'Mn': 25,
    'Fe': 26,
    'Co': 27,
    'Ni': 28,
    'Cu': 29,
    'Zn': 30,
    'Ga': 31,
    'Ge': 32,
    'As': 33,
    'Se': 34,
    'Br': 35,
    'Kr': 36,
    'Rb': 37,
    'Sr': 38,
    'Y': 39,
    'Zr': 40,
    'Nb': 41,
    'Mo': 42,
    'Tc': 43,
    'Ru': 44,
    'Rh': 45,
    'Pd': 46,
    'Ag': 47,
    'Cd': 48,
    'In': 49,
    'Sn': 50,
    'Sb': 51,
    'Te': 52,
    'I': 53,
    'Xe': 54,
    'Cs': 55,
    'Ba': 56,
    'La': 57,
    'Ce': 58,
    'Pr': 59,
    'Nd': 60,
    'Pm': 61,
    'Sm': 62,
    'Eu': 63,
    'Gd': 64,
    'Tb': 65,
    'Dy': 66,
    'Ho': 67,
    'Er': 68,
    'Tm': 69,
    'Yb': 70,
    'Lu': 71,
    'Hf': 72,
    'Ta': 73,
    'W': 74,
    'Re': 75,
    'Os': 76,
    'Ir': 77,
    'Pt': 78,
    'Au': 79,
    'Hg': 80,
    'Tl': 81,
    'Pb': 82,
    'Bi': 83,
    'Po': 84,
    'At': 85,
    'Rn': 86,
    'Fr': 87,
    'Ra': 88,
    'Ac': 89,
    'Th': 90,
    'Pa': 91,
    'U': 92,
    'Np': 93,
    'Pu': 94,
    'Am': 95,
    'Cm': 96,
    'Bk': 97,
    'Cf': 98,
    'D': 1,
}

atoms = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg',
         'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
         'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y',
         'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te',
         'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb',
         'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt',
         'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
         'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'D']

sorted_atoms = ['C', 'D', 'H', 'N', 'O', 'Cl', 'Br', 'I', 'F', 'S', 'P', 'Ac', 'Ag', 'Al',
                'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bi', 'Bk', 'Ca', 'Cd', 'Ce',
                'Cf', 'Cm', 'Co', 'Cr', 'Cs', 'Cu', 'Dy', 'Er', 'Eu', 'Fe', 'Fr', 'Ga', 'Gd',
                'Ge', 'He', 'Hf', 'Hg', 'Ho', 'In', 'Ir', 'K', 'Kr', 'La', 'Li', 'Lu', 'Mg',
                'Mn', 'Mo', 'Na', 'Nb', 'Nd', 'Ne', 'Ni', 'Np', 'Os', 'Pa', 'Pb', 'Pd', 'Pm',
                'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Re', 'Rh', 'Rn', 'Ru', 'Sb', 'Sc', 'Se',
                'Si', 'Sm', 'Sn', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Tl', 'Tm', 'U',
                'V', 'W', 'Xe', 'Y', 'Yb', 'Zn', 'Zr']


num2covradius = {
    0: 0.74,
    1: 0.50,
    2: 1.23,
    3: 0.9,
    4: 0.82,
    5: 0.77,
    6: 0.75,
    7: 0.73,
    8: 0.72,
    9: 0.71,
    10: 1.54,
    11: 1.36,
    12: 1.18,
    13: 1.11,
    14: 1.06,
    15: 1.02,
    16: 0.99,
    17: 0.98,
    18: 2.03,
    19: 1.74,
    20: 1.44,
    21: 1.32,
    22: 1.22,
    23: 1.18,
    24: 1.17,
    25: 1.17,
    26: 1.16,
    27: 1.15,
    28: 1.17,
    29: 1.25,
    30: 1.26,
    31: 1.22,
    32: 1.2,
    33: 1.16,
    34: 1.14,
    35: 1.12,
    36: 2.16,
    37: 1.91,
    38: 1.62,
    39: 1.45,
    40: 1.34,
    41: 1.3,
    42: 1.27,
    43: 1.25,
    44: 1.25,
    45: 1.28,
    46: 1.34,
    47: 1.48,
    48: 1.44,
    49: 1.41,
    50: 1.4,
    51: 1.36,
    52: 1.33,
    53: 1.31,
    54: 2.35,
    55: 1.98,
    56: 1.69,
    57: 1.65,
    58: 1.65,
    59: 1.64,
    60: 1.63,
    61: 1.62,
    62: 1.85,
    63: 1.61,
    64: 1.59,
    65: 1.59,
    66: 1.58,
    67: 1.57,
    68: 1.56,
    69: 1.74,
    70: 1.56,
    71: 1.44,
    72: 1.34,
    73: 1.3,
    74: 1.28,
    75: 1.26,
    76: 1.27,
    77: 1.3,
    78: 1.34,
    79: 1.49,
    80: 1.48,
    81: 1.47,
    82: 1.46,
    83: 1.46,
    84: 1.45,
    85: 1.0,
    86: 1.0,
    87: 1.0,
    88: 1.88,
    89: 1.65,
    90: 1.61,
    91: 1.42,
    92: 1.30,
    93: 1.51,
    94: 1.82,
    95: 1.20,
    96: 1.20,
    97: 1.20,
    98: 1.20,
    99: 0.5
}


element2cov = {
    'H': 0.50,
    'He': 1.23,
    'Li': 0.9,
    'Be': 0.82,
    'B': 0.77,
    'C': 0.75,
    'N': 0.73,
    'O': 0.72,
    'F': 0.71,
    'Ne': 1.54,
    'Na': 1.36,
    'Mg': 1.18,
    'Al': 1.11,
    'Si': 1.06,
    'P':  1.02,
    'S':  0.99,
    'Cl': 0.98,
    'Ar': 2.03,
    'K':  1.74,
    'Ca': 1.44,
    'Sc': 1.32,
    'Ti': 1.22,
    'V':  1.18,
    'Cr': 1.17,
    'Mn': 1.17,
    'Fe': 1.16,
    'Co': 1.15,
    'Ni': 1.17,
    'Cu': 1.25,
    'Zn': 1.26,
    'Ga': 1.22,
    'Ge': 1.2,
    'As': 1.16,
    'Se': 1.14,
    'Br': 1.12,
    'Kr': 2.16,
    'Rb': 1.91,
    'Sr': 1.62,
    'Y':  1.45,
    'Zr': 1.34,
    'Nb': 1.3,
    'Mo': 1.27,
    'Tc': 1.25,
    'Ru': 1.25,
    'Rh': 1.28,
    'Pd': 1.34,
    'Ag': 1.48,
    'Cd': 1.44,
    'In': 1.41,
    'Sn': 1.4,
    'Sb': 1.36,
    'Te': 1.33,
    'I':  1.31,
    'Xe': 2.35,
    'Cs': 1.98,
    'Ba': 1.69,
    'La': 1.65,
    'Ce': 1.65,
    'Pr': 1.64,
    'Nd': 1.63,
    'Pm': 1.62,
    'Sm': 1.85,
    'Eu': 1.61,
    'Gd': 1.59,
    'Tb': 1.59,
    'Dy': 1.58,
    'Ho': 1.57,
    'Er': 1.56,
    'Tm': 1.74,
    'Yb': 1.56,
    'Lu': 1.44,
    'Hf': 1.34,
    'Ta': 1.3,
    'W':  1.28,
    'Re': 1.26,
    'Os': 1.27,
    'Ir': 1.3,
    'Pt': 1.34,
    'Au': 1.49,
    'Hg': 1.48,
    'Tl': 1.47,
    'Pb': 1.46,
    'Bi': 1.46,
    'Po': 1.45,
    'At': 1.0,
    'Rn': 1.0,
    'Fr': 1.0,
    'Ra': 1.88,
    'Ac': 1.65,
    'Th': 1.61,
    'Pa': 1.42,
    'U':  1.30,
    'Np': 1.51,
    'Pu': 1.82,
    'Am': 1.20,
    'Cm': 1.20,
    'Bk': 1.20,
    'Cf': 1.20,
    'D':  0.5
}

def get_radius(atomic_number: int) -> float:
    """
    Get the covalent radius in pm for the element.

    >>> get_radius(6)
    0.75
    """
    return num2covradius[atomic_number]


def get_radius_from_element(element: str) -> float:
    """
    Returns the radius of an atom by its element name.

    >>> get_radius_from_element('F')
    0.71
    """
    return element2cov[element.capitalize()]


def get_atomic_number(element: str) -> int:
    """
    returns the atomic number from the element symbol

    >>> get_atomic_number('F')
    9
    """
    return element2num[element]


def get_element(atomic_number: int) -> str:
    """
    returns the element symbol from the atomic number

    >>> get_element(7)
    'N'
    """
    return num2element[atomic_number]


def get_atomlabel(input_atom: str) -> str:
    """
    converts an atom name like C12 to the element symbol C.

    >>> get_atomlabel('C12')
    'C'
    >>> get_atomlabel('Te1+')
    'Te'
    """
    atom = ''
    for x in input_atom:  # iterate over characters in i
        if re.match(r'^[A-Za-z#]', x):  # Alphabet and "#" as allowed characters in names
            atom = atom + x.upper()  # add characters to atoms until numbers occur
        else:  # now we have atoms like C, Ca, but also Caaa
            break
    try:
        if atom[0:2].capitalize() in atoms:  # fixes names like Caaa to be just Ca
            return atom[0:2].capitalize()  # atoms first, search for all two-letter atoms
        elif atom[0].upper() in atoms:
            return atom[0]  # then for all one-letter atoms
        else:
            #print('*** {} is not a valid atom!! ***'.format(atom))
            raise KeyError
    except(IndexError):
        #print('*** {} is not a valid atom! ***'.format(atom))
        raise KeyError


if __name__ == '__main__':
    import doctest

    failed, attempted = doctest.testmod()  # verbose=True)
    if failed == 0:
        print('passed all {} tests!'.format(attempted))
    else:
        print('{} of {} tests failed'.format(failed, attempted))
