"""Diagnose 1519506.cif – understand why Z=1 instead of Z=2."""
import sys
sys.path.insert(0, '.')
from pathlib import Path
from gemmi import cif as gcif
from finalcif.tools.z_from_packing import (
    _filter_disorder, _expand_to_unit_cell, _build_bond_graph,
    _get_components, _z_from_components, count_z_and_zprime,
)

path = Path('/Users/daniel/Downloads/cod-database/cif/1/51/95/1519506.cif')
doc = gcif.read(str(path))
block = doc[0]

# Raw CIF info
print('_cell_formula_units_Z:', gcif.as_string(block.find_value('_cell_formula_units_Z')))
print('_chemical_formula_sum:', gcif.as_string(block.find_value('_chemical_formula_sum') or ''))
print('_space_group_name_H-M:', gcif.as_string(block.find_value('_space_group_name_H-M_alt') or block.find_value('_symmetry_space_group_name_H-M') or ''))

# Read atoms
loop = block.find('_atom_site_', ['label', 'type_symbol', 'fract_x', 'fract_y', 'fract_z'])
if not loop:
    loop = block.find('_atom_site_', ['label', 'fract_x', 'fract_y', 'fract_z'])
atoms_raw = []
for row in loop:
    label = gcif.as_string(row[0])
    if len(row) == 5:
        typ = gcif.as_string(row[1])
        x, y, z = [float(gcif.as_string(row[i]).split('(')[0]) for i in (2, 3, 4)]
    else:
        typ = label.rstrip('0123456789').capitalize()
        x, y, z = [float(gcif.as_string(row[i]).split('(')[0]) for i in (1, 2, 3)]
    atoms_raw.append([label, typ, x, y, z, 0, 1.0, 0.02])

print(f'\nTotal atoms in loop: {len(atoms_raw)}')

# Check for disorder column
dis_col = block.find_loop('_atom_site_disorder_group')
occ_col = block.find_loop('_atom_site_occupancy')
print(f'Has disorder_group column: {len(dis_col) > 0}')
print(f'Has occupancy column: {len(occ_col) > 0}')

# Read full atom site data
full_loop = block.find('_atom_site_', ['label', 'type_symbol', 'fract_x', 'fract_y', 'fract_z',
                                        'disorder_group', 'occupancy'])
if full_loop:
    print(f'\nFull loop ({len(full_loop)} rows):')
    atoms_full = []
    for row in full_loop:
        label, typ = gcif.as_string(row[0]), gcif.as_string(row[1])
        x, y, z = [float(gcif.as_string(row[i]).split('(')[0]) for i in (2, 3, 4)]
        dg_str = gcif.as_string(row[5]) if len(row) > 5 else '0'
        occ_str = gcif.as_string(row[6]) if len(row) > 6 else '1.0'
        try:
            dg = int(dg_str)
        except:
            dg = 0
        try:
            occ = float(occ_str)
        except:
            occ = 1.0
        atoms_full.append([label, typ, x, y, z, dg, occ, 0.02])
        print(f'  {label:8s} {typ:4s} {x:.4f} {y:.4f} {z:.4f}  dg={dg}  occ={occ}')
else:
    print('\nFull loop not found, using atoms_raw')
    atoms_full = atoms_raw

# Symmops
ops = []
for tag in ('_space_group_symop_operation_xyz', '_symmetry_equiv_pos_as_xyz'):
    col = block.find_values(tag)
    if col:
        ops = [gcif.as_string(v).strip().strip("'\"") for v in col]
        break
print(f'\nSymmops ({len(ops)}): {ops}')

# Cell
ctags = ['_cell_length_a','_cell_length_b','_cell_length_c',
         '_cell_angle_alpha','_cell_angle_beta','_cell_angle_gamma']
cell = tuple(float(gcif.as_string(block.find_value(t)).split('(')[0]) for t in ctags)
print(f'Cell: {cell}')

# Run filter and expansion
print('\n--- After _filter_disorder ---')
filtered = _filter_disorder(atoms_full)
print(f'Filtered: {len(filtered)} atoms')
for a in filtered:
    print(f'  {a[0]:8s} {a[1]:4s}  dg={a[5]}  occ={a[6]}')

print('\n--- Expanded unit cell ---')
expanded = _expand_to_unit_cell(filtered, ops, cell)
print(f'Expanded: {len(expanded)} atoms')

print('\n--- Bond graph + components ---')
adj = _build_bond_graph(expanded, cell)
comps = _get_components(adj, expanded)
print(f'Components: {len(comps)}')
from collections import Counter
for i, c in enumerate(comps):
    print(f'  [{i}] {dict(Counter(c))}')

z = _z_from_components(comps)
print(f'\nZ (GCD): {z}')

# Full result
result = count_z_and_zprime(atoms_full, ops, cell)
print(f'ZResult: z={result.z}, z_prime={result.z_prime}, z_sg={result.z_sg}, confidence={result.confidence}')


