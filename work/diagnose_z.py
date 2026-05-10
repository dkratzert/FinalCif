from pathlib import Path
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.z_from_packing import _filter_disorder, _expand_to_unit_cell, _frac_to_orth_matrix, _build_bond_graph, _count_components
from collections import deque, Counter
from math import gcd
from functools import reduce

def get_components(adj, expanded):
    visited = set()
    components = []
    for start in adj:
        if start not in visited:
            q = deque([start])
            visited.add(start)
            comp = []
            while q:
                n = q.popleft()
                comp.append(expanded[n][0])
                for nb in adj[n]:
                    if nb not in visited:
                        visited.add(nb)
                        q.append(nb)
            components.append(comp)
    return components

def z_from_components(components):
    if not components:
        return 1
    comp_counts = {}
    for comp in components:
        key = tuple(sorted(Counter(comp).items()))
        comp_counts[key] = comp_counts.get(key, 0) + 1
    return reduce(gcd, comp_counts.values())

for path in [
    'test-data/1000006-finalcif.cif',
    'test-data/DK_ML7-66-final.cif',
    'test-data/DK_Zucker2_0m-finalcif.cif',
    'test-data/ntd106c-P-1-final.cif',
    'tests/examples/multi.cif',
    'tests/examples/1979688_small.cif',
]:
    cif = CifContainer(Path(path))
    atoms = list(cif.atoms_fract)
    filtered = _filter_disorder(atoms)
    expanded = _expand_to_unit_cell(filtered, cif.symmops)
    M = _frac_to_orth_matrix(cif.cell[:6])
    adj = _build_bond_graph(expanded, M)
    components = get_components(adj, expanded)
    z_gcd = z_from_components(components)
    z_cif = cif['_cell_formula_units_Z']
    match = '✓' if str(z_gcd) == str(z_cif) else f'✗ (CIF={z_cif})'
    print(f'{path:<45s}  gcd_Z={z_gcd}  {match}  components={len(components)}')
