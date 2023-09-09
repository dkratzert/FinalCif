#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import os
import sys
import time
import traceback
from pathlib import Path
from typing import Type

from PyQt5.QtGui import QIcon

from finalcif import VERSION
from finalcif.app_path import application_path
from finalcif.appwindow import AppWindow, DEBUG, app
from finalcif.gui.dialogs import show_bug_found_warning


def my_exception_hook(exctype: Type[BaseException], value: BaseException, error_traceback: traceback,
                      exit=True) -> None:
    """
    Hooks into Exceptions to create debug reports.
    """
    errortext = (f'FinalCif V{VERSION} crash report\n\n'
                 f'Please send also the corresponding CIF file, if possible. \n'
                 f'Python {sys.version}\n'
                 f'Platform: {sys.platform}\n'
                 f'Date: {time.asctime(time.localtime(time.time()))}\n'
                 f'Finalcif crashed during the following operation:\n\n'
                 f'{"-" * 120}\n'
                 f'{"".join(traceback.format_tb(error_traceback))}\n'
                 f'{str(exctype.__name__)}: '
                 f'{str(value)} \n'
                 f'{"-" * 120}\n')
    logfile = Path.home().joinpath(Path(r'finalcif-crash.txt'))
    try:
        logfile.write_text(errortext)
    except PermissionError:
        pass
    sys.__excepthook__(exctype, value, error_traceback)
    show_bug_found_warning(logfile)
    if exit:
        sys.exit(1)


def main():
    if not DEBUG:
        sys.excepthook = my_exception_hook
    # windows_style = QStyleFactory.create('Fusion')
    # app.setStyle(windows_style)
    w = AppWindow()
    app.setWindowIcon(QIcon(os.path.join(application_path, r'icon/finalcif2.png')))
    w.setWindowTitle('FinalCif v{}'.format(VERSION))
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
