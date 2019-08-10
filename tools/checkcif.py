#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from pathlib import Path

import requests
from PyQt5.QtCore import QUrl, QPoint
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow


class WebPage(QWebEngineView):
    def __init__(self, file: Path):
        QWebEngineView.__init__(self)
        # self.load(QUrl("https://checkcif.iucr.org/"))
        self.url = QUrl.fromLocalFile(str(file.absolute()))
        self.load(self.url)
        # self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self):
        self.page().toHtml(self.Callable)
        print("Finished Loading")

    def Callable(self, html_str):
        self.html = html_str


class MakeCheckCif():

    def __init__(self, parent, cif: Path, outfile: Path):
        self.parent = parent
        # _, self.out_file = mkstemp(suffix='.html')
        self.out_file = outfile
        self.show_report_window(cif)

    def get_checkcif(self, file_name: str, out_file: Path):
        """
        Requests a checkcif run from IUCr servers.
        """
        f = open(file_name, 'rb')

        headers = {
            "file"      : f,  # Path(file_name).open(),  # .read_text(encoding='ascii'),
            "runtype"   : "symmonly",
            "referer"   : "checkcif_server",
            "outputtype": 'HTML',
            "validtype" : "checkcif_only",
            # "valout"    : 'vrfno',
            # "UPLOAD"    : 'submit',
        }
        print('Report request sent')
        url = 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl'
        r = requests.post(url, files=headers, timeout=150)
        out_file.write_bytes(r.content)
        f.close()
        print('ready')
        return out_file

    def show_report_window(self, cif):
        self.get_checkcif(cif.absolute(), self.out_file)
        app = QMainWindow(self.parent)
        web = WebPage(self.out_file)
        app.setCentralWidget(web)
        app.setBaseSize(900, 900)
        app.show()
        app.setMinimumWidth(900)
        app.setMinimumHeight(700)
        app.move(QPoint(100, 50))
        web.show()


if __name__ == "__main__":
    # outfile = get_checkcif('test-data/p21c.cif')
    # app = QApplication(sys.argv)
    # web = WebPage(outfile)
    # web.show()
    # app.exec_()
    # web.close()
    # try:
    #    Path(outfile).unlink()
    # except PermissionError:
    #    print('can not delete 1')

    #outfile = get_checkcif('test-data/p21c.cif')
    #app = QWindow()
    #web = WebPage(outfile)
    #web.show()
    #app.setWidth(500)
    #app.exec_()
    #web.close()
    pass
