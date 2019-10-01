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
from pprint import pprint
from tempfile import mkstemp
from typing import List

import gemmi
import requests
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtNetwork import QNetworkReply
from requests.exceptions import MissingSchema

from tools.misc import strip_finalcif_of_name


class MakeCheckCif():

    def __init__(self, parent, cif: Path, outfile: Path):
        self.parent = parent
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
        if self.parent and self.parent.cif.block.find_value('_shelx_hkl_file'):
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
        if hkl == 'checkcif_only' and fd:
            try:
                # a trick to close the file descriptor:
                f = os.fdopen(fd, 'w')
                f.close()
                os.unlink(tmp)
            except ValueError:
                print('can not delete tempfile from checkcif:')
                print(tmp)
        print('ready')

    def _open_pdf_result(self):
        """
        Opens the resulkting pdf file in the systems pdf viewer.
        """
        parser = MyHTMLParser(self.html_out_file.read_text())
        # the link to the pdf file resides in this html file:
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
    def __init__(self, data):
        self.link = ''
        self.imageurl = ''
        super(MyHTMLParser, self).__init__()
        self.pdf = ''
        self.vrf = ''
        self.alert_levels = []
        self.feed(data)

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

    def handle_data(self, data: str):
        if 'Validation Reply Form' in data:
            self.vrf = data
        if data.startswith('PLAT') and len(data) == 17:
            self.alert_levels.append(data)

    def get_image(self):
        try:
            return requests.get(self.imageurl).content
        except MissingSchema:
            return b''

    @property
    def response_forms(self) -> List[dict]:
        """
        :returns
        [
        {'level'     : 'PLAT035_ALERT_1_B',
         'name'      : '_vrf_PLAT035_DK_zucker2_0m',
         'problem'   : '_chemical_absolute_configuration Info  Not Given     Please Do '
                       '!  ',
         'alert_num': 'PLAT035'},
         {...},
         ]
        """
        forms = []
        form = {}
        n = 0
        for line in self.vrf.split('\n'):
            if line.startswith('_vrf'):
                form = {'level': ''}
                plat = line.split('_')[2]
                form.update({'name': line, 'alert_num': plat})
            if line.startswith(';'):
                continue
            if line.startswith('PROBLEM'):
                problem = line[9:]
                form.update({'problem': problem})
                for x in self.alert_levels:
                    if form['alert_num'] == x[:7]:
                        form.update({'level': x})
                n += 1
                forms.append(form)
        return forms


class AlertHelp():
    def __init__(self, checkdef: list):
        self.checkdef = checkdef  # Path('../check.def').read_text().splitlines(keepends=False)

    def get_help(self, alert: str):
        if len(alert) > 4:
            alert = alert[4:]
        help = self._parse_checkdef(alert)
        if not help:
            return 'No help available.'
        return help

    def _parse_checkdef(self, alert):
        found = False
        helptext = []
        for line in self.checkdef:
            if line.startswith('_' + alert):
                found = True
                continue
            if found and line.startswith('#=='):
                return '\n'.join(helptext[2:])
            if found:
                helptext.append(line)


class AlertHelpRemote():
    def __init__(self, alert: str):
        self.netman = QNetworkAccessManager()
        self.helpurl = r'https://journals.iucr.org/services/cif/checking/' + alert + '.html'
        print('url:', self.helpurl)
        self.netman.finished.connect(self._parse_result)

    def get_help(self):
        url = QUrl(self.helpurl)
        req = QNetworkRequest(url)
        print('doing request')
        self.netman.get(req)

    def _parse_result(self, reply: QNetworkReply):
        if reply.error():
            print(reply.errorString())
        print('parsing reply')
        text = 'no help available'
        try:
            text = bytes(reply.readAll()).decode('ascii', 'ignore')
        except Exception as e:
            print(e)
            pass
        print(text)
        return text


if __name__ == "__main__":
    cif = Path('test-data/1000007-finalcif.cif')
    html = Path(r'./test-data/checkcif-DK_zucker2_0m-finalcif.html')
    # ckf = MakeCheckCif(None, cif, outfile=html)
    # ckf.show_html_report()
    # sys.exit()
    # ckf.show_pdf_report()
    # html = Path(r'D:\frames\guest\BreitPZ_R_122\BreitPZ_R_122\checkcif-BreitPZ_R_122_0m_a.html')

    parser = MyHTMLParser(html.read_text())
    # print(parser.imageurl)
    pprint(parser.response_forms)
    # print(parser.alert_levels)
    # print(parser.vrf)
    # print(parser.pdf)
    # print(parser.link)

    # a = AlertHelp()
    # a.get_help('PLAT115')
