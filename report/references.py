#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

from typing import List

from docx.text.paragraph import Paragraph

from datafiles.p4p_reader import read_file_to_list


class ReferenceList():
    """
    This reference list holds a list of all used references. During each self.append(Reference()), a new reference is
    appended to the list. 
    At the end of the document, a numbered list of references can be generated with self.make_make_literature_list().
    """

    def __init__(self, paragraph: Paragraph):
        self.paragraph = paragraph
        self._references: List[ReferenceFormater] = list()

    def append(self, ref):
        if not ref in self._references:
            self._references.append(ref)
        self.paragraph.add_run('[{}]'.format(self._references.index(ref) + 1)).font.superscript = True

    def append_list(self, reflist):
        last = len(reflist) - 1
        for ref in reflist:
            if not ref in self._references:
                self._references.append(ref)
            num = self._references.index(ref)
            if num == 0:
                self.paragraph.add_run('[').font.superscript = True
            self.paragraph.add_run('{}'.format(self._references.index(ref) + 1)).font.superscript = True
            if num == last:
                self.paragraph.add_run(']').font.superscript = True
            else:
                self.paragraph.add_run(',').font.superscript = True

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
        txt = 'Foo: '
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
    (doi: 10.1107/S1600576718004508)
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
        SAINT, Bruker, 2012, Bruker AXS Inc., Madison, Wisconsin, USA.
        """
        super().__init__(paragraph)
        self.authors = name
        self.journal = 'version ' + version
        self.year = '2012'
        # self.volume = 'Bruker'
        self.pages = 'Bruker AXS Inc., Madison, Wisconsin, USA'
