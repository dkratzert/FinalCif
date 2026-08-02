import time
from pathlib import Path

from qtpy.QtCore import QThread

from finalcif.appwindow import AppWindow
from tests.helpers import AppWindowTestCase


class _SlowThread(QThread):
    def run(self) -> None:
        time.sleep(0.5)


class TestBackgroundThreadShutdown(AppWindowTestCase):
    """Qt aborts the process when a running QThread is deleted with its parent."""

    def setUp(self) -> None:
        self.testcif = Path('tests/examples/work/cu_BruecknerJK_153F40_0m.cif').resolve()
        self.app = AppWindow(file=self.testcif)

    def test_running_worker_thread_is_finished_by_close(self):
        thread = _SlowThread(parent=self.app)
        thread.start()
        self.assertTrue(thread.isRunning())

        self.app.close()

        self.assertFalse(thread.isRunning())

    def test_no_worker_thread_runs_after_close(self):
        self.app.close()

        running = [t for t in self.app.findChildren(QThread) if t.isRunning()]
        self.assertEqual([], running)
