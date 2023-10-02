import shutil
from pathlib import Path
from typing import List, Tuple

from qtpy import QtWidgets

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.import_selector_ui import Ui_importSelectMainWindow
from finalcif.tools import misc
from finalcif.tools.misc import do_not_import_keys, do_not_import_from_stoe_cfx
from finalcif.tools.settings import FinalCifSettings


class ImportSelector(QtWidgets.QMainWindow):
    def __init__(self, parent, import_cif: CifContainer, target_cif: CifContainer, settings: FinalCifSettings):
        super().__init__(parent)
        self.parent = parent
        self.import_cif = import_cif
        self.target_cif = target_cif
        self.settings = settings
        self.ui = Ui_importSelectMainWindow()
        self.ui.setupUi(self)
        self.show()
        self.keys_to_import: int = 0
        self.loops_to_import: int = 0
        self.selected: int = 0
        self._connect_signals_and_slots()

    def _connect_signals_and_slots(self):
        self.ui.saveSelectionPushbutton.clicked.connect(self._save_selection)
        self.ui.selectOnlyNewPB.clicked.connect(self._select_only_new)

    def show_import_window(self, imp_cif: 'CifContainer') -> None:
        row = 0
        excluded_kv, excluded_loops = self._get_excluded_items()
        for item in imp_cif.block:
            if item.pair is not None:
                key, _ = item.pair
                self._add_checkbox(key, row, self.ui.importTable_keys, checked=key not in excluded_kv)
                self.keys_to_import += 1
            else:
                continue
            row += 1

        row = 0
        for item in imp_cif.block:
            if item.loop is not None:
                first_key = item.loop.tags[0]
                self.loops_to_import += 1
                key = '\n'.join([x for x in item.loop.tags])
                self._add_checkbox(key, row, self.ui.importTable_loops, checked=first_key not in excluded_loops)
            else:
                continue
            row += 1

        self.ui.importTable_keys.resizeColumnsToContents()
        self.ui.importTable_loops.resizeColumnsToContents()
        self.ui.importTable_keys.resizeRowsToContents()
        self.ui.importTable_loops.resizeRowsToContents()
        self._set_label()

    def _save_selection(self):
        # excluded_kv, excluded_loops = self._get_excluded_items()
        self.settings.save_key_value('do_not_import_keys', self._get_keys_to_exclude())
        self.settings.save_key_value('do_not_import_loops', self._get_loops_to_exclude())

        #self.settings.save_key_value('do_not_import_keys', [])
        #self.settings.save_key_value('do_not_import_loops', [])
        # print(f'Saved keys\n{excluded_kv} and loops\n{excluded_loops}\nto settings')

    def _get_excluded_items(self) -> Tuple[List[str], List[List[str]]]:
        excluded_kv = misc.do_not_import_keys
        excluded_loops = misc.do_not_loop_import
        exclude_kv_from_settings = self.settings.load_value_of_key('do_not_import_keys')
        exclude_loops_from_settings = self.settings.load_value_of_key('do_not_import_loops')
        if exclude_kv_from_settings:
            excluded_kv = exclude_kv_from_settings
        if exclude_loops_from_settings:
            excluded_loops = exclude_loops_from_settings
        return excluded_kv, excluded_loops

    def _set_label(self):
        self.ui.importInfoLabel.setText(f"The CIF to import contains {self.keys_to_import} keys "
                                        f"and {self.loops_to_import} loops to import from which "
                                        f"{len(self._get_keys_to_import()) + len(self._get_loops_to_import())} "
                                        f"are selected for import.")

    def _add_checkbox(self, text: str,
                      row: int,
                      col: QtWidgets.QTableWidget,
                      checked: bool = False):
        if col.rowCount() <= row:
            col.insertRow(row)

        checkbox = QtWidgets.QCheckBox(col)
        checkbox.stateChanged.connect(self._set_label)
        checkbox.setText(text)
        col.setCellWidget(row, 0, checkbox)
        checkbox.setChecked(checked)

    def _get_keys_to_import(self) -> List[str]:
        keys = []
        rows = self.ui.importTable_keys.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_keys.cellWidget(row, 0)
            if widget and widget.isChecked():
                keys.append(widget.text())
        return keys

    def _get_keys_to_exclude(self) -> List[str]:
        keys = []
        rows = self.ui.importTable_keys.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_keys.cellWidget(row, 0)
            if widget and not widget.isChecked():
                keys.append(widget.text())
        return keys

    def _get_loops_to_import(self) -> List[List[str]]:
        loops = []
        rows = self.ui.importTable_loops.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_loops.cellWidget(row, 0)
            if widget and widget.isChecked():
                loop: List[str] = widget.text().splitlines(keepends=True)
                loops.append(loop)
        return loops

    def _get_loops_to_exclude(self) -> List[str]:
        loops = []
        rows = self.ui.importTable_loops.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_loops.cellWidget(row, 0)
            if widget and not widget.isChecked():
                loop: List[str] = widget.text().splitlines(keepends=False)
                loops.append(loop[0])
        print(loops)
        return loops

    def import_loops(self, imp_cif: 'CifContainer'):
        """
        Import all loops from the CifContainer imp_cif to the current block.
        """
        # TODO: read table and import loops accordingly
        for loop in imp_cif.loops:
            if self.ui.importOnlyNewDataCheckBox.isChecked() and self.cif.block.find(loop.tags):
                # Import only new loops
                continue
            if loop.tags[0] in do_not_loop_import:
                continue
            new_loop = self.cif.block.init_loop('', loop.tags)
            for row in imp_cif.block.find(loop.tags):
                new_loop.add_row(row)

    def import_key_value_pairs(self, imp_cif: CifContainer) -> None:
        # TODO: read table and import k/v accordingly
        for item in imp_cif.block:
            if item.pair is not None:
                key, value = item.pair
                # leave out unit cell etc.:
                if self.do_not_import_this_key(key):
                    continue
                if self.ui.importOnlyNewDataCheckBox.isChecked() and self.cif[key]:
                    # Import only new key/values
                    continue
                value = imp_cif.as_string(value)
                if key in self.ui.cif_main_table.vheaderitems:
                    self.ui.cif_main_table.setText(key=key, column=Column.EDIT, txt=value, color=light_green)
                else:
                    self.add_row(key, value)  # , column =Column.EDIT

    def do_not_import_this_key(self, key: str) -> bool:
        value = self.import_cif[key]
        if value == '?' or value.strip() == '':
            return True
        if key in do_not_import_keys:
            return True
        if key in do_not_import_from_stoe_cfx and '.cfx' in self.import_cif.fileobj.name:
            return True
        return False

    def _select_only_new(self):
        rows = self.ui.importTable_keys.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_keys.cellWidget(row, 0)
            key = widget.text()
            if self.target_cif[key]:
                # Import only new key/values
                widget.setChecked(False)
                continue
            widget.setChecked(True)
        rows = self.ui.importTable_loops.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.ui.importTable_loops.cellWidget(row, 0)
            loop = widget.text()
            first_key = loop.splitlines(keepends=False)[0]
            if self.target_cif[first_key]:
                # Import only new key/values
                widget.setChecked(False)
                continue
            widget.setChecked(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    imp_cif = CifContainer('test-data/MCK41.cfx')
    shutil.copyfile('test-data/p21c.cif', 'test-data/p21c-copy.cif')
    targetcif = CifContainer('test-data/p21c-copy.cif')
    settings = FinalCifSettings()
    imp = ImportSelector(None, import_cif=imp_cif, target_cif=targetcif, settings=settings)
    imp.show_import_window(imp_cif)
    app.exec()
    Path('test-data/p21c-copy.cif').unlink(missing_ok=True)
    sys.exit()
