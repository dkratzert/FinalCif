from qtpy import QtCore
from qtpy.QtWidgets import QTextEdit, QSizePolicy


class SingleLineTextEdit(QTextEdit):
    """A QTextEdit that mimics QLineEdit height behaviour: fixed single-line height,
    expanding horizontally.  The widget still renders rich/HTML text, which is why a
    plain QLineEdit cannot be used here."""

    def __init__(self, parent=None):
        super().__init__(parent)
        sp = self.sizePolicy()
        sp.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(sp)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTabChangesFocus(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def _single_line_height(self) -> int:
        fm = self.fontMetrics()
        # font cap height + descenders + standard vertical padding (matches QLineEdit)
        return fm.height() + 10

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(super().sizeHint().width(), self._single_line_height())

    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(super().minimumSizeHint().width(), self._single_line_height())
