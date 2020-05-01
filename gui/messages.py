from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSplashScreen

from tools.version import VERSION


def unable_to_open_message(filepath: Path, not_ok: Exception) -> None:
    """
    Shows a message if the current cif file can not be opened.
    """
    info = QMessageBox()
    info.setIcon(QMessageBox.Information)
    print('Output from gemmi:', not_ok)
    try:
        line = str(not_ok)[4:].split(':')[1]
    except IndexError:
        line = None
    if line:
        try:
            int(line)
            info.setText('This cif file is not readable!\n'
                         'Please check line {} in\n{}'.format(line, filepath.name))
        except ValueError:
            info.setText('This cif file is not readable! "{}"\n{}'.format(filepath.name, not_ok))
    else:
        info.setText('This cif file is not readable! "{}"\n{}'.format(filepath.name, not_ok))
    info.show()
    info.exec()
    return


def show_checksum_warning(res=True) -> None:
    """
    A message box to display if the checksums do not agree.
    """
    info = QMessageBox()
    info.setIcon(QMessageBox.Warning)
    if res:
        info.setText('The "_shelx_res_checksum" is not\nconsistent with the .res file content!')
    else:
        info.setText('The "_shelx_hkl_checksum" is not\nconsistent with the .hkl file content!')
    info.show()
    info.exec()


def show_general_warning(warn_text: str = '') -> None:
    """
    A message box to display if the checksums do not agree.
    """
    if not warn_text:
        return
    box = QMessageBox()
    box.setTextFormat(Qt.AutoText)
    box.setWindowTitle(" ")
    box.setTextInteractionFlags(Qt.TextBrowserInteraction)
    box.setText(warn_text)
    box.exec()


def bad_z_message(Z):
    zinfo = QMessageBox()
    zinfo.setIcon(QMessageBox.Information)
    zinfo.setText('The number of formula units Z={:.0f} is probably wrong.'
                  '\nYou may restart refinement with a correct value.'.format(Z))
    zinfo.show()
    zinfo.exec()


def bug_found_warning(logfile):
    window = QMainWindow()
    text = 'Congratulations, you found a bug in ' \
           'FinalCif!<br>Please send the file <br>"{}" <br>to Daniel Kratzert:  ' \
           '<a href="mailto:daniel.kratzert@ac.uni-freiburg.de?subject=FinalCif version {} crash report">' \
           'daniel.kratzert@ac.uni-freiburg.de</a>'.format(logfile.absolute(), VERSION)
    QMessageBox.warning(window, 'Warning', text)
    window.show()


def show_splash(text: str):
    splash = QSplashScreen()
    splashFont = QFont()
    # splashFont.setFamily("Arial")
    splashFont.setBold(True)
    splashFont.setPixelSize(16)
    splashFont.setStretch(120)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.SplashScreen)
    splash = QSplashScreen()
    splash.show()
    splash.setStyleSheet("background-color:#fcc77c;")
    splash.setFont(splashFont)
    splash.setMinimumWidth(400)
    splash.setMaximumHeight(100)
    splash.showMessage(text, alignment=Qt.AlignCenter, )
    return splash