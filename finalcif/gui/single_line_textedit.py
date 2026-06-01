from qtpy import QtCore
from qtpy.QtWidgets import QAbstractScrollArea, QTextEdit, QSizePolicy


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
        # AdjustIgnored prevents content width from being used as the minimum width,
        # which would otherwise prevent the window from being resized narrower.
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.setTabChangesFocus(True)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

    def _single_line_height(self) -> int:
        fm = self.fontMetrics()
        # font cap height + descenders + standard vertical padding (matches QLineEdit)
        return fm.height() + 10

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(super().sizeHint().width(), self._single_line_height())

    def minimumSizeHint(self) -> QtCore.QSize:
        # Width 0 means no minimum horizontal constraint, so the window can be freely
        # resized narrower without being blocked by the content width of these fields.
        return QtCore.QSize(0, self._single_line_height())
