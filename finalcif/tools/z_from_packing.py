"""Determine Z (formula units per unit cell) by packing the unit cell
and counting discrete connected molecular graphs.

Disorder handling
-----------------
Only the first disorder component (disorder_group in {0, 1, -1}) is kept,
because all site occupancies across disorder groups always sum to 1.
This means every atomic site is represented exactly once, regardless of how
many alternative positions were refined.

Algorithm
---------
1. Filter ASU atoms (disorder rule above).
2. Build a gemmi SmallStructure from the filtered atoms and space-group ops.
3. Call SmallStructure.get_all_unit_cell_sites() — gemmi applies every
   symmetry operation and deduplicates atoms that collapse onto the same
   fractional site (special positions), with no arbitrary threshold.
4. Build a bond-adjacency graph using covalent-radii distances with periodic
   boundary conditions (±1 neighbour images along each axis), using
   gemmi.UnitCell.orthogonalize() for fractional→Cartesian conversion.
5. Count connected components via BFS → that count is Z.

The fastmolwidget package is used for the unit-cell volume helper (calc_volume),
which lets callers cross-check the geometry without importing gemmi separately.
"""
from __future__ import annotations

import dataclasses
import math
import re
from collections import Counter, deque
from functools import reduce
from math import gcd
from typing import SupportsIndex

import gemmi

from finalcif.cif.atoms import element2cov as _ELEMENT2COV
from finalcif.tools.chemparse import parse_formula
from finalcif.tools.formal_charge import (METALS, ChargeAtom, FragmentCharge, SpeciesCharge,
                                          balance_charges, format_charge, parse_oxidation_state,
                                          perceive_fragment_charge)

# One atom of a bond-graph component.  The third field carries the atom's
# non-metal neighbours as ``(element, degree)`` pairs and is optional so that
# callers may still pass plain ``(element, occupancy)`` pairs.
AtomRecord = tuple[str, float] | tuple[str, float, tuple[tuple[str, int], ...]]

# One symmetry-expanded unit-cell site.  The disorder group is optional so that
# tests and callers may pass plain ``(element, position, occupancy)`` triples.
ExpandedAtom = (tuple[str, tuple[float, float, float], float]
                | tuple[str, tuple[float, float, float], float, int])

# Regex matching the bare element letters at the start of a type_symbol string.
# CIF _atom_site_type_symbol values often include oxidation-state suffixes such
# as 'Fe3+', 'O1-', 'Ni0+'; this pattern strips everything after the letters.
_ELEMENT_LETTERS_RE: re.Pattern[str] = re.compile(r'^[A-Za-z]+')

# Covalent radii sourced from finalcif.cif.atoms.element2cov (Å).
# A small fallback covers elements absent from that table.
DEFAULT_RADIUS: float = 1.50


def _normalize_element(symbol: str) -> str:
    """Return the bare element symbol, stripping any oxidation-state suffix.

    CIF ``_atom_site_type_symbol`` values may include oxidation-state suffixes
    such as ``'Fe3+'``, ``'O1-'``, or ``'Ni0+'``.  This function returns the
    leading letters only (capitalized), e.g. ``'Fe3+' → 'Fe'``.

    If *symbol* contains no leading ASCII letters (e.g. an empty string or a
    purely numeric token) it is returned as-is after ``.capitalize()``.  Such
    inputs are not valid CIF element symbols and will simply fail the downstream
    covalent-radius lookup, falling back to :data:`DEFAULT_RADIUS`.

    Examples::

        >>> _normalize_element('Ni0+')
        'Ni'
        >>> _normalize_element('Fe3+')
        'Fe'
        >>> _normalize_element('O1-')
        'O'
        >>> _normalize_element('C')
        'C'
    """
    m = _ELEMENT_LETTERS_RE.match(symbol)
    return m.group(0).capitalize() if m else symbol.capitalize()


BOND_TOLERANCE: float = 0.40

# Occupancy at which an atom counts as fully occupied, and therefore as shared
# between all disorder alternatives rather than being one of them.
FULL_OCCUPANCY: float = 0.99

# Two hydrogens are never bonded to each other.  Their covalent-radii cutoff of
# 1.4 A would otherwise turn a short H...H contact into a bond, which happens
# between the alternative positions of a disordered molecule and fuses them into
# one oversized fragment.  Real H...H contacts never fall below the van der
# Waals range, so no genuine bond is lost.
_HYDROGEN: frozenset[str] = frozenset({'H', 'D'})


def _atom_element(atom: AtomRecord) -> str:
    """Return the raw type symbol of a component atom (oxidation suffix included)."""
    return atom[0]


def _atom_occupancy(atom: AtomRecord) -> float:
    """Return the site occupancy of a component atom."""
    return float(atom[1])


def _atom_neighbours(atom: AtomRecord) -> tuple[tuple[str, int], ...]:
    """Return the ``(element, degree)`` pairs of a component atom's non-metal neighbours."""
    return atom[2] if len(atom) > 2 else ()


def _disorder_group(atom) -> int:
    """Return the ``_atom_site_disorder_group`` of an ASU atom record as an int.

    Unparseable or absent values are reported as 0 (an ordered atom).
    """
    try:
        return int(atom[5])
    except (TypeError, ValueError, IndexError):
        return 0


def _expanded_disorder_group(atom: ExpandedAtom) -> int:
    """Return the disorder group of an expanded site, or 0 when it carries none."""
    return int(atom[3]) if len(atom) > 3 else 0


def _parts_may_bond(first: int, second: int,
                    first_occupancy: float = 0.0, second_occupancy: float = 0.0) -> bool:
    """Return ``True`` when two atoms of the given disorder groups may be bonded.

    Following the SHELXL ``PART`` convention, atoms belonging to *different*
    non-zero disorder groups are alternative positions of the same region of the
    structure and are never bonded to each other.  Atoms of group 0 are ordered
    and bond to everything, which keeps a molecule whose disordered side chain is
    split over several PARTs in one piece.

    Without this rule two different solvent molecules sharing one pocket (e.g.
    benzene in PART 1 and fluorobenzene in PART 2) are fused into a single
    bond-graph component whose composition is a meaningless average of both,
    such as ``'C6 H5.78 F0.22'``.

    A **fully occupied** atom is treated as shared whatever PART it is labelled
    with.  Alternative positions are by definition only partly occupied, so an
    occupancy of one identifies an atom that is present in every alternative.
    Depositors regularly leave such a pivot atom inside one of the PARTs instead
    of PART 0 — a rotationally disordered CF3 group whose carbon sits in PART 1
    while the fluorines are spread over PARTs 1, 2 and 3, for instance.  Without
    this exception the fluorines of PARTs 2 and 3 would be torn off the carbon.
    """
    if first == second or first == 0 or second == 0:
        return True
    return first_occupancy >= FULL_OCCUPANCY or second_occupancy >= FULL_OCCUPANCY

# Decimal precision for occupancy-weighted element counts.  Two decimal places
# is generous enough to absorb rounding errors in SHELXL .res / CIF output
# (e.g. occupancies written as 0.55 + 0.44 summing to 0.99) and small
# imperfections in disorder models, while still preserving meaningful
# fractional ratios (e.g. 0.6 / 0.4 mixed-element disorder).
_OCC_DECIMALS: int = 2

# When a weighted element count is within this tolerance of an integer, snap
# it to that integer for display.  Catches sums like 1.01 / 0.99 that arise
# from rounded occupancies (PART 1 occ=0.55 + PART 2 occ=0.44 = 0.99 → 1).
_OCC_INT_SNAP_TOL: float = 0.05

# A bond-graph component is treated as "uniform occupancy" (a single fractional
# copy of a molecule) when max(occ) − min(occ) ≤ this tolerance.  Otherwise
# the component is treated as multi-part disorder (e.g. PART 1 + PART 2 of
# the same site fused into one component by the bond graph).
_UNIFORM_OCC_TOL: float = 0.05


def _weighted_element_counts(
        component: list[AtomRecord],
) -> dict[str, float]:
    """Return occupancy-weighted element counts for one bond-graph component.

    Each atom contributes its occupancy (not 1) to the corresponding element
    tally.  Element symbols are normalized via :func:`_normalize_element` so
    oxidation-state suffixes are stripped.  Totals are rounded to
    :data:`_OCC_DECIMALS` decimal places.

    This is the central helper that lets the moiety-formula generator handle
    multi-part disorder correctly: a site refined as PART 1 (occ=0.6) + PART 2
    (occ=0.4) of the same element contributes 1.0 to that element's count.
    For mixed-element disorder (e.g. Cl 0.6 / Br 0.4) the fractional values
    are preserved.
    """
    weighted: dict[str, float] = {}
    for atom in component:
        key = _normalize_element(_atom_element(atom))
        weighted[key] = weighted.get(key, 0.0) + _atom_occupancy(atom)
    return {el: round(n, _OCC_DECIMALS) for el, n in weighted.items()}


def _snap_to_int_if_close(value: float) -> float:
    """Return ``round(value)`` if *value* is within :data:`_OCC_INT_SNAP_TOL` of an integer, else *value*."""
    nearest = round(value)
    if abs(value - nearest) <= _OCC_INT_SNAP_TOL:
        return float(nearest)
    return value


@dataclasses.dataclass(frozen=True)
class _ClassifiedComponent:
    """One bond-graph component reduced to the data needed for Z and moiety generation.

    Attributes:
        composition: Element counts identifying the chemical species.
        effective:   How many whole molecules of that species the component
                     represents (``max(occ)`` for a uniform component, ``1.0``
                     for a multi-part disorder aggregate).
        max_occupancy: Highest site occupancy inside the component.
        uniform:     ``True`` when all atoms share the same occupancy.
        modelled_non_h: Number of non-hydrogen atoms actually present in the
                     model, counting every disorder part once and ignoring
                     occupancies.  This is the quantity PLATON sorts its
                     residues on (see :func:`_moiety_formula_impl`).
    """

    composition: dict[str, float]
    effective: float
    max_occupancy: float
    uniform: bool
    modelled_non_h: int

    @property
    def species_key(self) -> tuple:
        """Hashable key grouping components of identical chemical composition."""
        return tuple(sorted((el, round(n, _OCC_DECIMALS))
                            for el, n in self.composition.items()))


def _classify_component(component: list[AtomRecord]) -> _ClassifiedComponent | None:
    """Classify a bond-graph component as uniform-occupancy or multi-part disorder.

    * **Uniform** (all occupancies equal within :data:`_UNIFORM_OCC_TOL`): the raw
      element counts identify the species and ``effective`` is that shared
      occupancy, so two half-occupied solvent copies add up to one molecule.
    * **Multi-part** (PART 1 + PART 2 of the same site fused into one component):
      occupancy-weighted, snap-to-integer counts identify the species and
      ``effective`` is ``1.0``, because the parts together are one molecule.

    Returns ``None`` for an empty component.
    """
    occupancies = [_atom_occupancy(atom) for atom in component]
    if not occupancies:
        return None
    uniform = (max(occupancies) - min(occupancies)) <= _UNIFORM_OCC_TOL
    if uniform:
        composition = {element: float(count) for element, count in
                       Counter(_normalize_element(_atom_element(atom))
                               for atom in component).items()}
        effective = max(occupancies)
    else:
        weighted = _weighted_element_counts(component)
        composition = {element: _snap_to_int_if_close(count) for element, count in weighted.items()}
        effective = 1.0
    modelled_non_h = sum(1 for atom in component
                         if _normalize_element(_atom_element(atom)) != 'H')
    return _ClassifiedComponent(composition=composition, effective=effective,
                                max_occupancy=max(occupancies), uniform=uniform,
                                modelled_non_h=modelled_non_h)


# Tolerance used when testing whether Z' is close to a simple fraction.
_ZPRIME_TOLERANCE: float = 0.05

# Minimum occupancy for an atom to be considered "fully ordered".
# Components whose *highest* occupancy is below this threshold consist entirely
# of partial-occupancy atoms and are treated as minor disordered fragments
# (e.g. disordered solvent with dg=0 and occ=0.5) that should not contribute
# to the GCD-based Z estimate.
# The fallback: when *all* components are below this threshold (e.g. a
# centrosymmetric molecule that sits entirely on an inversion centre and
# therefore has occ=0.5 for every atom), no filtering is applied so that the
# GCD calculation can still proceed correctly.
PARTIAL_OCC_THRESHOLD: float = 0.85

# Valid rotation-symmetry denominators in crystals (1-, 2-, 3-, 4-, 6-fold axes).
# Z' must be k/n for n in this set (k ≥ 1) to be crystallographically meaningful.
_VALID_Z_DENOMINATORS: tuple[int, ...] = (1, 2, 3, 4, 6)

# Tolerances used when comparing occupancy-weighted unit-cell element counts
# with `_chemical_formula_sum × Z`.  Occupancies of a disorder model rarely sum
# to exactly 1, and a squeezed / partially occupied structure may carry a
# genuinely fractional formula (e.g. 'F73.11'), so both an absolute and a
# relative slack are granted.
_FORMULA_ABS_TOL: float = 0.5
_FORMULA_REL_TOL: float = 0.01


@dataclasses.dataclass(frozen=True)
class ZResult:
    """Result of Z estimation with Z' and a reliability indicator.

    Attributes:
        z:               Estimated formula units per unit cell.
        z_prime:         ``z / z_sg`` — formula units per asymmetric unit.
        z_sg:            Number of general positions in the space group.
        formula_derived: ``True`` when Z was obtained from the per-element
                         ratio ``cell_counts / formula`` rather than from the
                         bond-graph GCD.  This happens for polymeric, extended,
                         or inorganic structures where all (or many) atoms in
                         the unit cell form a single connected network, making
                         the GCD method unreliable.
        moiety_formula:  IUCr-formatted ``_chemical_formula_moiety`` string
                         derived from the bond-graph connected components.
                         Empty string when the structure is polymeric/extended
                         (``formula_derived=True``), when there are no atoms,
                         or when generation fails for any reason.

    The ``reliable`` property is ``True`` when *z_prime* is within
    :data:`_ZPRIME_TOLERANCE` of a crystallographically valid fraction k/n,
    where n is from :data:`_VALID_Z_DENOMINATORS` (1, 2, 3, 4, 6) and k ≥ 1.

    This covers all site multiplicities that can arise from the rotation symmetries
    allowed by the crystallographic restriction theorem:

    * n=1 → Z′ = 1, 2, 3, …  (general positions only)
    * n=2 → Z′ = ½, 1, 1½, … (molecule on 2-fold axis or inversion centre)
    * n=3 → Z′ = ⅓, ⅔, 1, … (molecule on 3-fold axis; trigonal/hexagonal groups)
    * n=4 → Z′ = ¼, ½, ¾, … (molecule on 4-fold axis; tetragonal groups)
    * n=6 → Z′ = ⅙, ⅓, ½, … (molecule on 6-fold axis; hexagonal groups)

    Values outside this set indicate that the bond-graph GCD algorithm
    lost track of the true formula-unit count (e.g. infinite frameworks,
    polymers, or multi-component systems whose species counts share no
    common factor with the correct Z).
    """

    z: int
    z_prime: float
    z_sg: int
    formula_derived: bool = False
    moiety_formula: str = ''

    @property
    def reliable(self) -> bool:
        """``True`` when *z_prime* is a plausible crystallographic value.

        Checks whether *z_prime* is within :data:`_ZPRIME_TOLERANCE` of k/n
        for any *n* in :data:`_VALID_Z_DENOMINATORS` and positive integer *k*,
        restricted to Z′ ≤ 8.  Examples of valid fractions: ⅙, ¼, ⅓, ½, ⅔,
        ¾, 1, 1½, 2, …

        When :attr:`formula_derived` is ``True`` the Z value comes from the
        chemical formula rather than the bond graph, so the Z′ fraction may
        not be a standard molecular-crystal value (e.g. inorganic networks
        can legitimately have Z′ = 1/12 in high-symmetry space groups).
        In that case ``reliable`` is still evaluated by the same rules, but
        the ``confidence`` property returns ``'formula'`` instead of ``'low'``
        so callers can distinguish the two situations.
        """
        if self.z_prime <= 0 or self.z_prime > 8.0:
            return False
        for denom in _VALID_Z_DENOMINATORS:
            for k in range(1, int(8.0 * denom) + 1):
                if abs(self.z_prime - k / denom) < _ZPRIME_TOLERANCE:
                    return True
        return False

    @property
    def confidence(self) -> str:
        """A short human-readable confidence indicator.

        * **high**    — Z′ is a positive integer (1, 2, 3, …): the most common,
          most reliable case.
        * **medium**  — Z′ is a non-integer crystallographic fraction (½, ⅓, ¼,
          ⅙, ⅔, …): the molecule may sit on a crystallographic special position;
          the bond-graph Z could be an integer multiple of the true value.
        * **formula** — Z was derived from the chemical formula because the
          bond-graph GCD is unreliable (typical for coordination polymers,
          metal–organic frameworks, or inorganic extended structures).
        * **low**     — Z′ is not a multiple of any of 1, ½, ⅓, ¼, or ⅙, or is
          outside (0, 8]: the estimate is unlikely to match the true
          crystallographic Z.
        """
        if self.formula_derived:
            return 'formula'
        if not self.reliable:
            return 'low'
        # Distinguish integer Z' from non-integer crystallographic fraction
        if abs(self.z_prime - round(self.z_prime)) < _ZPRIME_TOLERANCE:
            return 'high'
        return 'medium'


def _get_radius(element: str) -> float:
    """Return the covalent radius (Å) for *element*, falling back to DEFAULT_RADIUS.

    The *element* string is first passed through :func:`_normalize_element` to
    strip any oxidation-state suffix (e.g. ``'Fe3+'`` → ``'Fe'``) before the
    table lookup, ensuring correct bond cutoffs for ionic/inorganic structures.
    """
    return _ELEMENT2COV.get(_normalize_element(element), DEFAULT_RADIUS)


# ---------------------------------------------------------------------------
# Step 1 - disorder filtering
# ---------------------------------------------------------------------------

def _filter_disorder(atoms_fract: list) -> list:
    """Keep only ordered atoms and the primary disorder component.

    Rules:
    * disorder_group == 0  → ordered atom, always included.
    * abs(disorder_group) == 1  → the 'A' (first) component; included.
    * abs(disorder_group) >= 2  → alternative component; excluded.

    Because the occupancies of all components at one site sum to 1, selecting
    only the primary component faithfully represents each site exactly once.
    """
    kept = []
    for atom in atoms_fract:
        dg = atom[5]
        try:
            dg = int(dg)
        except (TypeError, ValueError):
            dg = 0
        if dg == 0 or abs(dg) == 1:
            kept.append(atom)
    return kept


def _split_disorder(atoms_fract: list) -> tuple[list, list]:
    """Split ASU atoms into *regular* and *negative-PART special-position* lists.

    SHELXL ``PART -n`` for any negative ``n`` (``disorder_group < 0``) marks
    atoms that are disordered over a crystallographic special position of
    higher symmetry than the molecule can occupy (e.g. a methanol on a 2-fold
    axis, or several solvent fragments each on its own special position with
    distinct negative PART numbers).  The SHELXL manual states that bonds to
    symmetry-generated copies of negative-PART atoms must be *excluded*.
    Expanding them with the full space-group symmetry and then running the
    bond graph therefore produces wrong molecular components (copies that
    are sub-Å apart get incorrectly fused).

    All non-negative disorder groups (0, 1, 2, 3, …) are retained as *regular*
    atoms.  Per-site occupancies of all parts always sum to ≈1, so keeping
    every part is the correct way to obtain occupancy-weighted element
    counts for moiety-formula generation.  Bond detection across partial
    copies of the same site is harmless because the copies sit within a
    fraction of an Å of each other and end up in the same connected
    component, and the occupancy-weighted element counter in
    :func:`_moiety_formula_impl` then collapses them to integer counts.

    Returns:
        ``(regular, special)`` where:

        * *regular* — atoms with ``disorder_group >= 0`` (i.e. 0, 1, 2, …);
          safe to expand with all symmetry operations.
        * *special* — atoms with ``disorder_group < 0`` (i.e. -1, -2, -3, …);
          must **not** be symmetry-expanded.  Their moiety contribution is
          computed directly from the ASU occupancy via :func:`_asu_components`.
    """
    regular: list = []
    special: list = []
    for atom in atoms_fract:
        dg = atom[5]
        try:
            dg = int(dg)
        except (TypeError, ValueError):
            dg = 0
        if dg < 0:
            special.append(atom)
        else:
            regular.append(atom)
    return regular, special


# ---------------------------------------------------------------------------
# Step 2 - unit-cell expansion via gemmi SmallStructure
# ---------------------------------------------------------------------------

def _expand_to_unit_cell(
        filtered: list,
        symmops: list[str],
        cell: tuple[float, ...],
) -> list[ExpandedAtom]:
    """Expand the filtered ASU atoms to the full unit cell using gemmi.

    A minimal :class:`gemmi.SmallStructure` is constructed from *filtered*,
    *symmops*, and *cell*.  ``SmallStructure.get_all_unit_cell_sites()``
    then applies every space-group operation and deduplicates atoms that
    land on the same fractional position (special positions) using gemmi's
    own robust engine — no arbitrary deduplication threshold is needed.

    The disorder group of every site is carried along so that
    :func:`_build_bond_graph` can keep alternative disorder components apart.

    Fractional coordinates are wrapped into ``[0, 1)`` afterwards.  Deposited
    coordinates frequently lie outside that range (values such as 1.063 are
    common), and gemmi passes them through unchanged, so the symmetry copies of
    one molecule can end up spread over three cells.  The ±1 image search in
    :func:`_build_bond_graph` cannot bridge that, which tears molecules apart.
    Wrapping puts every site into one cell, where ±1 images are sufficient.

    Returns:
        List of ``(element_symbol, (fx, fy, fz), occupancy, disorder_group)``
        tuples covering all symmetry-equivalent sites in the conventional
        unit cell.
    """
    a, b, c, alpha, beta, gamma = cell[:6]

    ss = gemmi.SmallStructure()
    ss.cell = gemmi.UnitCell(a, b, c, alpha, beta, gamma)

    # Resolve the space group from the symmetry-operation strings.
    # gemmi.find_spacegroup_by_ops handles standard and non-standard settings.
    group_ops = gemmi.GroupOps([gemmi.Op(s) for s in symmops])
    sg = gemmi.find_spacegroup_by_ops(group_ops)
    if sg is not None:
        ss.spacegroup = sg

    for atom in filtered:
        site = gemmi.SmallStructure.Site()
        site.label = str(atom[0])
        site.type_symbol = str(atom[1])
        site.fract = gemmi.Fractional(float(atom[2]), float(atom[3]), float(atom[4]))
        site.occ = float(atom[6])
        site.disorder_group = _disorder_group(atom)
        ss.sites.append(site)

    ss.setup_cell_images()
    all_sites = ss.get_all_unit_cell_sites()

    return [
        (s.type_symbol,
         (s.fract.x - math.floor(s.fract.x),
          s.fract.y - math.floor(s.fract.y),
          s.fract.z - math.floor(s.fract.z)),
         s.occ, s.disorder_group)
        for s in all_sites
    ]


# ---------------------------------------------------------------------------
# Step 3 - bond graph construction
# ---------------------------------------------------------------------------

def _build_bond_graph(
        expanded: list[ExpandedAtom],
        cell: tuple[float, ...],
) -> dict[int, set[int]]:
    """Build an adjacency dict for all unit-cell atoms.

    Bond detection uses the sum of covalent radii + BOND_TOLERANCE.
    The 27 periodic images of each atom (shifts of +-1 along a, b, c) are
    checked to correctly bond atoms across cell boundaries.

    Atoms belonging to different non-zero disorder groups are never bonded to
    each other (see :func:`_parts_may_bond`), so that alternative positions of
    the same region of the structure end up in separate components.

    Fractional→Cartesian conversion is delegated to
    ``gemmi.UnitCell.orthogonalize()``, which handles all crystal systems
    correctly for any cell metric.

    Performance: a spatial grid built over the 27 image copies of each atom
    reduces the complexity from O(n²) to O(n) for typical crystal structures
    while preserving correct periodic-boundary-condition bonding.
    """
    n = len(expanded)
    adj: dict[int, set[int]] = {i: set() for i in range(n)}
    if n == 0:
        return adj

    a, b, c, alpha, beta, gamma = cell[:6]
    uc = gemmi.UnitCell(a, b, c, alpha, beta, gamma)

    # Cartesian coordinates for all expanded atoms via gemmi.
    orth = [uc.orthogonalize(gemmi.Fractional(*atom[1])) for atom in expanded]
    radii = [_get_radius(atom[0]) for atom in expanded]
    groups = [_expanded_disorder_group(atom) for atom in expanded]
    occupancies = [float(atom[2]) for atom in expanded]
    is_hydrogen = [_normalize_element(atom[0]) in _HYDROGEN for atom in expanded]

    # Maximum possible bond cutoff (largest atom pair + tolerance).
    max_radius = max(radii)
    max_cutoff = 2.0 * max_radius + BOND_TOLERANCE

    # Cartesian cell-translation vectors: a, b, c in Cartesian space.
    a_cart = uc.orthogonalize(gemmi.Fractional(1, 0, 0))
    b_cart = uc.orthogonalize(gemmi.Fractional(0, 1, 0))
    c_cart = uc.orthogonalize(gemmi.Fractional(0, 0, 1))

    # All 27 image translation vectors (including identity {0,0,0}).
    translations = [
        (da * a_cart.x + db * b_cart.x + dc * c_cart.x,
         da * a_cart.y + db * b_cart.y + dc * c_cart.y,
         da * a_cart.z + db * b_cart.z + dc * c_cart.z)
        for da in (-1, 0, 1)
        for db in (-1, 0, 1)
        for dc in (-1, 0, 1)
    ]

    # Grid cell size = max_cutoff ensures that any bonded pair is at most 1
    # grid cell apart.
    cell_size = max(max_cutoff, 1.0)

    # Build an image-extended grid: each atom is registered at all 27 image
    # positions so that cross-boundary bonds are found naturally.
    grid_ext: dict[tuple[int, int, int], list[tuple[int, float, float, float]]] = {}
    for j, pos in enumerate(orth):
        xj, yj, zj = pos.x, pos.y, pos.z
        for tx, ty, tz in translations:
            ix, iy, iz = xj + tx, yj + ty, zj + tz
            key = (math.floor(ix / cell_size),
                   math.floor(iy / cell_size),
                   math.floor(iz / cell_size))
            if key not in grid_ext:
                grid_ext[key] = []
            grid_ext[key].append((j, ix, iy, iz))

    # For each real atom i, search only the 27 neighboring grid cells.
    for i, pos in enumerate(orth):
        xi, yi, zi = pos.x, pos.y, pos.z
        ri = radii[i]
        gx = math.floor(xi / cell_size)
        gy = math.floor(yi / cell_size)
        gz = math.floor(zi / cell_size)
        seen_j: set[int] = set()
        for dgx in (-1, 0, 1):
            for dgy in (-1, 0, 1):
                for dgz in (-1, 0, 1):
                    for j, xj, yj, zj in grid_ext.get((gx + dgx, gy + dgy, gz + dgz), []):
                        if j <= i or j in seen_j:
                            continue
                        if not _parts_may_bond(groups[i], groups[j],
                                               occupancies[i], occupancies[j]):
                            continue
                        # Two hydrogens are never bonded to each other.
                        if is_hydrogen[i] and is_hydrogen[j]:
                            continue
                        rj = radii[j]
                        cutoff_sq = (ri + rj + BOND_TOLERANCE) ** 2
                        dx = xj - xi
                        dy = yj - yi
                        dz = zj - zi
                        if dx * dx + dy * dy + dz * dz < cutoff_sq:
                            adj[i].add(j)
                            adj[j].add(i)
                            seen_j.add(j)
    return adj


# ---------------------------------------------------------------------------
# Step 4 - connected-component counting
# ---------------------------------------------------------------------------

def _count_components(adj: dict[int, set[int]]) -> int:
    """Count connected components of the bond graph via BFS."""
    visited: set[int] = set()
    count = 0
    for start in adj:
        if start not in visited:
            count += 1
            queue: deque[int] = deque([start])
            visited.add(start)
            while queue:
                node = queue.popleft()
                for nbr in adj[node]:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
    return count


def _neighbour_table(
        adj: dict[int, set[int]],
        expanded: list[ExpandedAtom],
) -> dict[int, tuple[tuple[str, int], ...]]:
    """Return, per atom index, the ``(element, degree)`` pairs of its non-metal neighbours.

    *degree* is the neighbour's own number of non-metal neighbours.  Bonds to
    metals are excluded because they are coordinate bonds: a pyridine nitrogen
    coordinating a metal centre is neutral, not a quaternary ammonium ion.
    Knowing each neighbour's degree lets the charge rules recognise terminal
    oxygen atoms (amine *N*-oxides, ylides).
    """
    elements = [_normalize_element(atom[0]) for atom in expanded]
    non_metal_neighbours = {
        i: [j for j in adj[i] if elements[j] not in METALS] for i in adj
    }
    degrees = {i: len(nbrs) for i, nbrs in non_metal_neighbours.items()}
    return {
        i: tuple((elements[j], degrees[j]) for j in sorted(nbrs))
        for i, nbrs in non_metal_neighbours.items()
    }


def _get_components(
        adj: dict[int, set[int]],
        expanded: list[ExpandedAtom],
) -> list[list[AtomRecord]]:
    """Return each connected component as a list of ``(element, occupancy, neighbours)`` records."""
    neighbours = _neighbour_table(adj, expanded)
    visited: set[int] = set()
    components: list[list[AtomRecord]] = []
    for start in adj:
        if start not in visited:
            queue: deque[int] = deque([start])
            visited.add(start)
            comp: list[AtomRecord] = []
            while queue:
                node = queue.popleft()
                atom = expanded[node]
                comp.append((atom[0], atom[2], neighbours[node]))
                for nbr in adj[node]:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
            components.append(comp)
    return components


def _asu_components(
        special_atoms: list,
        cell: tuple[float, ...],
) -> list[list[AtomRecord]]:
    """Return connected components for negative-PART ASU atoms without symmetry expansion.

    Reuses :func:`_build_bond_graph` and :func:`_get_components` on the raw
    ASU atom list — no symmetry operations are applied — so atoms from distinct
    symmetry copies are never placed in the same graph and cannot be incorrectly
    fused.  Atoms from different negative PART numbers (-1, -2, -3, …) are
    processed together; the bond graph naturally groups them into separate
    components whenever they sit at different special positions, and into the
    same component when they form one chemical fragment (e.g. a single solvent
    molecule split across two negative PART labels).

    The ±1-cell-image search in :func:`_build_bond_graph` correctly handles
    O–H bonds whose donor and acceptor straddle a cell face (e.g. O at
    z = 1.04 bonded to H at z = 0.97).

    Args:
        special_atoms: Atoms with ``disorder_group < 0`` (any negative PART —
                       -1, -2, -3, …) from ``CifContainer.atoms_fract``
                       (same record format).
        cell:          Cell parameters ``(a, b, c, alpha, beta, gamma)``.

    Returns:
        List of connected components, each a list of ``(element, occupancy)``
        pairs — identical in structure to the output of :func:`_get_components`.
    """
    if not special_atoms:
        return []
    expanded = [
        (str(atom[1]), (float(atom[2]), float(atom[3]), float(atom[4])), float(atom[6]),
         _disorder_group(atom))
        for atom in special_atoms
    ]
    adj = _build_bond_graph(expanded, cell)
    return _get_components(adj, expanded)


def _z_from_components(components: list[list[AtomRecord]]) -> int | SupportsIndex:
    """Derive Z as the GCD of per-species molecule counts in the unit cell.

    Each distinct molecular species (identified by its elemental composition)
    appears exactly Z times in the unit cell.  Taking the GCD of those
    per-species counts gives Z without needing a packing coefficient.

    Components are reduced via :func:`_classify_component`, so a molecule that
    is disordered over two PARTs contributes ``1.0`` instead of appearing as
    two independent fractional species.  This matters for structures where only
    *some* copies of a species are disordered: eight anions of which two are
    PART-split would otherwise be counted as ``6 + 2 + 2`` and drag the GCD
    down to 2 instead of 8.

    A species enters the GCD only when

    * at least one of its components is (near-)fully occupied
      (``max(occ) ≥`` :data:`PARTIAL_OCC_THRESHOLD`), and
    * its summed molecule count is (near-)integral — fractionally disordered
      solvent (e.g. benzene/fluorobenzene sharing one site) never adds up to a
      whole number of molecules and must not constrain Z.

    If no species survives those filters, the rounded effective molecule count
    per species is used instead (e.g. a centrosymmetric molecule sitting
    entirely on an inversion centre, where every atom has ``occ = 0.5``).

    Examples
    --------
    * Simple organic (2 copies, same formula): GCD({formula: 2}) = 2.
    * Salt like R·HCl (4 organic + 4 Cl⁻): GCD({org: 4, Cl: 4}) = 4.
    * 1:1 co-crystal (4+4 of two different species): GCD = 4.
    * Z=2 organic + disordered solvent (occ=0.5, count=1): GCD({org: 2}) = 2.
    * Salt with 8 anions (2 of them PART-split) + 4 cations: GCD({8, 4}) = 4.

    Known limitation
    ----------------
    Solvate molecules sitting on a crystallographic special position appear
    fewer times in the expanded cell than the space-group multiplicity would
    suggest (they are deduplicated during expansion).  In such structures the
    returned Z may be lower than the CIF value.
    """
    if not components:
        return 1

    classified = [item for item in map(_classify_component, components) if item is not None]
    if not classified:
        return 1

    species: dict[tuple, list[_ClassifiedComponent]] = {}
    for item in classified:
        species.setdefault(item.species_key, []).append(item)

    whole_molecule_counts: list[int] = []
    for group in species.values():
        if max(item.max_occupancy for item in group) < PARTIAL_OCC_THRESHOLD:
            continue
        total = sum(item.effective for item in group)
        if abs(total - round(total)) > _OCC_INT_SNAP_TOL or round(total) < 1:
            continue
        whole_molecule_counts.append(round(total))

    if not whole_molecule_counts:
        # Fallback: no species is both fully occupied and integral (e.g. a
        # molecule that sits entirely on an inversion centre, or a site that is
        # split over two PARTs which the bond graph could not fuse).  Use the
        # rounded effective molecule count per species, but never below one.
        whole_molecule_counts = [
            max(1, round(sum(item.effective for item in group)))
            for group in species.values()
        ]

    return reduce(gcd, whole_molecule_counts)


# ---------------------------------------------------------------------------
# Moiety formula generation
# ---------------------------------------------------------------------------

def _composition_to_hill_str(comp_dict: dict[str, float]) -> str:
    """Format an element-count dict as a Hill-ordered CIF moiety formula token.

    Hill order: C first, H second (when C is present), then all remaining
    elements alphabetically.  Counts may be ``int`` or ``float``:

    * A count of exactly 1 (or 1.0) is written without a numeric suffix
      (``O`` not ``O1``), matching IUCr CIF convention.
    * Integer-valued floats are formatted as plain integers (``C10`` not
      ``C10.0``).  A count is treated as integer when it is within
      :data:`_OCC_INT_SNAP_TOL` of the nearest whole number.
    * Genuine fractional counts (e.g. partial-occupancy mixed-element
      disorder such as ``Cl0.6 Br0.4``) are formatted with up to
      :data:`_OCC_DECIMALS` decimal places, with trailing zeros stripped.
    * Counts that round to 0 at :data:`_OCC_DECIMALS` precision are
      omitted entirely.

    The returned parts are joined with a single space so the result looks
    like ``'C10 H8 N2 O'`` — matching the style used in COD CIF files and
    accepted by IUCr validation.

    Examples::

        >>> _composition_to_hill_str({'C': 10, 'H': 8, 'N': 2, 'O': 1})
        'C10 H8 N2 O'
        >>> _composition_to_hill_str({'C': 9.0, 'H': 9.0, 'Br': 0.6, 'Cl': 0.4})
        'C9 H9 Br0.6 Cl0.4'
        >>> _composition_to_hill_str({'Cl': 1})
        'Cl'
    """

    def _format_count(n: float) -> str:
        nearest = round(n)
        if abs(n - nearest) <= _OCC_INT_SNAP_TOL:
            return '' if nearest == 1 else str(int(nearest))
        # Fractional: keep up to _OCC_DECIMALS, strip trailing zeros.
        text = f'{n:.{_OCC_DECIMALS}f}'.rstrip('0').rstrip('.')
        return text or '0'

    def _is_visible(n: float) -> bool:
        return round(n, _OCC_DECIMALS) > 0

    parts: list[str] = []
    has_c = 'C' in comp_dict and _is_visible(comp_dict['C'])

    if has_c:
        parts.append(f'C{_format_count(comp_dict["C"])}')

    if 'H' in comp_dict and has_c and _is_visible(comp_dict['H']):
        parts.append(f'H{_format_count(comp_dict["H"])}')

    for el in sorted(comp_dict):
        if el == 'C' and has_c:
            continue
        if el == 'H' and has_c:
            continue
        n = comp_dict[el]
        if not _is_visible(n):
            continue
        parts.append(f'{el}{_format_count(n)}')

    return ' '.join(parts)


def moiety_formula_from_components(
        components: list[list[AtomRecord]],
        z: int,
        formula_derived: bool = False,
        formula_sum_dict: dict[str, float] | None = None,
) -> str:
    """Generate an IUCr ``_chemical_formula_moiety`` string from bond-graph components.

    Uses the occupancy-weighted effective count of each molecular species to
    derive the per-formula-unit multipliers, following the convention discussed
    in the crystallographic community (Peter Zavalij / Alejandro Metta et al.):

    * The **main molecule** (highest effective count) always gets an integer
      multiplier ≥ 1.  For the simplest case (one formula unit per ASU,
      Z′ = 1) the multiplier is exactly 1 and the parentheses are omitted.
    * **Solvent / co-former** counts may be fractional (e.g. ``0.75(H2 O)``
      when a water site has occupancy 0.75 and the same Wyckoff multiplicity
      as the main molecule).

    The effective count for a species accounts for partial occupancy: each
    component contributes ``max(occ)`` to the total, so a pair of half-occupied
    water molecules (occ = 0.5) contribute 1.0 to the effective count, giving
    a ratio of ``1.0 / Z`` per formula unit.

    The moieties are listed in PLATON's order — see :func:`_moiety_formula_impl`.

    **Polymeric / extended structures** (``formula_derived=True``):
    When *formula_sum_dict* is supplied, the per-formula-unit chemical formula
    is expressed as a single moiety token (e.g. ``'C24 H16 N4 Zn'`` for a Zn-MOF
    or ``'As Ni'`` for NiAs).  This matches what crystallographic software such as
    PLATON reports for coordination polymers and inorganic frameworks, where no
    discrete molecular species can be identified.  Returns ``''`` if
    *formula_derived=True* but *formula_sum_dict* is ``None``.

    Returns an empty string when:

    * ``formula_derived=True`` and no *formula_sum_dict* is provided.
    * ``z ≤ 0`` or *components* is empty (and no formula fallback).
    * Any unexpected exception during generation.

    Args:
        components:       Output of :func:`_get_components` — a list of
                          components where each component is a list of
                          ``(element, occupancy, neighbours)`` records.  Plain
                          ``(element, occupancy)`` pairs are accepted too; the
                          charge rules that need connectivity are then skipped.
        z:                Number of formula units per unit cell (from
                          :func:`_z_from_components` after formula correction).
        formula_derived:  Set to ``True`` for polymeric/extended structures
                          (see :class:`ZResult`).
        formula_sum_dict: Parsed ``_chemical_formula_sum`` dict (from
                          :func:`_parse_formula_sum`), used as a fallback
                          moiety for polymeric structures.

    Returns:
        IUCr-formatted moiety formula string, e.g.
        ``'C10 H8 N2, 0.75(H2 O)'`` or ``'C9 H9 Br Cl N2 1+, B F4 1-'``,
        or ``''`` on failure.
    """
    if formula_derived:
        # When formula_derived is True, the bond-graph GCD didn't match the
        # formula.  However, if the bond graph still identified multiple
        # *distinct* molecular species (> 1 composition type), the component-
        # based moiety is likely more informative than a flat formula.  Only
        # fall back to the flat formula when the bond graph truly failed to
        # separate species (≤ 1 distinct composition = polymeric network).
        if components and z > 0:
            try:
                result = _moiety_formula_impl(components, z)
                if result and ', ' in result:
                    # Multi-species moiety found — use it instead of flat formula.
                    return result
            except Exception:
                pass
        # True polymeric / single-species fallback.
        if formula_sum_dict:
            return _formula_dict_to_moiety_str(formula_sum_dict)
        return ''

    if not components or z <= 0:
        return ''

    try:
        return _moiety_formula_impl(components, z)
    except Exception:
        return ''


def _formula_dict_to_moiety_str(formula: dict[str, float]) -> str:
    """Format a parsed ``_chemical_formula_sum`` dict as a Hill-ordered moiety string.

    Used for polymeric / extended structures where discrete molecular components
    cannot be identified by the bond graph.  The per-formula-unit composition
    from ``_chemical_formula_sum`` is expressed as a single moiety token.

    Non-positive or very small counts (< 0.1) are discarded.  All remaining
    counts are rounded to the nearest integer before formatting, producing a
    valid IUCr formula token.  Returns an empty string when no valid elements
    remain.

    Examples::

        >>> _formula_dict_to_moiety_str({'As': 1.0, 'Ni': 1.0})
        'As Ni'
        >>> _formula_dict_to_moiety_str({'C': 24.0, 'H': 16.0, 'N': 4.0, 'Zn': 1.0})
        'C24 H16 N4 Zn'
    """
    int_counts = {el: round(n) for el, n in formula.items() if n >= 0.1}
    if not int_counts:
        return ''
    return _composition_to_hill_str(int_counts)


def _charge_atoms(component: list[AtomRecord]) -> tuple[ChargeAtom, ...]:
    """Convert a bond-graph component into :class:`ChargeAtom` records."""
    return tuple(
        ChargeAtom(
            element=_normalize_element(_atom_element(atom)),
            occupancy=_atom_occupancy(atom),
            neighbours=_atom_neighbours(atom),
            oxidation=parse_oxidation_state(_atom_element(atom)),
        )
        for atom in component
    )


def _format_moiety_token(formula_str: str, ratio: float, charge: int) -> str:
    """Format one moiety following the IUCr ``_chemical_formula_moiety`` rules.

    The charge token is appended after a space (``'B F4 1-'``) and a multiplier
    other than one wraps the whole moiety in parentheses (``'2(N O3 1-)'``).
    """
    charge_token = format_charge(charge)
    token = f'{formula_str} {charge_token}' if charge_token else formula_str

    nearest_int = round(ratio)
    if abs(ratio - nearest_int) < 1e-4:
        return token if nearest_int == 1 else f'{nearest_int}({token})'
    return f'{ratio:.4g}({token})'


def _composition_multiple(bigger: dict[str, float], smaller: dict[str, float]) -> int | None:
    """Return *k* when *bigger* is exactly ``k × smaller`` (k ≥ 2), else ``None``.

    Both compositions must contain the same elements and every element ratio has
    to yield the same integer factor.
    """
    if set(bigger) != set(smaller) or not smaller:
        return None
    factors: set[int] = set()
    for element, count in smaller.items():
        if count <= 0:
            return None
        ratio = bigger[element] / count
        nearest = round(ratio)
        if nearest < 2 or abs(ratio - nearest) > 1e-6:
            return None
        factors.add(nearest)
    return factors.pop() if len(factors) == 1 else None


def _is_integral(value: float) -> bool:
    """Return ``True`` when *value* is within rounding noise of a whole number."""
    return abs(value - round(value)) < 1e-4


def _merge_multiple_species(
        species: list[tuple[dict[str, float], float, bool, float, FragmentCharge, int, int]],
        z: int,
) -> list[tuple[dict[str, float], float, bool, float, FragmentCharge, int, int]]:
    """Fold aggregate species back into the monomer they are a multiple of.

    A molecule that is bonded to a symmetry copy of itself shows up twice: once
    whole and once as the fused aggregate, both with fractional multipliers, as
    in ``'0.25(C50 H72 K2 N8 Ni2 O4), 0.5(C25 H36 K N4 Ni O2)'`` where the
    aggregate is exactly twice the monomer.  Chemically there is only the
    monomer, and PLATON reports it as such.

    An aggregate is folded into its monomer only when

    * its composition is an exact integer multiple of the monomer's,
    * at least one of the two multipliers is fractional, and
    * the combined multiplier lands on a whole number.

    The last condition is what makes the rule safe: a genuine mixture of a
    dimer and a monomer keeps two independent multipliers that do not add up,
    and stays untouched.  So does ``'2(H2 O), 0.03833(H12 O6)'``, where the
    hexamer is a real, separate species.

    The monomer's own charge is kept, because it was perceived from that
    fragment's connectivity.
    """
    if z <= 0:
        return species
    merged = list(species)
    while True:
        for i, aggregate in enumerate(merged):
            for j, monomer in enumerate(merged):
                if i == j or aggregate[3] <= monomer[3]:
                    continue
                factor = _composition_multiple(aggregate[0], monomer[0])
                if factor is None:
                    continue
                if _is_integral(aggregate[1] / z) and _is_integral(monomer[1] / z):
                    continue
                total = monomer[1] + factor * aggregate[1]
                if not _is_integral(total / z):
                    continue
                merged[j] = (monomer[0], total, monomer[2] or aggregate[2],
                             monomer[3], monomer[4],
                             max(monomer[5], aggregate[5]),
                             min(monomer[6], aggregate[6]))
                del merged[i]
                break
            else:
                continue
            break
        else:
            return merged


def _moiety_formula_impl(
        components: list[list[AtomRecord]],
        z: int,
) -> str:
    """Inner implementation — called only by :func:`moiety_formula_from_components`.

    Each component is classified as either *uniform-occupancy* (all atoms share
    the same occupancy within :data:`_UNIFORM_OCC_TOL`) or *multi-part disorder*
    (atoms with varied occupancies, typically PART 1 + PART 2 of the same site
    that fused into one bond-graph component):

    * **Uniform**: composition keeps raw element counts; ``effective`` = the
      uniform occupancy.  This preserves fractional multipliers for half-
      occupancy solvates (e.g. ``0.5(C H4 O)``).
    * **Multi-part**: composition uses occupancy-weighted, snap-to-integer
      element counts (so PART 1 occ=0.6 + PART 2 occ=0.4 of the same atom
      yield count 1); ``effective`` = 1.0 because the parts together represent
      one whole physical molecule.

    Every species is finally given the formal charge perceived by
    :mod:`finalcif.tools.formal_charge` and balanced across the formula unit.

    The moieties are ordered the way PLATON orders them: by descending number
    of non-hydrogen atoms *as modelled*, i.e. every disorder part is counted
    once and occupancies are ignored.  A heavily disordered small ion can
    therefore precede a larger but fully ordered molecule.  The IUCr rules
    (``docs/formula_definitions.txt``) do not prescribe an order between
    moieties, but checkCIF raises ``042_ALERT_1_C`` when the reported sequence
    differs from PLATON's.  Charges are not part of that comparison — PLATON
    skips blanks and charge tokens while comparing the strings.
    """
    # Classify components and build per-component (comp_dict, effective, charge, non_h) tuples.
    classified: list[tuple[dict[str, float], float, FragmentCharge, int]] = []
    for comp in components:
        item = _classify_component(comp)
        if item is None:
            continue
        charge = perceive_fragment_charge(_charge_atoms(comp), item.composition,
                                          weighted=not item.uniform)
        classified.append((item.composition, item.effective, charge, item.modelled_non_h))

    if not classified:
        return ''

    # Group by composition and charge (rounded for float-stable equality).
    comp_groups: dict[tuple, list[tuple[dict[str, float], float, FragmentCharge, int]]] = {}
    for comp_dict, effective, charge, non_h in classified:
        key = (tuple(sorted((el, round(n, _OCC_DECIMALS)) for el, n in comp_dict.items())),
               charge.charge, charge.confident)
        comp_groups.setdefault(key, []).append((comp_dict, effective, charge, non_h))

    # For each species compute total effective count and an "is_major" flag.
    species: list[tuple[dict[str, float], float, bool, float, FragmentCharge, int, int]] = []
    for order, (_key, group) in enumerate(comp_groups.items()):
        total_effective = sum(eff for _cd, eff, _q, _nh in group)
        is_major = max(eff for _cd, eff, _q, _nh in group) >= PARTIAL_OCC_THRESHOLD
        comp_dict = group[0][0]
        atoms_per_mol = sum(comp_dict.values())
        max_non_h = max(nh for _cd, _eff, _q, nh in group)
        species.append((comp_dict, total_effective, is_major, atoms_per_mol,
                        group[0][2], max_non_h, order))

    species = _merge_multiple_species(species, z)

    # PLATON orders the moieties of `_chemical_formula_moiety` by descending
    # number of non-hydrogen atoms *as modelled* — every disorder part counts
    # once and occupancies are ignored (PLA283 prints the residues in the order
    # established by the GEN022 sort in platon_special.f).  Following that order
    # avoids checkCIF's `042_ALERT_1_C` ("Calc. and Reported MoietyFormula
    # Strings Differ"), which compares the moiety sequence.  Equal counts keep
    # the order in which the species were discovered.
    species.sort(key=lambda x: (-x[5], x[6]))

    entries: list[tuple[str, float, FragmentCharge, float]] = []
    for comp_dict, effective, _is_major, atoms_per_mol, charge, _non_h, _order in species:
        formula_str = _composition_to_hill_str(comp_dict)
        if not formula_str:
            continue
        ratio = round(effective / z, 6)
        if ratio <= 0:
            continue
        entries.append((formula_str, ratio, charge, atoms_per_mol))

    if not entries:
        return ''

    balanced = balance_charges([
        SpeciesCharge(charge=charge.charge, confident=charge.confident,
                      ratio=ratio, atom_count=atoms)
        for _formula, ratio, charge, atoms in entries
    ])
    # An unresolvable imbalance means the perception is untrustworthy — reporting
    # no charge at all is preferable to reporting a wrong one.
    if balanced is None:
        balanced = [0] * len(entries)

    return ', '.join(
        _format_moiety_token(formula_str, ratio, charge)
        for (formula_str, ratio, _perceived, _atoms), charge in zip(entries, balanced, strict=True)
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _parse_formula_sum(formula_sum: str | None) -> dict[str, float] | None:
    """Parse a ``_chemical_formula_sum`` string into ``{element: count}``.

    Returns ``None`` if the input is empty or cannot be parsed.  Whitespace
    between elements is stripped before parsing (matching the convention
    used by :mod:`finalcif.tools.sumformula`).
    """
    if not formula_sum:
        return None
    text = str(formula_sum).strip()
    if not text or text in {'?', '.'}:
        return None
    try:
        return parse_formula(text.replace(' ', ''))
    except Exception:
        return None


def _expanded_element_counts(
        expanded: list[ExpandedAtom],
) -> dict[str, float]:
    """Return occupancy-weighted total atom count per element across all expanded unit-cell sites.

    Each atom contributes its occupancy (not 1) so that PART 1 + PART 2
    disorder, whose per-site occupancies sum to ≈1, yields the same total
    as the corresponding ordered structure.  Element symbols are normalised
    via :func:`_normalize_element` so that oxidation-state suffixes (e.g.
    ``'Ni0+'``, ``'O1-'``) are stripped before aggregation.

    Totals are *not* rounded: a partially occupied solvent site legitimately
    contributes a fractional count that matches a fractional
    ``_chemical_formula_sum`` entry such as ``F73.11``.  Callers compare with
    a relative tolerance (see :data:`_FORMULA_REL_TOL`).
    """
    weighted: dict[str, float] = {}
    for atom in expanded:
        key = _normalize_element(atom[0])
        weighted[key] = weighted.get(key, 0.0) + float(atom[2])
    return weighted


def _counts_agree(actual: float, expected: float) -> bool:
    """Return ``True`` when *actual* matches *expected* within the formula tolerance.

    Both an absolute and a relative tolerance are allowed so that small
    element counts (rounding noise of a few hundredths) and large ones
    (fractional occupancies accumulated over hundreds of sites) are treated
    alike.
    """
    return abs(actual - expected) <= max(_FORMULA_ABS_TOL, _FORMULA_REL_TOL * abs(expected))


def _gcd_matches_formula(
        z_gcd: int,
        cell_counts: dict[str, float],
        formula: dict[str, float],
) -> bool:
    """Return True iff ``cell_counts ≈ formula × z_gcd`` for every non-H element.

    Hydrogen is excluded because riding/omitted hydrogens commonly cause a
    benign mismatch that has no bearing on Z.  All other elements present in
    the formula must match within :func:`_counts_agree`.
    """
    for el, n_per_fu in formula.items():
        if el == 'H' or n_per_fu <= 0:
            continue
        if not _counts_agree(cell_counts.get(el.capitalize(), 0.0), n_per_fu * z_gcd):
            return False
    return True


def _z_from_formula(
        cell_counts: dict[str, float],
        formula: dict[str, float],
) -> int | None:
    """Derive Z from the per-element ratio ``cell_counts / formula``.

    Hydrogen is ignored (see :func:`_gcd_matches_formula`).  Every remaining
    element in the formula must yield the *same* positive integer Z, each
    ratio being integral within :func:`_counts_agree`; otherwise ``None`` is
    returned and the caller falls back to the bond-graph GCD.
    """
    zs: list[int] = []
    for el, n_per_fu in formula.items():
        if el == 'H' or n_per_fu <= 0:
            continue
        n_in_cell = cell_counts.get(el.capitalize(), 0.0)
        if n_in_cell <= 0:
            return None
        ratio = n_in_cell / n_per_fu
        z = int(round(ratio))
        if z < 1 or not _counts_agree(n_in_cell, n_per_fu * z):
            return None
        zs.append(z)
    if not zs:
        return None
    if min(zs) != max(zs):
        return None
    return zs[0]


def _z_sg_from_symmops(symmops: list[str]) -> int:
    """Return the number of general positions (Z_sg) for the given symmetry operations.

    Builds a :class:`gemmi.GroupOps` from *symmops* and looks up the space group.
    If the space group is unrecognised (non-standard setting not in gemmi's table),
    falls back to ``len(symmops)``, which equals the total number of symmetry
    operations including centering translations.
    """
    group_ops = gemmi.GroupOps([gemmi.Op(s) for s in symmops])
    sg = gemmi.find_spacegroup_by_ops(group_ops)
    if sg is not None:
        ops = sg.operations()
        return len(ops.sym_ops) * len(ops.cen_ops)
    return len(symmops)  # fallback: count all provided ops


def count_z(atoms_fract, symmops: list[str], cell: tuple[float, ...],
            max_atoms: int = 5000,
            formula_sum: str | None = None) -> int:
    """Determine Z by packing the unit cell and counting molecular graphs.

    Disorder is handled correctly: only the first component of each disordered
    site (disorder_group in {0, 1, -1}) is retained before expansion, so each
    atomic site contributes exactly once regardless of its occupancy split.

    Unit-cell expansion is performed by :func:`_expand_to_unit_cell`, which
    builds a :class:`gemmi.SmallStructure` and calls
    ``get_all_unit_cell_sites()`` — gemmi's own symmetry engine applies all
    space-group operations and deduplicates atoms on special positions without
    an arbitrary position threshold.

    Fractional→Cartesian conversion in the bond-graph step uses
    ``gemmi.UnitCell.orthogonalize()``, the project's canonical converter.

    When *formula_sum* is supplied (e.g. ``_chemical_formula_sum``), the
    bond-graph GCD result is cross-checked against the expanded unit-cell
    elemental composition.  The GCD is kept whenever it is consistent with
    ``formula × Z_gcd`` for every non-H element.  If the GCD is provably
    inconsistent with the formula — which happens for polymeric/extended
    structures where one connected component spans several formula units
    (e.g. coordination polymers bridged through inversion centres) — Z is
    recomputed from the per-element ratio ``cell_counts / formula`` and used
    instead, provided every non-H element agrees on the same positive
    integer.  Hydrogen is always excluded from this check because riding /
    omitted hydrogens commonly cause benign mismatches.

    Args:
        atoms_fract:  Iterable of atom records as yielded by
                      ``CifContainer.atoms_fract``:
                      ``[label, element, fx, fy, fz, disorder_group, occ, u_iso]``
        symmops:      Symmetry-operation strings from ``CifContainer.symmops``.
        cell:         Cell parameters ``(a, b, c, alpha, beta, gamma)`` in Å/deg.
        max_atoms:    Skip expansion if the expected unit-cell atom count would
                      exceed this limit (avoids quadratic cost for huge structures).
        formula_sum:  Optional value of ``_chemical_formula_sum``; when given
                      and parseable, used to detect and correct cases where
                      the bond-graph GCD undercounts Z (see above).

    Returns:
        Number of formula units per unit cell (Z), at minimum 1.
    """
    z, _formula_derived, _moiety = _count_z_with_source(
        atoms_fract, symmops, cell, max_atoms, formula_sum
    )
    return z


def _combine_components(
        regular_components: list[list[AtomRecord]],
        special_atoms: list,
        n_symmops: int,
        cell: tuple[float, ...],
) -> list[list[AtomRecord]]:
    """Combine regular bond-graph components with negative-PART special-position fragments.

    For each connected component found in the negative-PART ASU atoms
    (``disorder_group < 0`` — i.e. PART -1, -2, -3, …) via
    :func:`_asu_components`, one synthetic copy per symmetry operation is
    appended to *regular_components*.  The regular atoms are symmetry-expanded
    to the whole unit cell, so the special ones have to be replicated the same
    way to end up on the same scale.  Their occupancy already accounts for any
    sharing on a special position, which makes the effective count inside
    :func:`_moiety_formula_impl` equal to ``max_occ × n_symmops`` — the true
    unit-cell content of the fragment.

    Example — methanol at occ = 0.5 in a Z = 4 structure with 4 symmetry
    operations::

        ASU component: [(C, 0.5), (H, 0.5), (H, 0.5), (H, 0.5), (H, 0.5), (O, 0.5)]
        4 copies appended → effective = 4 × 0.5 = 2.0
        ratio = 2.0 / 4 = 0.5  →  '0.5(C H4 O)'  ✓

    Using the symmetry-operation count rather than *Z* matters as soon as
    Z′ ≠ 1.  A toluene at occ = 0.5 in a Z = 2 structure with 4 symmetry
    operations really is ``4 × 0.5 = 2`` molecules per cell, hence one per
    formula unit, not the half a molecule that replicating *Z* times implies.
    """
    if not special_atoms:
        return regular_components
    asu_comps = _asu_components(special_atoms, cell)
    if not asu_comps:
        return regular_components
    return regular_components + asu_comps * max(1, n_symmops)


def _count_z_with_source(
        atoms_fract: list,
        symmops: list[str],
        cell: tuple[float, ...],
        max_atoms: int = 5000,
        formula_sum: str | None = None,
) -> tuple[int, bool, str]:
    """Internal implementation of Z estimation returning ``(z, formula_derived, moiety_formula)``.

    ``formula_derived`` is ``True`` when the formula-based correction overrode
    the bond-graph GCD result.  Used by :func:`count_z_and_zprime` to set the
    :attr:`ZResult.formula_derived` flag for caller-visible confidence reporting.

    ``moiety_formula`` is an IUCr-formatted ``_chemical_formula_moiety`` string
    derived from the bond-graph connected components.  It is an empty string
    when the structure is polymeric/extended or when generation fails.
    """
    if not symmops or symmops == ['']:
        return 1, False, ''

    # Separate regular atoms (dg >= 0) from negative-PART special-position atoms
    # (dg < 0, i.e. PART -1, -2, -3, …).  Only regular atoms are symmetry-expanded;
    # negative-PART atoms are processed as ASU components to avoid spurious
    # inter-copy bonds across symmetry equivalents.
    regular, special = _split_disorder(list(atoms_fract))
    if not regular and not special:
        return 1, False, ''

    # Guard against unreasonably large structures (e.g. proteins, MOFs).
    # Only regular atoms are expanded; special atoms stay in the ASU.
    if len(regular) * len(symmops) > max_atoms:
        return 1, False, ''

    if not regular:
        # Edge case: only negative-PART atoms (unusual).  Fall back to Z=1 and
        # derive the moiety solely from the ASU special components.
        asu_comps = _asu_components(special, cell)
        moiety = moiety_formula_from_components(asu_comps * 1, 1)
        return 1, False, moiety

    expanded = _expand_to_unit_cell(regular, symmops, cell)
    if not expanded:
        return 1, False, ''

    adj = _build_bond_graph(expanded, cell)
    components = _get_components(adj, expanded)
    z = _z_from_components(components)
    z = max(1, z)
    formula_derived = False
    # Preserved after the try block so polymeric structures can use it for moiety.
    parsed_formula: dict[str, float] | None = None

    try:
        # Optional formula-based consistency check / correction.
        parsed_formula = _parse_formula_sum(formula_sum)
        if parsed_formula:
            cell_counts = _expanded_element_counts(expanded)
            if not _gcd_matches_formula(z, cell_counts, parsed_formula):
                z_from_form = _z_from_formula(cell_counts, parsed_formula)
                if z_from_form is not None:
                    z = z_from_form
                    formula_derived = True
    except Exception:
        moiety = moiety_formula_from_components(
            _combine_components(components, special, len(symmops), cell), z, formula_derived=False,
        )
        return z, formula_derived, moiety

    moiety = moiety_formula_from_components(
        _combine_components(components, special, len(symmops), cell), z,
        formula_derived=formula_derived,
        formula_sum_dict=parsed_formula,
    )
    return z, formula_derived, moiety


def count_z_and_zprime(
        atoms_fract,
        symmops: list[str],
        cell: tuple[float, ...],
        max_atoms: int = 5000,
        formula_sum: str | None = None,
) -> ZResult:
    """Determine Z and Z′ by packing the unit cell and counting molecular graphs.

    Extends :func:`count_z` with a Z′ value and a reliability indicator.

    Z′ = Z / Z_sg, where Z_sg is the number of general positions in the space
    group (the maximum Z for a structure with all atoms in general positions).

    Crystallographically valid Z′ values are positive multiples of 1/n where
    n is a permitted rotation-symmetry order (1, 2, 3, 4, or 6):

    * **Z′ = 1** (most common) — one formula unit per asymmetric unit.
    * **Z′ = ½** — molecule on a 2-fold axis or inversion centre.
    * **Z′ = ⅓** — molecule on a 3-fold axis (trigonal / hexagonal groups).
    * **Z′ = ¼** — molecule on a 4-fold axis (tetragonal groups).
    * **Z′ = ⅙** — molecule on a 6-fold axis (hexagonal groups).
    * **Z′ = 2, 3, …** — multiple independent formula units in the ASU.

    A Z′ that is *not* close to any k/n (n ∈ {1,2,3,4,6}) signals that the
    bond-graph GCD algorithm returned an incorrect Z (typically an undercount
    for polymeric or multi-component structures).  When the chemical formula is
    provided and overrides the bond-graph result, :attr:`ZResult.formula_derived`
    is set to ``True`` and :attr:`ZResult.confidence` returns ``'formula'``.

    Args:
        atoms_fract:  Atom records as yielded by ``CifContainer.atoms_fract``.
        symmops:      Symmetry-operation strings from ``CifContainer.symmops``.
        cell:         Cell parameters ``(a, b, c, alpha, beta, gamma)`` in Å/deg.
        max_atoms:    Expansion guard (see :func:`count_z`).
        formula_sum:  Optional ``_chemical_formula_sum`` string; see
                      :func:`count_z` for how it is used to correct Z.

    Returns:
        A :class:`ZResult` with ``z``, ``z_prime``, ``z_sg``, ``formula_derived``,
        ``reliable``, and ``confidence`` attributes.
    """
    z, formula_derived, moiety = _count_z_with_source(
        atoms_fract, symmops, cell, max_atoms, formula_sum
    )
    z_sg = _z_sg_from_symmops(symmops) if symmops and symmops != [''] else 1
    z_prime = round(z / z_sg, 6) if z_sg > 0 else float('nan')
    return ZResult(z=z, z_prime=z_prime, z_sg=z_sg, formula_derived=formula_derived,
                   moiety_formula=moiety)
