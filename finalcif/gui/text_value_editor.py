import sys
from typing import Tuple, List, Union

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QApplication, QPlainTextEdit, \
    QListWidgetItem, QVBoxLayout, QLabel

# print('Compiling textedit ui ...')
# application_path = Path(os.path.abspath(__file__)).parent.parent
# uic.compileUiDir(os.path.join(application_path, 'gui'))
from finalcif.gui import text_templates


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
    def text(self) -> str:
        return self.textfield.toPlainText()

    def on_checkbox_clicked(self, checked: bool) -> None:
        if checked:
            self.checkbox_clicked.emit(self.textfield.toPlainText())
            self.number_label.setText(str(self._num))
            TextEditItem._num += 1
        else:
            self.number_label.setText('')

    def setText(self, text: str) -> None:
        self.textfield.setPlainText(text)

    def setCheckboxName(self, name: str) -> None:
        self.checkbox.setObjectName(name)

    def sizeHint(self) -> QSize:
        return QSize(400, 190)


class MyTextTemplateEdit(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = text_templates.Ui_TextTemplatesWidget()
        self.ui.setupUi(self)
        self.ui.cancelTextPushButton.clicked.connect(self._on_backbutton_clicked)

    def _on_backbutton_clicked(self):
        self.ui.templatesListWidget.clear()

    def add_textfields(self, text_list: Union[List, Tuple]) -> None:
        if text_list:
            for text in text_list:
                self.add_one_textfield(text)
        for empty in ('',) * 20:
            self.add_one_textfield(empty)

    def add_one_textfield(self, text):
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

    def clear_fields(self):
        self.ui.templatesListWidget.clear()
        self.ui.cifKeyLineEdit.clear()
        self.ui.plainTextEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyTextTemplateEdit()
    window.add_textfields(txts)
    window.show()
    sys.exit(app.exec_())
