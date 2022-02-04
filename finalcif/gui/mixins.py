class ItemTextMixin:

    def text(self, row: int, column: int) -> str:
        """
        Returns the text inside a table cell.
        """
        try:
            txt = self.item(row, column).text()
        except AttributeError:
            txt = ''
        if not txt:
            try:
                txt = self.item(row, column).data(0)
            except AttributeError:
                txt = ''
        if not txt:
            try:
                # for QPlaintextWidgets:
                txt = self.cellWidget(row, column).toPlainText()
            except AttributeError:
                txt = ''
        if not txt:
            # for comboboxes:
            try:
                txt = self.cellWidget(row, column).currentText()
            except AttributeError:
                txt = ''
        return txt