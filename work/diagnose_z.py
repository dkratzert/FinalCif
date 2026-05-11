from pathlib import Path
from finalcif.cif.cif_file_io import CifContainer
from finalcif.tools.z_from_packing import (
    _filter_disorder, _expand_to_unit_cell, _build_bond_graph,
    _count_components, _get_components, _z_from_components,
)

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
    cell = cif.cell[:6]
    expanded = _expand_to_unit_cell(filtered, cif.symmops, cell)
    adj = _build_bond_graph(expanded, cell)
    components = _get_components(adj, expanded)
    z_gcd = _z_from_components(components)
    z_cif = cif['_cell_formula_units_Z']
    match = '✓' if str(z_gcd) == str(z_cif) else f'✗ (CIF={z_cif})'
    print(f'{path:<45s}  gcd_Z={z_gcd}  {match}  components={len(components)}')
