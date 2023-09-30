from typing import List

from qtpy import QtWidgets

from finalcif.cif.cif_file_io import CifContainer
from finalcif.gui.import_selector_ui import Ui_importSelectMainWindow


class ImportSelector(QtWidgets.QMainWindow):
    def __init__(self, parent, cif: CifContainer):
        super().__init__(parent)
        self.parent = parent
        self.cif = cif
        self.w = Ui_importSelectMainWindow()
        self.w.setupUi(self)
        self.show()
        self.keys_to_import: int = 0
        self.loops_to_import: int = 0
        self.selected: int = 0

    def show_import_window(self, imp_cif: 'CifContainer') -> None:
        row = 0
        for item in imp_cif.block:
            if item.pair is not None:
                self.keys_to_import += 1
                text, _ = item.pair
            elif item.loop is not None:
                self.loops_to_import += 1
                text = '_loop'+'\n'.join([x for x in item.loop.tags])
            else:
                continue
            self.w.importTable.insertRow(row)
            self.add_checkbox(text, row, self.w)
            row += 1
        self.w.importTable.resizeColumnsToContents()
        self.w.importTable.resizeRowsToContents()
        self._set_label()

    def _set_label(self):
        self.w.importInfoLabel.setText(f"The CIF to import contains {self.keys_to_import} keys "
                                       f"and {self.loops_to_import} loops to import from which "
                                       f"{len(self.get_keys_to_import()) + len(self.get_loops_to_import())} "
                                       f"are selected.")

    def add_checkbox(self, text: str, row: int, w: Ui_importSelectMainWindow):
        c = QtWidgets.QCheckBox(w.importTable)
        c.stateChanged.connect(self._set_label)
        c.setText(text)
        w.importTable.setCellWidget(row, 0, c)

    def get_keys_to_import(self) -> List[str]:
        keys = []
        rows = self.w.importTable.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.w.importTable.cellWidget(row, 0)
            if widget.isChecked() and '_loop' not in widget.text():
                keys.append(widget.text())
        return keys

    def get_loops_to_import(self) -> List[List[str]]:
        loops = []
        rows = self.w.importTable.rowCount()
        for row in range(rows):
            widget: QtWidgets.QCheckBox = self.w.importTable.cellWidget(row, 0)
            if widget.isChecked() and '_loop' in widget.text():
                loop: List[str] = widget.text().splitlines(keepends=True)[1:]
                loops.append(loop)
        return loops


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    cif = CifContainer('test-data/1000006.cif')
    imp = ImportSelector(None, cif)
    imp.show_import_window(cif)
    sys.exit(app.exec())
