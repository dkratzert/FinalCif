import unittest

from PyQt5.QtGui import QIcon

from appwindow import AppWindow
from tools.statusbar import StatusBar
from tools.version import VERSION


class TestStausBarWithGraphics(unittest.TestCase):

    def setUp(self) -> None:
        self.myapp = AppWindow(unit_test=True)
        self.myapp.running_inside_unit_test = True
        self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
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
