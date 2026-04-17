from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from qtpy import QtCore
from qtpy.QtCore import QAbstractTableModel, QModelIndex, Qt
from qtpy.QtGui import QColor, QBrush

from finalcif.cif.text import retranslate_delimiter

white = QColor(255, 255, 255)
light_green = QColor(217, 255, 201)
light_blue = QColor(244, 244, 249)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)
light_red = QColor(254, 191, 189)

COLUMN_HEADERS = ['CIF Value', 'From Data Source', 'Own Data']


class Column(IntEnum):
    CIF = 0
    DATA = 1
    EDIT = 2


@dataclass
class CifRowData:
    """Data for a single row in the CIF table.

    The ``raw_value`` and ``strval`` fields are transient: they carry the
    original CIF value through the population loop in
    ``AppWindow.fill_cif_table`` so that a single list of ``CifRowData``
    objects can replace both the model rows *and* the former ``prepared``
    dicts.  The model itself never reads them.
    """
    key: str = ''
    cif_value: str = ''
    data_value: str = ''
    edit_value: str = ''
    cif_color: QColor | None = None
    data_color: QColor | None = None
    edit_color: QColor | None = None
    is_separator: bool = False
    # Transient fields used only during table population:
    raw_value: str = ''
    strval: str = ''


class CifTableModel(QAbstractTableModel):
    """Model for the main CIF table holding key-value-pair data."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows: list[CifRowData] = []
        self._key_index: dict[str, int] = {}  # key → row for O(1) lookup

    # --- Core QAbstractTableModel interface ---

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 3

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row_data = self._rows[index.row()]
        col = index.column()
        if row_data.is_separator:
            if role == Qt.ItemDataRole.BackgroundRole:
                brush = QBrush(blue)
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
                return brush
            if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
                return ''
            return None
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if col == 0:
                return row_data.cif_value
            elif col == 1:
                return row_data.data_value
            elif col == 2:
                return row_data.edit_value
        if role == Qt.ItemDataRole.BackgroundRole:
            if col == 0:
                return row_data.cif_color
            elif col == 1:
                return row_data.data_color
            elif col == 2:
                return row_data.edit_color
        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.ItemDataRole.EditRole) -> bool:
        if not index.isValid():
            return False
        row_data = self._rows[index.row()]
        col = index.column()
        if role == Qt.ItemDataRole.EditRole:
            if col == 0:
                row_data.cif_value = value
            elif col == 1:
                row_data.data_value = value
            elif col == 2:
                row_data.edit_value = value
            self.dataChanged.emit(index, index, [role])
            return True
        if role == Qt.ItemDataRole.BackgroundRole:
            if col == 0:
                row_data.cif_color = value
            elif col == 1:
                row_data.data_color = value
            elif col == 2:
                row_data.edit_color = value
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        row_data = self._rows[index.row()]
        if row_data.is_separator:
            return Qt.ItemFlag.ItemIsEnabled
        base = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        if index.column() == 2:
            base |= Qt.ItemFlag.ItemIsEditable
        return base

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if 0 <= section < len(COLUMN_HEADERS):
                    return COLUMN_HEADERS[section]
            elif orientation == Qt.Orientation.Vertical:
                if 0 <= section < len(self._rows):
                    return self._rows[section].key
        if role == Qt.ItemDataRole.BackgroundRole and orientation == Qt.Orientation.Vertical:
            if 0 <= section < len(self._rows) and self._rows[section].is_separator:
                brush = QBrush(blue)
                brush.setStyle(Qt.BrushStyle.DiagCrossPattern)
                return brush
        return None

    # --- Helper methods ---

    @property
    def vheaderitems(self) -> list[str]:
        """Return list of CIF keywords in row order (compatible with old MyCifTable.vheaderitems)."""
        return [r.key for r in self._rows]

    def row_from_key(self, key: str) -> int:
        """Return row index for a given CIF keyword (O(1) via index cache)."""
        try:
            return self._key_index[key]
        except KeyError:
            raise ValueError(f'Key {key!r} not found in model')

    def has_key(self, key: str) -> bool:
        return key in self._key_index

    def add_row(self, key: str, cif_value: str = '', data_value: str = '',
                edit_value: str = '', position: int | None = None,
                is_separator: bool = False) -> int:
        """Insert a new row. Returns the row index where it was inserted."""
        if position is None:
            position = len(self._rows)
        row_data = CifRowData(
            key=key,
            cif_value=cif_value,
            data_value=data_value,
            edit_value=edit_value,
            is_separator=is_separator,
        )
        self.beginInsertRows(QModelIndex(), position, position)
        self._rows.insert(position, row_data)
        # Rebuild key index for rows at and after the insertion point.
        for i in range(position, len(self._rows)):
            self._key_index[self._rows[i].key] = i
        self.endInsertRows()
        return position

    def bulk_load(self, rows: list[CifRowData]) -> None:
        """Replace all rows at once — much faster than per-row add_row.

        Uses a single ``beginResetModel``/``endResetModel`` pair instead
        of N ``beginInsertRows``/``endInsertRows`` calls.
        """
        self.beginResetModel()
        self._rows = list(rows)
        self._key_index = {r.key: i for i, r in enumerate(self._rows)}
        self.endResetModel()

    def remove_row(self, row: int) -> str:
        """Remove a row by index. Returns the key of the removed row."""
        if 0 <= row < len(self._rows):
            key = self._rows[row].key
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._rows[row]
            # Rebuild index for shifted rows.
            self._key_index.pop(key, None)
            for i in range(row, len(self._rows)):
                self._key_index[self._rows[i].key] = i
            self.endRemoveRows()
            return key
        return ''

    def get_row_data(self, row: int) -> CifRowData | None:
        if 0 <= row < len(self._rows):
            return self._rows[row]
        return None

    def set_cell_text(self, row: int, column: int, text: str) -> None:
        """Set text for a specific cell."""
        if 0 <= row < len(self._rows):
            idx = self.index(row, column)
            self.setData(idx, text, Qt.ItemDataRole.EditRole)

    def set_cell_color(self, row: int, column: int, color: QColor | None) -> None:
        """Set background color for a specific cell."""
        if 0 <= row < len(self._rows):
            idx = self.index(row, column)
            self.setData(idx, color, Qt.ItemDataRole.BackgroundRole)

    def get_cell_text(self, row: int, column: int) -> str:
        """Get text for a specific cell."""
        idx = self.index(row, column)
        return self.data(idx, Qt.ItemDataRole.DisplayRole) or ''

    def clear_all(self) -> None:
        """Remove all rows."""
        if self._rows:
            self.beginResetModel()
            self._rows.clear()
            self._key_index.clear()
            self.endResetModel()

    def set_separator(self, row: int) -> None:
        """Mark a row as the separator line."""
        if 0 <= row < len(self._rows):
            self._rows[row].is_separator = True
            self.dataChanged.emit(
                self.index(row, 0), self.index(row, 2),
                [Qt.ItemDataRole.BackgroundRole, Qt.ItemDataRole.DisplayRole],
            )
