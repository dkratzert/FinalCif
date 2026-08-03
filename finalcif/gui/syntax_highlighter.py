"""CIF syntax highlighting for the text editor.

Copyright (c) 2025, Daniel N. Rainer (ORCID: 0000-0002-3272-3161)
All rights reserved.

BSD 3-Clause License

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


* Almot comlete redesign by Daniel Kratzert from original Idea by Daniel N. Rainer
"""

import re

from qtpy.QtGui import QTextCharFormat, QSyntaxHighlighter, QColor, QFont

#: Prefix of the placeholder line that replaces a folded region in the text
#: view. Lines starting with it are never part of a real CIF file.
FOLD_PLACEHOLDER_PREFIX = '    \u2026 '


def _make_format(color: str | None = None, bold: bool = False) -> QTextCharFormat:
    """Build a QTextCharFormat, shared by the CIF and SHELX highlighters."""
    fmt = QTextCharFormat()
    if color is not None:
        fmt.setForeground(QColor(color))
    if bold:
        fmt.setFontWeight(QFont.Weight.Bold)
    return fmt


class CIFSyntaxHighlighter(QSyntaxHighlighter):

    MULTILINE = 1
    LOOP_FIELDS = 2
    LOOP_DATA = 3

    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------- Formats ----------

        self.bold_format = QTextCharFormat()
        self.bold_format.setFontWeight(QFont.Weight.Bold)

        self.field_format = QTextCharFormat()
        self.field_format.setForeground(QColor("#0000FF"))

        self.value_format = QTextCharFormat()
        self.value_format.setForeground(QColor("#008000"))

        self.multiline_format = QTextCharFormat()
        self.multiline_format.setForeground(QColor("#800080"))

        self.loop_keyword_format = QTextCharFormat()
        self.loop_keyword_format.setForeground(QColor("#FF6600"))
        self.loop_keyword_format.setFontWeight(QFont.Weight.Bold)

        self.loop_field_format = QTextCharFormat()
        self.loop_field_format.setForeground(QColor("#CC6600"))

        self.loop_values_format = QTextCharFormat()
        self.loop_values_format.setForeground(QColor("#996600"))

        self.vrf_values_format = QTextCharFormat()
        self.vrf_values_format.setForeground(QColor("#8b0000"))
        self.vrf_values_format.setFontWeight(QFont.Weight.Bold)

        self.folded_format = QTextCharFormat()
        self.folded_format.setForeground(QColor("#808080"))
        self.folded_format.setFontItalic(True)

        self.field_re = re.compile(r'^_[A-Za-z][A-Za-z0-9_.\-\[\]()/]*')
        self.quoted_re = re.compile(r"'[^']*'")

    def _highlight_multiline(self, text: str, in_multiline: bool) -> bool:
        """Format a ';' delimited text field; True when *text* belongs to one."""
        if text.startswith(';'):
            self.setFormat(0, 1, self.bold_format)
            # self.setFormat(0, len(text), self.multiline_format)
            self.setCurrentBlockState(0 if in_multiline else self.MULTILINE)
            return True
        if in_multiline:
            # Formatting the whole line here is quite slow:
            # self.setFormat(0, len(text), self.multiline_format)
            self.setCurrentBlockState(self.MULTILINE)
            return True
        return False

    def highlightBlock(self, text: str) -> None:
        prev_state = self.previousBlockState()

        # ---------- Placeholder of a folded region ----------

        # The block state is passed through unchanged so that folding a region
        # does not disturb the multiline/loop state machine of the following
        # blocks.
        if text.startswith(FOLD_PLACEHOLDER_PREFIX):
            self.setFormat(0, len(text), self.folded_format)
            self.setCurrentBlockState(prev_state)
            return

        in_multiline = prev_state == self.MULTILINE
        in_loop_fields = prev_state == self.LOOP_FIELDS
        in_loop_data = prev_state == self.LOOP_DATA

        stripped = text.strip()
        lower = stripped.lower()

        # ---------- Multiline text blocks ----------

        if self._highlight_multiline(text, in_multiline):
            return

        # ---------- Loop start ----------

        if lower == "loop_":
            self.setFormat(0, len(text), self.loop_keyword_format)
            self.setCurrentBlockState(self.LOOP_FIELDS)
            return

        # ---------- Loop handling ----------

        if in_loop_fields or in_loop_data:
            if lower.startswith(("data_", "save_", "global_", "stop_")):
                in_loop_fields = False
                in_loop_data = False
                self.setCurrentBlockState(0)
            elif stripped.startswith('_') and not in_loop_data:
                self.setFormat(0, len(text), self.loop_field_format)
                self.setCurrentBlockState(self.LOOP_FIELDS)
                return
            elif stripped and not stripped.startswith('_'):
                in_loop_data = True
                self.setFormat(0, len(text), self.loop_values_format)
                self.setCurrentBlockState(self.LOOP_DATA)
                return
            elif not stripped and in_loop_data:
                self.setCurrentBlockState(0)
                return

        # ---------- Data tags ----------

        if text.startswith("data_"):
            self.setFormat(0, len(text), self.bold_format)

        # ---------- Field names ----------

        if text.startswith('_'):
            m = self.field_re.match(text)
            if m:
                self.setFormat(m.start(), m.end() - m.start(), self.field_format)

        if text.startswith('_vrf'):
            self.setFormat(0, len(text), self.vrf_values_format)

        # ---------- Quoted values ----------

        if "'" in text:
            for m in self.quoted_re.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), self.value_format)

        self.setCurrentBlockState(0)


# SHELXL instruction keywords (from shelxfile.shelx.shelx.SHX_CARDS, deduplicated
# and stripped of padding spaces used there for fixed-width comparisons).
SHELX_KEYWORDS = frozenset((
    'TITL', 'CELL', 'ZERR', 'LATT', 'SYMM', 'SFAC', 'UNIT', 'LIST', 'L.S.', 'CGLS',
    'BOND', 'FMAP', 'PLAN', 'TEMP', 'ACTA', 'CONF', 'SIMU', 'RIGU', 'WGHT', 'FVAR',
    'DELU', 'SAME', 'DISP', 'LAUE', 'REM', 'MORE', 'TIME', 'END', 'HKLF', 'OMIT',
    'SHEL', 'BASF', 'TWIN', 'EXTI', 'SWAT', 'HOPE', 'MERG', 'SPEC', 'RESI', 'MOVE',
    'ANIS', 'AFIX', 'HFIX', 'FRAG', 'FEND', 'EXYZ', 'EADP', 'EQIV', 'CONN', 'BIND',
    'FREE', 'DFIX', 'BUMP', 'SADI', 'CHIV', 'FLAT', 'DEFS', 'ISOR', 'NCSY', 'SUMP',
    'BLOC', 'DAMP', 'STIR', 'MPLA', 'RTAB', 'HTAB', 'SIZE', 'WPDB', 'GRID', 'MOLE',
    'XNPD', 'REST', 'CHAN', 'FLAP', 'RNUM', 'SOCC', 'PRIG', 'WIGL', 'RANG', 'TANG',
    'ADDA', 'STAG', 'NEUT', 'ABIN', 'ANSC', 'ANSR', 'NOTR', 'TWST', 'PART', 'DANG',
    'BEDE', 'LONE',
))


class ShelxSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for SHELXL .ins/.res files.

    Highlights instruction/restraint keywords (e.g. TITL, CELL, SADI), REM
    comment lines, '!' inline comments (valid anywhere on a line per the
    SHELXL manual), indented lines that are comments rather than
    '='-continuations, and the '=' line-continuation marker. Shares the
    ``_make_format`` helper with :class:`CIFSyntaxHighlighter`.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.keyword_format = _make_format("#0057B7", bold=True)
        self.comment_format = _make_format("#808080")
        self.comment_format.setFontItalic(True)
        self.continuation_format = _make_format("#800080", bold=True)
        self.value_format = _make_format("#763127")

    @staticmethod
    def _strip_inline_comment(text: str) -> str:
        """Return *text* up to (excluding) a '!' comment, if any.

        Per the SHELXL manual, "All characters following '!' ... in an
        instruction line are ignored", so a trailing '=' continuation marker
        must be detected *before* any '!' comment on the same line.
        """
        bang_pos = text.find('!')
        return text if bang_pos == -1 else text[:bang_pos]

    def _ends_with_continuation_marker(self, text: str) -> bool:
        """Whether *text* is a '='-terminated continuation line, ignoring
        any trailing '!' comment."""
        return self._strip_inline_comment(text).rstrip().endswith('=')

    def _is_continuation_line(self) -> bool:
        """Whether the current block continues a preceding '='-terminated line.

        Reads the previous block's own text directly (rather than relying on
        ``previousBlockState()``) since that stays reliable across the
        multiple internal reformat passes Qt may perform on a block.
        """
        prev_block = self.currentBlock().previous()
        return prev_block.isValid() and self._ends_with_continuation_marker(prev_block.text())

    def _continuation_root_keyword(self) -> str:
        """Return the upper-cased first word of the line that started the
        current '='-continuation chain (the "root" instruction line), or ''
        if that root line is empty/unavailable.

        A continuation chain can itself span several '='-terminated lines,
        so this walks back to the earliest block in the unbroken chain.
        """
        block = self.currentBlock().previous()
        while True:
            earlier = block.previous()
            if earlier.isValid() and self._ends_with_continuation_marker(earlier.text()):
                block = earlier
            else:
                break
        root_stripped = block.text().strip()
        return root_stripped.split(None, 1)[0].upper() if root_stripped else ''

    def highlightBlock(self, text: str) -> None:
        stripped = text.strip()
        if not stripped:
            return

        leading_ws = len(text) - len(text.lstrip())
        is_continuation = self._is_continuation_line()

        # ---------- Indented lines that are not continuations are comments
        # (per the SHELXL manual: "Other lines beginning with spaces are
        # treated as comments"). A line following a trailing '=' is a real
        # continuation of the previous instruction, not a comment - it is
        # colored the same as the line it continues, as if there was no
        # line break at all. ----------

        if leading_ws > 0 and not is_continuation:
            self.setFormat(0, len(text), self.comment_format)
            return

        if is_continuation:
            root_word = self._continuation_root_keyword()
            if root_word == 'REM':
                self.setFormat(0, len(text), self.comment_format)
            elif root_word.split('_', 1)[0] in SHELX_KEYWORDS:
                self.setFormat(0, len(text), self.value_format)
        else:
            first_word = stripped.split(None, 1)[0]
            upper_word = first_word.upper()

            # ---------- Comments ----------

            if upper_word == 'REM':
                self.setFormat(0, len(text), self.comment_format)
                return

            # ---------- Keywords (restraint names may carry a residue-class
            # suffix, e.g. SADI_CCF3, so only the part before '_' is matched). ----------

            base_keyword = upper_word.split('_', 1)[0]
            if base_keyword in SHELX_KEYWORDS:
                self.setFormat(leading_ws, len(base_keyword), self.keyword_format)

                # ---------- Rest of the line following the keyword ----------

                rest_start = leading_ws + len(upper_word)
                if rest_start < len(text):
                    self.setFormat(rest_start, len(text) - rest_start, self.value_format)

        # ---------- Line continuation (ignoring any trailing '!' comment) ----------

        stripped_before_comment = self._strip_inline_comment(text).rstrip()
        if stripped_before_comment.endswith('='):
            self.setFormat(len(stripped_before_comment) - 1, 1, self.continuation_format)

        # ---------- Trailing '!' comment (anywhere on the line) ----------

        bang_pos = text.find('!')
        if bang_pos != -1:
            self.setFormat(bang_pos, len(text) - bang_pos, self.comment_format)

        # ---------- Trailing '!' comment (anywhere on the line) ----------

        bang_pos = text.find('!')
        if bang_pos != -1:
            self.setFormat(bang_pos, len(text) - bang_pos, self.comment_format)

        self.setCurrentBlockState(0)
