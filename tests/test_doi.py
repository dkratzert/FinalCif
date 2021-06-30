from pprint import pprint
from unittest import TestCase

from cif.cod.doi import resolve_doi, get_names_from_doi

doi_data = {
    'author': [{'ORCID'              : 'http://orcid.org/0000-0003-0970-9780',
                'affiliation'        : [],
                'authenticated-orcid': True,
                'family'             : 'Kratzert',
                'given'              : 'Daniel',
                'sequence'           : 'first'},
               {'ORCID'              : 'http://orcid.org/0000-0002-7182-4387',
                'affiliation'        : [],
                'authenticated-orcid': True,
                'family'             : 'Krossing',
                'given'              : 'Ingo',
                'sequence'           : 'additional'}],
}


class TestDOI(TestCase):
    def setUp(self) -> None:
        self.doi = resolve_doi('10.1107/S1600576718004508')
        pprint(self.doi)

    def test_resolve_doi_doi(self):
        self.assertEqual('2018', self.doi['_journal_year'])

    def test_authors(self):
        self.assertEqual('Kratzert, Daniel', self.doi['_publ_author_name'][0])

    def test_get_names_from_doi(self):
        self.assertEqual(['Kratzert, Daniel', 'Krossing, Ingo'], get_names_from_doi(doi_data))


class TestDOIOld(TestCase):
    def test_resolve_doi_online(self):
        result = {'_journal_name_full' : 'Inorganic Chemistry',
                  '_publ_author_name'  : ['Le Bail, A.', 'Marcos, M. D.', 'Amoros, P.'],
                  '_journal_page_first': '2607',
                  '_publ_section_title': 'Ab Initio Crystal Structure Determination of '
                                         'VO(H2PO2)2.cntdot.H2O from X-ray and Neutron Powder '
                                         'Diffraction Data. A Monodimensional Vanadium(IV) '
                                         'Hypophosphite',
                  '_journal_year'      : '1994'}
        self.assertEqual(result, resolve_doi('http://doi.org/10.1021/ic00090a021'))

    def test_empty_url(self):
        result = {'_journal_name_full' : '',
                  '_journal_page_first': '',
                  '_journal_year'      : '',
                  '_publ_author_name'  : [],
                  '_publ_section_title': ''}
        self.assertEqual(result, resolve_doi(''))

    def test_invalid_url(self):
        result = {'_journal_name_full' : '',
                  '_journal_page_first': '',
                  '_journal_year'      : '',
                  '_publ_author_name'  : [],
                  '_publ_section_title': ''}
        self.assertEqual(result, resolve_doi('http://doi.org/10.1021/ic00090a02'))
