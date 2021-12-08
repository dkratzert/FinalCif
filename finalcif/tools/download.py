import sys

import requests
from PyQt5.QtCore import pyqtSignal, QObject

from finalcif import VERSION


# noinspection PyUnresolvedReferences
class MyDownloader(QObject):
    progress = pyqtSignal(str)
    failed = pyqtSignal(int)
    finished = pyqtSignal()
    loaded = pyqtSignal(bytes)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def failed_to_load(self, txt: str) -> None:
        print('Failed to load {}', self.url)

    def download(self) -> None:
        # print('Downloading:', self.url)
        user_agent = 'FinalCif v{}'.format(VERSION)
        headers = {
            'User-Agent': user_agent,
        }
        try:
            response = requests.get(self.url, stream=True, headers=headers)
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
