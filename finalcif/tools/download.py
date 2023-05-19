import sys

import requests
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject, QThread, pyqtSlot

from finalcif import VERSION


def start_worker(runnable: QtCore.QObject, thread: QThread, onload: object):
    """
    Starts the worker class in a separate thread.
    """
    runnable.moveToThread(thread)
    runnable.loaded.connect(onload)
    thread.started.connect(runnable.download)
    runnable.finished.connect(thread.quit)
    runnable.finished.connect(runnable.deleteLater)
    thread.finished.connect(thread.deleteLater)
    thread.start()


# noinspection PyUnresolvedReferences
class MyDownloader(QObject):
    progress = pyqtSignal(str)
    failed = pyqtSignal(int)
    finished = pyqtSignal()
    loaded = pyqtSignal(bytes)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def failed_to_load(self, txt: str) -> None:
        print('Failed to load {}', self.url)

    @pyqtSlot()
    def download(self) -> None:
        # print('Downloading:', self.url)
        OS = sys.platform
        user_agent = f'FinalCif v{VERSION} ({OS})'
        headers = {
            'User-Agent': user_agent,
        }
        try:
            response = requests.get(self.url, stream=True, headers=headers, timeout=10)
        except requests.RequestException as e:
            print('Could not connect to download server', e)
            self.loaded.emit(b'')
            self.failed.emit(0)
            return
        if response.status_code != 200:
            # noinspection PyUnresolvedReferences
            self.failed.emit(response.status_code)
            # noinspection PyUnresolvedReferences
            self.finished.emit()
            return
        self.loaded.emit(response.content)
        self.finished.emit()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QThread

    app = QApplication(sys.argv)
    w = QWidget()
    l = QHBoxLayout()
    label = QLabel()
    l.addWidget(label)
    w.setLayout(l)
    w.setMinimumWidth(100)
    w.setMinimumHeight(100)
    w.show()


    def foo(bar: bytes):
        label.setText(bar.decode('ascii'))


    upd = MyDownloader("https://dkratzert.de/files/finalcif/version.txt")
    thread = QThread()
    upd.moveToThread(thread)
    upd.loaded.connect(foo)
    thread.start()
    upd.download()
    sys.exit(app.exec_())
