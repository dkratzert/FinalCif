#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

import requests
from PyQt5.QtCore import QPoint, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
from requests.exceptions import MissingSchema


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

    def __init__(self, parent: 'AppWindow', cif: Path, outfile: Path):
        self.parent = parent
        # _, self.out_file = mkstemp(suffix='.html')
        self.out_file = outfile
        self.cifobj = cif

    def _get_checkcif(self, out_file: Path, pdf=True):
        """
        Requests a checkcif run from IUCr servers.
        """
        f = open(str(self.cifobj.absolute()), 'rb')
        if pdf:
            report_type = 'PDF'
            vrf = 'vrfno'
        else:
            report_type = 'HTML'
            vrf = 'vrfab'
        if self.parent.cif.block.find_value('_shelx_hkl_file'):
            hkl = 'checkcif_with_hkl'
        else:
            hkl = 'checkcif_only'
        headers = {
            "runtype"   : "symmonly",
            "referer"   : "checkcif_server",
            "outputtype": report_type,
            "validtype" : hkl,
            "valout"    : vrf,
        }
        print('Report request sent')
        url = 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl'
        r = requests.post(url, files={'file': f}, data=headers, timeout=150)
        out_file.write_bytes(r.content)
        f.close()
        print('ready')
        return out_file

    def show_html_report(self):
        """
        Shows the html result of checkcif in a webengine window.
        """
        self._get_checkcif(self.out_file, pdf=False)
        app = QMainWindow(self.parent)
        web = WebPage(self.out_file)
        app.setCentralWidget(web)
        app.setBaseSize(900, 900)
        app.show()
        app.setMinimumWidth(900)
        app.setMinimumHeight(700)
        app.move(QPoint(100, 50))
        web.show()

    def _open_pdf_result(self, html_result: Path):
        """
        Opens the resulkting pdf file in the systems pdf viewer.
        """
        parser = MyHTMLParser()
        # the link to the pdf file resides in this html file:
        parser.feed(html_result.read_text())
        try:
            pdf = parser.get_pdf()
        except MissingSchema:
            print('Link is not valid anymore...')
            pdf = None
        if pdf:
            pdfobj = Path('checkcif-' + self.cifobj.stem + '.pdf')
            pdfobj.write_bytes(pdf)
            if sys.platform == 'win' or sys.platform == 'win32':
                subprocess.Popen([str(pdfobj.absolute())], shell=True)
            if sys.platform == 'darwin':
                subprocess.call(['open', str(pdfobj.absolute())])

    def show_pdf_report(self):
        html = self._get_checkcif(self.out_file, pdf=True)
        self._open_pdf_result(html)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.link = ''
        super(MyHTMLParser, self).__init__()
        self.pdf = ''

    def get_pdf(self):
        return requests.get(self.link).content

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len(attrs) > 1 and attrs[0][1] == '_blank':
                self.link = attrs[1][1]


if __name__ == "__main__":
    cif = Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\BreitPZ_R_122_0m_a-finalcif.cif')
    html = Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\checkcif-test.html')
    ckf = MakeCheckCif(None, cif, outfile=html)
    ckf.show_pdf_report()
    # html = Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\checkcif-BreitPZ_R_122_0m_a.html')
    # open_pdf_result(Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\BreitPZ_R_122_0m_a-finalcif.cif'), html)
    # Path(d:\tmp\
    # print(parser.pdf)
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

    # outfile = get_checkcif('test-data/p21c.cif')
    # app = QWindow()
    # web = WebPage(outfile)
    # web.show()
    # app.setWidth(500)
    # app.exec_()
    # web.close()
    pass
