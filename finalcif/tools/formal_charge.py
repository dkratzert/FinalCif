"""Formal-charge perception for the discrete fragments of a crystal structure.

The IUCr definition of ``_chemical_formula_moiety`` requires the charge of every
discrete ion to be given at the end of its moiety, separated from the last
element token by a space (``'C12 H17 N4 O S 1+, C6 H2 N3 O7 1-'``).

Charges are perceived in three stages:

1. **Explicit oxidation states** parsed from ``_atom_site_type_symbol`` suffixes
   (``'Cl1-'``, ``'Fe3+'``).  Whenever a structure carries them they win.
2. **Chemical perception** — whole-fragment templates for the common molecular
   ions and solvents, a table of unambiguous monatomic ions, and connectivity
   rules for those atom types whose formal charge follows unambiguously from
   their coordination number (e.g. four-coordinate nitrogen).
3. **Charge balancing** — a crystal is electrically neutral, so a single species
   of unknown charge can be assigned the charge that neutralises the cell.
   If the balance cannot be satisfied, no charges are reported at all, because a
   wrong charge is worse than a missing one.

Metal–ligand bonds are ignored when counting coordination numbers: a nitrogen
that donates a lone pair to a metal centre is neutral, not a quaternary
ammonium ion.
"""
from __future__ import annotations

import dataclasses
import re
from collections.abc import Sequence
from typing import NamedTuple

# Maximum absolute charge accepted for a derived (charge-balanced) species.
MAX_DERIVED_CHARGE: int = 8

# Tolerance for accepting a balanced charge as an integer.
_CHARGE_INT_TOL: float = 0.02

# Element counts within a fragment must be this close to an integer before the
# fragment can be matched against a composition template.
_COMPOSITION_INT_TOL: float = 0.02

# Oxidation-state suffix of a CIF type symbol: 'Fe3+', 'Cl1-', 'Ni0+', 'O2-'.
_OXIDATION_RE: re.Pattern[str] = re.compile(r'^[A-Za-z]+(\d*)([+-])$')

# Metals whose bonds are coordinate rather than covalent.  Bonds to these
# elements are ignored when coordination numbers are counted.  Metalloids that
# form genuine covalent bonds (B, Si, Ge, As, Sb, Te) are deliberately absent.
METALS: frozenset[str] = frozenset({
    'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr',
    'Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra',
    'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn',
    'Al', 'Ga', 'In', 'Tl', 'Sn', 'Pb', 'Bi', 'Po',
    'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er',
    'Tm', 'Yb', 'Lu',
    'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
    'Md', 'No', 'Lr',
})

# Monatomic ions whose charge is unambiguous.  Elements with several common
# oxidation states (Cu, Fe, Mn, Sn, Pb, Tl, …) are intentionally omitted so that
# the charge-balancing stage can derive them instead of guessing.
# Bare O/S/Se/N are omitted as well: an isolated oxygen far more often is a water
# molecule whose hydrogens were not modelled than an oxide ion.
MONATOMIC_ION_CHARGES: dict[str, int] = {
    'Li': 1, 'Na': 1, 'K': 1, 'Rb': 1, 'Cs': 1,
    'Be': 2, 'Mg': 2, 'Ca': 2, 'Sr': 2, 'Ba': 2,
    'F': -1, 'Cl': -1, 'Br': -1, 'I': -1,
    'Al': 3, 'Ga': 3, 'Sc': 3, 'Y': 3, 'Zn': 2, 'Cd': 2, 'Ag': 1,
    'La': 3, 'Ce': 3, 'Pr': 3, 'Nd': 3, 'Sm': 3, 'Gd': 3, 'Tb': 3,
    'Dy': 3, 'Ho': 3, 'Er': 3, 'Tm': 3, 'Lu': 3,
}

CompositionKey = tuple[tuple[str, int], ...]


def _key(*pairs: tuple[str, int]) -> CompositionKey:
    return tuple(sorted(pairs))


# Whole-fragment templates for ions whose composition identifies them beyond
# doubt.  Hydrogen-free entries keep working when hydrogens were not modelled.
POLYATOMIC_ION_CHARGES: dict[CompositionKey, int] = {
    # Complex fluorides / halogenometallates
    _key(('B', 1), ('F', 4)): -1,
    _key(('P', 1), ('F', 6)): -1,
    _key(('As', 1), ('F', 6)): -1,
    _key(('Sb', 1), ('F', 6)): -1,
    _key(('Si', 1), ('F', 6)): -2,
    _key(('Al', 1), ('Cl', 4)): -1,
    _key(('Ga', 1), ('Cl', 4)): -1,
    _key(('Fe', 1), ('Cl', 4)): -1,
    _key(('Au', 1), ('Cl', 4)): -1,
    _key(('Au', 1), ('Br', 4)): -1,
    _key(('Sb', 1), ('Cl', 6)): -1,
    _key(('Sn', 1), ('Cl', 3)): -1,
    _key(('Bi', 1), ('Cl', 4)): -1,
    _key(('Pt', 1), ('Cl', 6)): -2,
    _key(('Pd', 1), ('Cl', 6)): -2,
    _key(('Sn', 1), ('Cl', 6)): -2,
    _key(('Te', 1), ('Cl', 6)): -2,
    _key(('Ge', 1), ('F', 6)): -2,
    _key(('Ti', 1), ('F', 6)): -2,
    _key(('Zr', 1), ('F', 6)): -2,
    _key(('B', 1), ('H', 4)): -1,
    # Oxo anions
    _key(('Cl', 1), ('O', 4)): -1,
    _key(('Br', 1), ('O', 4)): -1,
    _key(('I', 1), ('O', 4)): -1,
    _key(('Cl', 1), ('O', 3)): -1,
    _key(('N', 1), ('O', 3)): -1,
    _key(('N', 1), ('O', 2)): -1,
    _key(('S', 1), ('O', 4)): -2,
    _key(('S', 1), ('O', 3)): -2,
    _key(('H', 1), ('S', 1), ('O', 4)): -1,
    _key(('P', 1), ('O', 4)): -3,
    _key(('H', 1), ('P', 1), ('O', 4)): -2,
    _key(('H', 2), ('P', 1), ('O', 4)): -1,
    _key(('C', 1), ('O', 3)): -2,
    _key(('C', 1), ('H', 1), ('O', 3)): -1,
    _key(('Cr', 1), ('O', 4)): -2,
    _key(('Mn', 1), ('O', 4)): -1,
    _key(('Re', 1), ('O', 4)): -1,
    _key(('V', 1), ('O', 3)): -1,
    _key(('Mo', 1), ('O', 4)): -2,
    _key(('W', 1), ('O', 4)): -2,
    # Pseudohalides and small anions
    _key(('C', 1), ('N', 1)): -1,
    _key(('C', 1), ('N', 1), ('S', 1)): -1,
    _key(('C', 1), ('N', 1), ('Se', 1)): -1,
    _key(('C', 1), ('N', 1), ('O', 1)): -1,
    _key(('N', 3),): -1,
    _key(('I', 3),): -1,
    _key(('Br', 3),): -1,
    _key(('H', 1), ('O', 1)): -1,
    _key(('H', 1), ('S', 1)): -1,
    _key(('H', 1), ('F', 2)): -1,
    _key(('H', 2), ('F', 3)): -1,
    _key(('H', 3), ('F', 4)): -1,
    # Sulfonates and carboxylates that are unambiguous without hydrogens
    _key(('C', 1), ('F', 3), ('O', 3), ('S', 1)): -1,
    _key(('C', 2), ('F', 3), ('O', 2)): -1,
    # Cations
    _key(('H', 4), ('N', 1)): 1,
    _key(('H', 3), ('O', 1)): 1,
    _key(('H', 5), ('O', 2)): 1,
}

# Tetrahalometallate dianions [MX4]2- of the divalent late transition metals.
# Iron is excluded: [FeCl4]- of iron(III) is by far the more common species.
POLYATOMIC_ION_CHARGES.update({
    _key((metal, 1), (halide, 4)): -2
    for metal in ('Mn', 'Co', 'Ni', 'Cu', 'Zn', 'Cd', 'Hg', 'Pd', 'Pt')
    for halide in ('Cl', 'Br', 'I')
})

# Fragments that are certainly neutral.  Keeping the common crystallisation
# solvents here stops the charge-balancing stage from dumping a derived charge
# onto a solvate molecule.
NEUTRAL_FRAGMENTS: frozenset[CompositionKey] = frozenset({
    _key(('H', 2), ('O', 1)),                                  # water
    _key(('H', 3), ('N', 1)),                                  # ammonia
    _key(('C', 1), ('H', 4), ('O', 1)),                        # methanol
    _key(('C', 2), ('H', 6), ('O', 1)),                        # ethanol
    _key(('C', 3), ('H', 8), ('O', 1)),                        # propanol
    _key(('C', 4), ('H', 10), ('O', 1)),                       # butanol / ether
    _key(('C', 2), ('H', 6), ('O', 2)),                        # ethylene glycol
    _key(('C', 2), ('H', 6), ('O', 1), ('S', 1)),              # DMSO
    _key(('C', 3), ('H', 7), ('N', 1), ('O', 1)),              # DMF
    _key(('C', 4), ('H', 9), ('N', 1), ('O', 1)),              # DMA / NMP
    _key(('C', 4), ('H', 8), ('O', 1)),                        # THF
    _key(('C', 4), ('H', 8), ('O', 2)),                        # dioxane / EtOAc
    _key(('C', 2), ('H', 3), ('N', 1)),                        # acetonitrile
    _key(('C', 3), ('H', 6), ('O', 1)),                        # acetone
    _key(('C', 5), ('H', 5), ('N', 1)),                        # pyridine
    _key(('C', 1), ('H', 2), ('Cl', 2)),                       # dichloromethane
    _key(('C', 1), ('H', 1), ('Cl', 3)),                       # chloroform
    _key(('C', 1), ('Cl', 4)),                                 # tetrachloromethane
    _key(('C', 2), ('H', 4), ('Cl', 2)),                       # dichloroethane
    _key(('C', 1), ('S', 2)),                                  # carbon disulfide
    _key(('C', 1), ('O', 2)),                                  # carbon dioxide
    _key(('N', 2),),                                           # dinitrogen
    _key(('O', 2),),                                           # dioxygen
    _key(('I', 2),),                                           # diiodine
    # Further solvents and co-crystal formers, most of them taken from the
    # fragment database of DSR (dsr_db.txt).  Pure hydrocarbons (benzene,
    # toluene, hexane, adamantane, naphthalene, …) need no entry — they are
    # recognised by :func:`_is_hydrocarbon`.
    _key(('C', 1), ('H', 3), ('N', 1), ('O', 2)),              # nitromethane
    _key(('C', 2), ('H', 2), ('Cl', 4)),                       # tetrachloroethane
    _key(('C', 2), ('H', 1), ('F', 3), ('O', 2)),              # trifluoroacetic acid
    _key(('C', 3), ('H', 2), ('F', 6), ('O', 1)),              # hexafluoroisopropanol
    _key(('C', 3), ('H', 4), ('N', 2)),                        # pyrazole / imidazole
    _key(('C', 3), ('H', 9), ('P', 1)),                        # trimethylphosphane
    _key(('C', 4), ('H', 4), ('N', 2)),                        # pyrazine
    _key(('C', 4), ('H', 4), ('O', 1)),                        # furan
    _key(('C', 4), ('H', 4), ('S', 1)),                        # thiophene
    _key(('C', 4), ('H', 6), ('N', 2)),                        # N-methylimidazole
    _key(('C', 4), ('H', 10), ('O', 2)),                       # dimethoxyethane
    _key(('C', 5), ('H', 11), ('N', 1)),                       # piperidine
    _key(('C', 5), ('H', 12), ('O', 1)),                       # methyl tert-butyl ether
    _key(('C', 6), ('H', 3), ('F', 3)),                        # trifluorobenzene
    _key(('C', 6), ('H', 3), ('Cl', 3)),                       # trichlorobenzene
    _key(('C', 6), ('H', 4), ('Cl', 2)),                       # dichlorobenzene
    _key(('C', 6), ('H', 4), ('F', 2)),                        # difluorobenzene
    _key(('C', 6), ('H', 5), ('Br', 1)),                       # bromobenzene
    _key(('C', 6), ('H', 5), ('Cl', 1)),                       # chlorobenzene
    _key(('C', 6), ('H', 5), ('F', 1)),                        # fluorobenzene
    _key(('C', 6), ('H', 5), ('I', 1)),                        # iodobenzene
    _key(('C', 6), ('H', 5), ('N', 1), ('O', 2)),              # nitrobenzene
    _key(('C', 6), ('H', 12), ('N', 2)),                       # DABCO
    _key(('C', 6), ('H', 14), ('O', 3)),                       # diglyme
    _key(('C', 6), ('H', 15), ('N', 1)),                       # triethylamine
    _key(('C', 6), ('H', 16), ('N', 2)),                       # TMEDA
    _key(('C', 6), ('H', 19), ('N', 1), ('Si', 2)),            # hexamethyldisilazane
    _key(('C', 7), ('H', 5), ('N', 1)),                        # benzonitrile
    _key(('C', 7), ('H', 10), ('N', 2)),                       # DMAP
    _key(('C', 8), ('H', 16), ('O', 4)),                       # 12-crown-4
    _key(('C', 9), ('H', 23), ('N', 3)),                       # PMDTA
    _key(('C', 10), ('H', 8), ('N', 2)),                       # 2,2'-bipyridine
    _key(('C', 12), ('H', 8), ('N', 2)),                       # 1,10-phenanthroline
    _key(('C', 12), ('H', 24), ('O', 6)),                      # 18-crown-6
    _key(('C', 12), ('H', 27), ('P', 1)),                      # tri-tert-butylphosphane
    _key(('C', 18), ('H', 15), ('P', 1)),                      # triphenylphosphane
    _key(('C', 18), ('H', 24), ('N', 2)),                      # di-tert-butylbipyridine
    _key(('C', 18), ('H', 36), ('N', 2), ('O', 6)),            # [2.2.2]cryptand
    _key(('C', 20),),                                          # fullerene C20
    _key(('C', 60),),                                          # fullerene C60
    _key(('C', 70),),                                          # fullerene C70
    _key(('O', 2), ('S', 1)),                                  # sulfur dioxide
})


class ChargeAtom(NamedTuple):
    """One atom of a fragment, prepared for charge perception.

    Attributes:
        element:     Bare element symbol, oxidation suffix already stripped.
        occupancy:   Site occupancy.
        neighbours:  ``(element, degree)`` of every *non-metal* bonded neighbour,
                     where *degree* is that neighbour's own non-metal
                     coordination number.
        oxidation:   Oxidation state read from the CIF type symbol, or ``None``.
    """

    element: str
    occupancy: float = 1.0
    neighbours: tuple[tuple[str, int], ...] = ()
    oxidation: int | None = None


@dataclasses.dataclass(frozen=True)
class FragmentCharge:
    """Perceived charge of one fragment.

    Attributes:
        charge:    Formal charge of a single (whole) fragment.
        confident: ``True`` when the charge is trusted and must not be altered
                   by the charge-balancing stage.
    """

    charge: int = 0
    confident: bool = False


class SpeciesCharge(NamedTuple):
    """A distinct chemical species together with its abundance per formula unit."""

    charge: int
    confident: bool
    ratio: float
    atom_count: float


def parse_oxidation_state(type_symbol: str) -> int | None:
    """Return the oxidation state encoded in a CIF type symbol, or ``None``.

    Examples::

        >>> parse_oxidation_state('Fe3+')
        3
        >>> parse_oxidation_state('Cl1-')
        -1
        >>> parse_oxidation_state('O-')
        -1
        >>> parse_oxidation_state('C') is None
        True
    """
    match = _OXIDATION_RE.match(type_symbol.strip())
    if match is None:
        return None
    digits, sign = match.groups()
    value = int(digits) if digits else 1
    return value if sign == '+' else -value


def is_metal(element: str) -> bool:
    """Return ``True`` when *element* forms coordinate rather than covalent bonds."""
    return element.capitalize() in METALS


def composition_key(composition: dict[str, float]) -> CompositionKey | None:
    """Return a hashable integer composition key, or ``None`` if counts are fractional.

    Fractional element counts arise from mixed-element disorder; such fragments
    cannot be matched reliably against a template.
    """
    key: list[tuple[str, int]] = []
    for element, count in composition.items():
        nearest = round(count)
        if abs(count - nearest) > _COMPOSITION_INT_TOL:
            return None
        if nearest > 0:
            key.append((element, int(nearest)))
    return tuple(sorted(key))


def format_charge(charge: int) -> str:
    """Return the IUCr charge token for *charge* (``'1+'``, ``'2-'``, ``''``)."""
    if charge > 0:
        return f'{charge}+'
    if charge < 0:
        return f'{abs(charge)}-'
    return ''


def _atom_rule_charge(atom: ChargeAtom) -> int:
    """Return the formal charge that follows unambiguously from *atom*'s coordination.

    Only rules that cannot be confused by missing bond orders are applied:

    * Four-coordinate nitrogen is an ammonium/iminium centre (1+), unless one of
      its neighbours is a terminal oxygen — then the fragment is an amine
      *N*-oxide or ylide whose two formal charges cancel.
    * Four-coordinate boron is a borate (1-).
    * Four-coordinate phosphorus/arsenic/antimony bonded only to carbon is an
      onium centre (1+); six-coordinate is a hexahalogenometallate-like anion (1-).
    * Three-coordinate sulfur/selenium bonded only to carbon is a sulfonium (1+).

    Carbon and oxygen are deliberately left alone: their formal charge cannot be
    derived from connectivity without knowing bond orders (an aromatic carbon and
    a carbanion both have three neighbours, a ketone oxygen and a carboxylate
    oxygen both have one).
    """
    element = atom.element
    degree = len(atom.neighbours)
    only_carbon = degree > 0 and all(el == 'C' for el, _deg in atom.neighbours)
    has_terminal_oxygen = any(el == 'O' and deg == 1 for el, deg in atom.neighbours)

    if element == 'N' and degree == 4:
        return 0 if has_terminal_oxygen else 1
    if element == 'B' and degree == 4:
        return -1
    if element in ('P', 'As', 'Sb'):
        if degree == 6:
            return -1
        if degree == 4 and only_carbon:
            return 1
    if element in ('S', 'Se') and degree == 3 and only_carbon:
        return 1
    return 0


def _explicit_charge(atoms: Sequence[ChargeAtom], weighted: bool) -> int | None:
    """Return the fragment charge from explicit oxidation states, or ``None``.

    ``None`` is returned when not a single atom of the fragment carries an
    oxidation state, so that the caller can fall back to perception.
    """
    if all(atom.oxidation is None for atom in atoms):
        return None
    total = 0.0
    for atom in atoms:
        state = atom.oxidation or 0
        total += state * atom.occupancy if weighted else state
    return round(total)


def perceive_fragment_charge(
        atoms: Sequence[ChargeAtom],
        composition: dict[str, float],
        weighted: bool = False,
) -> FragmentCharge:
    """Perceive the formal charge of a single fragment.

    Args:
        atoms:       The fragment's atoms with their connectivity.
        composition: Element counts of *one whole* fragment (already collapsed
                     over disorder parts).
        weighted:    ``True`` when *atoms* holds several disorder parts of the
                     same fragment, so that per-atom contributions have to be
                     weighted by occupancy to yield a single molecule.

    Returns:
        The perceived :class:`FragmentCharge`.
    """
    explicit = _explicit_charge(atoms, weighted)
    if explicit is not None:
        return FragmentCharge(charge=explicit, confident=True)

    key = composition_key(composition)
    if key is not None:
        if key in NEUTRAL_FRAGMENTS:
            return FragmentCharge(charge=0, confident=True)
        template = POLYATOMIC_ION_CHARGES.get(key)
        if template is not None:
            return FragmentCharge(charge=template, confident=True)
        if len(key) == 1 and key[0][1] == 1:
            monatomic = MONATOMIC_ION_CHARGES.get(key[0][0])
            if monatomic is not None:
                return FragmentCharge(charge=monatomic, confident=True)
        if _is_hydrocarbon(key):
            return FragmentCharge(charge=0, confident=True)

    total = 0.0
    for atom in atoms:
        rule = _atom_rule_charge(atom)
        if not rule:
            continue
        total += rule * atom.occupancy if weighted else rule
    return FragmentCharge(charge=round(total), confident=False)


def _is_hydrocarbon(key: CompositionKey) -> bool:
    """Return ``True`` for a fragment built solely from carbon and hydrogen.

    Requires hydrogen to be present so that a carbon skeleton whose hydrogens
    were never modelled is not mistaken for a neutral hydrocarbon.
    """
    elements = {element for element, _count in key}
    return elements == {'C', 'H'}


def balance_charges(species: Sequence[SpeciesCharge]) -> list[int] | None:
    """Return charge-balanced charges for *species*, or ``None`` if impossible.

    A crystal is electrically neutral, so ``Σ ratio × charge`` over all species
    of one formula unit must vanish.  When it does not, the charge of a single
    species of unperceived charge is derived from the imbalance.  Species whose
    charge was perceived with confidence (templates, monatomic ions, explicit
    oxidation states) are never modified.

    The species chosen to absorb the imbalance is the largest one whose charge is
    still zero; if every unconfident species already carries a charge, the
    largest of those is used instead.  This puts a carboxylate charge on the
    organic anion rather than on a co-crystallised solvent molecule.

    Returns ``None`` when the imbalance cannot be resolved — the caller should
    then report no charges at all rather than wrong ones.
    """
    if not species:
        return []
    charges = [entry.charge for entry in species]
    total = sum(entry.ratio * entry.charge for entry in species)
    if abs(total) < _CHARGE_INT_TOL:
        return charges

    adjustable = [i for i, entry in enumerate(species)
                  if not entry.confident and entry.ratio > 0]
    if not adjustable:
        return None
    preferred = [i for i in adjustable if species[i].charge == 0] or adjustable
    index = max(preferred, key=lambda i: (species[i].atom_count, species[i].ratio))

    derived = species[index].charge - total / species[index].ratio
    nearest = round(derived)
    if abs(derived - nearest) > _CHARGE_INT_TOL or abs(nearest) > MAX_DERIVED_CHARGE:
        return None
    charges[index] = nearest
    return charges
