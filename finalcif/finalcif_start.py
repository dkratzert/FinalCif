#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import sys
from typing import Type


if 'compile_ui' in sys.argv:
    COMPILE = True
    del sys.argv[sys.argv.index('compile_ui')]
else:
    COMPILE = False
import os

from finalcif.app_path import application_path

if COMPILE:
    from PyQt5 import uic

    print('Compiling ui ...')
    uic.compileUiDir(os.path.join(application_path, 'gui'))

import time
import traceback
from pathlib import Path

from finalcif.gui.dialogs import bug_found_warning
from finalcif import VERSION

from PyQt5.QtGui import QIcon
from finalcif.appwindow import AppWindow, DEBUG, app

r"""
TODO:
- Try https://qpageview.org/usage.html
- generate picture with local platon
- dist errors: Giacovazzo p.122
- Read measurement time from SAINT 0m._ls file and its list of integrated files. Or even better from the .xml file.
- Extract more data from .xml file
- Extract "_diffrn_measurement_details from .xml file
- maybe add refinement model description via ShelXFile parser 
- Add one picture of the vzs video file to report.
- Improve handling of SQUEEZEd data
- Improove handling of Flack x parameter
    - citation, method used, success
"""
# They must be here in order to have directly updated ui files from the ui compiler:


if __name__ == '__main__':
    def my_exception_hook(exctype: Type[BaseException], value: BaseException, error_traceback) -> None:
        """
        Hooks into Exceptions to create debug reports.
        """
        errortext = 'FinalCif V{} crash report\n\n'.format(VERSION)
        errortext += 'Please send also the corresponding CIF file, if possible.'
        errortext += 'Python ' + sys.version + '\n'
        errortext += sys.platform + '\n'
        errortext += time.asctime(time.localtime(time.time())) + '\n'
        errortext += "Finalcif crashed during the following operation:" + '\n'
        errortext += '-' * 80 + '\n'
        errortext += ''.join(traceback.format_tb(error_traceback)) + '\n'
        errortext += str(exctype.__name__) + ': '
        errortext += str(value) + '\n'
        errortext += '-' * 80 + '\n'
        logfile = Path.home().joinpath(Path(r'finalcif-crash.txt'))
        try:
            logfile.write_text(errortext)
        except PermissionError:
            pass
        sys.__excepthook__(exctype, value, error_traceback)
        # Hier Fenster für meldung öffnen
        bug_found_warning(logfile)
        sys.exit(1)


    if not DEBUG:
        sys.excepthook = my_exception_hook

    # windows_style = QStyleFactory.create('Fusion')
    # app.setStyle(windows_style)
    w = AppWindow()
    app.setWindowIcon(QIcon(os.path.join(application_path, r'icon/finalcif2.png')))
    w.setWindowTitle('FinalCif v{}'.format(VERSION))
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
