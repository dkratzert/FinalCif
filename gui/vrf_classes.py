from PyQt5.QtWidgets import QWidget, QVBoxLayout


class MyVRFContainer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainVLayout = QVBoxLayout(self)
        self.setLayout(self.mainVLayout)

