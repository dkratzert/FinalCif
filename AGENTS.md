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
- **External Tool Integration:** Offline CheckCIF uses PLATON via `finalcif/tools/platon.py`; executable resolution checks bundled `platon/platon_special.exe`, then `C:\pwt\platon.exe` (Windows), then `platon` on `PATH`.

## Workflow & Commands
- **Dependency Management:** The project uses `uv` for package management (e.g., `uv.lock`, `pyproject.toml`).
  - *Setup:* `uv sync --all-extras --dev`
- **Testing:** 
  - *Command:* `uv run pytest tests`
  - *CI/Linux Headless:* run tests with `QT_QPA_PLATFORM=offscreen` (see `.github/workflows/python_tests.yml`).
  - *Network-Gated Tests:* set `NO_NETWORK=1` to skip network-dependent checks (see `tests/test_checkcif.py`, `tests/test_doi.py`).
- **Linting:** 
  - *Command:* `ruff check .`
  - *CI Lint:* GitHub Actions currently runs `flake8` in `.github/workflows/python_tests.yml`.
- **UI Compilation:** 
  - *Command:* `python scripts/compile_ui_files.py` (this discovers `.ui` files, compiles them, and hot-fixes imports to `qtpy`).
- **Build/Releases:** Packaged with `hatchling`. Desktop releases use scripts in the `scripts/` directory (like `make_win_release.bat`).
