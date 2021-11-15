import sys

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from finalcif.tools.version import VERSION


class MyDownloader(QThread):
    progress = pyqtSignal(str)
    failed = pyqtSignal(int)
    finished = pyqtSignal(bytes)

    def __init__(self, parent, url: str):
        super().__init__(parent)
        self.url = url

    def run(self):
        self.download(self.url)

    def print_status(self, status: str) -> None:
        print(status)

    def failed_to_download(self, status_code: int):
        print('Failed to download: {}'.format(self.url))
        print('HTTP status was {}'.format(status_code))

    def download(self, full_url: str, user_agent=None) -> bytes:
        user_agent = user_agent if user_agent else 'FinalCif v{}'.format(VERSION)
        headers = {
            'User-Agent': user_agent,
        }
        # noinspection PyUnresolvedReferences
        # self.progress.emit('Starting download: {}'.format(full_url))
        response = requests.get(full_url, stream=True, headers=headers)
        if response.status_code != 200:
            # noinspection PyUnresolvedReferences
            self.failed.emit(response.status_code)
            # noinspection PyUnresolvedReferences
            self.finished.emit(b'')
            return b''
        # noinspection PyUnresolvedReferences
        self.finished.emit(response.content)
        return response.content


if __name__ == "__main__":
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = QWidget()
    w.show()


    def foo(bar: bytes):
        print(bar.decode('ascii'))


    upd = MyDownloader(None, "https://dkratzert.de/files/finalcif/version.txt")
    upd.finished.connect(foo)
    upd.failed.connect(upd.failed_to_download)
    upd.progress.connect(upd.print_status)
    upd.start()
    sys.exit(app.exec_())
