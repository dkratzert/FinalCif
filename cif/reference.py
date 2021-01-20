#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
from typing import List


class Author():

    def __init__(self, name: str, citation_id: int):
        self.name = name
        self.citation_id = citation_id


class Authors():
    """
    loop_
    _citation_author_citation_id
    _citation_author_name
      1  'Fitzgerald, P.M.D.'
      2  'McKeever, B.M.'
      3  'Van Middlesworth, J.F.'
    """

    def __init__(self):
        self._authors: List[Author] = []

    def add_author(self, name: str, citation_id: int):
        self._authors.append(Author(name=name, citation_id=citation_id))

    def get_authors_by_id(self, citation_id: int):
        results = []
        for author in self._authors:
            if author.citation_id == citation_id:
                results.append(author)
        return results


class Reference():
    _count = 0

    @classmethod
    def incr(self):
        self._count += 1
        return self._count

    def __init__(self):
        """
        loop_
        _citation.id
        _citation.coordinate_linkage
        _citation.title
        _citation.country
        _citation.journal_abbrev
        _citation.journal_volume
        _citation.journal_issue
        _citation.page_first
        _citation.page_last
        _citation.year
        _citation.journal_id_ASTM
        _citation.journal_id_ISSN
        _citation.journal_id_CSD
        _citation.book_title
        _citation.book_publisher
        _citation.book_id_ISBN
        _citation.details
        """
        self.citation_id = self.incr()

    def id(self):
        pass

    def coordinate_linkage(self):
        pass

    def title(self):
        pass

    def country(self):
        pass

    def journal_abbrev(self):
        pass

    def journal_volume(self):
        pass

    def journal_issue(self):
        pass

    def page_first(self):
        pass

    def page_last(self):
        pass

    def authors(self) -> Authors:
        pass
