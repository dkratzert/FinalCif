"""Bulk-validate count_z against COD database CIF files.

Uses gemmi directly (no SHELX parsing) for speed.
Samples by generating random COD IDs (1_000_001 – 9_999_999) rather than
walking the full 496k-file tree.

Usage:
    uv run python work/validate_cod.py [N=500]
"""
import sys
import random
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent.parent))

from gemmi import cif as gcif
from finalcif.tools.z_from_packing import count_z

COD_ROOT = Path('/Users/daniel/Downloads/cod-database/cif')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
RANDOM_SEED = 42

random.seed(RANDOM_SEED)


def _cod_path(cod_id: int) -> Path:
    """Reconstruct the COD filesystem path from a numeric COD entry ID."""
    s = str(cod_id)       # e.g. "1000006"
    top = s[0]            # "1"
    mid = s[1:3]          # "00"
    sub = s[3:5]          # "00"
    return COD_ROOT / top / mid / sub / f'{cod_id}.cif'


def _sample_existing(n: int, seed: int) -> list[Path]:
    """Return up to *n* existing CIF paths by random COD-ID sampling."""
    rng = random.Random(seed)
    found: list[Path] = []
    attempts = 0
    max_attempts = n * 20   # try at most 20x to find N files
    while len(found) < n and attempts < max_attempts:
        attempts += 1
        cod_id = rng.randint(1_000_001, 9_999_999)
        p = _cod_path(cod_id)
        if p.exists():
            found.append(p)
    return found


print(f'Sampling up to {N} COD structures by random ID (seed={RANDOM_SEED}) …')
sample = _sample_existing(N, RANDOM_SEED)
print(f'Found {len(sample)} existing CIF files\n')

ok = 0
wrong = 0
skipped = 0
organic_ok = 0
organic_wrong = 0
failures: list[tuple[str, int, int]] = []
wrong_by_delta: Counter[int] = Counter()

# Elements that define "organic-like" structures (small-molecule target for FinalCif)
ORGANIC_ELEMENTS = {'C', 'H', 'D', 'N', 'O', 'S', 'F', 'Cl', 'Br', 'I', 'P', 'B', 'Si'}


import re

def _is_organic(block: gcif.Block) -> bool:
    """Return True if the formula contains C and only organic-typical elements."""
    f = block.find_value('_chemical_formula_sum')
    if not f:
        return False
    formula = gcif.as_string(f).strip("'\" ")
    # Extract element symbols: lead capital + optional lower-case letters
    elements = set(re.findall(r'[A-Z][a-z]?', formula))
    return bool(elements) and 'C' in elements and elements <= ORGANIC_ELEMENTS


def _get_block(path: Path) -> gcif.Block | None:
    try:
        doc = gcif.read(str(path))
        return doc[0]
    except Exception:
        return None


def _symmops(block: gcif.Block) -> list[str]:
    for tag in ('_space_group_symop_operation_xyz', '_symmetry_equiv_pos_as_xyz'):
        col = block.find_values(tag)
        if col:
            ops = [gcif.as_string(v).strip().strip("'\"") for v in col]
            if ops:
                return ops
    return []


def _cell(block: gcif.Block) -> tuple[float, ...] | None:
    tags = ['_cell_length_a', '_cell_length_b', '_cell_length_c',
            '_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma']
    vals = []
    for t in tags:
        v = block.find_value(t)
        if not v or gcif.as_string(v) in ('?', '.', ''):
            return None
        try:
            vals.append(float(gcif.as_string(v).split('(')[0]))
        except ValueError:
            return None
    return tuple(vals)  # type: ignore[return-value]


def _atoms(block: gcif.Block) -> list:
    loop = block.find('_atom_site_', ['label', 'type_symbol', 'fract_x', 'fract_y', 'fract_z'])
    if not loop:
        loop = block.find('_atom_site_', ['label', 'fract_x', 'fract_y', 'fract_z'])
        if not loop:
            return []
    atoms = []
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
            atoms.append([label, typ, x, y, z, 0, 1.0, 0.02])
        except (ValueError, IndexError):
            continue
    return atoms


for cif_path in sample:
    try:
        block = _get_block(cif_path)
        if block is None:
            skipped += 1
            continue
        z_raw = block.find_value('_cell_formula_units_Z')
        if not z_raw or gcif.as_string(z_raw) in ('?', '.', ''):
            skipped += 1
            continue
        z_cif = int(float(gcif.as_string(z_raw)))
        symmops = _symmops(block)
        if not symmops:
            skipped += 1
            continue
        cell = _cell(block)
        if cell is None:
            skipped += 1
            continue
        atoms = _atoms(block)
        if not atoms:
            skipped += 1
            continue
        z_calc = count_z(atoms, symmops, cell)
        is_org = _is_organic(block)
        if z_calc == z_cif:
            ok += 1
            if is_org:
                organic_ok += 1
        else:
            wrong += 1
            if is_org:
                organic_wrong += 1
            delta = z_calc - z_cif
            wrong_by_delta[delta] += 1
            failures.append((str(cif_path.name), z_calc, z_cif))
    except Exception:
        skipped += 1

total_evaluated = ok + wrong
print(f'Results over {total_evaluated} evaluable structures ({skipped} skipped):')
print(f'  Correct : {ok:4d}  ({100*ok/max(total_evaluated,1):.1f}%)')
print(f'  Wrong   : {wrong:4d}  ({100*wrong/max(total_evaluated,1):.1f}%)')
print()
org_total = organic_ok + organic_wrong
if org_total:
    print(f'Organic-only subset ({org_total} structures):')
    print(f'  Correct : {organic_ok:4d}  ({100*organic_ok/org_total:.1f}%)')
    print(f'  Wrong   : {organic_wrong:4d}  ({100*organic_wrong/org_total:.1f}%)')
    print()
print()
if wrong_by_delta:
    print('Failures by (calc - cif) delta:')
    for delta, cnt in sorted(wrong_by_delta.items(), key=lambda x: -x[1]):
        print(f'  delta={delta:+d}: {cnt} cases')
    print()
if failures:
    print(f'First 30 failures (filename, calc_Z, cif_Z):')
    for name, zc, zcif in failures[:30]:
        print(f'  {name}  calc={zc}  cif={zcif}  (delta={zc-zcif:+d})')




