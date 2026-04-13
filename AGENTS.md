# FinalCif AI Developer Instructions

## General Principles
- **No Assumptions:** If information or code is missing, ask for it. Do not make assumptions.
- **Refuse over Guessing:** Prefer refusing over guessing. If you don't know how to complete the code, say you don't know.
- **Require Specifications:** If the user asks you to write code, ask for a detailed specification first. Do not write code until you have a detailed specification.
- **Quality Standards:** Follow the rules of 'Refactoring' and 'Clean Code' as described by Martin Fowler and Robert C. Martin, respectively.

## Core Setup Conventions
- **Language/Runtime:** Assume Python 3.14.
- **UI Framework:** Assume PySide6. UI imports in the codebase are typically routed through `qtpy` (note that UI files are compiled locally via bindings).

## Architecture
- **Desktop Application:** FinalCif is a crystallographic information file (CIF) editor built with a Qt frontend.
- **Entry Point:** The application starts from `finalcif/finalcif_start.py` (registered as `finalcif` in `pyproject.toml`).

## Workflow & Commands
- **Dependency Management:** The project uses `uv` for package management (e.g., `uv.lock`, `pyproject.toml`).
  - *Setup:* `uv sync --all-extras --dev`
- **Testing:** 
  - *Command:* `uv run pytest tests`
- **Linting:** 
  - *Command:* `ruff check .`
- **UI Compilation:** 
  - *Command:* `python scripts/compile_ui_files.py` (this discovers `.ui` files, compiles them, and hot-fixes imports to `qtpy`).
- **Build/Releases:** Packaged with `hatchling`. Desktop releases use scripts in the `scripts/` directory (like `make_win_release.bat`).
