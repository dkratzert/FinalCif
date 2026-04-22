from __future__ import annotations

from qtpy import QtCore
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QTableWidgetItem

# Re-export Column from its canonical location so existing imports still work.
from finalcif.gui.cif_table_model import Column  # noqa: F401

white = QColor(255, 255, 255)
light_green = QColor(217, 255, 201)
light_blue = QColor(244, 244, 249)
blue = QColor(102, 150, 179)
yellow = QColor(250, 247, 150)  # #faf796
light_red = QColor(254, 191, 189)


class MyTableWidgetItem(QTableWidgetItem):

    def __init__(self, *args, **kwargs):
        # args and kwargs are essential here. Otherwise, the horizontal header text is missing!
        super().__init__(*args, **kwargs)

    def setUneditable(self) -> None:
        # noinspection PyTypeChecker
        self.setFlags(self.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable)
        # noinspection PyTypeChecker
        self.setFlags(self.flags() | QtCore.Qt.ItemFlag.ItemIsSelectable)


class CifOrderItem(MyTableWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setUneditable()

    def isEssential(self):
        return self.checkState() == Qt.Checked

    def setEssential(self, state: bool):
        if state is True:
            self.setCheckState(Qt.Checked)
        else:
            self.setCheckState(Qt.Unchecked)
