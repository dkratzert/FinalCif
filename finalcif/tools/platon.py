import os
import subprocess
import sys
import threading
import time
from contextlib import suppress
from pathlib import Path
from shutil import which

from qtpy import QtCore
from qtpy.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, \
    QPlainTextEdit


class PlatonRunner(QtCore.QObject):
    finished = QtCore.Signal(bool)
    tick = QtCore.Signal(str)

    def __init__(self, parent, output_widget: QPlainTextEdit, log_widget: QPlainTextEdit, cif_file: Path):
        super().__init__(parent)
        self.cif_file = cif_file.resolve().absolute()
        self.process = None
        self.is_stopped = False
        self._origdir = None
        self.output_widget = output_widget
        self.log_widget = log_widget
        self.formula_moiety = ''
        self.Z = ''
        self.chk_file_text = ''

    def run_process(self):
        self._origdir = os.curdir
        # os.chdir(self.cif_file.parent)
        self.formula_moiety = ''
        self.Z = ''
        self.process = QtCore.QProcess()
        self.output_widget.clear()
        threading.Thread(target=self._monitor_output_log, daemon=True).start()
        # self.process.readyReadStandardOutput.connect(self.on_ready_read)
        self.process.finished.connect(self._onfinished)
        self.process.setWorkingDirectory(str(self.cif_file.parent))
        self.cif_file.with_suffix('.chk').unlink(missing_ok=True)
        self.process.start(self.platon_exe, ["-U", str(self.cif_file.name)])

    def _onfinished(self) -> None:
        self._on_ready_read()
        # os.chdir(self._origdir)
        self._parse_chk_file()
        self.output_widget.setPlainText(self.chk_file_text)
        self.finished.emit(True)
        self.delete_orphaned_files()

    def _on_ready_read(self) -> None:
        output = self.process.readAllStandardOutput().data().decode()
        self.log_widget.appendPlainText(output)

    def _monitor_output_log(self) -> None:
        """Poll the .chk file for PLATON completion markers.

        Runs in a daemon thread.  Uses ``continue`` (not ``break``) when the
        .chk file does not yet exist so the monitor is not prematurely killed
        during the window between startup (old .chk deleted) and PLATON writing
        the first content.  A hard timeout of ~120 s prevents infinite looping
        if PLATON never creates the file.
        """
        max_ticks = 400  # ~120 s at 0.3 s/tick
        ticks = 0
        while not self.is_stopped and ticks < max_ticks:
            self.tick.emit('#')
            time.sleep(0.3)
            ticks += 1
            try:
                log_file = self.cif_file.with_suffix('.chk').read_text('latin1', errors='ignore')
                if 'Unresolved or to be Checked Issue' in log_file:
                    self._stop_program()
                    break
                if '! Congratulations !' in log_file:
                    self._stop_program()
                    break
            except FileNotFoundError:
                continue  # .chk not yet created; keep waiting

    def _stop_program(self) -> None:
        """Signal PLATON to terminate.  Safe to call from any thread."""
        self.is_stopped = True
        # QProcess.terminate() must be called from the main (Qt) thread.
        # Using a queued invoke ensures thread safety without adding a signal.
        QtCore.QMetaObject.invokeMethod(
            self.process,
            'terminate',
            QtCore.Qt.ConnectionType.QueuedConnection,
        )

    def _parse_chk_file(self) -> None:
        try:
            self.chk_file_text = self.cif_file.with_suffix('.chk').read_text(encoding='latin1', errors='ignore')
        except FileNotFoundError as e:
            print('CHK file not found:', e)
            self.chk_file_text = ''
        for num, line in enumerate(self.chk_file_text.splitlines(keepends=False)):
            if line.startswith('# MoietyFormula'):
                self.formula_moiety = ' '.join(line.split(' ')[2:])
            if line.startswith('# Z'):
                self.Z = line[19:24].strip(' ')

    @property
    def platon_exe(self) -> str:
        """Return the path to the PLATON executable for the current platform.

        On **Windows** the lookup order is:

        1. Bundled ``platon/platon_special.exe`` (ships with FinalCif on Windows).
        2. ``C:\\pwt\\platon.exe`` (traditional PLATON install location).
        3. Any ``platon.exe`` found on ``PATH`` via :func:`shutil.which`.

        On **macOS / Linux** only ``PATH`` is searched; the Windows ``.exe``
        files are never considered because they cannot run on these platforms
        even if the file happens to be present in the repository checkout.
        """
        if sys.platform.startswith('win'):
            special_platon = Path(__file__).resolve().parent.parent.parent / 'platon' / 'platon_special.exe'
            if special_platon.exists():
                return str(special_platon)
            in_pwt = Path(r'C:\pwt\platon.exe')
            if in_pwt.exists():
                return str(in_pwt)
        found = which('platon')
        return found if found else 'platon'

    def kill(self):
        if sys.platform.startswith('win'):
            with suppress(FileNotFoundError):
                subprocess.run(["taskkill", "/f", "/im", "platon.exe"], check=False, shell=False)
        if sys.platform[:5] in ('linux', 'darwi'):
            with suppress(FileNotFoundError):
                subprocess.run(["killall", "platon"], check=False, shell=False)

    def delete_orphaned_files(self):
        # delete orphaned files:
        for ext in ['.ckf', '.fcf', '.def', '.lis', '.sar', '.ckf',
                    '.sum', '.hkp', '.pjn', '.bin', '.spf']:
            try:
                file = self.cif_file.resolve().with_suffix(ext)
                if file.stat().st_size < 100:
                    file.unlink(missing_ok=True)
                if file.suffix in ['.sar', '.spf', '.ckf']:
                    file.unlink(missing_ok=True)
            except FileNotFoundError:
                pass


class ProcessWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.text_widget = QPlainTextEdit()
        self.log_widget = QPlainTextEdit()
        layout.addWidget(self.log_widget)
        layout.addWidget(self.text_widget)
        self.button = QPushButton("Run QProcess")
        layout.addWidget(self.button)
        self.time_label = QLabel()
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.runner = PlatonRunner(parent=self, output_widget=self.text_widget, log_widget=self.log_widget,
                                   cif_file=Path("tests/examples/work/cu_BruecknerJK_153F40_0m.cif"))
        self.button.clicked.connect(lambda x: self.button.setDisabled(True))
        self.button.clicked.connect(lambda x: self.runner.run_process())
        self.button.clicked.connect(lambda x: self.log_widget.setPlainText('Running Platon'))
        self.runner.finished.connect(lambda x: self.button.setEnabled(True))

        # Only to show that the main thread works continuously:
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        current_time = QtCore.QTime.currentTime()
        time_text = current_time.toString("hh:mm:ss")
        self.time_label.setText(f"Current Time: {time_text}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("QProcess Example")
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)

    process_widget = ProcessWidget()
    window.setCentralWidget(process_widget)

    window.show()

    sys.exit(app.exec())
