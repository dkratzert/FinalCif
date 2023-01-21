if __name__ == '__main__':
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication([])

    dialog = QtWidgets.QDialog()
    l = QtWidgets.QVBoxLayout(dialog)
    dialog.setLayout(l)

    p = QtWidgets.QProgressBar(dialog)

    l.addWidget(p)
    dialog.show()
    app.processEvents()

    p.setValue(30)

    app.exec()