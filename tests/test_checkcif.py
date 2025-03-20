import os
import ssl
import unittest
from pathlib import Path
from unittest import TestCase

import requests
from lxml.html import fromstring

from finalcif.cif.checkcif.checkcif import MyHTMLParser, fix_iucr_urls

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

if os.environ.get('NO_NETWORK'):
    print('Skipping network based tests.')
    url = ''
    request = None
else:
    # Do not do this request for each test:
    try:
        request = requests.get('https://checkcif.iucr.org/', timeout=5)
    except (ssl.SSLError, requests.exceptions.SSLError):
        request = requests.get('http://checkcif.iucr.org/', timeout=5)
    except Exception:
        request = None


@unittest.skipIf(not request, 'Skip without network')
class TestCheckCifInterface(TestCase):
    def setUp(self) -> None:
        os.environ["RUNNING_TEST"] = 'True'
        if os.environ.get('NO_NETWORK'):
            self.skipTest('No network available.')
        page = fromstring(request.text)
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
        self.assertEqual('//checkcif.iucr.org/cgi-bin/checkcif_hkl.pl', self.form.action)

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
            ['Qemailaddress', 'UPLOAD', 'filecif', 'from_index', 'outputtype', 'referer', 'runtype', 'validtype', 'valout'],
            fields
        )


@unittest.skip('not necessary')
class TestCheckCIfServerURL(TestCase):
    def test_url(self):
        if os.environ.get('NO_NETWORK'):
            self.skipTest('No network available.')
        url = 'https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl'
        req = requests.post(url, files={'file': None}, data={"runtype": "symmonly",
                                                             "referer": "checkcif_server"}, timeout=1)
        self.assertEqual(200, req.status_code)


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
        form = {'alert_num': 'PLAT413',
                'data_name': 'cu_BruecknerJK_153F40_0m',
                'level'    : 'PLAT413_ALERT_2_C',
                'name'     : '_vrf_PLAT413_cu_BruecknerJK_153F40_0m',
                'problem'  : 'Short Inter XH3 .. XHn     H13      ..H19B     .       2.14 '
                             'Ang.  '}
        self.assertEqual(form, self.parser.response_forms[0])


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
