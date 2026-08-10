#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from __future__ import annotations

import re
import subprocess
import sys
import time
from collections.abc import Callable
from contextlib import suppress
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import requests
from qtpy.QtCore import QThread, Signal
from requests import Response
from requests.exceptions import MissingSchema

from finalcif.cif.cif_file_io import CifContainer
from finalcif.cif.vrf_entry import VRFEntry
from finalcif.gui.dialogs import show_general_warning
from finalcif.tools.misc import strip_finalcif_of_name

#: Text of the intermediate CheckCIF page that asks for an explicit upload of the
#: structure factor file.
STRUCTURE_FACTOR_REQUEST_TEXT = 'File name of structure factor file'
#: Name of the submit button of the form that continues without structure factors.
SUBMIT_WITHOUT_HKL_NAME = 'Qsubmitnow'
#: Maximum difference in seconds between the modification time of a CIF file and a
#: structure factor file in order to regard them as belonging together.
MAX_FCF_TIME_DIFFERENCE = 3600.0


class HtmlForm:
    """A single HTML form of the CheckCIF intermediate page."""

    def __init__(self, action: str = '') -> None:
        self.action = action
        self.hidden_data: dict[str, str] = {}
        self.submit_data: dict[str, str] = {}
        self.file_input_name: str = ''

    @property
    def payload(self) -> dict[str, str]:
        return {**self.hidden_data, **self.submit_data}

    def url(self, base_url: str) -> str:
        return urljoin(base_url, self.action) if self.action else base_url


class CheckCifFormParser(HTMLParser):
    """
    Extracts the forms of the CheckCIF page that asks for a structure factor upload.
    """

    def __init__(self, html: str = '') -> None:
        super().__init__()
        self.forms: list[HtmlForm] = []
        self._current_form: HtmlForm | None = None
        if html:
            self.feed(html)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {key: value or '' for key, value in attrs}
        if tag == 'form':
            self._current_form = HtmlForm(action=attrs_dict.get('action', ''))
            self.forms.append(self._current_form)
        elif tag == 'input' and self._current_form is not None:
            self._add_input(attrs_dict)

    def _add_input(self, attrs_dict: dict[str, str]) -> None:
        name = attrs_dict.get('name')
        if not name or self._current_form is None:
            return
        input_type = attrs_dict.get('type', '').lower()
        value = attrs_dict.get('value', '')
        if input_type == 'hidden':
            self._current_form.hidden_data[name] = value
        elif input_type == 'submit':
            self._current_form.submit_data[name] = value
        elif input_type == 'file':
            self._current_form.file_input_name = name

    def handle_endtag(self, tag: str) -> None:
        if tag == 'form':
            self._current_form = None

    @property
    def fcf_upload_form(self) -> HtmlForm | None:
        """The form with a file input field for the structure factor file."""
        for form in self.forms:
            if form.file_input_name:
                return form
        return None

    @property
    def no_structure_factors_form(self) -> HtmlForm | None:
        """The form that continues the check without the remaining structure factors."""
        for form in self.forms:
            if SUBMIT_WITHOUT_HKL_NAME in form.submit_data:
                return form
        for form in self.forms:
            if not form.file_input_name:
                return form
        return None


def needs_structure_factor_upload(html: str) -> bool:
    """Whether the CheckCIF server answered with the structure factor upload form."""
    return STRUCTURE_FACTOR_REQUEST_TEXT in html


def _fcf_candidates(cif_file: Path) -> list[Path]:
    """Possible structure factor files belonging to *cif_file*, without duplicates."""
    stem_without_finalcif = Path(strip_finalcif_of_name(cif_file.stem, till_name_ends=True)).name
    names = [f'{cif_file.stem}.fcf', f'{stem_without_finalcif}.fcf']
    candidates = []
    for name in names:
        candidate = cif_file.parent / name
        if candidate.exists() and candidate not in candidates:
            candidates.append(candidate)
    return candidates


def _reference_cif_file(cif_file: Path) -> Path:
    """
    The CIF file the structure factors should be compared against. This is the file
    without the '-finalcif' suffix, because that is the file the current CIF was made from.
    """
    stem_without_finalcif = Path(strip_finalcif_of_name(cif_file.stem, till_name_ends=True)).name
    source_cif = cif_file.parent / f'{stem_without_finalcif}.cif'
    return source_cif if source_cif.exists() else cif_file


def find_matching_fcf_file(cif_file: Path,
                           max_time_difference: float = MAX_FCF_TIME_DIFFERENCE) -> Path | None:
    """
    Returns the structure factor file that was created together with *cif_file*.

    Files named like the CIF with and without the '-finalcif' suffix are considered.
    A file is only accepted if its modification time differs by less than
    *max_time_difference* seconds from the modification time of the CIF file the
    current CIF was made from.
    """
    reference_file = _reference_cif_file(cif_file)
    with suppress(OSError):
        reference_time = reference_file.stat().st_mtime
        matches = []
        for candidate in _fcf_candidates(cif_file):
            difference = abs(candidate.stat().st_mtime - reference_time)
            if difference < max_time_difference:
                matches.append((difference, candidate))
        if matches:
            return min(matches)[1]
    return None


def _post_form(form: HtmlForm, base_url: str, files: dict | None = None) -> str:
    response = requests.post(form.url(base_url), data=form.payload, files=files, timeout=900)
    response.raise_for_status()
    return response.text


def upload_structure_factors(response_html: str, fcf_file: Path, url: str,
                             progress: Callable[[str], None] = print) -> str:
    """
    Answers the structure factor upload form of CheckCIF with *fcf_file*.

    Returns the final report or the unchanged *response_html* if the upload failed.
    """
    form = CheckCifFormParser(response_html).fcf_upload_form
    if form is None:
        progress('Could not find the structure factor upload form of CheckCIF.')
        return response_html
    if not fcf_file.exists():
        progress(f'Structure factor file {fcf_file.name} not found.')
        return response_html
    try:
        with fcf_file.open('rb') as file_handle:
            files = {form.file_input_name: (fcf_file.name, file_handle, 'application/octet-stream')}
            progress(f'Uploading structure factors from {fcf_file.name} ...')
            html = _post_form(form, url, files=files)
        progress('Structure factor upload finished.')
        return html
    except (OSError, requests.exceptions.RequestException) as e:
        progress(f'Structure factor upload failed: {e}')
        return response_html


def submit_without_structure_factors(response_html: str, url: str,
                                     progress: Callable[[str], None] = print) -> str:
    """
    Continues a CheckCIF run without the remaining structure factors.
    """
    form = CheckCifFormParser(response_html).no_structure_factors_form
    if form is None:
        progress('Could not find the CheckCIF form to continue without structure factors.')
        return response_html
    try:
        progress('Requesting the report without the remaining structure factors ...')
        return _post_form(form, url)
    except requests.exceptions.RequestException as e:
        progress(f'Request without structure factors failed: {e}')
        return response_html


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
            Path('finalcif_checkcif_tmp.cif').unlink(missing_ok=True)

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
