"""
Check the input if the conditions for deposit are met.

Published:
    Should contain complete bibliographic information:
    authors' names,
    journal name,
    publication year,
    volume,
    issue,
    pages.
    a) MUST have bibliography:
        '_journal_name_full'
        '_publ_section_title'
        '_journal_year'
        '_journal_volume'
        '_journal_page_first'
        '_journal_article_reference'

Prepublication
    a) There MUST be an option "on-hold", which is valid until
       publication, but for period no longer than 1 year.
       After that period, if structure was not published,
       author is contacted (using e-mail provided, see [b]
       particle) to ask, what to do next;
    b) Quality checks must be more stringent; at least as good
       as in IUCr (i.e. PLATON). Checks are made using
       `cif_cod_check` as well;
    c) It SHOULD NOT contain bibliography entries;
    d) It MUST contain author's names, affiliations and e-mails.
       Later is being kept private and communication with author
       is made possible using web-form, which uses CAPTCHA.

Personal (private communication)
    a) Quality checks must be more stringent
    b) Bibliography MUST define the following:
       o) _journal_name_full    'Personal communications to COD'
       o) _journal_year         2010 # year part of deposition timestamp
       o) _journal_issue        06   # month part of deposition timestamp
       o) _cod_publication_date 2010-06-11   # year-month-day of deposition
       o) _publ_author_name     One or more author names
    c) It MUST contain name, affiliation and e-mail of at least
       one (here - depositing) author.
"""
from typing import List

from cif.cif_file_io import CifContainer


class DepositCheck():
    def __init__(self, cif: CifContainer):
        self.cif = cif

    @property
    def prepublication_needs(self):
        tocheck = ('_journal_name_full',
                   '_publ_section_title',
                   '_journal_year',
                   '_journal_volume',
                   '_journal_page_first',
                   #'_journal_article_reference'
                   )
        return tocheck

    def list_missing_for_prepublication(self) -> List[int]:
        """
        Lists the index numbers of missing items from prepublication_needs.
        """
        missing = []
        for num, item in enumerate(self.prepublication_needs):
            if item not in self.cif:
                missing.append(num)
        return missing

    def is_complete_for_prepublication(self):
        if not self.list_missing_for_prepublication():
            return True
        return False
