import os
import sys
import threading
import traceback
from pathlib import Path

from qtpy import QtCore, compat
from qtpy import QtWidgets
from qtpy.QtCore import QProcess
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QMessageBox, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QFrame, QProgressDialog

from finalcif import VERSION
from finalcif.tools.selfupdate import ElevationRefused, UpdateCancelled, UpdateError, can_self_update, \
    download_installer, start_exit_watchdog, start_installer, start_user_installer, user_installation_directory

# Keeps the running downloads alive, a local variable would be garbage collected:
_running_updates: set = set()


class InstallerDownload:
    """Downloads the FinalCif installer in a background thread.

    Not a single Qt object is touched from that thread; the GUI polls the state of the
    download with a timer instead (see :func:`update_installation`).
    """

    def __init__(self, version: str) -> None:
        self.version = version
        self.setup_file: Path | None = None
        self.error = ''
        self.finished = False
        self._lock = threading.Lock()
        self._received = 0
        self._total = 0
        self._cancelled = False

    def start(self) -> None:
        threading.Thread(target=self.run, daemon=True).start()

    def cancel(self) -> None:
        self._cancelled = True

    @property
    def progress(self) -> tuple[int, int]:
        with self._lock:
            return self._received, self._total

    def _report_progress(self, received: int, total: int) -> None:
        with self._lock:
            self._received = received
            self._total = total

    def run(self) -> None:
        try:
            self.setup_file = download_installer(self.version,
                                                 progress=self._report_progress,
                                                 should_cancel=lambda: self._cancelled)
        except UpdateCancelled:
            pass
        except UpdateError as err:
            self.error = str(err)
        except Exception as err:  # The dialog would wait forever for a thread that died:
            traceback.print_exc()
            self.error = f'The installer could not be downloaded:\n{err!r}'
        finally:
            self.finished = True


def do_update_program(version: str, parent=None) -> None:
    if can_self_update():
        update_installation(version, parent)
    else:
        print('No update available.')


def update_installation(version: str, parent=None) -> None:
    """Download the installer and hand the installation directory over to it."""
    progress_dialog = QProgressDialog('Downloading the FinalCif installer...', 'Cancel', 0, 100, parent)
    progress_dialog.setWindowTitle('FinalCif update')
    progress_dialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
    progress_dialog.setAutoClose(False)
    progress_dialog.setAutoReset(False)
    progress_dialog.setMinimumDuration(0)
    progress_dialog.setValue(0)
    downloader = InstallerDownload(version)
    # Everything below runs in the GUI thread, driven by this timer:
    timer = QtCore.QTimer(progress_dialog)
    timer.setInterval(200)
    # Plain local variables would be garbage collected while the thread is downloading:
    running_update = (downloader, progress_dialog)

    def show_progress() -> None:
        received, total = downloader.progress
        if total:
            progress_dialog.setRange(0, 100)
            progress_dialog.setValue(int(100 * received / total))
        elif received:
            # Without a content-length there is nothing to calculate a percentage from:
            progress_dialog.setRange(0, 0)
        if received and received == total:
            progress_dialog.setLabelText('Verifying the downloaded installer...')
        else:
            progress_dialog.setLabelText(f'Downloading the FinalCif installer... '
                                         f'({received / 1024 ** 2:.1f} MB)')

    def on_failed(message: str) -> None:
        progress_dialog.close()
        show_general_warning(parent, warn_text='The update failed.', info_text=message,
                             window_title='FinalCif update')

    def on_downloaded(setup_file: Path) -> None:
        progress_dialog.setLabelText('Starting the installer...')
        progress_dialog.setRange(0, 100)
        progress_dialog.setValue(100)
        QApplication.processEvents()
        release_installation_directory()
        try:
            start_installer(setup_file)
        except ElevationRefused as err:
            progress_dialog.close()
            if not install_into_user_directory(setup_file, str(err), parent):
                return
        except UpdateError as err:
            on_failed(str(err))
            return
        progress_dialog.close()
        quit_application()

    def check_download() -> None:
        show_progress()
        if not downloader.finished:
            return
        timer.stop()
        _running_updates.discard(running_update)
        if downloader.error:
            on_failed(downloader.error)
        elif downloader.setup_file is not None:
            on_downloaded(downloader.setup_file)
        else:
            progress_dialog.close()

    timer.timeout.connect(check_download)
    progress_dialog.canceled.connect(downloader.cancel)
    _running_updates.add(running_update)
    downloader.start()
    progress_dialog.show()
    timer.start()


def install_into_user_directory(setup_file: Path, reason: str, parent=None) -> bool:
    """Offer the per-user installation to accounts without administrator rights."""
    question = QMessageBox(parent)
    question.setWindowTitle('FinalCif update')
    question.setIcon(QMessageBox.Icon.Question)
    question.setText('FinalCif can be installed in your personal folder instead.')
    question.setInformativeText(f'{reason}\n\n'
                                f'Install FinalCif into\n{user_installation_directory()}\ninstead? '
                                f'This needs no administrator rights.\n\n'
                                f'The current installation stays where it is. Start the new FinalCif '
                                f'from your personal start menu entry afterwards.')
    question.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    question.setDefaultButton(QMessageBox.StandardButton.Yes)
    if question.exec() != QMessageBox.StandardButton.Yes:
        return False
    try:
        start_user_installer(setup_file)
    except UpdateError as err:
        show_general_warning(parent, warn_text='The update failed.', info_text=str(err),
                             window_title='FinalCif update')
        return False
    return True


def release_installation_directory() -> None:
    """Kill child processes like PLATON, they lock their executable in the installation dir."""
    app = QApplication.instance()
    if app is None:
        return
    for widget in app.topLevelWidgets():
        for process in widget.findChildren(QProcess):
            if process.state() != QProcess.ProcessState.NotRunning:
                process.kill()
                process.waitForFinished(3000)


def quit_application() -> None:
    """Leave FinalCif so that the installer can replace all files."""
    start_exit_watchdog()
    app = QApplication.instance()
    if app is None:
        os._exit(0)
    app.closeAllWindows()
    app.quit()


def unable_to_open_message(parent, filepath: Path, not_ok: Exception) -> None:
    """
    Shows a message if the current cif file can not be opened.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        print('DBG> Running inside a pytest -> not showing error message.')
        return
    info = QMessageBox(parent=parent)
    info.setIcon(QMessageBox.Icon.Information)
    print('Output from gemmi:', not_ok)
    try:
        line = str(not_ok)[4:].split(':')[1]
    except IndexError:
        line = None
    info.setText('This cif file is not readable!                                           ')
    if line:
        try:
            int(line)
            info.setInformativeText(f'\nPlease check line {line} in\n{filepath.name}')
        except ValueError:
            info.setInformativeText(f'"{filepath.name}"\n{not_ok}')
    else:
        info.setInformativeText(f'"{filepath.name}"\n{not_ok}')
    info.setModal(True)
    info.show()


def show_res_checksum_warning(parent) -> None:
    """
    A message box to display if the checksums do not agree.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        print('DBG> Running inside a pytest -> not showing error message.')
        return
    info = QMessageBox(parent=parent)
    info.setIcon(QMessageBox.Icon.Warning)
    info.setText('The "_shelx_res_checksum" is not consistent with the .res file content!\n\n'
                 'This error might originate from non-ascii Characters like Umlauts in you SHELX file.')
    info.setModal(True)
    info.show()


def show_hkl_checksum_warning(parent) -> None:
    """
    A message box to display if the checksums do not agree.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        print('DBG> Running inside a pytest -> not showing error message.')
        return
    info = QMessageBox(parent=parent)
    info.setIcon(QMessageBox.Icon.Warning)
    info.setText('The "_shelx_hkl_checksum" is not\nconsistent with the .hkl file content!')
    info.setModal(True)
    info.show()


def show_general_warning(parent, warn_text: str = '', info_text: str = '', window_title=' ') -> None:
    """
    A message box to display if the checksums do not agree.
    warn_text is displayed bold.
    info_text is displayed regular.
    """
    if not warn_text:
        return None
    if "PYTEST_CURRENT_TEST" in os.environ:
        print(f'DBG> Running inside a pytest -> not showing error message:\n{warn_text}\n{info_text}')
        return None
    box = QMessageBox(parent=parent)
    box.setTextFormat(QtCore.Qt.TextFormat.AutoText)
    box.setWindowTitle(window_title)
    box.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
    box.setText(warn_text)
    box.setModal(True)
    if info_text:
        box.setInformativeText(info_text)
        box.setStyleSheet("QLabel{min-width:600 px; font-size: 14px;}")
    box.show()
    if parent is None:
        box.exec()
        box.close()


def show_keyword_help(parent, helptext: str, title: str = ''):
    """
    A window to display help texts from the CIF dictionaries.
    """
    nlines = len(helptext.splitlines())
    window = QMainWindow(parent=parent)
    window.setWindowTitle(title)

    def close_window(event) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            window.close()

    window.keyPressEvent = close_window
    widget = QFrame()
    layout = QVBoxLayout()
    button = QPushButton('close')
    textedit = QTextEdit()
    textedit.setReadOnly(True)
    textedit.setFontFamily('monospace')
    textedit.setText(helptext)
    layout.addWidget(textedit)
    layout.addWidget(button)
    widget.setLayout(layout)
    window.setCentralWidget(widget)
    width = textedit.fontMetrics().horizontalAdvance('X' * 70)
    height = textedit.fontMetrics().horizontalAdvance('X' * nlines)
    textedit.setMinimumWidth(max([600, width]))
    textedit.setMinimumHeight(max([400, height]))
    window.move(300, 100)
    window.show()
    button.clicked.connect(window.close)


def show_ok_cancel_warning(parent, warn_text: str = '') -> bool:
    box = QMessageBox(parent=parent)
    box.setTextFormat(QtCore.Qt.TextFormat.AutoText)
    box.setWindowTitle(" ")
    box.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
    box.setText(warn_text)
    box.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
    box.setDefaultButton(QMessageBox.StandardButton.Ok)
    box.setModal(True)
    box.show()
    return box.result() == QMessageBox.StandardButton.Ok


def show_update_warning(parent, remote_version: int = 0) -> None:
    """
    A message box to display if the checksums do not agree.
    """
    warn_text = "A newer version {} of FinalCif is available under: <br>" \
                "<a href='https://dkratzert.de/finalcif.html'>" \
                "https://dkratzert.de/finalcif.html</a>"
    box = QMessageBox(parent)
    box.setTextFormat(QtCore.Qt.TextFormat.AutoText)
    box.setWindowTitle(" ")
    box.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
    if sys.platform.startswith("win"):
        warn_text += r"<br><br>Updating now will end all running FinalCIF programs!"
        update_button = box.addButton('Update Now', QMessageBox.ButtonRole.AcceptRole)
        update_button.clicked.connect(lambda: do_update_program(str(remote_version), parent))
    box.setText(warn_text.format(remote_version))
    box.setModal(True)
    box.show()


def bad_z_message(parent, z: float) -> None:
    zinfo = QMessageBox(parent)
    zinfo.setIcon(QMessageBox.Icon.Information)
    zinfo.setText(f'The number of formula units Z={z:.0f} is probably wrong.\n'
                  f'You may restart refinement with a correct value.')
    zinfo.setModal(True)
    zinfo.show()


def show_bug_found_warning(logfile) -> None:
    window = QMainWindow()
    title = 'Congratulations, you found a bug in FinalCif!'
    text = (f'<br>Please send the file <br>'
            f'<a href={logfile.resolve()}>{logfile.resolve()}</a> '
            f'<br>to Daniel Kratzert:  '
            f'<a href="mailto:dkratzert@gmx.de?subject=FinalCif version {VERSION} crash report">'
            f'dkratzert@gmx.de</a><br>'
            f'<br>If possible, the corresponding CIF file is also desired.')
    box = QMessageBox(parent=window)
    box.setWindowTitle('Warning')
    box.setText(title)
    box.setInformativeText(text)
    box.setTextFormat(QtCore.Qt.TextFormat.RichText)
    box.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextBrowserInteraction)
    box.exec()
    window.show()


def show_yes_now_question(title: str, question: str, parent=None) -> bool:
    response = QMessageBox.question(parent, title, question,
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                    QMessageBox.StandardButton.No)
    if response == QMessageBox.StandardButton.Yes:
        return True
    else:
        return False


def cif_file_open_dialog(parent: object = None, filter: str = "CIF file (*.cif)", last_dir='', options=None) -> str:
    """
    Returns a cif file name from a file dialog.
    """
    filename, _ = compat.getopenfilename(parent=parent,
                                         caption='Open a .cif File',
                                         basedir=last_dir,
                                         filters=filter,
                                         selectedfilter=filter,
                                         options=options
                                         )
    return filename


def cif_file_save_dialog(filename: str, parent=None) -> str:
    """
    Returns a cif file name from a file dialog.
    """
    filter = "CIF file (*.cif)"
    filename, _ = compat.getsavefilename(parent=parent,
                                         filters=filter,
                                         caption='Save .cif File',
                                         selectedfilter=filter)
    return filename


def video_file_open_dialog(parent: object = None, filter: str = "Video file (*.vzs; *.jpg)", last_dir='', options=None) -> str:
    filename, _ = compat.getopenfilename(parent=parent,
                                         caption='Open a crystal video file',
                                         basedir=last_dir,
                                         filters=filter,
                                         selectedfilter=filter,
                                         options=options
                                         )
    return filename


if __name__ == '__main__':
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    window = QtWidgets.QMainWindow()
    w = QtWidgets.QWidget()
    window.setCentralWidget(w)
    l = QtWidgets.QVBoxLayout()
    w.setLayout(l)
    # answer = show_yes_now_question(title='Delete templates', question='Fobar?', parent=w)
    # bad_z_message(parent=w, z=3.0)
    # show_update_warning(parent=w, remote_version=123)
    # show_bug_found_warning(Path(r'test.txt'))
    # show_ok_cancel_warning(parent=w, warn_text='foobar')
    # show_keyword_help(parent=w, helptext="This is a helptext", title='A Title')
    # show_general_warning(parent=w, warn_text='Warning text', info_text='Info text', window_title='Title')
    #show_hkl_checksum_warning(parent=w)
    # show_res_checksum_warning(parent=w)
    unable_to_open_message(parent=w, not_ok=Exception('foo'), filepath=Path('C:/foo.txt'))
    #do_update_program('170')
    w.show()

    app.exec()
