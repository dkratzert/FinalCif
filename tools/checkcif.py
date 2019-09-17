#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import os
import subprocess
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from tempfile import mkstemp
import gemmi

import requests
from PyQt5.QtCore import QUrl, QPoint
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QMainWindow
from requests.exceptions import MissingSchema

from tools.misc import strip_finalcif_of_name


class WebPage(QWebEngineView):
    def __init__(self, file: Path):
        QWebEngineView.__init__(self)
        self.url = QUrl.fromLocalFile(str(file.absolute()))
        self.load(self.url)

    def _on_load_finished(self):
        self.page().toHtml(self.Callable)
        print("Finished Loading")

    def Callable(self, html_str):
        self.html = html_str


class MakeCheckCif():

    def __init__(self, parent, cif: Path, outfile: Path):
        self.parent = parent
        # _, self.out_file = mkstemp(suffix='.html')
        self.html_out_file = outfile
        self.cifobj = cif

    def _get_checkcif(self, pdf=True):
        """
        Requests a checkcif run from IUCr servers.
        """
        tmp, fd = None, None
        f = open(str(self.cifobj.absolute()), 'rb')
        if pdf:
            report_type = 'PDF'
            vrf = 'vrfno'
        else:
            report_type = 'HTML'
            vrf = 'vrfab'
        if self.parent.cif.block.find_value('_shelx_hkl_file'):
            hkl = 'checkcif_with_hkl'
            if self.parent.ui.structfactCheckBox.isChecked():
                hkl = 'checkcif_only'
                f.close()
                tmp, fd = self._get_cif_without_hkl()
                f = open(tmp, 'rb')
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
        t1 = time.perf_counter()
        r = requests.post(url, files={'file': f}, data=headers, timeout=180)
        t2 = time.perf_counter()
        print('Report took {}s.'.format(str(round(t2 - t1, 2))))
        self.html_out_file.write_bytes(r.content)
        f.close()
        if hkl == 'checkcif_only':
            try:
                # a trick to clos the file descriptor:
                f = os.fdopen(fd, 'w')
                f.close()
                os.unlink(tmp)
            except ValueError:
                print('can not delete tempfile from checkcif:')
                print(tmp)
        print('ready')

    def show_html_report(self):
        """
        Shows the html result of checkcif in a webengine window.
        """
        self._get_checkcif(pdf=False)
        app = QMainWindow(self.parent)
        web = WebPage(self.html_out_file)
        app.setCentralWidget(web)
        app.setBaseSize(900, 900)
        app.show()
        app.setMinimumWidth(900)
        app.setMinimumHeight(700)
        app.move(QPoint(100, 50))
        web.show()

    def _open_pdf_result(self):
        """
        Opens the resulkting pdf file in the systems pdf viewer.
        """
        parser = MyHTMLParser()
        # the link to the pdf file resides in this html file:
        parser.feed(self.html_out_file.read_text())
        try:
            pdf = parser.get_pdf()
        except MissingSchema:
            print('Link is not valid anymore...')
            pdf = None
        if pdf:
            pdfobj = Path(strip_finalcif_of_name('checkcif-' + self.cifobj.stem) + '-finalcif.pdf')
            pdfobj.write_bytes(pdf)
            if sys.platform == 'win' or sys.platform == 'win32':
                subprocess.Popen([str(pdfobj.absolute())], shell=True)
            if sys.platform == 'darwin':
                subprocess.call(['open', str(pdfobj.absolute())])

    def show_pdf_report(self):
        self._get_checkcif(pdf=True)
        self._open_pdf_result()

    def _get_cif_without_hkl(self):
        fd, tmp = mkstemp(prefix='finalcif-', suffix='.cif')
        doc = gemmi.cif.read_string(self.cifobj.read_text())
        block = doc.sole_block()
        block.set_pair('_shelx_hkl_file', '')
        p = Path(tmp)
        p.write_text(doc.as_string(gemmi.cif.Style.Indent35))
        return tmp, fd


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.link = ''
        self.imageurl = ''
        super(MyHTMLParser, self).__init__()
        self.pdf = ''
        self.vrf = ''

    def get_pdf(self):
        return requests.get(self.link).content

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len(attrs) > 1 and attrs[0][1] == '_blank':
                self.link = attrs[1][1]
        if tag == "img":
            if len(attrs) > 1:
                if attrs[0][0] == 'width' and '.gif' in attrs[1][1]:
                    self.imageurl = attrs[1][1]

    def handle_data(self, data):
        if 'Validation Reply Form' in data:
            self.vrf = data

    def get_image(self):
        try:
            return requests.get(self.imageurl).content
        except MissingSchema:
            return b''


if __name__ == "__main__":
    #cif = Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\BreitPZ_R_122_0m_a-finalcif.cif')
    html = Path(r'/Users/daniel/GitHub/FinalCif/test-data/checkcif-DK_zucker2_0m.html')
    # ckf = MakeCheckCif(None, cif, outfile=html)
    # ckf.show_pdf_report()
    # html = Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\checkcif-BreitPZ_R_122_0m_a.html')

    from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest, QHttpMultiPart, QHttpPart
    from PyQt5.QtWebEngineWidgets import QWebEngineView

    parser = MyHTMLParser()
    parser.feed(html.read_text())
    print(parser.imageurl)
    print(parser.vrf)
    print(parser.pdf)
    print(parser.link)

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

    headers = {
        "runtype"   : "symmonly",
        "referer"   : "checkcif_server",
        "outputtype": 'HTML',
        "validtype" : 'checkcif_only',
        "valout"    : 'vrfno',
    }

    def show_update_warning(reply: QNetworkReply):
        """
        Reads the reply from the server and displays a warning in case of an old version.
        """
        print(reply.readAll()).decode('ascii', 'ignore')


