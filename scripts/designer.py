
import sys
import os.path
from pathlib import Path
from pprint import pprint

from PyQt5.QtCore import QCoreApplication, QLibraryInfo, QProcess, QProcessEnvironment


def main():
    app = QCoreApplication([])
    base_dir = Path(__file__).parent.parent
    plugins_dir = os.path.join(base_dir, "finalcif/gui/customWidgets")
    lib_dir = os.path.join(base_dir)

    env = QProcessEnvironment.systemEnvironment()
    #print(plugins_dir)
    env.insert("PYQTDESIGNERPATH", plugins_dir)
    #env.insert("QT_DEBUG_PLUGINS", '1')
    print('Designerpath:', os.environ.get('PYQTDESIGNERPATH'))
    env.insert("PYTHONPATH", '/Users/daniel/Documents/GitHub/FinalCif')
    #pprint([x for x in os.environ.items()])
    print(os.environ.get('PYTHONPATH'))

    # Start Designer.
    designer = QProcess()
    designer.setProcessEnvironment(env)

    designer_bin = QLibraryInfo.location(QLibraryInfo.BinariesPath)

    if sys.platform == "darwin":
        #designer_bin = '/usr/local/Cellar/qt/6.5.0/bin/Designer'
        designer_bin = '/usr/local/Cellar/qt@5/5.15.8_3/libexec/Designer.app/Contents/MacOS/Designer'
    else:
        designer_bin += "/designer"

    designer.start(designer_bin)
    designer.waitForFinished(-1)

    sys.exit(designer.exitCode())


if __name__ == "__main__":
    main()