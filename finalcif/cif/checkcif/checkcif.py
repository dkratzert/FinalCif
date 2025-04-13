#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import re
import subprocess
import sys
import time
from contextlib import suppress
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional, Dict

import requests
from PySide6.QtCore import QThread, Signal
from requests.exceptions import MissingSchema

from finalcif.cif.cif_file_io import CifContainer


class CheckCif(QThread):
    progress = Signal(str)
    failed = Signal(str)

    def __init__(self, parent, cif: CifContainer, outfile: Path, hkl_upload: bool = True,
                 pdf: bool = False, url: str = '', full_iucr: bool = False):
        # hkl == False means no hkl upload
        super().__init__(parent=parent)
        self.hkl_upload = hkl_upload
        self.html_out_file = outfile
        self.cif = cif
        self.pdf = pdf
        self.checkcif_url = url
        self.full_iucr = full_iucr

    def _html_check(self):
        if self.hkl_upload:
            self.progress.emit('Running Checkcif with hkl data')
        else:
            self.progress.emit('Running Checkcif with no hkl data')

    def get_vrf(self):
        if self.pdf:
            return 'vrfno'
        else:
            # Currently, the vrfabc option misses some validation response forms. Only vrfab gives correct results.
            return 'vrfabc'

    def run(self) -> None:
        """
        Requests a checkcif run from IUCr servers.
        """
        self._html_check()
        temp_cif = bytes(self.cif.cif_as_string(), encoding='ascii')
        validation_type = 'checkcif_only'
        if not self.hkl_upload:
            temp_cif = bytes(self.cif.cif_as_string(without_hkl=True), encoding='ascii')
        elif len(self.cif.hkl_file) > 0 and self.hkl_upload and self.full_iucr:
            validation_type = 'iucr_checkcif_with_hkl'
        elif len(self.cif.hkl_file) > 0:
            validation_type = 'checkcif_with_hkl'
        vrf = self.get_vrf()
        headers = {
            "runtype"   : "symmonly",
            "referer"   : "checkcif_server",
            "outputtype": 'PDF' if self.pdf else 'HTML',
            "validtype" : validation_type,
            "valout"    : vrf,
        }
        t1 = time.perf_counter()
        self.progress.emit('Report request sent. Please wait...')
        req = self._do_the_server_request(headers, temp_cif)
        if req:
            self.progress.emit('request finished')
            if req.status_code != 200:
                self.failed.emit('Request failed with code: {}'.format(str(req.status_code)))
            else:
                t2 = time.perf_counter()
                time.sleep(0.1)
                self.progress.emit('Report took {}s.'.format(str(round(t2 - t1, 2))))
                try:
                    self.html_out_file.write_bytes(fix_iucr_urls(req.content.decode()).encode())
                except PermissionError:
                    print('html checkcif result could not be written.')
                    return
        with suppress(Exception):
            # parameter missing_ok=True is only available after 3.8
            Path('finalcif_checkcif_tmp.cif').unlink()

    def _do_the_server_request(self, headers: dict, temp_cif: bytes):
        req = None
        try:
            req = requests.post(self.checkcif_url, files={'file': temp_cif}, data=headers, timeout=900)
        except requests.exceptions.ReadTimeout:
            message = r"Checkcif server took too long. Try it at 'https://checkcif.iucr.org' directly."
            self.failed.emit(message)
        except requests.exceptions.MissingSchema:
            message = "URL for checkcif missing in options."
            self.failed.emit(message)
        except requests.exceptions.ConnectionError:
            message = "The checkcif server is not reachable. Is your network connection working?<br>" \
                      "The server URL might also have changed..."
            self.failed.emit(message)
        return req

    def _open_pdf_result(self) -> None:
        """
        Opens the resulkting pdf file in the systems pdf viewer.
        """
        try:
            parser = MyHTMLParser(self.html_out_file.read_text())
        except FileNotFoundError:
            self.failed.emit('Could not find checkcif result...')
            pdf = None
            return
        # the link to the pdf file resides in this html file:
        try:
            pdf = parser.get_pdf()
        except MissingSchema:
            self.failed.emit('PDF link is not valid anymore...')
            pdf = None
        if pdf:
            pdfobj = self.cif.finalcif_file_prefixed(prefix='checkcif-', suffix='-finalcif.pdf')
            try:
                pdfobj.write_bytes(pdf)
            except PermissionError:
                # Most probably because of an already opened report.
                return
            if sys.platform == 'win' or sys.platform == 'win32':
                subprocess.Popen([str(pdfobj.absolute())], shell=True)
            if sys.platform == 'darwin':
                subprocess.call(['open', str(pdfobj.absolute())])

    def show_pdf_report(self) -> None:
        self._open_pdf_result()


def fix_iucr_urls(content: str):
    """
    The IuCr checkcif page suddenly contains urls where the protocol is missing.
    """
    href = re.sub(r'\s+href\s*=\s*"//', ' href="https://', content)
    return re.sub(r'\s+src\s*=\s*"//', ' src="https://', href)


class MyHTMLParser(HTMLParser):
    def __init__(self, data):
        self.pdf_link = ''
        self.structure_factor_report = ''
        self.imageurl = ''
        super(MyHTMLParser, self).__init__()
        self.vrf = ''
        self.alert_levels = []
        self.feed(data)

    def get_pdf(self) -> Optional[bytes]:
        return requests.get(self.pdf_link, timeout=10).content

    def handle_starttag(self, tag: str, attrs: str) -> None:
        # if tag and tag not in ('font', 'div', 'link', 'meta', 'html', 'table', 'td') and attrs:
        #    # For debug:
        #    print(f'tag: {tag}, attrs: {attrs}')
        if tag == "a" and len(attrs) > 1 and attrs[1][0] == 'href' and attrs[1][1].endswith('.pdf'):
            self.pdf_link = attrs[1][1]
        if tag == "a" and len(attrs) > 1 and attrs[0][0] == 'href' and attrs[0][1].endswith('ckf.html'):
            self.structure_factor_report = attrs[0][1]
        if tag == "img" and len(attrs) > 1 and attrs[0][0] == 'width' and attrs[1][1].endswith('.gif'):
            url = attrs[1][1]
            self.imageurl = url

    def handle_data(self, data: str) -> None:
        if 'Validation Reply Form' in data:
            self.vrf = data
        if data.startswith('PLAT') and len(data) == 17:
            self.alert_levels.append(data)

    def save_image(self, image_file: Path) -> None:
        try:
            image = requests.get(self.imageurl, timeout=10).content
        except MissingSchema:
            print('debug: Got no image from checkcif server.')
            image = b''
        if image:
            image_file.write_bytes(image)

    def get_ckf(self) -> str:
        try:
            return requests.get(self.structure_factor_report, timeout=10).content.decode('latin1', 'ignore')
        except MissingSchema:
            return ''

    @property
    def response_forms(self) -> List[Dict[str, str]]:
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
        single_form = {}
        for line in self.vrf.split('\n'):
            if line.startswith('_vrf'):
                single_form = {'level': ''}
                plat = line.split('_')[2]
                data = line.split('_', 3)[3]
                single_form.update({'name': line, 'alert_num': plat, 'data_name': data})
            if line.startswith(';'):
                continue
            if line.startswith('PROBLEM'):
                problem = line[9:]
                single_form.update({'problem': problem})
                for x in self.alert_levels:
                    if single_form['alert_num'] == x[:7]:
                        single_form.update({'level': x})
                        break
                forms.append(single_form)
        return forms


class AlertHelp():
    def __init__(self, checkdef: list):
        self.checkdef = checkdef  # Path('../check.def').read_text().splitlines(keepends=False)

    def get_help(self, alert: str) -> str:
        checkdef_help = self._parse_checkdef(alert)
        if not checkdef_help or 'PLAT' not in alert:
            return 'No help available.'
        return checkdef_help

    def _parse_checkdef(self, alert: str) -> str:
        """
        Parses check.def from PLATON in order to get help about an Alert from Checkcif.

        :param alert: alert number of the respective checkcif alert as three digit string or 'PLAT' + three digits
        """
        found = False
        helptext = []
        if len(alert) > 4:
            alert = alert[4:]
        for line in self.checkdef:
            if line.startswith('_' + alert):
                found = True
                continue
            if found and line.startswith('#==='):
                return '\n'.join(helptext[2:])
            if found:
                helptext.append(line)
        return ''


if __name__ == "__main__":
    html = Path(r'tests/checkcif_results/check_html_ab.html')
    html_pdf = Path(r'tests/checkcif_results/check_pdf_ab.html')
    parser = MyHTMLParser(html.read_text())
    print('html report link:', parser.structure_factor_report)
    print('pdf link:', parser.pdf_link)
    print('image url:', parser.imageurl)
    print('###')
    parser = MyHTMLParser(html_pdf.read_text())
    print('html report link:', parser.structure_factor_report)
    print('pdf link:', parser.pdf_link)
    print('image url:', parser.imageurl)

    # pprint(parser.response_forms)
    # print(parser.alert_levels)
    # print(parser.vrf)
    # print(parser.pdf)
    # print(parser.link)

    # a = AlertHelp()
    # a.get_help('PLAT115')
