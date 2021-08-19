import unittest
from pathlib import Path
from unittest import TestCase

from tools.checkcif import CheckCif, MyHTMLParser, fix_iucr_urls


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
        htmlfile = Path('tests/examples/work/checkcif-cu_BruecknerJK_153F40_0m-test2.html')
        self.parser = MyHTMLParser(fix_iucr_urls(htmlfile.read_text()))

    def test_pdf_link_not_there(self):
        # This html has no pdf link!
        self.assertEqual('', self.parser.pdf_link)

    def test_image_url(self):
        self.assertEqual('https://checkcif.iucr.org/tpLFd4ecNpOHF/081921084958927101865/platon_cu_BruecknerJK_153F40_0mte.gif', self.parser.imageurl)

    def test_response_forms(self):
        form = {'alert_num': 'PLAT413',
                'level': 'PLAT413_ALERT_2_C',
                'name': '_vrf_PLAT413_cu_BruecknerJK_153F40_0m',
                'problem': 'Short Inter XH3 .. XHn     H13      ..H19B     .       2.14 '
                           'Ang.  '}
        self.assertEqual(form, self.parser.response_forms[0])


class TestMyHTMLParserPDF(TestCase):
    def setUp(self) -> None:
        htmlfile = Path('tests/examples/work/checkcif-cu_BruecknerJK_153F40_0m-pdf-test2.html')
        self.parser = MyHTMLParser(fix_iucr_urls(htmlfile.read_text()))

    def test_pdf_link_there(self):
        # This html has a pdf link
        self.assertEqual('https://checkcif.iucr.org/XGW8nDLA5N4Xd/081921091639544652566/checkcif.pdf', self.parser.pdf_link)