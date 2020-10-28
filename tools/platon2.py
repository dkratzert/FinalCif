import asyncio
import subprocess
import sys
from pathlib import Path

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

from finalcif import AppWindow


class CheckCifPlaton(QThread):
    progress = pyqtSignal(str)
    failed = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, cif: Path):
        super().__init__()
        self.myapp = AppWindow()  # ([x for x in Path('.').rglob('1979688.cif')][0].absolute())
        # self.myapp.setWindowIcon(QIcon('./icon/multitable.png'))
        # self.myapp.setWindowTitle('FinalCif v{}'.format(VERSION))
        self.myapp.hide()
        self.cif_fileobj = cif
        self.chkfile = Path(self.cif_fileobj.with_suffix('.chk'))
        self.outfile = Path('platon.out')

    async def runplaton(self):
        print('sdg#fdsgf')
        try:
            # This is only available on windows:
            si = subprocess.STARTUPINFO()
            si.dwFlags = 1
            si.wShowWindow = 0
        except AttributeError:
            si = None
        subprocess.run(['platon', '-u', self.cif_fileobj.absolute()], shell=True)
        print('danach')

    def run(self) -> None:
        pass
        # probably I need a thread to run platon and another to observe the platon.out file
        


if __name__ == '__main__':
    def ckf_progress(txt: str):
        print('##foo## ' + txt)


    def ckf_finished():
        print('yeahyeah')


    app = QApplication(sys.argv)
    fname = Path('test-data/DK_zucker2_0m.cif')
    c = CheckCifPlaton(fname)
    c.progress.connect(ckf_progress)
    c.finished.connect(ckf_finished)
    c.start()
    """
    class Slave(QtCore.QProcess):
    def __init__(self, parent=None):
        super().__init__()
        self.readyReadStandardOutput.connect(self.stdoutEvent)
        self.readyReadStandardError.connect(self.stderrEvent)
 
    def stdoutEvent(self):
        stdout = self.readAllStandardOutput()
        self.echo(stdout)
 
    def stderrEvent(self):
        stderr = self.readAllStandardError()
        self.echo(stderr)
 
    def echo(self, data):
        data = bytes(data).decode("utf8")
        if data:
            print(data, end="")
    """
