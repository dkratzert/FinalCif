"""Validate Z+Z' against 1000 COD structures; show how confidence correlates with accuracy."""
import sys, random
from pathlib import Path
from collections import Counter
sys.path.insert(0, '.')
from gemmi import cif as gcif
from finalcif.tools.z_from_packing import count_z_and_zprime

COD_ROOT = Path('/Users/daniel/Downloads/cod-database/cif')
random.seed(42)

def _cod_path(cod_id):
    s = str(cod_id)
    return COD_ROOT / s[0] / s[1:3] / s[3:5] / f'{cod_id}.cif'

def _sample(n, seed):
    rng = random.Random(seed)
    found = []
    while len(found) < n:
        p = _cod_path(rng.randint(1_000_001, 9_999_999))
        if p.exists():
            found.append(p)
    return found

def _symmops(block):
    for tag in ('_space_group_symop_operation_xyz', '_symmetry_equiv_pos_as_xyz'):
        col = block.find_values(tag)
        if col:
            ops = [gcif.as_string(v).strip().strip("'\"") for v in col]
            if ops: return ops
    return []

def _cell(block):
    tags = ['_cell_length_a','_cell_length_b','_cell_length_c',
            '_cell_angle_alpha','_cell_angle_beta','_cell_angle_gamma']
    try:
        return tuple(float(gcif.as_string(block.find_value(t)).split('(')[0]) for t in tags)
    except Exception:
        return None

def _atoms(block):
    loop = block.find('_atom_site_', ['label','type_symbol','fract_x','fract_y','fract_z'])
    if not loop:
        loop = block.find('_atom_site_', ['label','fract_x','fract_y','fract_z'])
        if not loop: return []
    atoms = []
    for row in loop:
        try:
            label = gcif.as_string(row[0])
            if len(row) == 5:
                typ = gcif.as_string(row[1]); x,y,z = [float(gcif.as_string(row[i]).split('(')[0]) for i in (2,3,4)]
            else:
                typ = label.rstrip('0123456789').capitalize(); x,y,z = [float(gcif.as_string(row[i]).split('(')[0]) for i in (1,2,3)]
            atoms.append([label, typ, x, y, z, 0, 1.0, 0.02])
        except Exception: continue
    return atoms

sample = _sample(1000, 42)

# Stats per confidence level
stats = {
    'high':   {'ok': 0, 'wrong': 0},
    'medium': {'ok': 0, 'wrong': 0},
    'low':    {'ok': 0, 'wrong': 0},
}
zprime_dist: Counter = Counter()
skipped = 0

for p in sample:
    try:
        doc = gcif.read(str(p)); block = doc[0]
        z_raw = block.find_value('_cell_formula_units_Z')
        if not z_raw or gcif.as_string(z_raw) in ('?', '.', ''): skipped += 1; continue
        z_cif = int(float(gcif.as_string(z_raw)))
        ops = _symmops(block)
        if not ops: skipped += 1; continue
        cell = _cell(block)
        if cell is None: skipped += 1; continue
        atoms = _atoms(block)
        if not atoms: skipped += 1; continue

        result = count_z_and_zprime(atoms, ops, cell)
        conf = result.confidence
        # Round z_prime to nearest 0.5 for distribution
        bucket = round(result.z_prime * 2) / 2
        zprime_dist[f"{bucket:.1f}"] += 1

        if result.z == z_cif:
            stats[conf]['ok'] += 1
        else:
            stats[conf]['wrong'] += 1
    except Exception:
        skipped += 1

print(f'Skipped: {skipped}')
print()
print('=== Accuracy by confidence level ===')
for conf in ('high', 'medium', 'low'):
    ok = stats[conf]['ok']
    wrong = stats[conf]['wrong']
    total = ok + wrong
    pct = 100 * ok / total if total else 0
    print(f"  {conf:8s}: {ok:3d}/{total:3d} correct = {pct:.1f}%")

print()
print('=== Z′ distribution (rounded to nearest 0.5) ===')
for bucket, count in sorted(zprime_dist.items(), key=lambda x: float(x[0])):
    bar = '█' * (count // 5)
    print(f"  Z′ = {bucket}: {count:4d}  {bar}")

