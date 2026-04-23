#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   Dr. Daniel Kratzert
#   ----------------------------------------------------------------------------
"""
Dialog that lets the user assign solvent formulae and generates the
``_platon_squeeze_details`` or ``_smtbx_masks_special_details`` text for
structures refined with PLATON SQUEEZE or Olex2/SMTBX solvent masks.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from qtpy import QtCore, compat
from qtpy.QtGui import QColor
from qtpy.QtWidgets import (
    QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QMessageBox,
    QPlainTextEdit, QPushButton, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget,
)

from finalcif.tools.squeeze import build_details_text, electrons_from_formula

if TYPE_CHECKING:
    from finalcif.cif.cif_file_io import CifContainer

# Column indices in the void table
_COL_NR = 0
_COL_VOL = 1
_COL_ELEC_PLATON = 2
_COL_FORMULA = 3
_COL_ELEC_CALC = 4
_COL_DELTA = 5

# ── PLATON SQUEEZE keys ──────────────────────────────────────────────────────
_SQUEEZE_LOOP_KEY = '_platon_squeeze_void_nr'
_SQUEEZE_LOOP_TAGS = [
    '_platon_squeeze_void_nr',
    '_platon_squeeze_void_average_x',
    '_platon_squeeze_void_average_y',
    '_platon_squeeze_void_average_z',
    '_platon_squeeze_void_volume',
    '_platon_squeeze_void_count_electrons',
    '_platon_squeeze_void_content',
    '_platon_squeeze_void_probe_radius',
]

# ── Olex2/SMTBX solvent mask keys ────────────────────────────────────────────
_SMTBX_LOOP_KEY = '_smtbx_masks_void_nr'
_SMTBX_LOOP_TAGS = [
    '_smtbx_masks_void_nr',
    '_smtbx_masks_void_average_x',
    '_smtbx_masks_void_average_y',
    '_smtbx_masks_void_average_z',
    '_smtbx_masks_void_volume',
    '_smtbx_masks_void_count_electrons',
    '_smtbx_masks_void_content',
]

# ── Per-mode dialog configuration ────────────────────────────────────────────
_MODE_CONFIG: dict[str, dict] = {
    'squeeze': {
        'loop_key': _SQUEEZE_LOOP_KEY,
        'loop_tags': _SQUEEZE_LOOP_TAGS,
        'vol_tag': '_platon_squeeze_void_volume',
        'elec_tag': '_platon_squeeze_void_count_electrons',
        'content_tag': '_platon_squeeze_void_content',
        'details_key': '_platon_squeeze_details',
        'title': 'PLATON SQUEEZE \u2013 Assign Solvent Content',
        'info': (
            'PLATON/SQUEEZE was used. '
            'Assign the solvent formula per void <b>per unit cell</b>, e.g. <tt>2(H2O)</tt>.'
        ),
        'details_label': 'SQUEEZE details (<i>_platon_squeeze_details</i>):',
        'electrons_col_header': 'Electrons\n(PLATON)',
    },
    'smtbx': {
        'loop_key': _SMTBX_LOOP_KEY,
        'loop_tags': _SMTBX_LOOP_TAGS,
        'vol_tag': '_smtbx_masks_void_volume',
        'elec_tag': '_smtbx_masks_void_count_electrons',
        'content_tag': '_smtbx_masks_void_content',
        'details_key': '_smtbx_masks_special_details',
        'title': 'Olex2/SMTBX Masks \u2013 Assign Solvent Content',
        'info': (
            'Olex2/SMTBX solvent masks were used. '
            'Assign the solvent formula per void <b>per unit cell</b>, e.g. <tt>2(H2O)</tt>.'
        ),
        'details_label': 'Masks details (<i>_smtbx_masks_special_details</i>):',
        'electrons_col_header': 'Electrons\n(Masks)',
    },
}

_COLOR_OK = QColor(200, 255, 200)      # light green
_COLOR_WARN = QColor(255, 200, 200)    # light red
_COLOR_NEUTRAL = QColor(255, 255, 255) # white


class SqueezeSolventDialog(QDialog):
    """
    Modal dialog for entering PLATON SQUEEZE or Olex2/SMTBX solvent mask content.

    The dialog reads the existing void loop from *cif* and lets the user assign a
    chemical formula (per unit cell) to each void.  The electron count from that
    formula is automatically calculated and compared to the value reported by the
    refinement program so the user can judge whether the assignment is chemically
    reasonable.

    Supported modes (auto-detected from the CIF when *mode* is not given):

    * ``'squeeze'`` - PLATON SQUEEZE (``_platon_squeeze_*`` keys)
    * ``'smtbx'``   - Olex2/SMTBX solvent masks (``_smtbx_masks_*`` keys)

    After the user clicks **OK**:
    * The ``_*_void_content`` column in the void loop is updated.
    * The corresponding details key is written as a descriptive sentence
      for each void.

    For SQUEEZE mode: if no loop is present in *cif*, the dialog first offers to
    locate and import the corresponding ``.sqf`` file.
    """

    def __init__(
        self,
        cif: 'CifContainer',
        mode: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.cif = cif
        # Validate and resolve operating mode
        if mode is not None and mode not in _MODE_CONFIG:
            raise ValueError(
                f"Invalid mode {mode!r}. Valid modes are: {list(_MODE_CONFIG)}"
            )
        self._loop_mode: str = mode if mode is not None else self._auto_detect_mode()
        self._cfg = _MODE_CONFIG[self._loop_mode]
        self.setWindowTitle(self._cfg['title'])
        self.setMinimumWidth(750)
        self._build_ui()
        if self._has_loop():
            self._populate_table()
        elif self._loop_mode == 'squeeze':
            self._ask_for_sqf_file()
        else:
            # smtbx loop absent - nothing to import; populate (empty) table
            self._populate_table()

    # ------------------------------------------------------------------
    # Mode detection
    # ------------------------------------------------------------------

    def _auto_detect_mode(self) -> str:
        """Return 'smtbx' when an smtbx void loop is present, else 'squeeze'."""
        if self._check_loop_present(_SMTBX_LOOP_KEY):
            return 'smtbx'
        return 'squeeze'

    def _check_loop_present(self, key: str) -> bool:
        """Return True when a CIF loop containing *key* exists and is non-empty."""
        try:
            loop = self.cif.get_loop(key)
            return loop is not None and loop.width() > 0
        except (AttributeError, RuntimeError, TypeError):
            return False

    def _has_loop(self) -> bool:
        """Return True when the mode-appropriate void loop is present in the CIF."""
        return self._check_loop_present(self._cfg['loop_key'])

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        # info label
        info = QLabel(self._cfg['info'])
        info.setWordWrap(True)
        layout.addWidget(info)

        # void table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            'Void #', 'Volume (\u00c5\u00b3)', self._cfg['electrons_col_header'],
            'Solvent formula\n(per unit cell)',
            'Electrons\n(calc.)', '\u0394 electrons',
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(_COL_NR, 55)
        self.table.setColumnWidth(_COL_VOL, 85)
        self.table.setColumnWidth(_COL_ELEC_PLATON, 85)
        self.table.setColumnWidth(_COL_FORMULA, 160)
        self.table.setColumnWidth(_COL_ELEC_CALC, 85)
        self.table.verticalHeader().setVisible(False)
        self.table.itemChanged.connect(self._on_formula_changed)
        layout.addWidget(self.table)

        # fill-down button row
        btn_row = QHBoxLayout()
        self.fill_down_btn = QPushButton('Fill down from void 1')
        self.fill_down_btn.setToolTip(
            'Copy the formula from the first void to all other voids.'
        )
        self.fill_down_btn.clicked.connect(self._fill_down)
        btn_row.addWidget(self.fill_down_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        # details label + editor
        layout.addWidget(QLabel(self._cfg['details_label']))
        self.details_edit = QPlainTextEdit()
        self.details_edit.setPlaceholderText(
            'Auto-generated when you enter formulae above. You may edit freely.'
        )
        self.details_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.details_edit.setMinimumHeight(80)
        self.details_edit.setMaximumHeight(140)
        layout.addWidget(self.details_edit)

        # pre-fill from existing details key if present
        self._details_user_modified = False
        existing_details = self.cif[self._cfg['details_key']]
        if existing_details:
            self._details_user_modified = True
            self.details_edit.setPlainText(existing_details)
        self.details_edit.textChanged.connect(self._on_details_text_changed)

        # button box
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self._on_accept)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    # ------------------------------------------------------------------
    # Data helpers
    # ------------------------------------------------------------------

    def _ask_for_sqf_file(self) -> None:
        """
        Try to auto-locate a .sqf file next to the CIF.  If not found,
        open a file-chooser dialog.  Import the chosen file into the CIF.
        (SQUEEZE mode only.)
        """
        cif_path = Path(self.cif.fileobj)
        candidate = cif_path.with_suffix('.sqf')
        sqf_path: str = ''

        if candidate.exists():
            sqf_path = str(candidate)
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('PLATON SQUEEZE \u2013 .sqf file required')
            msg.setText(
                'No SQUEEZE data found in the current CIF.\n\n'
                'Please locate the corresponding .sqf file produced by PLATON.'
            )
            msg.setIcon(QMessageBox.Icon.Information)
            open_btn = msg.addButton('Choose .sqf file\u2026', QMessageBox.ButtonRole.AcceptRole)
            msg.addButton('Skip', QMessageBox.ButtonRole.RejectRole)
            msg.exec()
            if msg.clickedButton() is open_btn:
                sqf_path, _ = compat.getopenfilename(
                    parent=self,
                    caption='Open PLATON .sqf file',
                    basedir=str(cif_path.parent),
                    filters='PLATON SQUEEZE file (*.sqf)',
                    selectedfilter='PLATON SQUEEZE file (*.sqf)',
                )

        if sqf_path:
            self._import_sqf(Path(sqf_path))
        # Populate table regardless (may stay empty if import failed / skipped)
        self._populate_table()

    def _import_sqf(self, sqf_path: Path) -> None:
        """
        Import the SQUEEZE loop from the .sqf file into the current CIF block.
        """
        from finalcif.cif.cif_file_io import CifContainer
        try:
            sqf_cif = CifContainer(sqf_path)
        except Exception as exc:
            QMessageBox.warning(self, 'Import failed', f'Could not read {sqf_path.name}:\n{exc}')
            return

        # The .sqf loop uses any subset of _SQUEEZE_LOOP_TAGS
        existing_tags = [t for t in _SQUEEZE_LOOP_TAGS if sqf_cif.get_loop_column(t)]
        if not existing_tags:
            QMessageBox.warning(
                self, 'Import failed',
                f'No SQUEEZE loop data found in {sqf_path.name}.'
            )
            return

        columns = [sqf_cif.get_loop_column(t) for t in existing_tags]
        self.cif.add_loop_from_columns(existing_tags, columns)

    def _populate_table(self) -> None:
        """Fill the void table from the current CIF's mode-appropriate void loop."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        if not self._has_loop():
            self.table.blockSignals(False)
            return

        # Fetch each column, falling back to empty list when absent
        def _col(tag: str) -> list[str]:
            try:
                return self.cif.get_loop_column(tag)
            except (AttributeError, RuntimeError):
                return []

        cfg = self._cfg
        nrs = _col(cfg['loop_key'])
        volumes = _col(cfg['vol_tag'])
        electrons = _col(cfg['elec_tag'])
        contents = _col(cfg['content_tag'])

        n_rows = len(nrs)
        self.table.setRowCount(n_rows)

        for row_idx in range(n_rows):
            nr_item = QTableWidgetItem(nrs[row_idx] if row_idx < len(nrs) else '?')
            nr_item.setFlags(nr_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            vol_item = QTableWidgetItem(volumes[row_idx] if row_idx < len(volumes) else '?')
            vol_item.setFlags(vol_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            elec_item = QTableWidgetItem(electrons[row_idx] if row_idx < len(electrons) else '?')
            elec_item.setFlags(elec_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            formula_val = ''
            if row_idx < len(contents) and contents[row_idx] not in ('?', '.', ''):
                formula_val = contents[row_idx]
            formula_item = QTableWidgetItem(formula_val)

            elec_calc_item = QTableWidgetItem('')
            elec_calc_item.setFlags(elec_calc_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            delta_item = QTableWidgetItem('')
            delta_item.setFlags(delta_item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

            self.table.setItem(row_idx, _COL_NR, nr_item)
            self.table.setItem(row_idx, _COL_VOL, vol_item)
            self.table.setItem(row_idx, _COL_ELEC_PLATON, elec_item)
            self.table.setItem(row_idx, _COL_FORMULA, formula_item)
            self.table.setItem(row_idx, _COL_ELEC_CALC, elec_calc_item)
            self.table.setItem(row_idx, _COL_DELTA, delta_item)

            # Initialise calculated columns for any pre-existing formula
            if formula_val:
                self._update_row_calculations(row_idx)

        self.table.blockSignals(False)
        self._regenerate_details()

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _on_details_text_changed(self) -> None:
        """Mark details as user-modified so auto-regeneration stops overwriting it."""
        self._details_user_modified = True

    def _on_formula_changed(self, item: QTableWidgetItem) -> None:
        if item.column() != _COL_FORMULA:
            return
        self._update_row_calculations(item.row())
        self._regenerate_details()

    def _update_row_calculations(self, row_idx: int) -> None:
        """Recalculate Electrons (calc.) and Δ for a given row."""
        formula_item = self.table.item(row_idx, _COL_FORMULA)
        elec_platon_item = self.table.item(row_idx, _COL_ELEC_PLATON)
        elec_calc_item = self.table.item(row_idx, _COL_ELEC_CALC)
        delta_item = self.table.item(row_idx, _COL_DELTA)

        if not all([formula_item, elec_platon_item, elec_calc_item, delta_item]):
            return

        formula = formula_item.text().strip()

        if not formula:
            elec_calc_item.setText('')
            elec_calc_item.setBackground(_COLOR_NEUTRAL)
            delta_item.setText('')
            delta_item.setBackground(_COLOR_NEUTRAL)
            return

        calc_e = electrons_from_formula(formula)
        elec_calc_item.setText(str(calc_e))

        try:
            platon_e = float(elec_platon_item.text())
            delta = calc_e - round(platon_e)
            delta_item.setText(str(delta))
            color = _COLOR_OK if abs(delta) <= 5 else _COLOR_WARN
            delta_item.setBackground(color)
            elec_calc_item.setBackground(color)
        except (ValueError, TypeError):
            delta_item.setText('')
            delta_item.setBackground(_COLOR_NEUTRAL)
            elec_calc_item.setBackground(_COLOR_NEUTRAL)

    def _fill_down(self) -> None:
        """Copy the formula from void 1 (row 0) to all subsequent rows."""
        if self.table.rowCount() < 2:
            return
        first_item = self.table.item(0, _COL_FORMULA)
        if not first_item:
            return
        formula = first_item.text()
        self.table.blockSignals(True)
        for row_idx in range(1, self.table.rowCount()):
            item = self.table.item(row_idx, _COL_FORMULA)
            if item:
                item.setText(formula)
            self._update_row_calculations(row_idx)
        self.table.blockSignals(False)
        self._regenerate_details()

    def _regenerate_details(self) -> None:
        """Auto-regenerate the details text, but only while the user hasn't modified it."""
        if self._details_user_modified:
            return
        void_rows = []
        for row_idx in range(self.table.rowCount()):
            vol_item = self.table.item(row_idx, _COL_VOL)
            formula_item = self.table.item(row_idx, _COL_FORMULA)
            elec_item = self.table.item(row_idx, _COL_ELEC_PLATON)
            void_rows.append({
                'nr': row_idx + 1,
                'volume': vol_item.text() if vol_item else '?',
                'electrons_platon': elec_item.text() if elec_item else '?',
                'formula': formula_item.text() if formula_item else '',
            })
        text = build_details_text(void_rows, method=self._loop_mode)
        if text:
            # Block textChanged so our programmatic update doesn't set _details_user_modified
            self.details_edit.blockSignals(True)
            self.details_edit.setPlainText(text)
            self.details_edit.blockSignals(False)

    # ------------------------------------------------------------------
    # Accept / write-back
    # ------------------------------------------------------------------

    def _on_accept(self) -> None:
        """Write formulae and details back to the CIF and close."""
        if not self._has_loop():
            self.accept()
            return

        cfg = self._cfg

        # Gather all current loop column data
        def _col(tag: str) -> list[str]:
            try:
                return self.cif.get_loop_column(tag)
            except (AttributeError, RuntimeError):
                return []

        # Determine which tags are present in the existing loop
        present_tags = [t for t in cfg['loop_tags'] if _col(t)]
        if not present_tags:
            self.accept()
            return

        # Build updated column values; replace _void_content with user input
        n_rows = self.table.rowCount()
        new_formulae: list[str] = []
        for row_idx in range(n_rows):
            item = self.table.item(row_idx, _COL_FORMULA)
            formula = item.text().strip() if item else '?'
            new_formulae.append(formula if formula else '?')

        # Reconstruct column data with the updated content column
        content_tag = cfg['content_tag']
        columns: list[list[str]] = []
        for tag in present_tags:
            if tag == content_tag:
                columns.append(new_formulae)
            else:
                col_data = _col(tag)
                # Pad or truncate to n_rows for safety
                while len(col_data) < n_rows:
                    col_data.append('?')
                columns.append(col_data[:n_rows])

        # If content column was not in the original loop, add it
        if content_tag not in present_tags:
            present_tags.append(content_tag)
            columns.append(new_formulae)

        self.cif.add_loop_from_columns(present_tags, columns)

        # Write details text
        details_key = cfg['details_key']
        details = self.details_edit.toPlainText().strip()
        if details:
            self.cif[details_key] = details
        elif details_key in self.cif:
            del self.cif[details_key]

        self.accept()

    # ------------------------------------------------------------------
    # Table data accessor (for tests)
    # ------------------------------------------------------------------

    def formula_for_row(self, row: int) -> str:
        """Return the formula text for the given row index (for testing)."""
        item = self.table.item(row, _COL_FORMULA)
        return item.text() if item else ''

    def delta_for_row(self, row: int) -> str:
        """Return the delta text for the given row index (for testing)."""
        item = self.table.item(row, _COL_DELTA)
        return item.text() if item else ''


# ---------------------------------------------------------------------------
# Module-level helpers (usable without instantiating the dialog)
# ---------------------------------------------------------------------------

def has_smtbx_masks_loop(cif: 'CifContainer') -> bool:
    """Return True when an Olex2/SMTBX solvent masks loop is present in *cif*."""
    try:
        loop = cif.get_loop(_SMTBX_LOOP_KEY)
        return loop is not None and loop.width() > 0
    except (AttributeError, RuntimeError, TypeError):
        return False
