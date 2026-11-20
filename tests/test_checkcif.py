import os
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.parse import urljoin, urlsplit

import requests
from lxml.html import fromstring

from finalcif import VERSION
from finalcif.cif.checkcif.checkcif import REQUEST_HEADERS, CheckCif, MyHTMLParser, fix_iucr_urls
from finalcif.cif.cif_file_io import CifContainer

data = Path('tests')

form_choices = {'filecif'      : [],
                'runtype'      : [],
                'from_index'   : [],
                'referer'      : [],
                'outputtype'   : ['HTML', 'PDF', 'PDFEMAIL'],
                'Qemailaddress': [],
                'validtype'    : ['checkcif_with_hkl', 'iucr_checkcif_with_hkl', 'checkcif_only'],
                'valout'       : ['vrfa', 'vrfab', 'vrfabc', 'vrfno'],
                'UPLOAD'       : []
                }


class TestCheckCifInterface(TestCase):
    """Checks the submission form of the CheckCIF start page, which is fetched once for all tests."""
    response: requests.Response | None = None

    @classmethod
    def setUpClass(cls) -> None:
        if os.environ.get('NO_NETWORK'):
            raise unittest.SkipTest('No network available.')
        try:
            cls.response = requests.get('https://checkcif.iucr.org/', headers=REQUEST_HEADERS, timeout=5)
            cls.response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise unittest.SkipTest(f'CheckCIF start page is not available: {e}') from e

    def setUp(self) -> None:
        page = fromstring(self.response.text)
        self.form = page.forms[0]
        self.form_items = self._get_form_items()

    def _get_form_items(self):
        """
        Returns a dictionary where keys are html form keys and values are the choices for the checkcif form.
        """
        formdict = {}
        for key in self.form.fields.keys():
            if key is None:
                continue
            choices = []
            for t in self.form.inputs[key]:
                choice = t.values()[t.keys().index('value')]
                choices.append(choice)
            formdict[key] = choices
        return formdict

    def test_form_action_url(self):
        action = urlsplit(urljoin(self.response.url, self.form.action))
        self.assertEqual(('checkcif.iucr.org', '/cgi-bin/checkcif_hkl.pl'), (action.hostname, action.path))

    def test_form_choices_filecif(self):
        self.assertEqual([], self.form_items['filecif'])

    def test_form_choices_runtype(self):
        self.assertEqual([], self.form_items['runtype'])

    def test_form_choices_referer(self):
        self.assertEqual([], self.form_items['referer'])

    def test_form_choices_Qemailaddress(self):
        self.assertEqual([], self.form_items['Qemailaddress'])

    def test_form_choices_UPLOAD(self):
        self.assertEqual([], self.form_items['UPLOAD'])

    def test_form_choices_outputtype(self):
        self.assertEqual(['HTML', 'PDF', 'PDFEMAIL'], self.form_items['outputtype'])

    def test_form_choices_validtype(self):
        self.assertEqual(['checkcif_with_hkl', 'iucr_checkcif_with_hkl', 'checkcif_only'], self.form_items['validtype'])

    def test_form_choices_valout(self):
        self.assertEqual(['vrfa', 'vrfab', 'vrfabc', 'vrfno'], self.form_items['valout'])

    def test_form_field_keys(self):
        fields = self.form.fields.keys()
        fields.sort()
        self.assertEqual(
            ['Qemailaddress',
             'UPLOAD',
             'duplic',
             'filecif',
             'from_index',
             'outputtype',
             'referer',
             'runtype',
             'validtype',
             'valout'],
            fields
        )


class TestCheckCif(TestCase):
    def setUp(self) -> None:
        self.good_html = '''<link rel="stylesheet" type="text/css" href="https://journals.iucr.org/style/infoweb.css" />
        <img width=792 src="https://checkcif.iucr.org/foo/bar/baz.gif" />'''

    def test__fix_urls_without_spaces(self):
        html = '''<link rel="stylesheet" type="text/css" href="//journals.iucr.org/style/infoweb.css" />
        <img width=792 src="//checkcif.iucr.org/foo/bar/baz.gif" />'''
        self.assertEqual(self.good_html, fix_iucr_urls(html))

    def test__fix_urls_with_spaces(self):
        html = '''<link rel="stylesheet" type="text/css" href = "//journals.iucr.org/style/infoweb.css" />
        <img width=792 src = "//checkcif.iucr.org/foo/bar/baz.gif" />'''
        self.assertEqual(self.good_html, fix_iucr_urls(html))


def _response(status_code: int) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = b''
    return response


class TestCheckCifRequestErrors(TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.outfile = Path(self.tmpdir.name) / 'checkpdf.html'
        self.cif = CifContainer(data / 'examples/1979688.cif')
        self.failures: list[str] = []

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def _run_checkcif(self, **post_kwargs: object) -> MagicMock:
        ckf = CheckCif(parent=None, cif=self.cif, outfile=self.outfile, pdf=True,
                       url='https://checkcif.example/cgi-bin/checkcif_hkl.pl')
        ckf.failed.connect(self.failures.append)
        with patch('finalcif.cif.checkcif.checkcif.requests.post', **post_kwargs) as post:
            ckf.run()
        return post

    def test_rejected_request_is_reported(self):
        self._run_checkcif(return_value=_response(403))
        self.assertEqual(1, len(self.failures))
        self.assertFalse(self.outfile.exists())

    def test_unexpected_request_exception_is_reported(self):
        self._run_checkcif(side_effect=requests.exceptions.ChunkedEncodingError())
        self.assertEqual(1, len(self.failures))
        self.assertFalse(self.outfile.exists())

    def test_request_identifies_finalcif(self):
        post = self._run_checkcif(return_value=_response(403))
        user_agent = post.call_args.kwargs['headers']['User-Agent']
        self.assertTrue(user_agent.startswith(f'FinalCif/{VERSION} '), user_agent)


class TestMyHTMLParser(TestCase):
    def setUp(self) -> None:
        htmlfile = data / 'examples/work/checkcif-cu_BruecknerJK_153F40_0m-test2.html'
        self.parser = MyHTMLParser(fix_iucr_urls(htmlfile.read_text()))

    def test_pdf_link_not_there(self):
        # This html has no pdf link!
        self.assertEqual('', self.parser.pdf_link)

    def test_image_url(self):
        self.assertEqual(
            'https://checkcif.iucr.org/tpLFd4ecNpOHF/081921084958927101865/platon_cu_BruecknerJK_153F40_0mte.gif',
            self.parser.imageurl)

    def test_response_forms(self):
        from finalcif.cif.vrf_entry import VRFEntry
        entry = self.parser.response_forms[0]
        self.assertIsInstance(entry, VRFEntry)
        self.assertEqual('PLAT413', entry.alert_num)
        self.assertEqual('cu_BruecknerJK_153F40_0m', entry.data_name)
        self.assertEqual('PLAT413_ALERT_2_C', entry.level)
        self.assertEqual('_vrf_PLAT413_cu_BruecknerJK_153F40_0m', entry.key)
        self.assertEqual(
            'Short Inter XH3 .. XHn     H13      ..H19B     .       2.14 Ang.  ',
            entry.problem,
        )


class TestMyHTMLParserPDF(TestCase):
    def setUp(self) -> None:
        htmlfile = (data / 'examples/work/checkcif-cu_BruecknerJK_153F40_0m-pdf-test2.html').resolve().absolute()
        self.parser = MyHTMLParser(fix_iucr_urls(htmlfile.read_text()))

    def test_pdf_link_there(self):
        # This html has a pdf link
        self.assertEqual('https://checkcif.iucr.org/XGW8nDLA5N4Xd/081921091639544652566/checkcif.pdf',
                         self.parser.pdf_link)


class TestMyHTMLParserNew(unittest.TestCase):

    def test_parser_with_html(self):
        # Read the sample HTML content from file
        html_content = (data / r'checkcif_results/check_html_ab.html').read_text()
        parser = MyHTMLParser(html_content)

        self.assertEqual(parser.structure_factor_report,
                         "https://checkcif.iucr.org/4ocPADzJV04fN/092423121633543345593/ckf.html")
        self.assertEqual(parser.pdf_link, "")
        self.assertEqual(parser.imageurl,
                         "https://checkcif.iucr.org/4ocPADzJV04fN/092423121633543345593/platon_cu_BruecknerJK_153F40_0mte.gif")

    def test_parser_with_html_pdf(self):
        # Read the sample HTML PDF content from file
        html_pdf_content = (data / r'checkcif_results/check_pdf_ab.html').read_text()

        parser = MyHTMLParser(html_pdf_content)

        self.assertEqual(parser.structure_factor_report,
                         "https://checkcif.iucr.org/A2pZY9P2WqtE7/092423121840336981715/ckf.html")
        self.assertEqual(parser.pdf_link, "https://checkcif.iucr.org/A2pZY9P2WqtE7/092423121840336981715/checkcif.pdf")
        self.assertEqual(parser.imageurl, "")


if __name__ == '__main__':
    unittest.main()
