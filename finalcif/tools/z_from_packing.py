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
from collections import Counter, deque
from functools import reduce
from math import gcd

import gemmi

from fastmolwidget.molecule2D import calc_volume  # re-exported for callers
from finalcif.cif.atoms import element2cov as _ELEMENT2COV

# Covalent radii sourced from finalcif.cif.atoms.element2cov (Å).
# A small fallback covers elements absent from that table.
DEFAULT_RADIUS: float = 1.50
BOND_TOLERANCE: float = 0.40

# Tolerance used when testing whether Z' is close to a simple fraction.
_ZPRIME_TOLERANCE: float = 0.05


@dataclasses.dataclass(frozen=True)
class ZResult:
    """Result of Z estimation with Z' and a reliability indicator.

    Attributes:
        z:        Estimated formula units per unit cell (GCD bond-graph method).
        z_prime:  ``z / z_sg`` — formula units per asymmetric unit.
        z_sg:     Number of general positions in the space group (symmetry-derived Z).

    The ``reliable`` property is ``True`` when *z_prime* is within
    :data:`_ZPRIME_TOLERANCE` of a positive multiple of 0.5 (the set of
    crystallographically meaningful fractions: ½, 1, 1½, 2, …).
    Values outside this set indicate that the bond-graph GCD algorithm
    lost track of the true formula-unit count (e.g. infinite frameworks,
    polymers, or multi-component systems whose species counts share no
    common factor with the correct Z).
    """

    z: int
    z_prime: float
    z_sg: int

    @property
    def reliable(self) -> bool:
        """``True`` when *z_prime* is a plausible crystallographic value.

        Checks whether *z_prime* is within :data:`_ZPRIME_TOLERANCE` of
        k/2 for any positive integer *k* up to 16 (i.e. Z′ ≤ 8).
        """
        if self.z_prime <= 0 or self.z_prime > 8.0:
            return False
        for k in range(1, 17):          # 0.5, 1.0, 1.5, … 8.0
            if abs(self.z_prime - k / 2) < _ZPRIME_TOLERANCE:
                return True
        return False

    @property
    def confidence(self) -> str:
        """A short human-readable confidence indicator: ``'high'``, ``'medium'``, or ``'low'``.

        * **high**   — Z′ is a positive integer (1, 2, 3, …): the most common,
          most reliable case.
        * **medium** — Z′ is a half-integer (0.5, 1.5, …): the molecule may sit
          on a crystallographic special position; the bond-graph Z could be half
          of the true value.
        * **low**    — Z′ is not a multiple of 0.5, or is outside (0, 8]:
          the estimate is unlikely to match the true crystallographic Z.
        """
        if not self.reliable:
            return 'low'
        # Distinguish integer Z' from half-integer Z'
        if abs(self.z_prime - round(self.z_prime)) < _ZPRIME_TOLERANCE:
            return 'high'
        return 'medium'


def _get_radius(element: str) -> float:
    """Return the covalent radius (Å) for *element*, falling back to DEFAULT_RADIUS."""
    return _ELEMENT2COV.get(element.capitalize(), DEFAULT_RADIUS)


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
        (s.type_symbol, (s.fract.x, s.fract.y, s.fract.z))
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
    orth = [uc.orthogonalize(gemmi.Fractional(*pos)) for _, pos in expanded]
    radii = [_get_radius(el) for el, _ in expanded]

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
        expanded: list[tuple[str, tuple[float, float, float]]],
) -> list[list[str]]:
    """Return each connected component as a list of element symbols."""
    visited: set[int] = set()
    components: list[list[str]] = []
    for start in adj:
        if start not in visited:
            queue: deque[int] = deque([start])
            visited.add(start)
            comp: list[str] = []
            while queue:
                node = queue.popleft()
                comp.append(expanded[node][0])
                for nbr in adj[node]:
                    if nbr not in visited:
                        visited.add(nbr)
                        queue.append(nbr)
            components.append(comp)
    return components


def _z_from_components(components: list[list[str]]) -> int:
    """Derive Z as the GCD of per-composition component multiplicities.

    Each distinct molecular species (identified by its elemental composition)
    appears exactly Z times in the unit cell.  Taking the GCD of those
    per-species counts gives Z without needing a packing coefficient.

    Examples
    --------
    * Simple organic (2 copies, same formula): GCD({formula: 2}) = 2.
    * Salt like R·HCl (4 organic + 4 Cl⁻): GCD({org: 4, Cl: 4}) = 4.
    * 1:1 co-crystal (4+4 of two different species): GCD = 4.

    Known limitation
    ----------------
    Solvate molecules sitting on a crystallographic special position appear
    fewer times in the expanded cell than the space-group multiplicity would
    suggest (they are deduplicated during expansion).  In such structures the
    returned Z may be lower than the CIF value.
    """
    if not components:
        return 1
    comp_counts: dict[tuple, int] = {}
    for comp in components:
        key = tuple(sorted(Counter(comp).items()))
        comp_counts[key] = comp_counts.get(key, 0) + 1
    return reduce(gcd, comp_counts.values())


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

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
            max_atoms: int = 5000) -> int:
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

    Args:
        atoms_fract:  Iterable of atom records as yielded by
                      ``CifContainer.atoms_fract``:
                      ``[label, element, fx, fy, fz, disorder_group, occ, u_iso]``
        symmops:      Symmetry-operation strings from ``CifContainer.symmops``.
        cell:         Cell parameters ``(a, b, c, alpha, beta, gamma)`` in Å/deg.
        max_atoms:    Skip expansion if the expected unit-cell atom count would
                      exceed this limit (avoids quadratic cost for huge structures).

    Returns:
        Number of formula units per unit cell (Z), at minimum 1.
    """
    if not symmops or symmops == ['']:
        return 1

    filtered = _filter_disorder(list(atoms_fract))
    if not filtered:
        return 1

    # Guard against unreasonably large structures (e.g. proteins, MOFs).
    if len(filtered) * len(symmops) > max_atoms:
        return 1

    expanded = _expand_to_unit_cell(filtered, symmops, cell)
    if not expanded:
        return 1

    adj = _build_bond_graph(expanded, cell)
    components = _get_components(adj, expanded)
    z = _z_from_components(components)
    return max(1, z)


def count_z_and_zprime(
        atoms_fract,
        symmops: list[str],
        cell: tuple[float, ...],
        max_atoms: int = 5000,
) -> ZResult:
    """Determine Z and Z′ by packing the unit cell and counting molecular graphs.

    Extends :func:`count_z` with a Z′ value and a reliability indicator.

    Z′ = Z / Z_sg, where Z_sg is the number of general positions in the space
    group (the maximum Z for a structure with all atoms in general positions).

    A Z′ that is a positive multiple of 0.5 is crystallographically meaningful:

    * **Z′ = 1** (most common) — one formula unit per asymmetric unit.
    * **Z′ = 0.5** — molecule on a 2-fold special position.
    * **Z′ = 2, 3, …** — multiple independent formula units in the ASU.

    A Z′ that is *not* a multiple of 0.5 signals that the bond-graph GCD
    algorithm returned an incorrect Z (typically an undercount for polymeric or
    multi-component structures).

    Args:
        atoms_fract:  Atom records as yielded by ``CifContainer.atoms_fract``.
        symmops:      Symmetry-operation strings from ``CifContainer.symmops``.
        cell:         Cell parameters ``(a, b, c, alpha, beta, gamma)`` in Å/deg.
        max_atoms:    Expansion guard (see :func:`count_z`).

    Returns:
        A :class:`ZResult` with ``z``, ``z_prime``, ``z_sg``, ``reliable``,
        and ``confidence`` attributes.
    """
    z = count_z(atoms_fract, symmops, cell, max_atoms)
    z_sg = _z_sg_from_symmops(symmops) if symmops and symmops != [''] else 1
    z_prime = round(z / z_sg, 6) if z_sg > 0 else float('nan')
    return ZResult(z=z, z_prime=z_prime, z_sg=z_sg)

