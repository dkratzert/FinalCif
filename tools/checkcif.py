#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import sys
from pathlib import Path

import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication


class WebPage(QWebEngineView):
    def __init__(self):
        QWebEngineView.__init__(self)
        #self.load(QUrl("https://checkcif.iucr.org/"))
        self.load(QUrl("cifreport.html"))
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self):
        print("Finished Loading")
        self.page().toHtml(self.Callable)

    def Callable(self, html_str):
        self.html = html_str
        '''
        self.page().runJavaScript(
            """
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState === 4 && this.status === 200) {
                    document.getElementsByTagName("body").innerHTML =
                    this.responseText;
                }
            };
            xhttp.open("POST", "//checkcif.iucr.org/cgi-bin/checkcif_hkl.pl", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("filecif=='/Users/daniel/GitHub/FinalCif/test-data/ntd106c-P-1-final.cif'");
            
            """
        )'''



def get_checkcif():
    file_name = 'test-data/DK_zucker2_0m.cif'
    out_file = "cifreport.html"
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
    url1 = url = 'http://checkcif.iucr.org'
    url = 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl'

    # r1 = requests.get(url1)
    # for i in r1.cookies:
    #    print(i, '##')

    r = requests.post(url, files=headers, timeout=150)
    print(r.text)
    Path(out_file).write_bytes(r.content)
    print('ready')


if __name__ == "__main__":
    get_checkcif()
    #app = QApplication(sys.argv)
    #web = WebPage()
    #web.show()
    #sys.exit(app.exec_())
