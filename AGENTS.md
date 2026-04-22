# FinalCif AI Developer Instructions

## General Principles
- **No Assumptions:** If information or code is missing, ask for it. Do not make assumptions.
- **Refuse over Guessing:** Prefer refusing over guessing. If you don't know how to complete the code, say you don't know.
- **Require Specifications:** If the user asks you to write code, ask for a detailed specification first. Do not write code until you have a detailed specification.
- **Quality Standards:** Follow the rules of 'Refactoring' and 'Clean Code' as described by Martin Fowler and Robert C. Martin, respectively.

## Core Setup Conventions
- **Language/Runtime:** Use Python >=3.12 (`pyproject.toml`), with CI tested on 3.12/3.13/3.14 (`.github/workflows/python_tests.yml`).
- **UI Framework:** Assume PySide6. UI imports in the codebase are typically routed through `qtpy` (note that UI files are compiled locally via bindings).
- **Qt Binding Selection:** Set `QT_API=pyside6` before `qtpy` imports (see `finalcif/finalcif_start.py`).

## Architecture
- **Desktop Application:** FinalCif is a crystallographic information file (CIF) editor built with a Qt frontend.
- **Entry Point:** The application starts from `finalcif/finalcif_start.py` (registered as `finalcif` in `pyproject.toml`).
- **Main Window:** `AppWindow` (QMainWindow) in `finalcif/appwindow.py` is the orchestrator wiring all subsystems; UI defined in `finalcif/gui/finalcif_gui_ui.ui`.
- **Subpackage Map:**
  - `finalcif/cif/` — CIF I/O via `gemmi.cif` wrapped in `CifContainer` (`cif_file_io.py`); dict definitions (core/powder/modulation/twin/restraints); subpackages `checkcif/` (IUCr CheckCIF HTML/PDF parsing) and `cod/` (COD/CCDC deposition: `deposit.py`, `upload.py`, `doi.py`, `website_parser.py`).
  - `finalcif/ciforder/` — CIF key ordering dialog.
  - `finalcif/datafiles/` — raw instrument data importers: Bruker (`bruker_data.py`, `bruker_frame.py`), SAINT, SADABS, SHELX `.lst` (`shelx_lst.py`), `.p4p`, CCDC deposition mail parser (`ccdc_mail.py`).
  - `finalcif/displaymol/` — 3D molecular display (`vtk_molecule.py`) is not used; 2D rendering is provided by the external `fastmolwidget` package (custom widget in `finalcif_gui_ui.ui`).
  - `finalcif/equip_property/` — Equipment/Properties/AuthorLoops template tables (`equipment.py`, `properties.py`, `author_loop_templates.py`).
  - `finalcif/gui/` — Qt widgets; `.ui` files compiled to sibling `*_ui.py` modules.
  - `finalcif/report/` — DOCX report generation via `docxtpl` (`DocxTemplate`, `RichText`, `InlineImage`) in `templated_report.py`; also archive reports, tables, references, symmetry.
  - `finalcif/template/` — Report template infrastructure (`ReportTemplates`).
  - `finalcif/tools/` — cross-cutting helpers: `platon.py` (`PlatonRunner`), `shred.py`, `space_groups.py`, `sumformula.py`, `settings.py` (`FinalCifSettings` QSettings wrapper), `download.py`, `pupdate.py` (auto-updater), `statusbar.py`, `chemparse.py`, `dsrmath.py`.
- **External Tool Integration:**
  - Offline CheckCIF uses PLATON via `finalcif/tools/platon.py`; executable resolution checks bundled `platon/platon_special.exe`, then `C:\pwt\platon.exe` (Windows), then `platon` on `PATH`.
  - Online CheckCIF (IUCr) via HTTP in `finalcif/cif/checkcif/checkcif.py`.
  - CCDC/COD deposition in `finalcif/cif/cod/` (`deposit.py`, `upload.py`, `deposit_check.py`); deposition email parsing in `finalcif/datafiles/ccdc_mail.py`.
  - DOI / CrossRef lookups via `crossrefapi` (see `finalcif/cif/cod/doi.py`).
  - SHELX parsing via the external `shelxfile` package (used in `report/templated_report.py`); in-tree `.lst` parser in `datafiles/shelx_lst.py`.
- **CIF Parsing:** Standardized on `gemmi` (>=0.7.5); `gemmi.set_leak_warnings(False)` is set at startup.

## Conventions
- **UI Files:** Edit `.ui` files in Qt Designer (`scripts/designer.py`), then regenerate via `python scripts/compile_ui_files.py`. Never hand-edit generated `*_ui.py`.
- **qtpy Imports:** `from qtpy import QtCore, QtGui, QtWebEngineWidgets, QtWidgets, compat` — `QtWebEngine` is used and requires `PySide6-Addons`.
- **App Bootstrap:** `appwindow.py` uses `QApplication.instance() or QApplication([])` with `app.setStyle("windowsvista")`. A `DEBUG` flag in `finalcif_start.py` toggles the crash hook; crash reports are written to `~/finalcif-crash.txt` by `my_exception_hook`.
- **Settings:** Persisted via `FinalCifSettings` (QSettings wrapper) in `finalcif/tools/settings.py`.

## Workflow & Commands
- **Dependency Management:** The project uses `uv` for package management (`uv.lock`, `pylock.toml`, `pyproject.toml`).
  - *Setup:* `uv sync --all-extras --dev`
- **Testing:** 
  - *Command:* `uv run pytest tests`
  - *CI/Linux Headless:* run tests with `QT_QPA_PLATFORM=offscreen` (see `.github/workflows/python_tests.yml`).
  - *Network-Gated Tests:* set `NO_NETWORK=1` to skip network-dependent checks (CheckCIF/DOI/deposit/PLATON; see `tests/test_checkcif.py`, `tests/test_doi.py`).
  - *Helpers:* shared base class `AppWindowTestCase` and `processevents()` in `tests/helpers.py`; `get_platon_exe()` resolves `C:\pwt\platon.exe` on Windows or `which('platon')`. Fixtures live in `tests/examples/`, `tests/statics/`, `tests/checkcif_results/`, and top-level `test-data/`.
- **Linting:** 
  - *Command (local):* `ruff check .` — configured via `.ruff.toml` (line-length 120, target py312).
  - *CI Lint:* GitHub Actions runs `flake8` in `.github/workflows/python_tests.yml` (ruff is not invoked in CI).
- **UI Compilation:** 
  - *Command:* `python scripts/compile_ui_files.py` (discovers `.ui` files, compiles them, and hot-fixes imports to `qtpy`).
- **Build/Releases:**
  - Packaged with `hatchling`; tag pushes trigger `.github/workflows/python-dist.yml` which runs `uv build` and publishes to PyPI via trusted publishing.
  - Desktop installers built with PyInstaller specs (`Finalcif_installer_win.spec`, `Finalcif_linux_onefile.spec`, `Finalcif_mac.spec`) plus `scripts/_make_win_release.py`, `scripts/make_win_release.bat`, and Inno Setup `scripts/finalcif-install_win64.iss`.
  - Dev launchers: `run_finalcif.bat` / `run_finalcif` / `scripts/finalcif-start.sh`.
