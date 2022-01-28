import os
import sys
from pathlib import Path
from typing import Tuple, List, Union

from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QApplication, QPlainTextEdit, \
    QListWidgetItem, QVBoxLayout, QLabel

print('Compiling textedit ui ...')
application_path = Path(os.path.abspath(__file__)).parent.parent
uic.compileUiDir(os.path.join(application_path, 'gui'))
from finalcif.gui import text_templates

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
""", 'fghfh', 'ffg') + ('',) * 20


class TextEditItem(QWidget):
    """
    Text editor for large text inside of dropdown widgets.
    """
    _num = 1
    checkbox_clicked = pyqtSignal(str)

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
        self.checkbox.clicked.connect(self.on_checkbox_clicked)

    @property
    def text(self):
        return self.textfield.toPlainText()

    def on_checkbox_clicked(self, checked):
        if checked:
            self.checkbox_clicked.emit(self.textfield.toPlainText())
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
        self.ui = text_templates.Ui_TextTemplatesWidget()
        self.ui.setupUi(self)

    def add_textfields(self, text_list: Union[List, Tuple]) -> None:
        for text in text_list:
            edit_item = TextEditItem(self.ui.templatesListWidget)
            edit_item.setText(text)
            edit_item.checkbox_clicked.connect(lambda x: self.ui.plainTextEdit.appendPlainText(x))
            item = QListWidgetItem(parent=self.ui.templatesListWidget)
            item.setSizeHint(edit_item.sizeHint())
            # item.setIcon(qtawesome.icon('fa5.image'))
            self.ui.templatesListWidget.addItem(item)
            self.ui.templatesListWidget.setItemWidget(item, edit_item)

    def get_template_texts(self) -> List[str]:
        texts = []
        for num in range(self.ui.templatesListWidget.count()):
            item = self.ui.templatesListWidget.item(num)
            txt = self.ui.templatesListWidget.itemWidget(item).text
            if txt.strip():
                texts.append(txt)
        return texts


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyTextTemplateEdit()
    window.add_textfields(txts)
    window.show()
    sys.exit(app.exec_())
