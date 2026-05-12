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

import gemmi

from fastmolwidget.molecule2D import calc_volume  # re-exported for callers
from finalcif.cif.atoms import element2cov as _ELEMENT2COV
from finalcif.tools.chemparse import parse_formula as _parse_formula

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


# ---------------------------------------------------------------------------
# Step 2 - unit-cell expansion via gemmi SmallStructure
# ---------------------------------------------------------------------------

def _expand_to_unit_cell(
        filtered: list,
        symmops: list[str],
        cell: tuple[float, ...],
) -> list[tuple[str, tuple[float, float, float]]]:
    """Expand the filtered ASU atoms to the full unit cell using gemmi.

    A minimal :class:`gemmi.SmallStructure` is constructed from *filtered*,
    *symmops*, and *cell*.  ``SmallStructure.get_all_unit_cell_sites()``
    then applies every space-group operation and deduplicates atoms that
    land on the same fractional position (special positions) using gemmi's
    own robust engine — no arbitrary deduplication threshold is needed.

    Returns:
        List of ``(element_symbol, (fx, fy, fz))`` tuples covering all
        symmetry-equivalent sites in the conventional unit cell.
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
        ss.sites.append(site)

    ss.setup_cell_images()
    all_sites = ss.get_all_unit_cell_sites()

    return [
        (s.type_symbol, (s.fract.x, s.fract.y, s.fract.z), s.occ)
        for s in all_sites
    ]


# ---------------------------------------------------------------------------
# Step 3 - bond graph construction
# ---------------------------------------------------------------------------

def _build_bond_graph(
        expanded: list[tuple[str, tuple[float, float, float]]],
        cell: tuple[float, ...],
) -> dict[int, set[int]]:
    """Build an adjacency dict for all unit-cell atoms.

    Bond detection uses the sum of covalent radii + BOND_TOLERANCE.
    The 27 periodic images of each atom (shifts of +-1 along a, b, c) are
    checked to correctly bond atoms across cell boundaries.

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
    orth = [uc.orthogonalize(gemmi.Fractional(*pos)) for _, pos, _occ in expanded]
    radii = [_get_radius(el) for el, _pos, _occ in expanded]

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


def _get_components(
        adj: dict[int, set[int]],
        expanded: list[tuple[str, tuple[float, float, float], float]],
) -> list[list[tuple[str, float]]]:
    """Return each connected component as a list of ``(element, occupancy)`` pairs."""
    visited: set[int] = set()
    components: list[list[tuple[str, float]]] = []
    for start in adj:
        if start not in visited:
            queue: deque[int] = deque([start])
            visited.add(start)
            comp: list[tuple[str, float]] = []
            while queue:
                node = queue.popleft()
                el, _pos, occ = expanded[node]
                comp.append((el, occ))
                for nbr in adj[node]:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
            components.append(comp)
    return components


def _z_from_components(components: list[list[tuple[str, float]]]) -> int:
    """Derive Z as the GCD of per-composition component multiplicities.

    Each distinct molecular species (identified by its elemental composition)
    appears exactly Z times in the unit cell.  Taking the GCD of those
    per-species counts gives Z without needing a packing coefficient.

    Minor disordered fragments — components in which *every* atom has an
    occupancy below :data:`PARTIAL_OCC_THRESHOLD` (e.g. a pair of disordered
    solvent oxygens with ``dg=0, occ=0.5`` and no disorder-group label) — are
    excluded from the GCD calculation because they do not represent complete
    formula units.  If, however, *all* components fall below the threshold
    (e.g. a centrosymmetric molecule sitting entirely on an inversion centre),
    no filtering is applied so that the algorithm can still return a meaningful
    result.

    Examples
    --------
    * Simple organic (2 copies, same formula): GCD({formula: 2}) = 2.
    * Salt like R·HCl (4 organic + 4 Cl⁻): GCD({org: 4, Cl: 4}) = 4.
    * 1:1 co-crystal (4+4 of two different species): GCD = 4.
    * Z=2 organic + disordered solvent (occ=0.5, count=1): GCD({org: 2}) = 2.

    Known limitation
    ----------------
    Solvate molecules sitting on a crystallographic special position appear
    fewer times in the expanded cell than the space-group multiplicity would
    suggest (they are deduplicated during expansion).  In such structures the
    returned Z may be lower than the CIF value.
    """
    if not components:
        return 1

    # Separate components into "major" (contain at least one fully-ordered atom)
    # and "minor" (all atoms are partially occupied — likely disordered solvent).
    major = [
        comp for comp in components
        if max(occ for _el, occ in comp) >= PARTIAL_OCC_THRESHOLD
    ]
    # Fallback: if every component is partial-occupancy (e.g. the whole molecule
    # sits on an inversion centre), do not exclude anything.
    active = major if major else components

    comp_counts: dict[tuple, int] = {}
    for comp in active:
        key = tuple(sorted(Counter(_normalize_element(el) for el, _occ in comp).items()))
        comp_counts[key] = comp_counts.get(key, 0) + 1
    return reduce(gcd, comp_counts.values())


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
        return _parse_formula(text.replace(' ', ''))
    except Exception:
        return None


def _expanded_element_counts(
        expanded: list[tuple[str, tuple[float, float, float], float]],
) -> dict[str, int]:
    """Return total atom count per element across all expanded unit-cell sites.

    Element symbols are normalised via :func:`_normalize_element` so that
    oxidation-state suffixes (e.g. ``'Ni0+'``, ``'O1-'``) are stripped before
    aggregation, enabling correct comparison with parsed formula strings.
    """
    counts: dict[str, int] = {}
    for el, _pos, _occ in expanded:
        key = _normalize_element(el)
        counts[key] = counts.get(key, 0) + 1
    return counts


def _gcd_matches_formula(
        z_gcd: int,
        cell_counts: dict[str, int],
        formula: dict[str, float],
) -> bool:
    """Return True iff ``cell_counts == formula × z_gcd`` for every non-H element.

    Hydrogen is excluded because riding/omitted hydrogens commonly cause a
    benign mismatch that has no bearing on Z.  All other elements present in
    the formula must match exactly (the expanded unit cell is integer-valued
    by construction once disorder has been collapsed).
    """
    for el, n_per_fu in formula.items():
        if el == 'H' or n_per_fu <= 0:
            continue
        expected = int(round(n_per_fu * z_gcd))
        if cell_counts.get(el.capitalize(), 0) != expected:
            return False
    return True


def _z_from_formula(
        cell_counts: dict[str, int],
        formula: dict[str, float],
) -> int | None:
    """Derive Z from the per-element ratio ``cell_counts / formula``.

    Hydrogen is ignored (see :func:`_gcd_matches_formula`).  Every remaining
    element in the formula must yield the *same* positive integer Z (spread
    of zero, exact integer ratio); otherwise ``None`` is returned and the
    caller falls back to the bond-graph GCD.
    """
    zs: list[int] = []
    for el, n_per_fu in formula.items():
        if el == 'H' or n_per_fu <= 0:
            continue
        n_in_cell = cell_counts.get(el.capitalize(), 0)
        if n_in_cell <= 0:
            return None
        ratio = n_in_cell / n_per_fu
        z = int(round(ratio))
        if z < 1 or abs(ratio - z) > 1e-6:
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
    z, _formula_derived = _count_z_with_source(
        atoms_fract, symmops, cell, max_atoms, formula_sum
    )
    return z


def _count_z_with_source(
        atoms_fract,
        symmops: list[str],
        cell: tuple[float, ...],
        max_atoms: int = 5000,
        formula_sum: str | None = None,
) -> tuple[int, bool]:
    """Internal implementation of Z estimation returning ``(z, formula_derived)``.

    ``formula_derived`` is ``True`` when the formula-based correction overrode
    the bond-graph GCD result.  Used by :func:`count_z_and_zprime` to set the
    :attr:`ZResult.formula_derived` flag for caller-visible confidence reporting.
    """
    if not symmops or symmops == ['']:
        return 1, False

    filtered = _filter_disorder(list(atoms_fract))
    if not filtered:
        return 1, False

    # Guard against unreasonably large structures (e.g. proteins, MOFs).
    if len(filtered) * len(symmops) > max_atoms:
        return 1, False

    expanded = _expand_to_unit_cell(filtered, symmops, cell)
    if not expanded:
        return 1, False

    adj = _build_bond_graph(expanded, cell)
    components = _get_components(adj, expanded)
    z = _z_from_components(components)
    z = max(1, z)
    formula_derived = False

    try:
        # Optional formula-based consistency check / correction.
        formula = _parse_formula_sum(formula_sum)
        if formula:
            cell_counts = _expanded_element_counts(expanded)
            if not _gcd_matches_formula(z, cell_counts, formula):
                z_from_form = _z_from_formula(cell_counts, formula)
                if z_from_form is not None:
                    z = z_from_form
                    formula_derived = True
    except Exception:
        return z, formula_derived
    return z, formula_derived



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
    z, formula_derived = _count_z_with_source(
        atoms_fract, symmops, cell, max_atoms, formula_sum
    )
    z_sg = _z_sg_from_symmops(symmops) if symmops and symmops != [''] else 1
    z_prime = round(z / z_sg, 6) if z_sg > 0 else float('nan')
    return ZResult(z=z, z_prime=z_prime, z_sg=z_sg, formula_derived=formula_derived)
