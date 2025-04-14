import os

os.environ["RUNNING_TEST"] = 'True'
import unittest

from PySide6.QtGui import QIcon

from finalcif.appwindow import AppWindow
from finalcif.tools.statusbar import StatusBar
from finalcif import VERSION


class TestStausBarWithGraphics(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow()
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle(f'FinalCif v{VERSION}')
        self.status = StatusBar(self.myapp.ui)
        self.myapp.hide()

    def tearDown(self) -> None:
        self.myapp.close()

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
