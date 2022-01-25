import os
import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QApplication, QPlainTextEdit, \
    QListWidgetItem, QVBoxLayout, QLabel

print('Compiling ui ...')
application_path = Path(os.path.abspath(__file__)).parent.parent
uic.compileUiDir(os.path.join(application_path, 'gui'))
from finalcif.gui import text_templates


class TextEditItem(QWidget):
    """
    Text editor for large text inside of dropdown widgets.
    """
    _num = 1
    checkbox_cl = pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.vlayout = QVBoxLayout()
        self.vlayout.setAlignment(Qt.AlignVCenter)
        self.checkbox = QCheckBox()
        self.number_label = QLabel()
        self.vlayout.addWidget(self.number_label)
        self.textfield = QPlainTextEdit(self)
        self.vlayout.addWidget(self.checkbox)
        layout.addLayout(self.vlayout)
        layout.addWidget(self.textfield)
        layout.setContentsMargins(4, 8, 4, 4)
        self.setAutoFillBackground(False)
        self.checkbox.clicked.connect(self.checkbox_clicked)

    def checkbox_clicked(self, checked):
        if checked:
            self.checkbox_cl.emit(self.textfield.toPlainText())
            self.number_label.setText(str(self._num))
            TextEditItem._num += 1
        else:
            self.number_label.setText('')

    def setText(self, text: str):
        self.textfield.setPlainText(text)

    def setCheckboxName(self, name: str):
        self.checkbox.setObjectName(name)

    def sizeHint(self) -> QSize:
        return QSize(400, 190)


class MyTextTemplateEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = text_templates.Ui_text_templates_window()
        self.ui.setupUi(self)


if __name__ == "__main__":
    txts = ("""In addition to the twinning, the structure also exhibits large 
    volume sections consisting of highly disordered solvate or other 
    small molecules. No satisfactory model for the solvate molecules 
    could be developed, and the contribution of the solvate molecules 
    was instead taken into account by reverse Fourier transform methods. 
    The data were first detwinned (using the LIST 8 function of 
    Shelxl2018) and then the cif and fcf files were subjected to the 
    SQUEEZE routine as implemented in the program Platon. The resultant files were used in the further refinement. (Both the hklf 5 type HKL file and the detwinned FAB file are appended to this cif file). A volume of ??? cubic Angstrom per unit cell containing ??? electrons was corrected for.
    """, 'bar dftzh hkjft Hällö Daniel Daß is ein T!"§$%&/()=?', 'baz rtzhj dtju', """In addition to the twinning, the structure also exhibits large 
    volume sections consisting of highly disordered solvate or other 
    small molecules. No satisfactory model for the solvate molecules 
    could be developed, and the contribution of the solvate molecules 
    was instead taken into account by reverse Fourier transform methods. 
    The data were first detwinned (using the LIST 8 function of 
    Shelxl2018) and then the cif and fcf files were subjected to the 
    SQUEEZE routine as implemented in the program Platon. The resultant files were used in the further refinement. (Both the hklf 5 type HKL file and the detwinned FAB file are appended to this cif file). A volume of ??? cubic Angstrom per unit cell containing ??? electrons was corrected for.
    """, 'fghfh', 'ffg') * 20
    app = QApplication(sys.argv)
    window = MyTextTemplateEdit()

    for text in txts:
        editItem = TextEditItem(window.ui.listWidget)
        editItem.setText(text)
        editItem.checkbox_cl.connect(lambda x: window.ui.plainTextEdit.appendPlainText(x))
        item = QListWidgetItem(parent=window.ui.listWidget)
        item.setSizeHint(editItem.sizeHint())
        # item.setIcon(qtawesome.icon('fa5.image'))
        window.ui.listWidget.addItem(item)
        window.ui.listWidget.setItemWidget(item, editItem)
    window.show()
    sys.exit(app.exec_())
