"""Regression tests for CIFSyntaxHighlighter.

These tests lock down the current highlighting behaviour so that future
changes (e.g. adding ShelxSyntaxHighlighter / sharing code) do not
accidentally change how CIF files are highlighted.
"""
import os

os.environ["RUNNING_TEST"] = "True"
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import unittest

from qtpy.QtGui import QFont, QTextDocument
from qtpy.QtWidgets import QApplication

from finalcif.gui.syntax_highlighter import CIFSyntaxHighlighter

app = QApplication.instance() or QApplication([])


def _formats(document: QTextDocument, block_number: int) -> list:
    """Return the list of QTextLayout.FormatRange for a given block."""
    block = document.findBlockByNumber(block_number)
    return list(block.layout().formats())


def _highlighted_document(text: str) -> QTextDocument:
    doc = QTextDocument()
    doc.setPlainText(text)
    highlighter = CIFSyntaxHighlighter(doc)
    # Keep a reference alive on the document so it is not garbage collected
    # before rehighlighting has happened.
    doc._highlighter = highlighter  # type: ignore[attr-defined]
    app.processEvents()
    return doc


class TestCIFSyntaxHighlighterDataBlock(unittest.TestCase):

    def test_data_tag_is_bold(self) -> None:
        doc = _highlighted_document("data_test\n")
        formats = _formats(doc, 0)
        self.assertEqual(1, len(formats))
        self.assertEqual(QFont.Weight.Bold, formats[0].format.fontWeight())
        self.assertEqual(0, formats[0].start)
        self.assertEqual(len("data_test"), formats[0].length)


class TestCIFSyntaxHighlighterFieldNames(unittest.TestCase):

    def test_field_name_is_blue(self) -> None:
        doc = _highlighted_document("_cell_length_a 10.123\n")
        formats = _formats(doc, 0)
        self.assertEqual(1, len(formats))
        self.assertEqual("#0000ff", formats[0].format.foreground().color().name())
        self.assertEqual(0, formats[0].start)
        self.assertEqual(len("_cell_length_a"), formats[0].length)

    def test_vrf_field_is_bold_dark_red(self) -> None:
        doc = _highlighted_document("_vrf_PLAT023_test something\n")
        formats = _formats(doc, 0)
        # The vrf-specific format is applied on top of / in addition to the
        # generic field-name format.
        vrf_formats = [
            f for f in formats
            if f.format.foreground().color().name() == "#8b0000"
        ]
        self.assertEqual(1, len(vrf_formats))
        self.assertEqual(QFont.Weight.Bold, vrf_formats[0].format.fontWeight())
        self.assertEqual(0, vrf_formats[0].start)


class TestCIFSyntaxHighlighterQuotedValues(unittest.TestCase):

    def test_quoted_value_is_green(self) -> None:
        doc = _highlighted_document("_chemical_name_common      'quartz'\n")
        formats = _formats(doc, 0)
        green_formats = [
            f for f in formats
            if f.format.foreground().color().name() == "#008000"
        ]
        self.assertEqual(1, len(green_formats))
        text = doc.findBlockByNumber(0).text()
        self.assertEqual("'quartz'", text[green_formats[0].start:
                                          green_formats[0].start + green_formats[0].length])


class TestCIFSyntaxHighlighterLoop(unittest.TestCase):

    def setUp(self) -> None:
        self.text = (
            "loop_\n"
            " _atom_type_symbol\n"
            " _atom_type_description\n"
            " 'C'  'C'\n"
            " 'H'  'H'\n"
            "\n"
            "_after_loop_field    1\n"
        )
        self.doc = _highlighted_document(self.text)

    def test_loop_keyword_is_orange_bold(self) -> None:
        formats = _formats(self.doc, 0)
        self.assertEqual(1, len(formats))
        self.assertEqual("#ff6600", formats[0].format.foreground().color().name())
        self.assertEqual(QFont.Weight.Bold, formats[0].format.fontWeight())

    def test_loop_field_lines_are_orange(self) -> None:
        for block_number in (1, 2):
            formats = _formats(self.doc, block_number)
            self.assertEqual(1, len(formats))
            self.assertEqual("#cc6600", formats[0].format.foreground().color().name())

    def test_loop_data_lines_are_dark_yellow(self) -> None:
        for block_number in (3, 4):
            formats = _formats(self.doc, block_number)
            self.assertEqual(1, len(formats))
            self.assertEqual("#996600", formats[0].format.foreground().color().name())

    def test_field_after_loop_ends_is_highlighted_as_field_again(self) -> None:
        formats = _formats(self.doc, 6)
        self.assertEqual(1, len(formats))
        self.assertEqual("#0000ff", formats[0].format.foreground().color().name())


class TestCIFSyntaxHighlighterMultiline(unittest.TestCase):

    def test_semicolon_start_is_bold_and_state_persists(self) -> None:
        text = (
            "_shelx_space_group_comment\n"
            ";\n"
            "This is a multi-line\n"
            "comment block.\n"
            ";\n"
            "_after_multiline   1\n"
        )
        doc = _highlighted_document(text)
        opening = _formats(doc, 1)
        self.assertEqual(1, len(opening))
        self.assertEqual(QFont.Weight.Bold, opening[0].format.fontWeight())
        self.assertEqual(0, opening[0].start)
        self.assertEqual(1, opening[0].length)

        # Lines inside the multiline block currently receive no extra format.
        inside = _formats(doc, 2)
        self.assertEqual(0, len(inside))

        closing = _formats(doc, 4)
        self.assertEqual(1, len(closing))

        after = _formats(doc, 5)
        self.assertEqual(1, len(after))
        self.assertEqual("#0000ff", after[0].format.foreground().color().name())


if __name__ == "__main__":
    unittest.main()
