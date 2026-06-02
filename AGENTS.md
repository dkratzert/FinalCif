# FinalCif AI Developer Instructions

## General Principles

- Code only, no explanation. 
- Bullets over paragraphs. No explanations unless asked.
- **No Assumptions:** If information or code is missing, ask for it. Do not make assumptions.
- **Refuse over Guessing:** Prefer refusing over guessing. If you don't know how to complete the code, say you don't know.
- **Require Specifications:** If the user asks you to write code, ask for a detailed specification first. Do not write code until you have a detailed specification.
- **Quality Standards:** Follow the rules of the books 'Refactoring' and 'Clean Code'.

## Core Setup Conventions
- **Language/Runtime:** Use Python >=3.12 (`pyproject.toml`), with CI tested on 3.12/3.13/3.14 (`.github/workflows/python_tests.yml`).
- **UI Framework:** Assume PySide6. UI imports in the codebase are typically routed through `qtpy` (note that UI files are compiled locally via bindings).
- **Qt Binding Selection:** Set `QT_API=pyside6` before `qtpy` imports (see `finalcif/finalcif_start.py`).

## Architecture
- **Desktop Application:** FinalCif is a crystallographic information file (CIF) editor built with a Qt frontend.
- **Entry Point:** The application starts from `finalcif/finalcif_start.py` (registered as `finalcif` in `pyproject.toml`).
- **Main Window:** `AppWindow` (QMainWindow) in `finalcif/appwindow.py` is the orchestrator wiring all subsystems; UI defined in `finalcif/gui/finalcif_gui_ui.ui`.
- **Subpackage Map:**
  - `finalcif/cif/` — CIF I/O via `gemmi.cif` wrapped in `CifContainer` (`cif_file_io.py`); dict definitions (core/powder/modulation/twin/restraints); subpackages `checkcif/` (IUCr CheckCIF HTML/PDF parsing) and `cod/` (COD/CCDC deposition: `deposit.py`, `deposit_check.py`, `deposition_list.py`, `upload.py`, `doi.py`, `website_parser.py`).
  - `finalcif/ciforder/` — CIF key ordering dialog.
  - `finalcif/datafiles/` — raw instrument data importers: Bruker (`bruker_data.py`, `bruker_frame.py`), SAINT, SADABS, SHELX `.lst` (`shelx_lst.py`), `.p4p`, CCDC deposition mail parser (`ccdc_mail.py`).
  - `finalcif/displaymol/` — 3D molecular display (`vtk_molecule.py`) is not used; 2D rendering is provided by the external `fastmolwidget` package (custom widget in `finalcif_gui_ui.ui`).
  - `finalcif/equip_property/` — Equipment/Properties/AuthorLoops template tables (`equipment.py`, `properties.py`, `author_loop_templates.py`).
  - `finalcif/gui/` — Qt widgets; `.ui` files compiled to sibling `*_ui.py` modules.
  - `finalcif/report/` — DOCX report generation via `docxtpl` (`DocxTemplate`, `RichText`, `InlineImage`) in `templated_report.py`; also archive reports (`archive_report.py`), tables, references, symmetry. The `report/gui/` subpackage hosts the standalone report-options window (`mainwindow.py` + `mainwindow.ui`).
  - `finalcif/template/` — Report template infrastructure (`ReportTemplates`).
  - `finalcif/tools/` — cross-cutting helpers: `platon.py` (`PlatonRunner`), `shred.py`, `space_groups.py` / `spgr_format.py`, `sumformula.py`, `settings.py` (`FinalCifSettings` QSettings wrapper), `options.py`, `download.py`, `pupdate.py` (auto-updater), `statusbar.py`, `chemparse.py`, `dsrmath.py`, `z_from_packing.py`, `misc.py`.
- **External Tool Integration:**
  - Offline CheckCIF uses PLATON via `finalcif/tools/platon.py`; executable resolution checks bundled `platon/platon_special.exe`, then `C:\pwt\platon.exe` (Windows), then `platon` on `PATH`.
  - Online CheckCIF (IUCr) via HTTP in `finalcif/cif/checkcif/checkcif.py`.
  - CCDC/COD deposition in `finalcif/cif/cod/` (`deposit.py`, `upload.py`, `deposit_check.py`); deposition email parsing in `finalcif/datafiles/ccdc_mail.py`.
  - DOI / CrossRef lookups via `crossrefapi` (see `finalcif/cif/cod/doi.py`).
  - SHELX parsing via the external `shelxfile` package (used in `report/templated_report.py`); in-tree `.lst` parser in `datafiles/shelx_lst.py`.
- **CIF Parsing:** Standardized on `gemmi` (>=0.7.5); `gemmi.set_leak_warnings(False)` is set at startup.
- **Key Third-Party Runtime Deps:** `qtpy` + `pyside6` / `pyside6-addons`, `gemmi`, `docxtpl[subdoc]`, `python-docx`, `shelxfile`, `fastmolwidget`, `crossrefapi`, `QtAwesome` (icon fonts), `pyenchant` (spell-check), `html2text`, `lxml`, `numpy<2.4`, `chardet` / `charset-normalizer`, `requests`/`urllib3`, `packaging`, `pefile` (see `pyproject.toml`).
- Use gemmi for CIF parsinf if many files need to be processed, because it is much faster than CifContainer. CifContainer is a wrapper around gemmi.cif that provides a dict-like interface and additional features, but it is slower than using gemmi directly.

## Conventions
- **UI Files:** Edit `.ui` files in Qt Designer (`scripts/designer.py`), then regenerate via `python scripts/compile_ui_files.py`. Never hand-edit generated `*_ui.py`.
- **qtpy Imports:** `from qtpy import QtCore, QtGui, QtWebEngineWidgets, QtWidgets, compat` — `QtWebEngine` is used and requires `PySide6-Addons`.
- **App Bootstrap:** `appwindow.py` uses `QApplication.instance() or QApplication([])` with `app.setStyle("windowsvista")`. A `DEBUG` flag in `finalcif_start.py` toggles the crash hook; crash reports are written to `~/finalcif-crash.txt` by `my_exception_hook`.
- **Settings:** Persisted via `FinalCifSettings` (QSettings wrapper) in `finalcif/tools/settings.py`.

## Typing Conventions
- Type hints are used throughout the codebase; follow the existing style (e.g. `def func(arg: int) -> str:`).
- Don't use string literals for type hints; import the annotaions from __future__ if needed (e.g. `from __future__ import annotations`).

## Workflow & Commands
- **Testing:** 
  - *Command:* `uv run pytest tests`
- **Linting:** 
  - *Command (local):* `ruff check .` — configured via `.ruff.toml`
- **Type Checking:** The dev dependency group includes `ty` and `pyside6-stubs`;
- **UI Compilation:** 
  - *Command:* `python scripts/compile_ui_files.py` (discovers `.ui` files, compiles them, and hot-fixes imports to `qtpy`).
- **Build/Releases:**
  - tag pushes trigger `.github/workflows/python-dist.yml` which runs `uv build` and publishes to PyPI via trusted publishing.
  - Desktop installers built with PyInstaller specs (`Finalcif_installer_win.spec`, `Finalcif_linux_onefile.spec`, `Finalcif_mac.spec`) plus `scripts/_make_win_release.py`, `scripts/make_win_release.bat`, and Inno Setup `scripts/finalcif-install_win64.iss`.
  - Dev launchers: `run_finalcif.bat` / `run_finalcif` / `scripts/finalcif-start.sh`.
