"""Investigate specific COD failure cases."""
import sys
sys.path.insert(0, '.')
from gemmi import cif as gcif
from finalcif.tools.z_from_packing import count_z, _filter_disorder, _expand_to_unit_cell, _build_bond_graph, _get_components, _z_from_components

def get_block(p):
    doc = gcif.read(str(p))
    return doc[0]

def symmops(b):
    for tag in ('_space_group_symop_operation_xyz', '_symmetry_equiv_pos_as_xyz'):
        col = b.find_values(tag)
        if col:
            ops = [gcif.as_string(v).strip().strip("'\"") for v in col]
            if ops:
                return ops
    return []

def cell(b):
    tags = ['_cell_length_a', '_cell_length_b', '_cell_length_c',
            '_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma']
    return tuple(float(gcif.as_string(b.find_value(t)).split('(')[0]) for t in tags)

def atoms(b):
    loop = b.find('_atom_site_', ['label', 'type_symbol', 'fract_x', 'fract_y', 'fract_z'])
    if not loop:
        loop = b.find('_atom_site_', ['label', 'fract_x', 'fract_y', 'fract_z'])
        if not loop:
            return []
    result = []
    for row in loop:
        try:
            label = gcif.as_string(row[0])
            if len(row) == 5:
                typ = gcif.as_string(row[1])
                x = float(gcif.as_string(row[2]).split('(')[0])
                y = float(gcif.as_string(row[3]).split('(')[0])
                z = float(gcif.as_string(row[4]).split('(')[0])
            else:
                typ = label.rstrip('0123456789').capitalize()
                x = float(gcif.as_string(row[1]).split('(')[0])
                y = float(gcif.as_string(row[2]).split('(')[0])
                z = float(gcif.as_string(row[3]).split('(')[0])
            result.append([label, typ, x, y, z, 0, 1.0, 0.02])
        except Exception:
            continue
    return result

for cid in ['1533225', '1538553', '4305701', '1527022', '7241349']:
    cid_s = str(cid)
    p = f'/Users/daniel/Downloads/cod-database/cif/{cid_s[0]}/{cid_s[1:3]}/{cid_s[3:5]}/{cid_s}.cif'
    b = get_block(p)
    z_cif = int(float(gcif.as_string(b.find_value('_cell_formula_units_Z'))))
    ops = symmops(b)
    c = cell(b)
    a_list = atoms(b)
    sg_tag = b.find_value('_space_group_name_H-M_alt') or b.find_value('_symmetry_space_group_name_H-M')
    sg = gcif.as_string(sg_tag) if sg_tag else '?'
    formula_tag = b.find_value('_chemical_formula_sum')
    formula = gcif.as_string(formula_tag) if formula_tag else '?'
    filtered = _filter_disorder(a_list)
    expected_expansion = len(filtered) * len(ops)
    expanded = _expand_to_unit_cell(filtered, ops, c)
    adj = _build_bond_graph(expanded, c)
    comps = _get_components(adj, expanded)
    z_calc = _z_from_components(comps)
    comp_sizes = sorted([len(c2) for c2 in comps], reverse=True)[:10]
    print(f'{cid_s}: Z_cif={z_cif} calc={z_calc}  sg={sg}  formula={formula}')
    print(f'  ASU={len(a_list)} filter={len(filtered)} expected_expand={expected_expansion} actual_expand={len(expanded)}')
    print(f'  n_components={len(comps)} top_sizes={comp_sizes}')
    print()

