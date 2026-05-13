"""Compare z_from_packing.py estimates against PLATON's Z[Calc] on 500 COD structures.

Usage (from the FinalCif repo root):
    uv run python work/compare_z_platon.py

PLATON is invoked with ``platon -U <cif>`` which writes a ``.chk`` file
containing the line::

    # Z         =         4[Calc],         4[Rep]

The script reads Z[Calc] (PLATON's computed value) and Z[Rep] (the CIF-reported
value), then compares both against our :func:`~finalcif.tools.z_from_packing.count_z_and_zprime`
estimate.

Results are written to ``work/compare_z_platon_results.csv`` and a summary is
printed to stdout.
"""
from __future__ import annotations

import csv
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# ── Make sure FinalCif package is importable ─────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import gemmi as _g  # noqa: E402

from finalcif.tools.z_from_packing import count_z_and_zprime  # noqa: E402

# ── Configuration ─────────────────────────────────────────────────────────────
COD_DIR = Path("/Users/daniel/Downloads/cod-database/cif/2")
N_FILES = 5000
PLATON_EXE = shutil.which("platon") or "/usr/local/bin/platon"
PLATON_TIMEOUT = 30  # seconds per structure
MAX_WORKERS = 8       # parallel platon runs
RANDOM_SEED = 42
OUTPUT_CSV = REPO_ROOT / "work" / "compare_z_platon_5000_results.csv"

# ── Regexes ───────────────────────────────────────────────────────────────────
_Z_CHK_RE = re.compile(
    r"#\s*Z\s*=\s*(\d+)\[Calc\]\s*,\s*(\d+)\[Rep\]", re.IGNORECASE
)


# ── CIF loading (no Qt / CifContainer needed) ─────────────────────────────────

def _load_cif_raw(path: Path):
    """Return (atoms, symmops, cell, formula, z_cif) from a CIF file."""
    doc = _g.cif.read(str(path))
    block = doc[0]

    # Symmetry operations
    symmops: list[str] = []
    for tag in ("_space_group_symop_operation_xyz", "_symmetry_equiv_pos_as_xyz"):
        col = block.find_values(tag)
        if col:
            symmops = [_g.cif.as_string(v).strip().strip("'\"") for v in col]
            break

    # Unit cell
    try:
        cell = tuple(
            float(_g.cif.as_string(block.find_value(t)).split("(")[0])
            for t in (
                "_cell_length_a", "_cell_length_b", "_cell_length_c",
                "_cell_angle_alpha", "_cell_angle_beta", "_cell_angle_gamma",
            )
        )
    except Exception:
        return None  # unusable

    # Atom sites
    loop_full = block.find(
        "_atom_site_",
        ["label", "type_symbol", "fract_x", "fract_y", "fract_z", "disorder_group", "occupancy"],
    )
    loop_no_dis = block.find(
        "_atom_site_",
        ["label", "type_symbol", "fract_x", "fract_y", "fract_z", "occupancy"],
    )
    loop_bare = block.find(
        "_atom_site_",
        ["label", "type_symbol", "fract_x", "fract_y", "fract_z"],
    )
    loop = loop_full or loop_no_dis or loop_bare
    if not loop:
        return None

    atoms = []
    for row in loop:
        try:
            label = _g.cif.as_string(row[0])
            typ = _g.cif.as_string(row[1])
            x = float(_g.cif.as_string(row[2]).split("(")[0])
            y = float(_g.cif.as_string(row[3]).split("(")[0])
            z = float(_g.cif.as_string(row[4]).split("(")[0])
            if loop is loop_full:
                dg_raw = _g.cif.as_string(row[5]).strip()
                dg = int(dg_raw) if dg_raw not in ("", ".", "?") else 0
                occ_raw = _g.cif.as_string(row[6]).split("(")[0]
                occ = float(occ_raw) if occ_raw not in ("", ".", "?") else 1.0
            elif loop is loop_no_dis:
                dg = 0
                occ_raw = _g.cif.as_string(row[5]).split("(")[0]
                occ = float(occ_raw) if occ_raw not in ("", ".", "?") else 1.0
            else:
                dg, occ = 0, 1.0
            atoms.append([label, typ, x, y, z, dg, occ, 0.02])
        except (ValueError, IndexError):
            continue

    if not atoms:
        return None

    # Formula sum
    fv = block.find_value("_chemical_formula_sum")
    formula = _g.cif.as_string(fv).strip("'\" ") if fv else None

    # Reported Z
    zv = block.find_value("_cell_formula_units_Z")
    try:
        z_cif = int(float(_g.cif.as_string(zv))) if zv else None
    except (ValueError, TypeError):
        z_cif = None

    return atoms, symmops, cell, formula, z_cif


# ── PLATON runner ─────────────────────────────────────────────────────────────

def _run_platon(cif_path: Path) -> tuple[int | None, int | None]:
    """Run ``platon -U <cif>`` in an isolated temp dir and parse the .chk file.

    Returns (z_calc, z_rep) or (None, None) on failure.
    """
    with tempfile.TemporaryDirectory(prefix="finalcif_platon_") as tmpdir:
        tmp_cif = Path(tmpdir) / cif_path.name
        shutil.copy2(cif_path, tmp_cif)
        try:
            subprocess.run(
                [PLATON_EXE, "-U", tmp_cif.name],
                cwd=tmpdir,
                timeout=PLATON_TIMEOUT,
                capture_output=True,
                check=False,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None, None

        chk_path = tmp_cif.with_suffix(".chk")
        if not chk_path.exists():
            return None, None

        try:
            chk_text = chk_path.read_text(encoding="latin1", errors="ignore")
        except OSError:
            return None, None

        m = _Z_CHK_RE.search(chk_text)
        if m:
            return int(m.group(1)), int(m.group(2))
        return None, None


# ── Per-file worker ───────────────────────────────────────────────────────────

def _process_one(cif_path: Path) -> dict | None:
    """Run both our algorithm and PLATON on *cif_path*; return a result dict."""
    # Load CIF data
    try:
        raw = _load_cif_raw(cif_path)
    except Exception as exc:
        return {"file": cif_path.name, "error": f"load: {exc}"}
    if raw is None:
        return {"file": cif_path.name, "error": "load: None returned"}

    atoms, symmops, cell, formula, z_cif = raw

    # Our estimate
    t0 = time.perf_counter()
    try:
        result = count_z_and_zprime(atoms, symmops, cell, formula_sum=formula)
        our_z = result.z
        confidence = result.confidence
        z_prime = result.z_prime
    except Exception as exc:
        return {"file": cif_path.name, "error": f"our: {exc}"}
    our_ms = (time.perf_counter() - t0) * 1000

    # PLATON estimate
    t1 = time.perf_counter()
    platon_z_calc, platon_z_rep = _run_platon(cif_path)
    platon_ms = (time.perf_counter() - t1) * 1000

    return {
        "file": cif_path.name,
        "error": "",
        "z_cif": z_cif,
        "our_z": our_z,
        "our_confidence": confidence,
        "our_z_prime": round(z_prime, 4),
        "platon_z_calc": platon_z_calc,
        "platon_z_rep": platon_z_rep,
        "our_ms": round(our_ms, 1),
        "platon_ms": round(platon_ms, 0),
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    # Collect CIF files
    all_cifs = sorted(COD_DIR.rglob("*.cif"))
    if len(all_cifs) < N_FILES:
        print(f"[warn] only {len(all_cifs)} CIF files found, using all of them")
        chosen = all_cifs
    else:
        rng = random.Random(RANDOM_SEED)
        chosen = rng.sample(all_cifs, N_FILES)

    print(f"Processing {len(chosen)} CIF files from {COD_DIR}")
    print(f"PLATON: {PLATON_EXE}  (timeout={PLATON_TIMEOUT}s, workers={MAX_WORKERS})")

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(_process_one, p): p for p in chosen}
        done = 0
        for fut in as_completed(futures):
            done += 1
            row = fut.result()
            results.append(row)
            if done % 50 == 0 or done == len(chosen):
                print(f"  {done}/{len(chosen)} done …", flush=True)

    # Write CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "file", "z_cif", "our_z", "our_confidence", "our_z_prime",
        "platon_z_calc", "platon_z_rep", "our_ms", "platon_ms", "error",
    ]
    with OUTPUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    print(f"\nCSV written → {OUTPUT_CSV}")

    # ── Statistics ────────────────────────────────────────────────────────────
    ok = [r for r in results if not r.get("error")]
    err = [r for r in results if r.get("error")]
    print(f"\n{'─'*70}")
    print(f"Total files processed : {len(results)}")
    print(f"  Errors (load/parse) : {len(err)}")
    print(f"  Successfully parsed : {len(ok)}")

    # Rows where both reported Z and platon Z[Calc] are available
    have_both = [r for r in ok if r["z_cif"] is not None and r["platon_z_calc"] is not None]
    have_ours = [r for r in ok if r["z_cif"] is not None]
    have_platon = [r for r in ok if r["platon_z_calc"] is not None]

    def _pct(n, d):
        return f"{100*n/d:.1f}%" if d else "n/a"

    # Accuracy vs. reported Z
    our_correct = sum(1 for r in have_ours if r["our_z"] == r["z_cif"])
    platon_correct = sum(1 for r in have_platon if r["platon_z_calc"] == r["z_cif"])

    print(f"\n{'─'*70}")
    print("Accuracy vs. CIF-reported Z (_cell_formula_units_Z):")
    print(f"  Our algorithm  : {our_correct}/{len(have_ours)} = {_pct(our_correct, len(have_ours))}")
    print(f"  PLATON Z[Calc] : {platon_correct}/{len(have_platon)} = {_pct(platon_correct, len(have_platon))}")

    # Where PLATON has a result, compare ours to PLATON
    if have_both:
        both_agree = sum(1 for r in have_both if r["our_z"] == r["platon_z_calc"])
        our_vs_rep = sum(1 for r in have_both if r["our_z"] == r["z_cif"])
        pl_vs_rep = sum(1 for r in have_both if r["platon_z_calc"] == r["z_cif"])
        print(f"\nOn the {len(have_both)} structures where both estimates exist:")
        print(f"  Our == PLATON[Calc]   : {both_agree} = {_pct(both_agree, len(have_both))}")
        print(f"  Our == Z_cif          : {our_vs_rep} = {_pct(our_vs_rep, len(have_both))}")
        print(f"  PLATON == Z_cif       : {pl_vs_rep} = {_pct(pl_vs_rep, len(have_both))}")

        # Disagreements
        disagree = [r for r in have_both if r["our_z"] != r["platon_z_calc"]]
        print(f"\n  Disagreements (our ≠ PLATON): {len(disagree)}")
        our_right = sum(1 for r in disagree if r["our_z"] == r["z_cif"])
        platon_right = sum(1 for r in disagree if r["platon_z_calc"] == r["z_cif"])
        neither_right = sum(1 for r in disagree
                            if r["our_z"] != r["z_cif"] and r["platon_z_calc"] != r["z_cif"])
        print(f"    Of those: we're right={our_right}, PLATON right={platon_right}, neither={neither_right}")

        if disagree:
            print(f"\n  Sample disagreements (first 15):")
            print(f"  {'file':<30} {'z_cif':>6} {'our':>5} {'platon':>7} {'conf':<9} {'z\'':<6}")
            print(f"  {'─'*30} {'─'*6} {'─'*5} {'─'*7} {'─'*9} {'─'*6}")
            for r in sorted(disagree, key=lambda x: x["file"])[:15]:
                print(f"  {r['file']:<30} {str(r['z_cif']):>6} {r['our_z']:>5} "
                      f"{str(r['platon_z_calc']):>7} {r['our_confidence']:<9} {r['our_z_prime']:<6}")

    # Timing
    our_times = [r["our_ms"] for r in ok if "our_ms" in r]
    platon_times = [r["platon_ms"] for r in ok if "platon_ms" in r and r["platon_ms"] > 0]
    if our_times:
        our_times_s = sorted(our_times)
        n = len(our_times_s)
        print(f"\nOur algorithm timing ({n} structures):")
        print(f"  min={our_times_s[0]:.1f} ms  "
              f"p50={our_times_s[n//2]:.1f} ms  "
              f"p90={our_times_s[int(n*0.9)]:.1f} ms  "
              f"p99={our_times_s[int(n*0.99)]:.1f} ms  "
              f"max={our_times_s[-1]:.1f} ms")
    if platon_times:
        pl_times_s = sorted(platon_times)
        n = len(pl_times_s)
        print(f"PLATON timing ({n} structures):")
        print(f"  min={pl_times_s[0]:.0f} ms  "
              f"p50={pl_times_s[n//2]:.0f} ms  "
              f"p90={pl_times_s[int(n*0.9)]:.0f} ms  "
              f"p99={pl_times_s[int(n*0.99)]:.0f} ms  "
              f"max={pl_times_s[-1]:.0f} ms")

    # Breakdown by confidence
    for conf in ("high", "medium", "formula", "low"):
        subset = [r for r in have_ours if r["our_confidence"] == conf]
        if not subset:
            continue
        correct = sum(1 for r in subset if r["our_z"] == r["z_cif"])
        print(f"\nOur confidence='{conf}': {correct}/{len(subset)} = {_pct(correct, len(subset))} correct")

    print(f"\n{'─'*70}")


if __name__ == "__main__":
    main()




