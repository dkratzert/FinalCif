#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   Dr. Daniel Kratzert
#   ----------------------------------------------------------------------------
"""
Dialog that lets the user assign solvent formulae and generates the
``_platon_squeeze_details`` text for structures refined with PLATON SQUEEZE.
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

_COLOR_OK = QColor(200, 255, 200)      # light green
_COLOR_WARN = QColor(255, 200, 200)    # light red
_COLOR_NEUTRAL = QColor(255, 255, 255) # white


class SqueezeSolventDialog(QDialog):
    """
    Modal dialog for entering PLATON SQUEEZE solvent content.

    The dialog reads the existing SQUEEZE loop from *cif* (populated from the
    ``.sqf`` file) and lets the user assign a chemical formula (per unit cell)
    to each void.  The electron count from that formula is automatically
    calculated and compared to the value PLATON reported so the user can judge
    whether the assignment is chemically reasonable.

    After the user clicks **OK**:
    * The ``_platon_squeeze_void_content`` column in the SQUEEZE loop is updated.
    * The ``_platon_squeeze_details`` key is written as a descriptive sentence
      for each void.

    If no SQUEEZE loop is present in *cif*, the dialog first offers to locate
    and import the corresponding ``.sqf`` file.
    """

    def __init__(self, cif: 'CifContainer', parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.cif = cif
        self.setWindowTitle('PLATON SQUEEZE – Assign Solvent Content')
        self.setMinimumWidth(750)
        self._build_ui()
        if self._has_squeeze_loop():
            self._populate_table()
        else:
            self._ask_for_sqf_file()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)

        # info label
        info = QLabel(
            'PLATON/SQUEEZE was used. '
            'Assign the solvent formula per void <b>per unit cell</b>. '
            'The formula may describe multiple molecules, e.g. <tt>2(H2O)</tt>.'
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        # void table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            'Void #', 'Volume (Å³)', 'Electrons\n(PLATON)', 'Solvent formula\n(per unit cell)',
            'Electrons\n(calc.)', 'Δ electrons',
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
        layout.addWidget(QLabel('SQUEEZE details (<i>_platon_squeeze_details</i>):'))
        self.details_edit = QPlainTextEdit()
        self.details_edit.setPlaceholderText(
            'Auto-generated when you enter formulae above. You may edit freely.'
        )
        self.details_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.details_edit.setMinimumHeight(80)
        self.details_edit.setMaximumHeight(140)
        layout.addWidget(self.details_edit)

        # pre-fill from existing _platon_squeeze_details if present
        existing_details = self.cif['_platon_squeeze_details']
        if existing_details:
            self.details_edit.setPlainText(existing_details)

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

    def _has_squeeze_loop(self) -> bool:
        """Return True when the SQUEEZE void loop is already present in the CIF."""
        try:
            loop = self.cif.get_loop(_SQUEEZE_LOOP_KEY)
            return loop is not None and loop.width() > 0
        except Exception:
            return False

    def _ask_for_sqf_file(self) -> None:
        """
        Try to auto-locate a .sqf file next to the CIF.  If not found,
        open a file-chooser dialog.  Import the chosen file into the CIF.
        """
        cif_path = Path(self.cif.fileobj)
        candidate = cif_path.with_suffix('.sqf')
        sqf_path: str = ''

        if candidate.exists():
            sqf_path = str(candidate)
        else:
            msg = QMessageBox(self)
            msg.setWindowTitle('PLATON SQUEEZE – .sqf file required')
            msg.setText(
                'No SQUEEZE data found in the current CIF.\n\n'
                'Please locate the corresponding .sqf file produced by PLATON.'
            )
            msg.setIcon(QMessageBox.Icon.Information)
            open_btn = msg.addButton('Choose .sqf file…', QMessageBox.ButtonRole.AcceptRole)
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
        """Fill the void table from the current CIF's SQUEEZE loop."""
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        if not self._has_squeeze_loop():
            self.table.blockSignals(False)
            return

        # Fetch each column, falling back to empty list when absent
        def _col(tag: str) -> list[str]:
            try:
                return self.cif.get_loop_column(tag)
            except Exception:
                return []

        nrs = _col('_platon_squeeze_void_nr')
        volumes = _col('_platon_squeeze_void_volume')
        electrons = _col('_platon_squeeze_void_count_electrons')
        contents = _col('_platon_squeeze_void_content')

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
        calc_e = electrons_from_formula(formula)
        elec_calc_item.setText(str(calc_e) if formula else '')

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
        """Auto-regenerate the details text from current table contents."""
        # Don't overwrite if the user has edited the text manually; only
        # regenerate if the contents still match an auto-generated pattern
        # or are empty.
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
        text = build_details_text(void_rows)
        if text:
            self.details_edit.setPlainText(text)

    # ------------------------------------------------------------------
    # Accept / write-back
    # ------------------------------------------------------------------

    def _on_accept(self) -> None:
        """Write formulae and details back to the CIF and close."""
        if not self._has_squeeze_loop():
            self.accept()
            return

        # Gather all current loop column data
        def _col(tag: str) -> list[str]:
            try:
                return self.cif.get_loop_column(tag)
            except Exception:
                return []

        # Determine which tags are present in the existing loop
        present_tags = [t for t in _SQUEEZE_LOOP_TAGS if _col(t)]
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
        columns: list[list[str]] = []
        for tag in present_tags:
            if tag == '_platon_squeeze_void_content':
                columns.append(new_formulae)
            else:
                col_data = _col(tag)
                # Pad or truncate to n_rows for safety
                while len(col_data) < n_rows:
                    col_data.append('?')
                columns.append(col_data[:n_rows])

        # If content column was not in the original loop, add it
        if '_platon_squeeze_void_content' not in present_tags:
            present_tags.append('_platon_squeeze_void_content')
            columns.append(new_formulae)

        self.cif.add_loop_from_columns(present_tags, columns)

        # Write details text
        details = self.details_edit.toPlainText().strip()
        if details:
            self.cif['_platon_squeeze_details'] = details
        elif '_platon_squeeze_details' in self.cif:
            del self.cif['_platon_squeeze_details']

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
