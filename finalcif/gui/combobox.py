from textwrap import wrap
from typing import TYPE_CHECKING

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtWidgets import QComboBox, QSizePolicy, QAction

from finalcif.gui.validators import validators

light_red = QtGui.QColor(254, 191, 189)
white = QtGui.QColor(255, 255, 255)

if TYPE_CHECKING:
    from finalcif.gui.custom_classes import MyCifTable


class MyComboBox(QComboBox):
    """
    A special QComboBox with convenient methods to set the background color and other things.
    """
    textTemplate = QtCore.pyqtSignal(int)

    def __init__(self, parent: 'MyCifTable' = None):
        super().__init__(parent)
        self.parent: 'MyCifTable' = parent
        self.cif_key = ''
        self.color = white
        self.default_palette = self.palette()
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

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        super().keyPressEvent(event)
        self.validate_text(self.currentText())

    def validate_text(self, text: str):
        validator = validators.get(self.cif_key, None)
        if validator and not validator.valid(text):
            self.setBadStyle()
            self.setToolTip(validator.help_text)
        else:
            self.setToolTip('')
            self.setRegularStyle()

    def setBadStyle(self) -> None:
        palette = self.palette()
        palette.setColor(self.backgroundRole(), light_red)
        self.setPalette(palette)

    def setRegularStyle(self) -> None:
        self.setPalette(self.default_palette)

    def setUneditable(self):
        # noinspection PyUnresolvedReferences
        self.setFlags(self.flags() ^ Qt.ItemIsEditable)

    def setText(self, txt: str):
        self.setEditText('\n'.join(wrap(txt, width=80)))

    def addItem(self, *__args):
        text = '\n'.join(wrap(__args[0], width=80))
        super().addItem(text, __args[1])
