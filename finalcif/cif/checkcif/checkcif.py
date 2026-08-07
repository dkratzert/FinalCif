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

import requests
from qtpy.QtCore import QThread, Signal
from requests import Response
from requests.exceptions import MissingSchema

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.vrf_entry import VRFEntry
from finalcif.gui.dialogs import show_general_warning

import os
import requests
from html.parser import HTMLParser
from urllib.parse import urljoin


# ============================================================================
# 1. PARSER-KLASSE (Nativer Python HTML-Parser, keine externen Abhängigkeiten)
# ============================================================================

class CheckCifFormParser(HTMLParser):
    """
    Ein minimalistischer Parser, der aus dem IUCr-HTML das Formular
    für den FCF-Upload extrahiert.
    """

    def __init__(self):
        super().__init__()
        self.action = None
        self.hidden_data = {}
        self.submit_data = {}
        self.file_input_name = None
        self.in_target_form = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Formular-Tag erkennen und Action-URL (Zieladresse) speichern
        if tag == 'form':
            self.in_target_form = True
            self.action = attrs_dict.get('action')

        # Inputs innerhalb des Formulars sammeln
        elif tag == 'input' and self.in_target_form:
            inp_type = attrs_dict.get('type', '').lower()
            name = attrs_dict.get('name')
            value = attrs_dict.get('value', '')

            if not name:
                return

            if inp_type == 'hidden':
                self.hidden_data[name] = value
            elif inp_type == 'submit':
                self.submit_data[name] = value
            elif inp_type == 'file':
                self.file_input_name = name

    def handle_endtag(self, tag):
        if tag == 'form':
            self.in_target_form = False


# ============================================================================
# 2. HILFSFUNKTION FÜR DEN FCF UPLOAD
# ============================================================================

def handle_fcf_upload_form(response_html: str, fcf_file_path: str, original_url: str) -> str:
    """
    Prüft, ob der IUCr-Server das FCF-Upload-Formular (Zwischenseite) zurückgegeben hat.
    Wenn ja, wird das Formular geparst und die .fcf Datei automatisch nachgereicht.
    Gibt den finalen HTML-Report (oder den ursprünglichen bei Fehlern) zurück.
    """
    # Prüfen, ob der spezifische Text der Zwischenseite in der Antwort steht
    if "File name of structure factor file" not in response_html:
        return response_html  # Alles normal, gib den originalen Report zurück

    print("Info: IUCr Server verlangt expliziten FCF Upload. Formular wird verarbeitet...")

    if not os.path.exists(fcf_file_path):
        print(f"Warnung: .fcf Datei nicht gefunden unter {fcf_file_path}. Report wird ohne FCF generiert.")
        return response_html

    # Formular mit dem eingebauten HTMLParser analysieren
    parser = CheckCifFormParser()
    parser.feed(response_html)

    # Prüfen, ob das Datei-Feld erfolgreich gefunden wurde
    if not parser.file_input_name:
        print("Fehler: Konnte das Datei-Upload-Feld im IUCr-Formular nicht finden.")
        return response_html

    # Action-URL und Parameter für den POST-Request zusammenbauen
    submit_url = urljoin(original_url, parser.action) if parser.action else original_url

    # Versteckte Felder (Session-IDs, Run-Hashes) und den Submit-Button in die Payload packen
    data = parser.hidden_data.copy()
    data.update(parser.submit_data)

    # Zweiten Request mit der FCF-Datei absenden
    try:
        with open(fcf_file_path, 'rb') as f:
            files = {
                parser.file_input_name: (os.path.basename(fcf_file_path), f, 'application/octet-stream')
            }
            print(f"Sende {os.path.basename(fcf_file_path)} an {submit_url} ...")

            # Request senden
            new_response = requests.post(submit_url, data=data, files=files, timeout=180)
            new_response.raise_for_status()

            print("Erfolg: FCF-Upload abgeschlossen, finaler Report empfangen.")
            return new_response.text

    except Exception as e:
        print(f"Fehler beim automatischen Senden der FCF-Datei: {e}")
        return response_html


# ============================================================================
# 3. HAUPTFUNKTION (Integration in die FinalCif CheckCIF Routine)
# ============================================================================

def send_checkcif_request(cif_file_path: str, url: str = "https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl") -> str:
    """
    Sendet die CIF-Datei an den Server und fängt automatisch die FCF-Rückfrage ab.
    Diese Methode ersetzt die bisherige Request-Logik in checkcif.py.
    """
    # Pfad zur FCF Datei ableiten (.cif Endung zu .fcf ändern)
    fcf_file_path = cif_file_path.rsplit('.', 1)[0] + '.fcf'

    # Standard-Parameter für FinalCif (müssen ggf. an deine genaue Config angepasst werden)
    data = {
        'runtype'    : 'full',
        'send_binary': '1',
        # Weitere Parameter (wie 'UPLOAD_FORMAT') hier hinzufügen, falls FinalCif sie nutzt
    }

    try:
        # 1. Ursprünglicher Request mit der .cif Datei
        with open(cif_file_path, 'rb') as cif_file:
            files = {
                'file': (os.path.basename(cif_file_path), cif_file, 'text/plain')
            }
            print(f"Sende initiale CIF-Datei an {url} ...")
            response = requests.post(url, data=data, files=files, timeout=180)
            response.raise_for_status()

            html_content = response.text

        # 2. Formular-Check (Das ist der neue, entscheidende Schritt)
        # Wenn der IUCr-Server nach der FCF-Datei fragt, greift diese Funktion ein.
        final_html_content = handle_fcf_upload_form(
            response_html=html_content,
            fcf_file_path=fcf_file_path,
            original_url=url
        )

        return final_html_content

    except requests.exceptions.RequestException as e:
        error_msg = f"<html><body><h3>Netzwerkfehler beim CheckCIF-Request:</h3><p>{e}</p></body></html>"
        print(error_msg)
        return error_msg

class CheckCif(QThread):
    progress = Signal(str)
    failed = Signal(str)

    def __init__(self, parent, cif: CifContainer, outfile: Path, hkl_upload: bool = True,
                 pdf: bool = False, url: str = '', full_iucr: bool = False, check_duplicates: bool = True):
        # hkl == False means no hkl upload
        super().__init__(parent=parent)
        self.hkl_upload = hkl_upload
        self.html_out_file = outfile
        self.cif = cif
        self.pdf = pdf
        self.checkcif_url = url
        self.full_iucr = full_iucr
        self.check_duplicates = check_duplicates

    def _html_check(self) -> None:
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
            "from_index": "from_index",
            "runtype"   : "symmonly",
            "referer"   : "checkcif_server",
            "outputtype": 'PDF' if self.pdf else 'HTML',
            "validtype" : validation_type,
            "valout"    : vrf,
            "duplic"    : "duplicyes" if self.check_duplicates else "duplicno",
        }
        t1 = time.perf_counter()
        self.progress.emit('Report request sent. Please wait...')
        req = self._do_the_server_request(headers, temp_cif)
        if req:
            self.progress.emit('request finished')
            if req.status_code != 200:
                self.failed.emit(f'Request failed with code: {req.status_code!s}')
            else:
                t2 = time.perf_counter()
                time.sleep(0.1)
                self.progress.emit(f'Report took {round(t2 - t1, 2)!s}s.')
                try:
                    self.html_out_file.write_bytes(fix_iucr_urls(req.content.decode()).encode())
                except PermissionError:
                    print('html checkcif result could not be written.')
                    return
        with suppress(Exception):
            # parameter missing_ok=True is only available after 3.8
            Path('finalcif_checkcif_tmp.cif').unlink()
        if self.pdf:
            self.finished.connect(self._open_pdf_result)

    def _do_the_server_request(self, headers: dict, temp_cif: bytes) -> Response | None:
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
                show_general_warning(self, f'The document {pdfobj.name} could not be opened to '
                                           f'write the report.\nIs the file already opened?')
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
        super().__init__()
        self.vrf = ''
        self.alert_levels = []
        self.feed(data)

    def get_pdf(self) -> bytes | None:
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
    def response_forms(self) -> list[VRFEntry]:
        """
        :returns a list of VRFEntry instances, one per alert with a validation response form.
        """
        entries = []
        current_key = ''
        current_plat = ''
        current_data = ''
        current_level = ''
        for line in self.vrf.split('\n'):
            if line.startswith('_vrf'):
                parts = line.split('_')
                current_key = line
                current_plat = parts[2] if len(parts) > 2 else ''
                current_data = line.split('_', 3)[3] if len(parts) > 3 else ''
                current_level = ''
            if line.startswith(';'):
                continue
            if line.startswith('PROBLEM'):
                problem = line[9:]
                for x in self.alert_levels:
                    if current_plat == x[:7]:
                        current_level = x
                        break
                entries.append(VRFEntry(
                    key=current_key,
                    data_name=current_data,
                    problem=problem,
                    response='?',
                    alert_num=current_plat,
                    level=current_level,
                ))
        return entries


class AlertHelp:
    def __init__(self, checkdef: list):
        self.checkdef = checkdef  # Path('../check.def').read_text().splitlines(keepends=False)

    def get_help(self, alert: str) -> str:
        checkdef_help = self._parse_checkdef(alert)
        if not checkdef_help or 'PLAT' not in alert:
            return ''
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
