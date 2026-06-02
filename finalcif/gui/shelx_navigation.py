"""Helpers for navigating the SHELXL file viewer by atom name."""
from __future__ import annotations

from qtpy import QtGui, QtWidgets



def find_shelx_line_for_atom(shx, atom_name: str) -> int:
    """Return the 0-based line number in the SHELXL text for *atom_name*.

    *atom_name* uses ``fastmolwidget``'s internal notation:

    - ``"Ga1"``     — atom ``Ga1`` in residue 0 (no residue suffix → ``_0``).
    - ``"F4_3"``    — atom ``F4`` in residue 3 (CIF ``_N`` suffix convention).
    - ``"Ga1>>2"``  — third occurrence of label ``Ga1`` in the grown molecule
      (symmetry copy); all copies map to the same ASU line.
    - ``"F4_3>>1"`` — second symmetry copy of ``F4`` in residue 3; same line.

    Delegates residue-suffix parsing and case-insensitive lookup to
    ``shelxfile``'s ``Atoms.get_atom_by_name`` which accepts both ``"C1"``
    (→ residue 0) and ``"C1_3"`` (→ residue 3) forms.

    Returns -1 when no match is found.
    """
    # Strip the fastmolwidget symmetry-copy suffix ("Ga1>>2" → "Ga1").
    # All copies of the same atom reference the same SHELXL definition line.
    base_name, _, _suffix = atom_name.partition('>>')
    atom = shx.atoms.get_atom_by_name(base_name)
    if atom is None:
        return -1
    return atom.index


def scroll_and_highlight_shelx_atom(
        text_edit: QtWidgets.QPlainTextEdit,
        shx,
        atom_name: str,
        highlight_color: QtGui.QColor | None = None,
) -> None:
    """Scroll *text_edit* to the SHELXL line for *atom_name* and highlight it.

    Args:
        text_edit: The ``QPlainTextEdit`` displaying the SHELXL file content.
        shx: A ``shelxfile.Shelxfile`` instance for the current structure.
        atom_name: Atom label in ``fastmolwidget`` notation (e.g. ``"Ga1"``
            or ``"Ga1>>2"``).
        highlight_color: Background colour for the highlighted line.  Defaults
            to a light blue if *None*.
    """
    if highlight_color is None:
        highlight_color = QtGui.QColor('#c8e6ff')
    line_num = find_shelx_line_for_atom(shx, atom_name)
    if line_num < 0:
        return
    doc = text_edit.document()
    block = doc.findBlockByNumber(line_num)
    if not block.isValid():
        return
    cursor = QtGui.QTextCursor(block)
    text_edit.setTextCursor(cursor)
    text_edit.centerCursor()
    highlight = QtWidgets.QTextEdit.ExtraSelection()
    highlight.cursor = cursor
    highlight.cursor.select(QtGui.QTextCursor.SelectionType.LineUnderCursor)
    highlight.format.setBackground(highlight_color)
    highlight.format.setFontWeight(QtGui.QFont.Weight.Bold)
    highlight.format.setProperty(QtGui.QTextFormat.Property.FullWidthSelection, True)
    text_edit.setExtraSelections([highlight])






