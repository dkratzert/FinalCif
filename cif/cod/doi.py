"""
Needed for 'published' deposition:
_publ_author_name
_journal_name_full
_publ_section_title
_journal_year or _journal_volume
_journal_page_first or _journal_article_reference
"""
from pprint import pprint
from typing import List, Dict

from crossref.restful import Works

from cif.text import delimit_string


def resolve_doi(doi: str) -> dict:
    works = Works()
    data = works.doi(doi)
    names = get_names_from_doi(data)
    journal = get_journal_name(data)
    paper_title = get_paper_title(data)
    year = get_publication_year(data)
    page = get_first_page(data)
    return {'names'      : names,
            'journal'    : journal,
            'paper_title': paper_title,
            'year'       : year,
            'page'       : page,
            }


def get_first_page(data: Dict[str, 'str']) -> str:
    if not 'page' in data:
        return ''
    return data['page'].split('-')[0]


def get_journal_name(data: Dict[str, List]) -> str:
    if not 'container-title' in data:
        return ''
    return data['container-title'][0]


def get_publication_year(data: Dict[str, Dict]) -> str:
    if not 'issued' in data:
        return ''
    return data['issued']['date-parts'][0][0]


def get_paper_title(data: Dict[str, List]) -> str:
    if not 'title' in data:
        return ''
    return data['title'][0]


def get_names_from_doi(data: Dict[str, List]):
    authors = []
    if not 'author' in data:
        return ''
    for person in data['author']:
        name = '{}, {}'.format(delimit_string(person['family']), delimit_string(person['given']))
        if 'sequence' in person and person['sequence'] == 'first':
            authors.insert(0, name)
        else:
            authors.append(name)
    return authors


def append_to_authors_list(authors, person, first=False):
    name = '{}, {}'.format(delimit_string(person['family']), delimit_string(person['given']))
    if first:
        authors.insert(0, name)
    else:
        authors.append(name)


if __name__ == '__main__':
    p = resolve_doi('http://doi.org/10.1021/ic00090a021')
    print('\n------')
    pprint(p)
