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
    d) It MUST contain
    author's names,
    affiliations, e-mails
    _publ_section_title
       Later is being kept private and communication with author
       is made possible using web-form, which uses CAPTCHA.

Personal (private communication)
    a) Quality checks must be more stringent
    b) Bibliography MUST define the following:
       o) _publ_author_name     One or more author names
    c) It MUST contain name, affiliation and e-mail of at least
       one (here - depositing) author.

"""

"""
'author_name' field is required to match at least one of the authors in '_publ_author_name' CIF loop 
                for 'prepublication' and 'personal' communication depositions.
'author_email' field will not be recorded in CIF, but instead it will go to the private COD database
                in order for us to contact the author if needed.
'journal' field will be recorded in '_journal_name_full' CIF data item
                for prepublication descriptions; it is not required to match anything.

Most common deposition errors:

1. Missing bibliography. Published and prepublication structures need
full bibliography, and personal communications should at least have
title and author.

2. Author name mismatch for prepublication and personal communication
structures. As said, 'author_name' API field must match at least one of
the authors in '_publ_author_name' CIF loop.

3. Missing atomic displacement parameters (ADPs) for structures
published after 1969. This is mandatory quality criterion in the COD.
ADPs have to be expressed in any form mandated by the core CIF dictionary.

4. Missing or unparsable '_chemical_formula_sum'. It must be a
space-separated list of atom types and their counts, like 'C18 H19 N7 O8 S'.

5. Missing or non-integer '_cell_formula_units_Z'.
"""

from typing import List, Tuple

from finalcif.cif.cif_file_io import CifContainer


class DepositCheck():
    def __init__(self, cif: CifContainer):
        self.cif = cif

    @property
    def personal_needs(self):
        tocheck = ('_journal_name_full',
                   '_publ_section_title',
                   '_publ_author_name',
                   '_publ_author_email',
                   )
        return tocheck

    @property
    def prepublication_needs(self):
        tocheck = ('_journal_name_full',
                   '_publ_section_title',
                   '_publ_author_name',
                   )
        return tocheck

    @property
    def published_needs(self):
        tocheck = ('_journal_name_full',
                   '_publ_section_title',
                   '_journal_year',
                   '_journal_volume',
                   '_journal_page_first',
                   '_publ_section_title'
                   )
        return tocheck

    def list_missing_for_deposit(self, needs: Tuple) -> List[int]:
        """
        Lists the index numbers of missing items from prepublication_needs.
        """
        missing = []
        for item in needs:
            if not any(self.needed_keywords_list(item)):
                missing.append(item)
        return missing

    def needed_keywords_list(self, item):
        return [item in self.cif, hasattr(self.cif.get_loop(item), 'values')]

    def is_complete_for_prepublication(self, needs: Tuple):
        if not self.list_missing_for_deposit(needs):
            return True
        return False


if __name__ == '__main__':
    d = DepositCheck(CifContainer('tests/examples/1979688-finalcif.cif'))
    print(d.list_missing_for_deposit(d.prepublication_needs))
    print(d.list_missing_for_deposit(d.published_needs))
    print(d.list_missing_for_deposit(d.personal_needs))
