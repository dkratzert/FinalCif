"""Tests for ShelxSyntaxHighlighter (SHELX .ins/.res highlighting).

Written before the implementation exists (TDD): these tests define the
expected behaviour of the highlighter used for the SHELX file viewer on the
results page.
"""
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest

from qtpy.QtGui import QFont, QTextDocument
from qtpy.QtWidgets import QApplication

from finalcif.gui.syntax_highlighter import ShelxSyntaxHighlighter

app = QApplication.instance() or QApplication([])


def _formats(document: QTextDocument, block_number: int) -> list:
    block = document.findBlockByNumber(block_number)
    return list(block.layout().formats())


def _highlighted_document(text: str) -> QTextDocument:
    doc = QTextDocument()
    doc.setPlainText(text)
    highlighter = ShelxSyntaxHighlighter(doc)
    doc._highlighter = highlighter  # type: ignore[attr-defined]
    app.processEvents()
    return doc


class TestShelxSyntaxHighlighterKeywords(unittest.TestCase):

    def test_titl_keyword_is_highlighted(self) -> None:
        doc = _highlighted_document("TITL p21c in P2(1)/c\n")
        formats = _formats(doc, 0)
        self.assertTrue(formats)
        self.assertEqual(0, formats[0].start)
        self.assertEqual(4, formats[0].length)
        self.assertEqual(QFont.Weight.Bold, formats[0].format.fontWeight())

    def test_cell_keyword_is_highlighted(self) -> None:
        doc = _highlighted_document("CELL 0.71073 10.5086 20.9035 20.5072 90 94.13 90\n")
        formats = _formats(doc, 0)
        self.assertTrue(formats)
        self.assertEqual(0, formats[0].start)
        self.assertEqual(4, formats[0].length)

    def test_ls_keyword_with_dot_is_highlighted(self) -> None:
        doc = _highlighted_document("L.S.  1\n")
        formats = _formats(doc, 0)
        self.assertTrue(formats)
        self.assertEqual(0, formats[0].start)
        self.assertEqual(4, formats[0].length)

    def test_restraint_keyword_with_underscore_suffix_is_highlighted(self) -> None:
        """SADI_CCF3 (residue-suffixed restraint name) still highlights SADI."""
        doc = _highlighted_document("SADI_CCF3 0.02 C1 C2 C1 C3 C1 C4\n")
        formats = _formats(doc, 0)
        self.assertTrue(formats)
        self.assertEqual(0, formats[0].start)

    def test_unknown_leading_word_is_not_highlighted_as_keyword(self) -> None:
        doc = _highlighted_document("GA1   6    0.639513    0.561736    0.237758\n")
        formats = _formats(doc, 0)
        keyword_formats = [f for f in formats if f.format.fontWeight() == QFont.Weight.Bold]
        self.assertEqual(0, len(keyword_formats))


class TestShelxSyntaxHighlighterNumbers(unittest.TestCase):

    def test_text_after_keyword_is_dark_brown(self) -> None:
        """Everything after the keyword (title text, numbers, symbols) is colored."""
        doc = _highlighted_document("CELL 0.71073 10.5086 20.9035 20.5072 90 94.13 90\n")
        formats = _formats(doc, 0)
        text = doc.findBlockByNumber(0).text()
        brown_formats = [
            f for f in formats
            if f.format.foreground().color().name() == "#763127"
        ]
        self.assertEqual(1, len(brown_formats))
        self.assertEqual(" 0.71073 10.5086 20.9035 20.5072 90 94.13 90",
                          text[brown_formats[0].start:brown_formats[0].start + brown_formats[0].length])

    def test_title_text_after_titl_keyword_is_dark_brown(self) -> None:
        """Non-numeric text (e.g. a title) after the keyword is colored too."""
        doc = _highlighted_document("TITL p21c in P2(1)/c\n")
        formats = _formats(doc, 0)
        text = doc.findBlockByNumber(0).text()
        brown_formats = [
            f for f in formats
            if f.format.foreground().color().name() == "#763127"
        ]
        self.assertEqual(1, len(brown_formats))
        self.assertEqual(" p21c in P2(1)/c",
                          text[brown_formats[0].start:brown_formats[0].start + brown_formats[0].length])

    def test_no_text_highlighted_on_non_keyword_line(self) -> None:
        """Atom coordinate lines are not "after a keyword" and stay unaffected."""
        doc = _highlighted_document("GA1   6    0.639513    0.561736    0.237758\n")
        formats = _formats(doc, 0)
        brown_formats = [
            f for f in formats
            if f.format.foreground().color().name() == "#763127"
        ]
        self.assertEqual(0, len(brown_formats))



class TestShelxSyntaxHighlighterComments(unittest.TestCase):

    def test_rem_line_is_highlighted_as_comment(self) -> None:
        doc = _highlighted_document("REM this is a comment\n")
        formats = _formats(doc, 0)
        self.assertEqual(1, len(formats))
        self.assertEqual(0, formats[0].start)
        self.assertEqual(len("REM this is a comment"), formats[0].length)

    def test_bang_comment_after_keyword_line_is_highlighted(self) -> None:
        """Anything after '!' is a comment, per the SHELXL manual."""
        text = "LIST 4 ! automatically inserted. Change 6 to 4 for CHECKCIF!!\n"
        doc = _highlighted_document(text)
        formats = _formats(doc, 0)
        block_text = doc.findBlockByNumber(0).text()
        comment_color = "#808080"
        comment_formats = [f for f in formats if f.format.foreground().color().name() == comment_color]
        self.assertEqual(1, len(comment_formats))
        bang_pos = block_text.index('!')
        self.assertEqual(bang_pos, comment_formats[0].start)
        self.assertEqual(block_text[bang_pos:], block_text[comment_formats[0].start:
                                                             comment_formats[0].start + comment_formats[0].length])

    def test_bang_comment_overrides_value_color(self) -> None:
        """The '!' comment takes priority over the keyword-value color."""
        text = "LIST 4 ! a comment\n"
        doc = _highlighted_document(text)
        formats = _formats(doc, 0)
        block_text = doc.findBlockByNumber(0).text()
        bang_pos = block_text.index('!')
        value_color_at_bang = [
            f for f in formats
            if f.format.foreground().color().name() == "#763127" and f.start <= bang_pos < f.start + f.length
        ]
        self.assertEqual(0, len(value_color_at_bang))

    def test_bang_comment_on_atom_line_is_highlighted(self) -> None:
        """'!' comments are not limited to keyword lines."""
        text = "GA1   6    0.639513    0.561736    0.237758 ! disordered\n"
        doc = _highlighted_document(text)
        formats = _formats(doc, 0)
        block_text = doc.findBlockByNumber(0).text()
        bang_pos = block_text.index('!')
        comment_formats = [f for f in formats if f.format.foreground().color().name() == "#808080"]
        self.assertEqual(1, len(comment_formats))
        self.assertEqual(bang_pos, comment_formats[0].start)


class TestShelxSyntaxHighlighterContinuationColoring(unittest.TestCase):
    """A '='-continuation line is treated as part of the unbroken logical
    line: it takes on the same color as the line it continues, not the
    generic indented-comment color."""

    def test_continuation_of_keyword_line_is_value_colored(self) -> None:
        text = (
            "CELL 0.71073 10.5086 20.9035 20.5072 90 94.13 =\n"
            "     90\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 1)
        self.assertEqual(1, len(formats))
        self.assertEqual("#763127", formats[0].format.foreground().color().name())
        self.assertEqual(0, formats[0].start)
        self.assertEqual(len("     90"), formats[0].length)

    def test_continuation_of_atom_line_is_not_colored(self) -> None:
        """Atom-instruction lines aren't keyword lines, so their
        continuation stays plain (no comment, no value color)."""
        text = (
            "GA1   6    0.639513    0.561736    0.237758    11.00000    0.02411    0.02509 =\n"
            "         0.02491    0.00000   -0.00158    0.00159\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 1)
        self.assertEqual(0, len(formats))

    def test_continuation_chain_over_multiple_lines_all_value_colored(self) -> None:
        text = (
            "CELL 0.71073 =\n"
            "     10.5086 =\n"
            "     20.9035\n"
        )
        doc = _highlighted_document(text)
        for block_number in (1, 2):
            formats = _formats(doc, block_number)
            value_formats = [f for f in formats if f.format.foreground().color().name() == "#763127"]
            self.assertEqual(1, len(value_formats))

    def test_continuation_recognized_when_bang_comment_follows_equals(self) -> None:
        """Per the manual, characters after '!' are ignored, so a '='
        followed by a '! comment' still starts a continuation."""
        text = (
            "CELL 0.71073 10.5086 = ! rest of cell on next line\n"
            "     20.9035 20.5072 90 94.13 90\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 1)
        value_formats = [f for f in formats if f.format.foreground().color().name() == "#763127"]
        self.assertEqual(1, len(value_formats))
        self.assertEqual(0, value_formats[0].start)
        self.assertEqual(len("     20.9035 20.5072 90 94.13 90"), value_formats[0].length)

    def test_continuation_root_lookup_skips_comment_after_equals(self) -> None:
        """The root-keyword lookup must also ignore a '!' comment after '='
        when walking back through a multi-line continuation chain."""
        text = (
            "CELL 0.71073 = ! first part\n"
            "     10.5086 = ! second part\n"
            "     20.9035\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 2)
        value_formats = [f for f in formats if f.format.foreground().color().name() == "#763127"]
        self.assertEqual(1, len(value_formats))

    def test_equals_sign_still_highlighted_when_followed_by_comment(self) -> None:
        """The '=' character itself keeps its purple continuation color even
        when trailed by a '! comment'."""
        text = "CELL 0.71073 = ! comment\n"
        doc = _highlighted_document(text)
        formats = _formats(doc, 0)
        block_text = doc.findBlockByNumber(0).text()
        eq_pos = block_text.index('=')
        continuation_formats = [
            f for f in formats
            if f.format.foreground().color().name() == "#800080" and f.start == eq_pos
        ]
        self.assertEqual(1, len(continuation_formats))


class TestShelxSyntaxHighlighterIndentedComments(unittest.TestCase):
    """Per the SHELXL manual: lines that start with spaces and are NOT the
    continuation of a preceding '='-terminated line are plain comments."""

    def test_indented_line_after_titl_is_a_comment(self) -> None:
        text = (
            "TITL p21c in P2(1)/c\n"
            "    p21c.res\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 1)
        self.assertEqual(1, len(formats))
        self.assertEqual(0, formats[0].start)
        self.assertEqual(len("    p21c.res"), formats[0].length)
        self.assertEqual("#808080", formats[0].format.foreground().color().name())

    def test_indented_continuation_line_is_not_a_comment(self) -> None:
        """A line following a trailing '=' is a real continuation, not a comment."""
        text = (
            "GA1   6    0.639513    0.561736    0.237758    11.00000    0.02411    0.02509 =\n"
            "         0.02491    0.00000   -0.00158    0.00159\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 1)
        comment_formats = [f for f in formats if f.format.foreground().color().name() == "#808080"]
        self.assertEqual(0, len(comment_formats))

    def test_indented_comment_chain_continues_over_multiple_lines(self) -> None:
        text = (
            "TITL p21c in P2(1)/c\n"
            "    p21c.res\n"
            "    created by SHELXL-2018/3 at 13:19:54 on 08-Aug-2019\n"
        )
        doc = _highlighted_document(text)
        for block_number in (1, 2):
            formats = _formats(doc, block_number)
            self.assertEqual(1, len(formats))
            self.assertEqual("#808080", formats[0].format.foreground().color().name())


class TestShelxSyntaxHighlighterContinuation(unittest.TestCase):

    def test_trailing_equals_sign_is_highlighted(self) -> None:
        text = (
            "GA1   6    0.639513    0.561736    0.237758    11.00000    0.02411    0.02509 =\n"
            "         0.02491    0.00000   -0.00158    0.00159\n"
        )
        doc = _highlighted_document(text)
        formats = _formats(doc, 0)
        eq_formats = [f for f in formats if doc.findBlockByNumber(0).text()[f.start:f.start + f.length] == '=']
        self.assertEqual(1, len(eq_formats))


class TestShelxSyntaxHighlighterEndKeyword(unittest.TestCase):

    def test_end_keyword_is_highlighted(self) -> None:
        doc = _highlighted_document("END\n")
        formats = _formats(doc, 0)
        self.assertTrue(formats)
        self.assertEqual(0, formats[0].start)


if __name__ == "__main__":
    unittest.main()
