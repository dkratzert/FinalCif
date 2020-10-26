import sys
import unittest

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from finalcif import AppWindow
from gui.finalcif_gui import Ui_FinalCifWindow
from tools.statusbar import StatusBar
from tools.version import VERSION

app = QApplication(sys.argv)


class TestStausBarWithGraphics(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow()  # ([x for x in Path('.').rglob('1979688.cif')][0].absolute())
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.hide()
        self.ui = Ui_FinalCifWindow()
        self.ui.setupUi(self.myapp)
        # self.ui = None
        self.status = StatusBar(self.ui)

    def test_show_hello(self):
        self.status.show_message('Hello!')
        self.assertEqual('Hello!', self.status.current_message)

    def test_show_list(self):
        self.status.show_message(['Hello', 'world!'])
        self.assertEqual('Hello world!', self.status.current_message)

    def test_show_2s(self):
        self.status.show_message('foobar', timeout=1)
        self.assertEqual('foobar', self.status.current_message)
        # I am not sure how to test this really


class TestStausBarConsole(unittest.TestCase):

    def setUp(self) -> None:
        self.status = StatusBar()

    def test_show_hello(self):
        self.status.show_message('Hello!')
        self.assertEqual('Hello!', self.status.current_message)

    def test_show_list(self):
        self.status.show_message(['Hello', 'world!'])
        self.assertEqual('Hello world!', self.status.current_message)
