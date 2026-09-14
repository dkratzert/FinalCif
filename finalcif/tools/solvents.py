#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   Dr. Daniel Kratzert
#   ----------------------------------------------------------------------------
"""
Lookup table that translates common solvent names into chemical formulae.

This allows users to type ``thf``, ``water`` or ``2 toluene`` instead of the
corresponding sum formula when assigning solvent content to voids.
"""
from __future__ import annotations

import re

# Canonical solvent name -> sum formula.
SOLVENTS: dict[str, str] = {
    'water'                  : 'H2O',
    'methanol'               : 'CH4O',
    'ethanol'                : 'C2H6O',
    '1-propanol'             : 'C3H8O',
    '2-propanol'             : 'C3H8O',
    '1-butanol'              : 'C4H10O',
    'tert-butanol'           : 'C4H10O',
    'ethylene glycol'        : 'C2H6O2',
    'acetone'                : 'C3H6O',
    'acetonitrile'           : 'C2H3N',
    'acetic acid'            : 'C2H4O2',
    'ethyl acetate'          : 'C4H8O2',
    'formic acid'            : 'CH2O2',
    'tetrahydrofuran'        : 'C4H8O',
    '2-methyltetrahydrofuran': 'C5H10O',
    'tetrahydropyran'        : 'C5H10O',
    '1,4-dioxane'            : 'C4H8O2',
    'diethyl ether'          : 'C4H10O',
    'diisopropyl ether'      : 'C6H14O',
    'tert-butyl methyl ether': 'C5H12O',
    'dimethoxyethane'        : 'C4H10O2',
    'diglyme'                : 'C6H14O3',
    'anisole'                : 'C7H8O',
    'dichloromethane'        : 'CH2Cl2',
    'chloroform'             : 'CHCl3',
    'carbon tetrachloride'   : 'CCl4',
    '1,2-dichloroethane'     : 'C2H4Cl2',
    'carbon disulfide'       : 'CS2',
    'benzene'                : 'C6H6',
    'toluene'                : 'C7H8',
    'xylene'                 : 'C8H10',
    'mesitylene'             : 'C9H12',
    'chlorobenzene'          : 'C6H5Cl',
    '1,2-dichlorobenzene'    : 'C6H4Cl2',
    'bromobenzene'           : 'C6H5Br',
    'fluorobenzene'          : 'C6H5F',
    '1,2-difluorobenzene'    : 'C6H4F2',
    'nitrobenzene'           : 'C6H5NO2',
    'nitromethane'           : 'CH3NO2',
    'pentane'                : 'C5H12',
    'hexane'                 : 'C6H14',
    'heptane'                : 'C7H16',
    'octane'                 : 'C8H18',
    'cyclohexane'            : 'C6H12',
    'cyclopentane'           : 'C5H10',
    'pyridine'               : 'C5H5N',
    'triethylamine'          : 'C6H15N',
    'dimethylformamide'      : 'C3H7NO',
    'dimethylacetamide'      : 'C4H9NO',
    'dimethyl sulfoxide'     : 'C2H6OS',
    'n-methylpyrrolidone'    : 'C5H9NO',
    'hexamethylphosphoramide': 'C6H18N3OP',
    'sulfolane'              : 'C4H8O2S',
    'aniline'                : 'C6H7N',
    'ammonia'                : 'H3N',
    'hydrazine'              : 'H4N2',
}

# Alias -> canonical solvent name.  Aliases must not look like a valid sum
# formula, otherwise a formula would silently be reinterpreted as a name.
ALIASES: dict[str, str] = {
    'h2o'                   : 'water',
    'aqua'                  : 'water',
    'meoh'                  : 'methanol',
    'etoh'                  : 'ethanol',
    'cyclohexan'            : 'cyclohexane',
    'n-propanol'            : '1-propanol',
    'propanol'              : '2-propanol',
    'isopropanol'           : '2-propanol',
    'iso-propanol'          : '2-propanol',
    'ipa'                   : '2-propanol',
    'iproh'                 : '2-propanol',
    'n-butanol'             : '1-butanol',
    'butanol'               : '1-butanol',
    't-butanol'             : 'tert-butanol',
    'tert-butyl alcohol'    : 'tert-butanol',
    'tbuoh'                 : 'tert-butanol',
    'glycol'                : 'ethylene glycol',
    'aceton'                : 'acetone',
    'mecn'                  : 'acetonitrile',
    'ch3cn'                 : 'acetonitrile',
    'etoac'                 : 'ethyl acetate',
    'ethylacetate'          : 'ethyl acetate',
    'thf'                   : 'tetrahydrofuran',
    'me-thf'                : '2-methyltetrahydrofuran',
    '2-me-thf'              : '2-methyltetrahydrofuran',
    '2-methyl-thf'          : '2-methyltetrahydrofuran',
    'methf'                 : '2-methyltetrahydrofuran',
    'thp'                   : 'tetrahydropyran',
    'dioxane'               : '1,4-dioxane',
    'ether'                 : 'diethyl ether',
    'et2o'                  : 'diethyl ether',
    'diethylether'          : 'diethyl ether',
    'ipr2o'                 : 'diisopropyl ether',
    'mtbe'                  : 'tert-butyl methyl ether',
    'tbme'                  : 'tert-butyl methyl ether',
    'dme'                   : 'dimethoxyethane',
    'glyme'                 : 'dimethoxyethane',
    '1,2-dimethoxyethane'   : 'dimethoxyethane',
    'methoxybenzene'        : 'anisole',
    'dcm'                   : 'dichloromethane',
    'methylene chloride'    : 'dichloromethane',
    'methylenechloride'     : 'dichloromethane',
    'dce'                   : '1,2-dichloroethane',
    'benzol'                : 'benzene',
    'toluol'                : 'toluene',
    'tol'                   : 'toluene',
    'p-xylene'              : 'xylene',
    'o-xylene'              : 'xylene',
    'm-xylene'              : 'xylene',
    'xylol'                 : 'xylene',
    '1,3,5-trimethylbenzene': 'mesitylene',
    'odcb'                  : '1,2-dichlorobenzene',
    'dfb'                   : '1,2-difluorobenzene',
    'n-pentane'             : 'pentane',
    'n-hexane'              : 'hexane',
    'n-heptane'             : 'heptane',
    'n-octane'              : 'octane',
    'pyr'                   : 'pyridine',
    'py'                    : 'pyridine',
    'net3'                  : 'triethylamine',
    'et3n'                  : 'triethylamine',
    'dmf'                   : 'dimethylformamide',
    'n,n-dimethylformamide' : 'dimethylformamide',
    'dma'                   : 'dimethylacetamide',
    'n,n-dimethylacetamide' : 'dimethylacetamide',
    'dmso'                  : 'dimethyl sulfoxide',
    'dimethylsulfoxide'     : 'dimethyl sulfoxide',
    'nmp'                   : 'n-methylpyrrolidone',
    'n-methyl-2-pyrrolidone': 'n-methylpyrrolidone',
    'hmpa'                  : 'hexamethylphosphoramide',
    'tetramethylene sulfone': 'sulfolane',
    'aminobenzene'          : 'aniline',
}

_NORMALIZE_RE = re.compile(r'[\s_]+')


def _norm(name: str) -> str:
    """Normalize a solvent name for case- and whitespace-insensitive lookup."""
    return _NORMALIZE_RE.sub(' ', name.strip().lower()).replace(' ', '')


_LOOKUP: dict[str, str] = {_norm(name): formula for name, formula in SOLVENTS.items()}
_LOOKUP.update({_norm(alias): SOLVENTS[canonical] for alias, canonical in ALIASES.items()})


def resolve_solvent(name: str) -> str | None:
    """Return the sum formula for a solvent name or alias.

    Args:
        name: Solvent name such as ``'thf'``, ``'Water'`` or ``'diethyl ether'``.

    Returns:
        The sum formula, or ``None`` when *name* is not a known solvent.
    """
    if not name:
        return None
    return _LOOKUP.get(_norm(name))


def solvent_names() -> list[str]:
    """Return all canonical solvent names and aliases, sorted alphabetically."""
    return sorted(set(SOLVENTS) | set(ALIASES))
