from contextlib import suppress
from textwrap import wrap

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtWidgets import QComboBox, QSizePolicy, QAction

with suppress(ImportError):
    from finalcif.gui.custom_classes import MyCifTable


class MyComboBox(QComboBox):
    """
    A special QComboBox with convenient methods to set the background color and other things.
    """
    textTemplate = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent: 'MyCifTable' = parent
        self.setParent(parent)
        self.cif_key = ''
        self.setFocusPolicy(Qt.StrongFocus)
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLength)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setEditable(True)  # only editable as new template
        self.installEventFilter(self)
        self.actionDelete = QAction("Delete Row", self)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(self.actionDelete)
        self.actionDelete.triggered.connect(self._delete_row)
        action_template = QAction("Text Template", self)
        self.addAction(action_template)
        action_template.triggered.connect(lambda: self.textTemplate.emit(self.row))

    def __str__(self):
        return self.currentText()

    @property
    def row(self) -> int:
        return self.parent.vheaderitems.index(self.cif_key)

    def _delete_row(self):
        self.parent.delete_row(self.row)

    def _on_create_template(self):
        self.textTemplate.emit(self.row)

    def eventFilter(self, widget: QObject, event: QEvent):
        """
        Event filter to ignore wheel events in comboboxes to prevent accidental changes to them.
        """
        if event.type() == QEvent.Wheel:  # and widget and not widget.hasFocus():
            event.ignore()
            return True
        return QObject.eventFilter(self, widget, event)

    def setUneditable(self):
        # noinspection PyUnresolvedReferences
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

    def setText(self, txt: str):
        self.setEditText('\n'.join(wrap(txt, width=80)))

    def addItem(self, *__args):
        text = '\n'.join(wrap(__args[0], width=80))
        super().addItem(text, __args[1])
