import ctypes
import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSplashScreen, QFileDialog, QVBoxLayout, QTextEdit, \
    QPushButton, QFrame

from finalcif import VERSION


def do_update_program(version) -> None:
    updater_exe = str(Path(__file__).parent.parent.parent.joinpath('update.exe'))
    args = ['-v', version,
            '-p', 'finalcif']
    # Using this, because otherwise I can not write to the program dir:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", updater_exe, " ".join(args), None, 1)


def unable_to_open_message(filepath: Path, not_ok: Exception) -> None:
    """
    Shows a message if the current cif file can not be opened.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        print('DBG> Running inside a pytest -> not showing error message.')
        return
    info = QMessageBox()
    info.setIcon(QMessageBox.Information)
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
    info.show()
    info.exec()


def show_res_checksum_warning() -> None:
    """
    A message box to display if the checksums do not agree.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        print('DBG> Running inside a pytest -> not showing error message.')
        return
    info = QMessageBox()
    info.setIcon(QMessageBox.Warning)
    info.setText('The "_shelx_res_checksum" is not consistent with the .res file content!\n\n'
                 'This error might originate from non-ascii Characters like Umlauts in you SHELX file.')
    info.show()
    info.exec()


def show_hkl_checksum_warning() -> None:
    """
    A message box to display if the checksums do not agree.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        print('DBG> Running inside a pytest -> not showing error message.')
        return
    info = QMessageBox()
    info.setIcon(QMessageBox.Warning)
    info.setText('The "_shelx_hkl_checksum" is not\nconsistent with the .hkl file content!')
    info.show()
    info.exec()


def show_general_warning(warn_text: str = '', info_text: str = '', window_title=' ') -> None:
    """
    A message box to display if the checksums do not agree.
    warn_text is displayed bold.
    info_text is displayed regular.
    """
    if not warn_text:
        return None
    box = QMessageBox()
    box.setTextFormat(Qt.AutoText)
    box.setWindowTitle(window_title)
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setText(warn_text)
    if info_text:
        box.setInformativeText(info_text)
        box.setStyleSheet("QLabel{min-width:600 px; font-size: 14px;}")
    box.exec()


def show_keyword_help(parent, helptext: str, title: str = ''):
    """
    A window to display help texts from the CIF dictionaries.
    """
    nlines = len(helptext.splitlines())
    window = QMainWindow(parent=parent)
    window.setWindowFlags(Qt.Tool)
    window.setWindowTitle(title)
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
    width = textedit.fontMetrics().width('X' * 70)
    height = textedit.fontMetrics().width('X' * nlines)
    textedit.setMinimumWidth(max([600, width]))
    textedit.setMinimumHeight(max([400, height]))
    window.move(300, 100)
    window.show()
    window.raise_()
    button.clicked.connect(window.close)


def show_ok_cancel_warning(warn_text: str = '') -> bool:
    box = QMessageBox()
    box.setTextFormat(Qt.AutoText)
    box.setWindowTitle(" ")
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setText(warn_text)
    box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    box.setDefaultButton(QMessageBox.Ok)
    box.exec()
    return box.result() == QMessageBox.Ok


def show_update_warning(remote_version: int = 0) -> None:
    """
    A message box to display if the checksums do not agree.
    """
    warn_text = "A newer version {} of FinalCif is available under: <br>" \
                "<a href='https://dkratzert.de/finalcif.html'>" \
                "https://dkratzert.de/finalcif.html</a>"
    box = QMessageBox()
    box.setTextFormat(Qt.AutoText)
    box.setWindowTitle(" ")
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    if sys.platform.startswith("win"):
        warn_text += r"<br><br>Updating now will end all running FinalCIF programs!"
        update_button = box.addButton('Update Now', QMessageBox.AcceptRole)
        update_button.clicked.connect(lambda: do_update_program(str(remote_version)))
    box.setText(warn_text.format(remote_version))
    box.exec()


def bad_z_message(z) -> None:
    zinfo = QMessageBox()
    zinfo.setIcon(QMessageBox.Information)
    zinfo.setText('The number of formula units Z={:.0f} is probably wrong.'
                  '\nYou may restart refinement with a correct value.'.format(z))
    zinfo.show()
    zinfo.exec()


def show_bug_found_warning(logfile) -> None:
    window = QMainWindow()
    title = f'Congratulations, you found a bug in FinalCif!'
    text = (f'<br>Please send the file <br>'
            f'<a href=file:{os.sep * 2}{logfile.resolve()}>{logfile.resolve()}</a> '
            f'<br>to Daniel Kratzert:  '
            f'<a href="mailto:dkratzert@gmx.de?subject=FinalCif version {VERSION} crash report">'
            f'dkratzert@gmx.de</a><br>'
            f'<br>If possible, the corresponding CIF file is also desired.')
    box = QMessageBox(parent=window)
    box.setWindowTitle('Warning')
    box.setText(title)
    box.setInformativeText(text)
    box.exec()
    window.show()


def show_yes_now_question(title: str, question: str, parent=None) -> bool:
    response = QMessageBox.question(parent, title, question, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if response == QMessageBox.Yes:
        return True
    else:
        return False


def show_splash(text: str) -> QSplashScreen:
    splash = QSplashScreen()
    splash_font = QFont()
    # splashFont.setFamily("Arial")
    splash_font.setBold(True)
    splash_font.setPixelSize(16)
    splash_font.setStretch(120)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    splash = QSplashScreen()
    splash.show()
    splash.setStyleSheet("background-color:#fcc77c;")
    splash.setFont(splash_font)
    splash.setMinimumWidth(400)
    splash.setMaximumHeight(100)
    splash.showMessage(text, alignment=Qt.AlignCenter, )
    return splash


def cif_file_open_dialog(filter: str = "CIF file (*.cif)", last_dir='') -> str:
    """
    Returns a cif file name from a file dialog.
    """
    filename, _ = QFileDialog.getOpenFileName(filter=filter,
                                              directory=last_dir,
                                              initialFilter=filter,
                                              caption='Open a .cif File')
    return filename


def cif_file_save_dialog(filename: str) -> str:
    """
    Returns a cif file name from a file dialog.
    """
    dialog = QFileDialog(filter="CIF file (*.cif)", caption='Save .cif File')
    dialog.setDefaultSuffix('.cif')
    dialog.selectFile(filename)
    filename, _ = dialog.getSaveFileName(None, 'Select file name', filename)
    return filename
