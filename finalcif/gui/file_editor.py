from __future__ import annotations
# QcodeEditor.py by acbetter.
# Taken from: https://stackoverflow.com/questions/40386194/create-text-area-textedit-with-line-number-in-pyqt
from collections.abc import Sequence
from dataclasses import dataclass, field

from PySide6.QtCore import QSize
from qtpy import QtCore, QtGui
from qtpy.QtCore import QRect, QSize, Signal
from qtpy.QtGui import QColor, QContextMenuEvent, QPainter, QTextFormat
from qtpy.QtWidgets import QWidget, QPlainTextEdit, QTextEdit

from finalcif.gui import syntax_highlighter
from finalcif.gui.syntax_highlighter import FOLD_PLACEHOLDER_PREFIX

#: Regions with at least this many lines are folded when a CIF is displayed.
FOLD_THRESHOLD = 500

FOLDED_MARKER = '\u25b8'
EXPANDED_MARKER = '\u25be'


@dataclass
class FoldRegion:
    """A range of consecutive, foldable lines of the displayed file.

    ``first`` and ``last`` are inclusive zero-based indices into the original
    line list and cover only the lines that disappear when folded. The line
    above ``first`` (the ``loop_`` header or the opening ``;``) always stays
    visible and carries the fold marker.
    """

    first: int
    last: int
    folded: bool = True

    @property
    def line_count(self) -> int:
        return self.last - self.first + 1


@dataclass
class FoldedText:
    """The document text of a folded file plus its line/marker mapping."""

    lines: list[str] = field(default_factory=list)
    #: original line number for every document block, -1 for placeholder lines
    line_map: list[int] = field(default_factory=list)
    #: document block number -> index into the region list
    marker_rows: dict[int, int] = field(default_factory=dict)


def fold_placeholder(region: FoldRegion) -> str:
    return f'{FOLD_PLACEHOLDER_PREFIX}{region.line_count} lines folded'


def _semicolon_region(lines: Sequence[str], start: int) -> tuple[FoldRegion | None, int]:
    """Foldable body of the semicolon delimited text field opening at *start*."""
    end = start + 1
    while end < len(lines) and not lines[end].startswith(';'):
        end += 1
    # The closing ';' stays visible, so the body ends one line before it.
    return FoldRegion(first=start + 1, last=end - 1), end + 1


def _loop_region(lines: Sequence[str], start: int) -> tuple[FoldRegion | None, int]:
    """Foldable data rows of the loop starting with ``loop_`` at *start*."""
    row = start + 1
    while row < len(lines) and lines[row].lstrip().startswith('_'):
        row += 1
    first_row = row
    while row < len(lines):
        line = lines[row]
        stripped = line.strip()
        if not stripped or stripped.lower() == 'loop_' or line.startswith((';', '_', 'data_')):
            break
        row += 1
    if row == first_row:
        return None, row
    return FoldRegion(first=first_row, last=row - 1), row


def find_foldable_regions(lines: Sequence[str], min_lines: int = FOLD_THRESHOLD) -> list[FoldRegion]:
    """Find semicolon text fields and loop bodies of at least *min_lines* lines."""
    regions: list[FoldRegion] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith(';'):
            region, index = _semicolon_region(lines, index)
        elif line.strip().lower() == 'loop_':
            region, index = _loop_region(lines, index)
        else:
            region, index = None, index + 1
        if region and region.first > 0 and region.line_count >= min_lines:
            regions.append(region)
    return regions


def build_folded_text(lines: Sequence[str], regions: Sequence[FoldRegion]) -> FoldedText:
    """Build the document content in which all folded regions are left out.

    The fold marker sits on the header line of a region (the ``loop_`` header
    or the opening ``;``), which stays visible in both states.
    """
    result = FoldedText()
    position = 0
    for index, region in enumerate(regions):
        for line_number in range(position, region.first):
            result.lines.append(lines[line_number])
            result.line_map.append(line_number)
        if result.lines:
            result.marker_rows.setdefault(len(result.lines) - 1, index)
        if region.folded:
            result.lines.append(fold_placeholder(region))
            result.line_map.append(-1)
        else:
            for line_number in range(region.first, region.last + 1):
                result.lines.append(lines[line_number])
                result.line_map.append(line_number)
        position = region.last + 1
    for line_number in range(position, len(lines)):
        result.lines.append(lines[line_number])
        result.line_map.append(line_number)
    return result


class QLineNumberArea(QWidget):
    def __init__(self, parent: QCodeEditor):
        super().__init__(parent=parent)
        self.codeEditor = parent

    def sizeHint(self) -> QSize:
        return QSize(self.codeEditor.line_number_area_width(), 0)

    def paintEvent(self, event: QtCore.QPaintEvent) -> None:
        self.codeEditor.line_number_area_paint_event(event)

    def mousePressEvent(self, event: QtCore.QMouseEvent) -> None:
        if not self.codeEditor.toggle_fold_at(int(event.position().y())):
            super().mousePressEvent(event)


class QCodeEditor(QPlainTextEdit):
    openInEditor = Signal()

    # The fold markers are drawn this much larger than the line numbers. This
    # does not change the line height, because the markers are painted into
    # the line number area and not into the document.
    marker_scale = 2.0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = syntax_highlighter.CIFSyntaxHighlighter(self)
        self.highlighter.setDocument(self.document())
        self.fold_threshold = FOLD_THRESHOLD
        self._lines: list[str] = []
        self._regions: list[FoldRegion] = []
        self._line_map: list[int] = []
        self._marker_rows: dict[int, int] = {}
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)

    # ---------------------------------------------------------------- folding

    def set_cif_text(self, text: str) -> None:
        """Display *text*, folding every region larger than the fold threshold.

        Folded lines are not inserted into the document at all, which makes
        displaying CIF files with embedded HKL data orders of magnitude faster.
        """
        self._lines = text.split('\n')
        self._regions = find_foldable_regions(self._lines, self.fold_threshold)
        self._rebuild_document()

    @property
    def fold_regions(self) -> list[FoldRegion]:
        return self._regions

    def toggle_fold_at(self, y_position: int) -> bool:
        """Fold or unfold the region whose marker is at *y_position*."""
        return self.toggle_fold_of_block(self._block_number_at(y_position))

    def toggle_fold_of_block(self, block_number: int) -> bool:
        region_index = self._marker_rows.get(block_number)
        if region_index is None:
            return False
        region = self._regions[region_index]
        region.folded = not region.folded
        self._rebuild_document(top_line=self._first_visible_line())
        return True

    def original_line_number(self, block_number: int) -> int:
        """The line number in the file for a block of the document, or -1."""
        if not self._line_map:
            return block_number + 1
        if 0 <= block_number < len(self._line_map):
            return self._line_map[block_number] + 1
        return -1

    def _rebuild_document(self, top_line: int | None = None) -> None:
        folded = build_folded_text(self._lines, self._regions)
        self._line_map = folded.line_map
        self._marker_rows = folded.marker_rows
        self.setPlainText('\n'.join(folded.lines))
        self.update_line_number_area_width(0)
        if top_line is not None:
            self._scroll_to_line(top_line)

    def _first_visible_line(self) -> int:
        block_number = self.firstVisibleBlock().blockNumber()
        return max(self.original_line_number(block_number) - 1, 0)

    def _scroll_to_line(self, line_number: int) -> None:
        for block_number, mapped in enumerate(self._line_map):
            if mapped >= line_number:
                self.verticalScrollBar().setValue(block_number)
                return
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def _block_number_at(self, y_position: int) -> int:
        block = self.firstVisibleBlock()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        while block.isValid() and top <= y_position:
            bottom = top + int(self.blockBoundingRect(block).height())
            if top <= y_position < bottom:
                return block.blockNumber()
            block = block.next()
            top = bottom
        return -1

    # ------------------------------------------------------------------- view

    def contextMenuEvent(self, event: QContextMenuEvent):
        menu = self.createStandardContextMenu(event.pos())
        menu.addSeparator()
        open_in_editor = menu.addAction("Open in Editor")
        open_in_editor.triggered.connect(self.openInEditor.emit)
        menu.exec(event.globalPos())

    def mouseDoubleClickEvent(self, event):
        """Double clicking the placeholder of a folded region expands it."""
        block = self.cursorForPosition(event.position().toPoint()).block()
        # The placeholder always follows the header line that carries the marker.
        if block.text().startswith(FOLD_PLACEHOLDER_PREFIX) and self.toggle_fold_of_block(block.blockNumber() - 1):
            return
        super().mouseDoubleClickEvent(event)

    def marker_font(self) -> QtGui.QFont:
        """The (enlarged) font of the fold markers in the line number area."""
        font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
        font.setPointSizeF(font.pointSizeF() * self.marker_scale)
        return font

    def marker_area_width(self) -> int:
        if not self._regions:
            return 0
        return QtGui.QFontMetrics(self.marker_font()).horizontalAdvance(f'{FOLDED_MARKER} ')

    def line_number_area_width(self):
        digits = 1
        max_value = max(1, len(self._lines) or self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = self.fontMetrics().horizontalAdvance('9 ') * digits
        return space + self.marker_area_width()

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
        number_font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
        marker_font = self.marker_font()
        painter.setFont(number_font)
        marker_width = self.marker_area_width()
        number_width = self.lineNumberArea.width() - marker_width
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                line_number = self.original_line_number(block_number)
                if line_number > 0:
                    painter.setPen(QtCore.Qt.GlobalColor.black)
                    painter.drawText(0, top, number_width, height,
                                     QtCore.Qt.AlignmentFlag.AlignRight, f'{line_number} ')
                region_index = self._marker_rows.get(block_number)
                if region_index is not None:
                    marker = FOLDED_MARKER if self._regions[region_index].folded else EXPANDED_MARKER
                    painter.setPen(QColor(90, 90, 90))
                    painter.setFont(marker_font)
                    painter.drawText(number_width, top, marker_width, bottom - top,
                                     QtCore.Qt.AlignmentFlag.AlignCenter, marker)
                    painter.setFont(number_font)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1


if __name__ == '__main__':
    from qtpy.QtWidgets import QApplication
    import gemmi

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    import sys

    codeEditor = QCodeEditor()
    codeEditor.setMinimumSize(800, 600)
    font = QtGui.QFontDatabase.systemFont(QtGui.QFontDatabase.SystemFont.FixedFont)
    codeEditor.setFont(font)
    options = gemmi.cif.WriteOptions(gemmi.cif.Style(gemmi.cif.Style.Indent35))
    ciftext = gemmi.cif.read('test-data/DK_Zucker2_0m.cif').sole_block().as_string(options)
    codeEditor.set_cif_text(ciftext)
    codeEditor.show()
    sys.exit(app.exec())
