import threading

import requests
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QMainWindow


class Class1(QObject):
    # Define a signal to emit the result of the class
    resultReady = pyqtSignal(str)

    def run(self):
        # Calculate the result
        r = requests.get(url='https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.2.tar.xz', timeout=10)
        # Emit the result using the signal
        self.resultReady.emit(f"Result from Class1 {r.status_code}\n")


class Class2(QObject):
    # Define a signal to emit the result of the class
    resultReady = pyqtSignal(str)

    def run(self):
        # Calculate the result
        r = requests.get(url='https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.3.tar.xz', timeout=10)
        # Emit the result using the signal
        self.resultReady.emit(f"Result from Class2 {r.status_code}\n")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a label to display the results
        self.label = QLabel()
        self.setCentralWidget(self.label)
        # Create instances of the classes
        self.class1 = Class1()
        self.class2 = Class2()

        # Connect the signals from the classes to slots in the main window
        self.class1.resultReady.connect(self.updateLabel)
        self.class2.resultReady.connect(self.updateLabel)

        # Create threads for each class and start them
        self.thread1 = threading.Thread(target=self.class1.run)
        self.thread2 = threading.Thread(target=self.class2.run)
        self.thread1.start()
        self.thread2.start()

    @pyqtSlot(str)
    def updateLabel(self, result):
        # Update the label with the result
        txt = self.label.text()
        self.label.setText(f"{txt}{result}")
        print(result, '##')


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


"""if __name__ == '__main__':
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication([])

    dialog = QtWidgets.QDialog()
    l = QtWidgets.QVBoxLayout(dialog)
    dialog.setLayout(l)

    gb = QtWidgets.QGroupBox(dialog)
    gb.setTitle('Foo Bar')

    l.addWidget(gb)
    dialog.show()

    l2 = QtWidgets.QVBoxLayout(gb)
    gb.setLayout(l2)
    q_label = QLabel('Foo')
    q_label.setEnabled(True)
    l2.addWidget(q_label)
    gb.setDisabled(True)

    app.exec()"""