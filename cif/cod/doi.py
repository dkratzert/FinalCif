"""
#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

Needed for 'published' deposition:
_publ_author_name
_journal_name_full
_publ_section_title
_journal_year or _journal_volume
_journal_page_first or _journal_article_reference

Strings in the result are not delimited!
"""
from pprint import pprint
from typing import List, Dict

from crossref.restful import Works


def resolve_doi(doi: str) -> dict:
    works = Works()
    data = works.doi(doi)
    names: list = get_names_from_doi(data)
    journal = get_journal_name(data)
    paper_title = get_paper_title(data)
    year = get_publication_year(data)
    page = get_first_page(data)
    return {'_publ_author_name'  : names,
            '_journal_name_full' : journal,
            '_publ_section_title': paper_title,
            '_journal_year'      : year,
            '_journal_page_first': page,
            }


def get_first_page(data: Dict[str, str]) -> str:
    if not data or 'page' not in data:
        return ''
    return data['page'].split('-')[0]


def get_journal_name(data: Dict[str, List]) -> str:
    if not data or 'container-title' not in data:
        return ''
    if data['container-title']:
        return data['container-title'][0]
    return ''


def get_publication_year(data: Dict[str, Dict]) -> str:
    if not data or 'issued' not in data or 'date-parts' not in data['issued']:
        return ''
    return str(data['issued']['date-parts'][0][0])


def get_paper_title(data: Dict[str, List]) -> str:
    if not data or 'title' not in data:
        return ''
    return data['title'][0]


def get_names_from_doi(data: Dict[str, List]) -> List:
    authors = []
    if not data or not 'author' in data:
        return []
    for person in data['author']:
        name = '{}, {}'.format(person['family'] if 'family' in person else '',
                               person['given'] if 'given' in person else '')
        if 'sequence' in person and person['sequence'] == 'first' and name != ', ':
            authors.insert(0, name)
        elif name != ', ':
            authors.append(name)
    return authors


def _append_to_authors_list(authors, person, first=False):
    name = '{}, {}'.format(person['family'], person['given'])
    if first:
        authors.insert(0, name)
    else:
        authors.append(name)


if __name__ == '__main__':
    p = resolve_doi('10.1002/zaac.201400201')
    print('\n------')
    pprint(p)
