#!/usr/bin/python3
# QcodeEditor.py by acbetter.
# -*- coding: utf-8 -*-
# Taken from: https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QColor, QPainter, QTextFormat, QFont
from PySide6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit


class QLineNumberArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.codeEditor = parent

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.codeEditor.line_number_area_paint_event(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

    def line_number_area_width(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = self.fontMetrics().horizontalAdvance('9 ') * digits
        return space

    def update_line_number_area_width(self, _):
        #                             left, top, right, bottom
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(QtCore.Qt.GlobalColor.lightGray).lighter(160)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = f'{block_number + 1} '
                painter.setPen(QtCore.Qt.GlobalColor.black)
                font = painter.font()
                font.setFamily("Courier")
                font.setStyleHint(QtGui.QFont.StyleHint.Monospace)
                painter.setFont(font)
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 QtCore.Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    import sys

    codeEditor = QCodeEditor()
    codeEditor.setPlainText('Foo bar')
    codeEditor.show()
    sys.exit(app.exec())
