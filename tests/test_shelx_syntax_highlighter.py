"""Tests for ShelxSyntaxHighlighter (SHELX .ins/.res highlighting).

Written before the implementation exists (TDD): these tests define the
expected behaviour of the highlighter used for the SHELX file viewer on the
results page.
"""
import os

os.environ["RUNNING_TEST"] = "True"
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
