from PyQt5.QtWidgets import QPlainTextEdit, QTableWidget, QWidget, QComboBox


class MyCifTable(QTableWidget):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)


class MyQPlainTextEdit(QPlainTextEdit):
    """
    A special plaintextedit with convenient methods to set the background color and other things.
    """
    def __init__(self, parent=None):
        super().__init__(parent)


class MyComboBox(QComboBox):
    """
    A special QComboBox with convenient methods to set the background color and other things.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
