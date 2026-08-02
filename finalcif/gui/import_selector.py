import shutil
from pathlib import Path
from typing import Any, Iterable

import gemmi
from qtpy import QtWidgets, QtCore

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.import_selector_ui import Ui_importSelectMainWindow
from finalcif.tools import misc
from finalcif.tools.settings import FinalCifSettings

EMPTY_VALUES = frozenset(('', '?'))


class ImportSelector(QtWidgets.QMainWindow):
    import_clicked = QtCore.Signal(list, list)

    def __init__(self, parent, import_cif: CifContainer, target_cif: CifContainer | None, settings: FinalCifSettings) -> None:
        super().__init__(parent)
        self.import_cif = import_cif
        self.target_cif = target_cif
        self.settings = settings
        self.ui = Ui_importSelectMainWindow()
        self.ui.setupUi(self)
        self.show()
        self.keys_to_import: int = 0
        self.loops_to_import: int = 0
        self.selected: int = 0
        self._raw_values: dict[str, str] = {}
        self._excluded_kv: Iterable[str] = ()
        self._excluded_loops: Iterable[str] = ()
        self._connect_signals_and_slots()

    def _connect_signals_and_slots(self) -> None:
        self.ui.saveSelectionPushbutton.clicked.connect(self._save_selection)
        self.ui.selectOnlyNewPB.clicked.connect(self._select_only_new)
        self.ui.importSelectedPushbutton.clicked.connect(self.import_key_loop)
        self.ui.skipEmptyValuesCheckBox.toggled.connect(self._apply_preselection)

    def import_key_loop(self) -> None:
        self.import_clicked.emit(self.get_keys(include=True), self.get_loops(include=True))

    def show_import_window(self) -> None:
        row = 0
        self._excluded_kv, self._excluded_loops = self._get_excluded_items()
        for item in self.import_cif.block:
            if item.pair is not None:
                key, raw_value = item.pair
                self._raw_values[key] = raw_value
                self._add_checkbox(key, row, self.ui.importTable_keys,
                                   checked=self._should_preselect(key))
                self.keys_to_import += 1
            else:
                continue
            row += 1
        row = 0
        for item in self.import_cif.block:
            if item.loop is not None:
                first_key = item.loop.tags[0]
                self.loops_to_import += 1
                key = '\n'.join(list(item.loop.tags))
                self._add_checkbox(key, row, self.ui.importTable_loops,
                                   checked=first_key not in self._excluded_loops)
            else:
                continue
            row += 1
        self.ui.importTable_keys.horizontalHeader().setStretchLastSection(True)
        self.ui.importTable_loops.horizontalHeader().setStretchLastSection(True)
        self.ui.importTable_keys.resizeRowsToContents()
        self.ui.importTable_loops.resizeRowsToContents()
        self._set_label()

    def _save_selection(self) -> None:
        # Keys that are unchecked only because of the automatic rules must not end up
        # in the persistent exclusion list.
        keys = [key for key in self.get_keys(include=False) if not self._is_auto_excluded(key)]
        self.settings.save_key_value('do_not_import_keys', keys)
        self.settings.save_key_value('do_not_import_loops', self.get_loops(include=False))

    def _empty_saved_selection(self) -> None:
        self.settings.save_key_value('do_not_import_keys', [])
        self.settings.save_key_value('do_not_import_loops', [])

    def _get_excluded_items(self) -> tuple[Iterable | list | int | float, Iterable | list | int | float]:
        excluded_kv = misc.do_not_import_keys
        excluded_loops = misc.do_not_loop_import
        exclude_kv_from_settings = self.settings.load_value_of_key('do_not_import_keys')
        exclude_loops_from_settings = self.settings.load_value_of_key('do_not_import_loops')
        if exclude_kv_from_settings:
            excluded_kv = exclude_kv_from_settings
        if exclude_loops_from_settings:
            excluded_loops = exclude_loops_from_settings
        return excluded_kv, excluded_loops

    def _set_label(self) -> None:
        self.ui.importInfoLabel.setText(f"Importing\n{self.import_cif.fileobj}\n\n"
                                        f"The CIF to import contains {self.keys_to_import} keys "
                                        f"and {self.loops_to_import} loops from which "
                                        f"{len(self.get_keys(include=True)) + len(self.get_loops(include=True))} "
                                        f"are selected for import.")

    def _add_checkbox(self, text: str, row: int, col: QtWidgets.QTableWidget, checked: bool = False) -> None:
        if col.rowCount() <= row:
            col.insertRow(row)
        checkbox = QtWidgets.QCheckBox(col)
        checkbox.stateChanged.connect(self._set_label)
        checkbox.setText(text)
        col.setCellWidget(row, 0, checkbox)
        checkbox.setChecked(checked)

    def get_keys(self, include: bool) -> list[str]:
        return [widget.text() for widget in self._key_widgets() if widget.isChecked() == include]

    def get_loops(self, include: bool) -> list[list[str]]:
        loops = []
        rows = self.ui.importTable_loops.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_loops.cellWidget(row, 0)
            if widget and widget.isChecked() == include:
                loop: list[str] = widget.text().splitlines(keepends=False)
                loops.append(loop)
        return loops

    def _is_empty_value(self, key: str) -> bool:
        return gemmi.cif.as_string(self._raw_values.get(key, '')).strip() in EMPTY_VALUES

    def _is_auto_excluded(self, key: str) -> bool:
        """A key that is never preselected because of an automatic rule."""
        if key.startswith('_vrf'):
            return True
        return self.ui.skipEmptyValuesCheckBox.isChecked() and self._is_empty_value(key)

    def _should_preselect(self, key: str) -> bool:
        if self._is_auto_excluded(key):
            return False
        return key not in self._excluded_kv

    def _apply_preselection(self) -> None:
        for widget in self._key_widgets():
            widget.setChecked(self._should_preselect(widget.text()))

    def _select_only_new(self) -> None:
        self.select_pairs()
        self.select_loops()

    def _key_widgets(self) -> list[QtWidgets.QCheckBox]:
        widgets = []
        for row in range(self.ui.importTable_keys.rowCount()):
            widget: QtWidgets.QCheckBox = self.ui.importTable_keys.cellWidget(row, 0)
            if widget:
                widgets.append(widget)
        return widgets

    def select_pairs(self):
        for widget in self._key_widgets():
            key = widget.text()
            # Import only new key/values
            widget.setChecked(not self.target_cif[key] and not self._is_auto_excluded(key))

    def select_loops(self):
        rows = self.ui.importTable_loops.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_loops.cellWidget(row, 0)
            loop = widget.text()
            first_key = loop.splitlines(keepends=False)[0]
            if self.target_cif.block.find_loop(first_key):
                # Import only new key/values
                widget.setChecked(False)
                continue
            widget.setChecked(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    imp_cif = CifContainer('test-data/DK_Zucker2_0m.cif')
    shutil.copyfile('test-data/p21c.cif', 'test-data/p21c-copy.cif')
    targetcif = CifContainer('test-data/p21c-copy.cif')
    settings = FinalCifSettings()
    imp = ImportSelector(None, import_cif=imp_cif, target_cif=targetcif, settings=settings)
    imp.show_import_window()
    app.exec()
    Path('test-data/p21c-copy.cif').unlink(missing_ok=True)
    sys.exit()
