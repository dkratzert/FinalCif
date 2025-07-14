# Create a QTextedit widget with a button to open a file dialog
# to select a file to be inserted into the QTextedit widget
# The file dialog is opened by pressing the button.
# The button should be placed above the QTextedit widget and appear on mouse over.

import sys

from qtpy import QtWidgets, QtCore, QtGui


class FloatingButtonWidget(QtWidgets.QPushButton):
    floatingButtonClicked = QtCore.Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.setText('edit')
        self.paddingLeft = 2
        self.paddingTop = 2
        self.setFixedSize(24, 16)
        self.setFlat(True)
        self.setStyleSheet(f'''QPushButton {{background-color: {QtGui.QColor(220, 232, 247).name()};
                                            padding-bottom: 1px;
                                            border-radius: 5px; 
                                            font-size: 11px; 
                                            border: 1px solid {QtGui.QColor(170, 172, 177).name()};
                                            }} 
                                            ''')

    def update_position(self):
        """Update the position of the button to be placed in the bottom right corner of the parent widget.
        """
        self.move(self.parent().width() - self.width() - self.paddingLeft,
                  self.parent().height() - self.height() - self.paddingTop)

    def mousePressEvent(self, event):
        self.floatingButtonClicked.emit()


class OverlayTestEdit(QtWidgets.QTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_button = FloatingButtonWidget(parent=self)
        # The button should be placed over the QTextedit widget as overlay and appear on mouse over.
        self.edit_button.hide()
        self.edit_button.update_position()

    def resizeEvent(self, event):
        self.edit_button.update_position()
        super().resizeEvent(event)

    def enterEvent(self, a0):
        print('enter')
        self.edit_button.show()

    def leaveEvent(self, a0):
        print('leave')
        self.edit_button.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = OverlayTestEdit()
    window.resize(130, 30)
    window.show()
    sys.exit(app.exec())
