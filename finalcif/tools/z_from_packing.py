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
2. Apply all space-group operations (via gemmi) and wrap positions to [0, 1).
3. Deduplicate atoms that collapse onto the same fractional site (special positions).
4. Build a bond-adjacency graph using covalent-radii distances with periodic
   boundary conditions (±1 neighbour images along each axis).
5. Count connected components via BFS → that count is Z.

The fastmolwidget package is used for the unit-cell volume helper (calc_volume),
which lets callers cross-check the geometry without importing gemmi separately.
"""
from __future__ import annotations

import math
from collections import Counter, deque
from functools import reduce
from math import gcd

import gemmi

from fastmolwidget.molecule2D import calc_volume  # re-exported for callers

# Single-bond covalent radii (A) from Alvarez (2008) Dalton Trans. 2832-2838.
# Covers the elements encountered in common small-molecule crystal structures.
COVALENT_RADII: dict[str, float] = {
    'H': 0.31, 'D': 0.31,
    'B': 0.84,
    'C': 0.76, 'N': 0.71, 'O': 0.66, 'F': 0.57,
    'Si': 1.11, 'P': 1.07, 'S': 1.05, 'Cl': 1.02,
    'Ge': 1.20, 'As': 1.19, 'Se': 1.20,
    'Br': 1.20, 'I': 1.39, 'Te': 1.38,
    'Li': 1.28, 'Na': 1.66, 'K': 2.03,
    'Mg': 1.41, 'Ca': 1.76, 'Al': 1.21,
    'Zn': 1.22, 'Cu': 1.32, 'Ni': 1.24, 'Co': 1.26,
    'Fe': 1.32, 'Mn': 1.61, 'Cr': 1.39, 'V': 1.34, 'Ti': 1.60,
    'Ag': 1.45, 'Au': 1.36, 'Pd': 1.39, 'Pt': 1.36, 'Hg': 1.32,
    'Ru': 1.46, 'Rh': 1.42, 'Os': 1.44, 'Ir': 1.41, 'Mo': 1.54,
    'W': 1.62, 'Re': 1.51,
    'Sc': 1.70, 'Y': 1.90, 'La': 2.07,
    'Zr': 1.75, 'Hf': 1.75, 'Nb': 1.47, 'Ta': 1.70,
    'Sn': 1.39, 'Sb': 1.39, 'Pb': 1.46, 'Bi': 1.48,
    'Tl': 1.45, 'In': 1.42, 'Ga': 1.22,
}
DEFAULT_RADIUS: float = 1.50  # fallback for unrecognised elements
BOND_TOLERANCE: float = 0.40  # added to the sum of covalent radii

# Fractional-coordinate threshold for deduplicating special-position atoms.
_DEDUP_THRESH: float = 0.005


# ---------------------------------------------------------------------------
# Internal geometry helpers
# ---------------------------------------------------------------------------

def _frac_to_orth_matrix(cell: tuple[float, ...]) -> list[list[float]]:
    """Return the 3x3 fractional-to-Cartesian transformation matrix.

    Convention: X = Ma * a,  Y = Mb * a + Mb * b,  Z = Mc * c
    (standard right-handed CIF / SHELX convention).
    """
    a, b, c, alpha, beta, gamma = cell[:6]
    ar, br, gr = math.radians(alpha), math.radians(beta), math.radians(gamma)
    ca, cb, cg = math.cos(ar), math.cos(br), math.cos(gr)
    sg = math.sin(gr)
    v_unit = math.sqrt(max(0.0, 1.0 - ca ** 2 - cb ** 2 - cg ** 2 + 2.0 * ca * cb * cg))
    return [
        [a,    b * cg,                     c * cb],
        [0.0,  b * sg,                     c * (ca - cb * cg) / sg],
        [0.0,  0.0,                         c * v_unit / sg],
    ]


def _apply_matrix(M: list[list[float]], xyz: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = xyz
    return (
        M[0][0] * x + M[0][1] * y + M[0][2] * z,
        M[1][1] * y + M[1][2] * z,
        M[2][2] * z,
    )


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
# Step 2 - unit-cell expansion via symmetry
# ---------------------------------------------------------------------------

def _wrap(v: float) -> float:
    """Wrap a fractional coordinate into [0, 1)."""
    return v % 1.0


def _expand_to_unit_cell(
        filtered: list,
        symmops: list[str],
) -> list[tuple[str, tuple[float, float, float]]]:
    """Apply all space-group operations, wrap to [0, 1)³, deduplicate.

    Deduplication removes atoms that land on the same fractional position
    after applying multiple symmetry operations (special positions).

    Returns:
        List of (element_symbol, (fx, fy, fz)) tuples.
    """
    ops = [gemmi.Op(o) for o in symmops]
    expanded: list[tuple[str, tuple[float, float, float]]] = []

    for atom in filtered:
        elem = str(atom[1])
        fx, fy, fz = float(atom[2]), float(atom[3]), float(atom[4])
        for op in ops:
            raw = op.apply_to_xyz([fx, fy, fz])
            wp: tuple[float, float, float] = (_wrap(raw[0]), _wrap(raw[1]), _wrap(raw[2]))
            # Deduplicate: skip if within threshold of any existing position.
            is_dup = False
            for _, epos in expanded:
                dr = (
                    min(abs(wp[0] - epos[0]), 1.0 - abs(wp[0] - epos[0])),
                    min(abs(wp[1] - epos[1]), 1.0 - abs(wp[1] - epos[1])),
                    min(abs(wp[2] - epos[2]), 1.0 - abs(wp[2] - epos[2])),
                )
                if dr[0] < _DEDUP_THRESH and dr[1] < _DEDUP_THRESH and dr[2] < _DEDUP_THRESH:
                    is_dup = True
                    break
            if not is_dup:
                expanded.append((elem, wp))
    return expanded


# ---------------------------------------------------------------------------
# Step 3 - bond graph construction
# ---------------------------------------------------------------------------

def _build_bond_graph(
        expanded: list[tuple[str, tuple[float, float, float]]],
        M: list[list[float]],
) -> dict[int, set[int]]:
    """Build an adjacency dict for all unit-cell atoms.

    Bond detection uses the sum of covalent radii + BOND_TOLERANCE.
    The 27 periodic images of each atom (shifts of +-1 along a, b, c) are
    checked to correctly bond atoms across cell boundaries.

    Performance: a spatial grid built over the 27 image copies of each atom
    reduces the complexity from O(n^2) to O(n) for typical crystal structures
    while preserving correct periodic-boundary-condition bonding.
    """
    n = len(expanded)
    adj: dict[int, set[int]] = {i: set() for i in range(n)}
    if n == 0:
        return adj

    # Cartesian coordinates and radii for all expanded atoms.
    orth = [_apply_matrix(M, pos) for _, pos in expanded]
    radii = [COVALENT_RADII.get(el.capitalize(), DEFAULT_RADIUS)
             for el, _ in expanded]

    # Maximum possible bond cutoff (largest atom pair + tolerance).
    max_radius = max(radii)
    max_cutoff = 2.0 * max_radius + BOND_TOLERANCE

    # Cartesian cell-translation vectors (columns of M for a, b, c).
    a_cart = (M[0][0], 0.0, 0.0)
    b_cart = (M[0][1], M[1][1], 0.0)
    c_cart = (M[0][2], M[1][2], M[2][2])

    # All 27 image translation vectors (including identity).
    translations = [
        (da * a_cart[0] + db * b_cart[0] + dc * c_cart[0],
         da * a_cart[1] + db * b_cart[1] + dc * c_cart[1],
         da * a_cart[2] + db * b_cart[2] + dc * c_cart[2])
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
    for j, (xj, yj, zj) in enumerate(orth):
        for tx, ty, tz in translations:
            ix, iy, iz = xj + tx, yj + ty, zj + tz
            key = (math.floor(ix / cell_size),
                   math.floor(iy / cell_size),
                   math.floor(iz / cell_size))
            if key not in grid_ext:
                grid_ext[key] = []
            grid_ext[key].append((j, ix, iy, iz))

    # For each real atom i, search only the 27 neighboring grid cells.
    for i, (xi, yi, zi) in enumerate(orth):
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

def count_z(atoms_fract, symmops: list[str], cell: tuple[float, ...],
            max_atoms: int = 5000) -> int:
    """Determine Z by packing the unit cell and counting molecular graphs.

    Disorder is handled correctly: only the first component of each disordered
    site (disorder_group in {0, 1, -1}) is retained before expansion, so each
    atomic site contributes exactly once regardless of its occupancy split.

    Args:
        atoms_fract:  Iterable of atom records as yielded by
                      ``CifContainer.atoms_fract``:
                      ``[label, element, fx, fy, fz, disorder_group, occ, u_iso]``
        symmops:      Symmetry-operation strings from ``CifContainer.symmops``.
        cell:         Cell parameters ``(a, b, c, alpha, beta, gamma)`` in A/deg.
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

    expanded = _expand_to_unit_cell(filtered, symmops)
    if not expanded:
        return 1

    M = _frac_to_orth_matrix(cell)
    adj = _build_bond_graph(expanded, M)
    components = _get_components(adj, expanded)
    z = _z_from_components(components)
    return max(1, z)

