#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
from contextlib import suppress
from typing import List

from docx.text.paragraph import Paragraph

"""
[1] SAINT
[2] SADABS/TWINABS
[3] SHELXT
[4] SHELXL
[5] ShelXle
[6] DSR
[7] Olex2
[8] Absolute structure (nach S. Parson)
[9] Überstrukturen (A non-mathematical introduction to superstructures)

[1] SAINT V8.37A, Bruker AXS, Madison, Wisconsin, USA, 2015.
[2] L. Krause, R. Herbst-Irmer, G. M. Sheldrick, D. Stalke, J. Appl. Cryst. 2015, 48, 3–10, doi:10.1107/S1600576714022985
[3] G. M. Sheldrick, Acta Cryst. 2015, A71, 3–8, doi:10.1107/S2053273314026370
[4] G. M. Sheldrick, Acta Cryst. 2015, C71, 3–8, doi:10.1107/S2053229614024218
[5] C. B. Hubschle, G. M. Sheldrick and B. Dittrich, J. Appl. Cryst. 2011, 44, 1281–1284, 10.1107/S0021889811043202
[6a] D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934. doi: 10.1107/S1600576718004508
[6b] D. Kratzert, J. J. Holstein, I. Krossing, J. Appl. Cryst. 2015, 48, 933–938, doi:10.1107/S1600576715005580
[7] L. J. Bourhis, O. V. Dolomanov, R. J. Gildea, J. A. K. Howard, H. Puschmann, Acta Cryst. 2015, A71, 59–75, doi:10.1107/S2053273314022207
[8] S. Parsons, H. D. Flack, T. Wagner, Acta Cryst. 2013, B69, 249-259, doi:10.1107/S2052519213010014
[9] T. Wagner, A. Schonleber, Acta Cryst. 2009, 65, 249–268, doi:10.1107/S0108768109015614
"""


class ReferenceList():
    """
    This reference list holds a list of all used references. During each self.append(Reference()), a new reference is
    appended to the list. 
    At the end of the document, a numbered list of references can be generated with self.make_make_literature_list().
    """

    def __init__(self, paragraph: Paragraph):
        self.paragraph = paragraph
        self._references = list()

    def append(self, ref) -> None:
        """Adds a superscript list of reference numbers in brackets to the document."""
        if isinstance(ref, (list, tuple)):
            if not ref:
                return None
            self._append_list(ref)
        else:
            if not ref in self._references:
                self._references.append(ref)
            self.paragraph.add_run('[{}]'.format(self._references.index(ref) + 1)).font.superscript = True
        self.paragraph.add_run(' ')

    def _append_list(self, reflist: List) -> None:
        reflst_long = []
        self.paragraph.add_run('[').font.superscript = True
        for n, ref in enumerate(reflist):
            if not ref in self._references:
                self._references.append(ref)
            refnum = self._references.index(ref) + 1
            reflst_long.append(refnum)
        reftxt = self.get_sequence(reflst_long)
        self.paragraph.add_run(reftxt).font.superscript = True
        self.paragraph.add_run(']').font.superscript = True

    @staticmethod
    def get_sequence(stringlist: List[int]):
        """
        Converts a list of numbers into a string of numbers where recurring sequences
        are described with a range.

        >>> ReferenceList.get_sequence([1, 3, 4, 5, 6, 8, 11])
        '1,3-6,8,11'
        """
        folg = []
        start = 0
        for n, val in enumerate(stringlist):
            val = int(val)
            nextval = 0
            with suppress(IndexError):
                nextval = int(stringlist[n + 1])
            nextnext = 0
            with suppress(IndexError):
                nextnext = int(stringlist[n + 2])
            # a sequence starts:
            if nextnext == val + 2 and not start:
                start = val
            # in a sequence and next value is not +1 -> squence ends with val:
            if start and nextval != val + 1:
                folg.append('{}-{}'.format(start, val))
                start = 0
                continue
            # everything outside a sequence:
            if not start:
                folg.append(val)
        return ','.join([str(x) for x in folg])

    def make_literature_list(self, paragraph_reflist):
        for num, ref in enumerate(self._references, 1):
            paragraph_reflist.add_run('[{}] '.format(str(num)))
            ref.add_reference(paragraph_reflist)
            paragraph_reflist.add_run('\n')


class ReferenceFormater():
    def __init__(self, paragraph: Paragraph):
        self.p = paragraph
        self.authors = ''
        self.journal = ''
        self.year = ''
        self.volume = ''
        self.pages = ''
        self.doi = ''
        self.program = ''

    def add_reference(self, p):
        if self.authors:
            p.add_run(self.authors)
            p.add_run(', ')
        if self.journal:
            p.add_run(self.journal).italic = True
            if not self.journal.endswith('.'):
                p.add_run(', ')
            else:
                p.add_run(' ')
        if self.year:
            p.add_run(self.year).bold = True
            p.add_run(', ')
        if self.volume:
            p.add_run(self.volume).italic = True
            p.add_run(', ')
        if self.pages:
            p.add_run(self.pages)
        if self.doi:
            if all([self.journal, self.year, self.authors]):
                p.add_run(', ')
            p.add_run(self.doi)
        if all([self.journal, self.year, self.authors]):
            p.add_run('.')

    def __repr__(self):
        txt = ''
        if self.authors:
            txt += self.authors
            txt += ', '
        if self.journal:
            txt += self.journal
            if not self.journal.endswith('.'):
                txt += ', '
            else:
                txt += ' '
        if self.year:
            txt += self.year
            txt += ', '
        if self.volume:
            txt += self.volume
            txt += ', '
        if self.pages:
            txt += self.pages
        if self.doi:
            if txt:
                txt += ', '
            txt += self.doi
        if all([self.journal, self.year, self.authors]):
            txt += '.'
        return txt


class DSRReference2015(ReferenceFormater):
    """D. Kratzert, J.J. Holstein, I. Krossing, J. Appl. Cryst. 2015, 48, 933-938. doi:10.1107/S1600576715005580

    >>> DSRReference2015('foo')
    D. Kratzert, J.J. Holstein, I. Krossing, J. Appl. Cryst. 2015, 48, 933-938.
    """

    def __init__(self, paragraph: Paragraph):
        super().__init__(paragraph)
        # self.doi = '(doi: 10.1107/S1600576715005580)'
        self.authors = 'D. Kratzert, J.J. Holstein, I. Krossing'
        self.journal = 'J. Appl. Cryst.'
        self.year = '2015'
        self.volume = '48'
        self.pages = '933-938'


class DSRReference2018(ReferenceFormater):
    """D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934. doi: 10.1107/S1600576718004508

    >>> DSRReference2018('foo')
    D. Kratzert, I. Krossing, J. Appl. Cryst. 2018, 51, 928-934.

    """

    def __init__(self, paragraph: Paragraph):
        super().__init__(paragraph)
        # self.doi = '(doi: 10.1107/S1600576718004508)'
        self.authors = 'D. Kratzert, I. Krossing'
        self.journal = 'J. Appl. Cryst.'
        self.year = '2018'
        self.volume = '51'
        self.pages = '928-934'


class BrukerReference(ReferenceFormater):
    def __init__(self, paragraph: Paragraph, name: str, version: str):
        """
        Bruker (2012). Program name(s). Bruker AXS Inc., Madison, Wisconsin, USA.

        >>> BrukerReference('foo', 'SAINT', '7.68a')
        SAINT, version 7.68a, 2012, Bruker AXS Inc., Madison, Wisconsin, USA.
        """
        super().__init__(paragraph)
        self.authors = name
        self.journal = 'version ' + version
        self.year = '2012'
        # self.volume = 'Bruker'
        self.pages = 'Bruker AXS Inc., Madison, Wisconsin, USA'


if __name__ == '__main__':
    r = ReferenceList.get_sequence([1, 2, 3, 4])
    print(r)
