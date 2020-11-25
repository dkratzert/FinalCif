#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

import sys
from typing import Type

if 'compile' in sys.argv:
    COMPILE = True
    del sys.argv[sys.argv.index('compile')]
else:
    COMPILE = False
import os

from app_path import application_path

if COMPILE:
    from PyQt5 import uic

    print('Compiling ui ...')
    uic.compileUiDir(os.path.join(application_path, 'gui'))
    # uic.compileUi('./gui/finalcif_gui.ui', open('./gui/finalcif_gui.py', 'w'))

import time
import traceback
from pathlib import Path

# noinspection PyUnresolvedReferences
from gemmi import cif
from gui.dialogs import bug_found_warning
from tools.version import VERSION

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from appwindow import AppWindow, DEBUG

r"""
TODO:
- Options: set path for own report template.
- Peters comments on equipment templates:
    * save state and order of selected templates in order to be able to undo a selection with a second click. 
- dist errors: Giacovazzo p.122
- Read measurement time from SAINT 0m._ls file and its list of integrated files. Or even better from the .xml file.
- make a modelview for the main table!
- Extract more data from .xml file
- Extract "_diffrn_measurement_details from .xml file
- maybe add refinement model description via ShelXFile parser 
- Add one picture of the vzs video file to report.
- Improve handling of SQUEEZEd data
- Improove handling of Flack x parameter
    - citation, method used, success
-Add possibility to add this:
data_global
loop_
_publ_author_name
'Feurer, Markus'
'Frey, Georg'
'Luu, Hieu-Trinh'
'Kratzert, Daniel'
'Streuff, Jan'
_publ_section_title
'The cross-selective titanium(III)-catalysed acyloin reaction.'
_journal_issue                   40
_journal_name_full
'Chemical communications (Cambridge, England)'
_journal_page_first              5370
_journal_page_last               5372
_journal_paper_doi               10.1039/c3cc46894a
_journal_volume                  50
_journal_year                    2014



# cif core dictionary to python dictionary:
c = CifContainer(Path('cif_core_dict.cif'))
cdic = json.loads(c.as_json())
[cdic[x]['_name'] for x in cdic.keys() if '_name' in cdic[x]]

as dict:
{str(cdic[x]['_name']): ' '.join(cdic[x]['_definition'].split()) for x in cdic.keys() if '_name' in cdic[x]}
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
        logfile = Path(r'./finalcif-crash.txt')
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

    app = QApplication(sys.argv)
    # windows_style = QStyleFactory.create('Fusion')
    # app.setStyle(windows_style)
    w = AppWindow()
    app.setWindowIcon(QIcon(os.path.join(application_path, r'icon/finalcif2.png')))
    w.setWindowTitle('FinalCif v{}'.format(VERSION))
    # w.showMaximized()  # For full screen view
    w.setBaseSize(1200, 780)
    sys.exit(app.exec_())
