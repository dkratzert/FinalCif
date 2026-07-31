# Summary of Uncommitted Changes

Repository: `dkratzert/FinalCif` — base commit `306fcb63`
Date: 2026-07-31

## Overview

Fixes the offline (PLATON) checkCIF run losing all structure-factor–based tests
because PLATON could not find or recreate an `.fcf` file. FinalCif now supplies
the `.fcf` itself and points PLATON at a SHELXL executable.

**Problem:** FinalCif checks `<name>-finalcif.cif`. PLATON resolves structure
factors by basename, so it looks for `<name>-finalcif.fcf`. That file usually
does not exist (the data is embedded in the CIF, or lives beside it as
`<name>.fcf`). PLATON then tries to regenerate it via SHELXL; when SHELXL is not
reachable this fails and it emits

```
995_ALERT_1_B  Can not Recreate .fcf from Embedded .res & .hkl
```

while silently skipping *every* structure-factor test (912, 969, 978, …).

## Changed files

| File | Change |
| --- | --- |
| `finalcif/tools/platon.py` | +105 / −2 — core fix |
| `finalcif/cif/cif_file_io.py` | +7 — new `fcf_file` property |
| `finalcif/appwindow.py` | +2 / −1 — pass fcf data to runner |
| `tests/test_platon_fcf.py` | new file, 142 lines |

## Details

### `finalcif/tools/platon.py`

`PlatonRunner.__init__` gains an optional `fcf_data: str = ''` parameter and a
`_temporary_fcf: Path | None` field tracking a file the runner created itself.

New members:

- `fcf_target` — property; the `.fcf` path PLATON expects (CIF basename).
- `_provide_fcf_file()` — makes that file available before the process starts.
  Precedence: existing file is left untouched → embedded `_shelx_fcf_file` data
  is written → sibling `<stem>.fcf` (with `-finalcif` stripped via
  `strip_finalcif_of_name(..., till_name_ends=True)`) is copied.
- `_write_fcf()` — static helper, writes latin1 / `\n` newlines, returns success.
- `_find_sibling_fcf()` — locates the pre-`-finalcif` `.fcf` neighbour.
- `_remove_temporary_fcf()` — deletes only a runner-created file; called from
  `_onfinished()`.
- `shelxl_exe` — property; resolves `shelxl`, then `xl` (SHELXTL/Bruker name)
  from `PATH`, else `''`.
- `_set_process_environment()` — sets `SHLEXE` in the QProcess environment when
  not already defined *and* an executable was actually found (PLATON aborts if
  `SHLEXE` points at a missing file).

`run_process()` now calls `_provide_fcf_file()` and `_set_process_environment()`
before starting PLATON.

`delete_orphaned_files()` skips `.fcf` when `_temporary_fcf is None`, so a
user-owned (possibly small) `.fcf` is never removed by the orphan cleanup.

New imports: `shutil`, `strip_finalcif_of_name`.

### `finalcif/cif/cif_file_io.py`

Added `CifContainer.fcf_file` property returning the embedded
`_shelx_fcf_file` value, or `''`. Mirrors the existing `fab_file` property.

### `finalcif/appwindow.py`

`PlatonRunner(...)` construction now passes `fcf_data=self.cif.fcf_file`.

### `tests/test_platon_fcf.py` (new)

11 unit tests, no PLATON required, using `TemporaryDirectory` and mocked
widgets:

- `.fcf` target derives from the CIF basename
- embedded data is written; sibling file is copied
- embedded data takes precedence over a sibling file
- nothing is created when no source exists
- an existing `.fcf` is neither overwritten nor tracked as temporary
- created files are removed afterwards; user files survive orphan cleanup
- a plain `foo.cif` finds no sibling to copy
- `shelxl_exe` falls back from `shelxl` to `xl`, and returns `''` when neither
  is on `PATH` (both via monkey-patched `which`)

## Notes / open points

- No version bump or changelog entry yet for this fix.
- The `.fcf` is written next to the CIF and removed after the run only when
  FinalCif created it.
