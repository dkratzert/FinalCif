import sys

import qtawesome
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QApplication, QVBoxLayout, QScrollArea, QPlainTextEdit, \
    QTextEdit, QListWidgetItem, QAbstractItemView, QLineEdit, QFormLayout

from finalcif.gui.custom_classes import MyQPlainTextEdit


class TextEditItem(QWidget):
    """
    Text editor for large text instedc of dropdown widgets.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.checkbox = QCheckBox()
        self.textfield = QPlainTextEdit(self)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.textfield)
        layout.setContentsMargins(4, 8, 4, 4)
        self.setLayout(layout)
        self.setAutoFillBackground(False)

    def setText(self, text: str):
        self.textfield.setPlainText(text)

    def setCheckboxName(self, name: str):
        self.checkbox.setObjectName(name)

    def sizeHint(self) -> QSize:
        return QSize(400, 150)


if __name__ == "__main__":
    txts = ("""In addition to the twinning, the structure also exhibits large 
    volume sections consisting of highly disordered solvate or other 
    small molecules. No satisfactory model for the solvate molecules 
    could be developed, and the contribution of the solvate molecules 
    was instead taken into account by reverse Fourier transform methods. 
    The data were first detwinned (using the LIST 8 function of 
    Shelxl2018) and then the cif and fcf files were subjected to the 
    SQUEEZE routine as implemented in the program Platon. The resultant files were used in the further refinement. (Both the hklf 5 type HKL file and the detwinned FAB file are appended to this cif file). A volume of ??? cubic Angstrom per unit cell containing ??? electrons was corrected for.
    """, 'bar dftzh hkjft', 'baz rtzhj dtju', """In addition to the twinning, the structure also exhibits large 
    volume sections consisting of highly disordered solvate or other 
    small molecules. No satisfactory model for the solvate molecules 
    could be developed, and the contribution of the solvate molecules 
    was instead taken into account by reverse Fourier transform methods. 
    The data were first detwinned (using the LIST 8 function of 
    Shelxl2018) and then the cif and fcf files were subjected to the 
    SQUEEZE routine as implemented in the program Platon. The resultant files were used in the further refinement. (Both the hklf 5 type HKL file and the detwinned FAB file are appended to this cif file). A volume of ??? cubic Angstrom per unit cell containing ??? electrons was corrected for.
    """, 'fghfh', 'ffg')
    app = QApplication(sys.argv)

    window = QWidget()
    vlayout = QVBoxLayout(window)
    ciflayout = QFormLayout(window)
    cifedit = QLineEdit()
    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
    cifedit.setSizePolicy(sizePolicy)
    ciflayout.addRow("CIF key:", cifedit)
    vlayout.addLayout(ciflayout)
    vlayout.setContentsMargins(6, 6, 6, 6)
    textEditListWidget = QtWidgets.QListWidget(window)
    textEditListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    textEditListWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
    window.setMinimumSize(600, 500)
    window.setLayout(vlayout)
    vlayout.addWidget(textEditListWidget)
    for text in txts:
        editItem = TextEditItem(window)
        editItem.setText(text)
        item = QListWidgetItem(parent=textEditListWidget)
        item.setSizeHint(editItem.sizeHint())
        #item.setIcon(qtawesome.icon('fa5.image'))
        textEditListWidget.addItem(item)
        textEditListWidget.setItemWidget(item, editItem)
    window.show()
    sys.exit(app.exec_())
