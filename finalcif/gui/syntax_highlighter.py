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

        self.field_re = re.compile(r'^_[A-Za-z][A-Za-z0-9_.\-\[\]()/]*')
        self.quoted_re = re.compile(r"'[^']*'")

    def highlightBlock(self, text: str) -> str:
        prev_state = self.previousBlockState()
        in_multiline = prev_state == self.MULTILINE
        in_loop_fields = prev_state == self.LOOP_FIELDS
        in_loop_data = prev_state == self.LOOP_DATA

        stripped = text.strip()
        lower = stripped.lower()

        # ---------- Multiline text blocks ----------

        if text.startswith(';'):
            self.setFormat(0, 1, self.bold_format)
            # self.setFormat(0, len(text), self.multiline_format)

            if in_multiline:
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(self.MULTILINE)
            return

        if in_multiline:
            # This line is quite slow:
            # self.setFormat(0, len(text), self.multiline_format)
            self.setCurrentBlockState(self.MULTILINE)
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

        # ---------- Quoted values ----------

        if "'" in text:
            for m in self.quoted_re.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), self.value_format)

        self.setCurrentBlockState(0)
