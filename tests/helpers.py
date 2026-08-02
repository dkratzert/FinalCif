#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import sys
from shutil import which
import unittest

addr = """Albert-Ludwigs-Universität Freiburg
Institut für Anorganische und Analytische Chemie
Albertstraße 21
Freiburg i. Br.
79104
Germany"""


def get_platon_exe() -> str:
    if sys.platform.startswith('win'):
        platon_exe = r'C:\pwt\platon.exe'
    else:
        platon_exe = which('platon')
    return platon_exe


def processevents() -> None:
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance()
    if app is not None:
        app.processEvents()


class AppWindowTestCase(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def tearDown(self) -> None:
        if getattr(self, 'app', None) is not None:
            try:
                self.app.close()
                self.app.deleteLater()
            except RuntimeError:
                pass
            self.app = None
            destroy_pending_widgets()
        super().tearDown()


def destroy_pending_widgets() -> None:
    """Really destroy the widgets of the closed window.

    No event loop runs during the tests, so deleteLater() alone leaks the whole
    widget tree. Draining the complete posted event queue first is essential:
    sendPostedEvents() with an event type filter has to walk the whole queue, so
    leftover paint/layout events would make every following teardown slower.
    """
    from qtpy.QtCore import QEvent
    from qtpy.QtWidgets import QApplication
    if QApplication.instance() is None:
        return
    QApplication.sendPostedEvents()
    QApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

