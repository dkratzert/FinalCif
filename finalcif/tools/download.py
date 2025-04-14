import sys

import requests
from PySide6.QtCore import Signal, QObject

from finalcif import VERSION


# noinspection PyUnresolvedReferences
class MyDownloader(QObject):
    progress = Signal(str)
    failed = Signal(int)
    finished = Signal()
    loaded = Signal(bytes)

    def __init__(self, url, parent=None):
        super().__init__(parent)
        self.url = url

    def failed_to_load(self, txt: str) -> None:
        print('Failed to load {}', self.url)

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
    from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
    from PySide6.QtWidgets import QApplication
    import threading

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


    worker = MyDownloader("https://dkratzert.de/files/finalcif/version.txt")
    worker.loaded.connect(foo)
    thread = threading.Thread(target=worker.download)
    thread.start()
    sys.exit(app.exec())
