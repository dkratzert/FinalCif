import base64
import email
from contextlib import suppress
from pathlib import Path
from typing import Union

import html2text as html2text

from finalcif.cif.cif_file_io import CifContainer


class CCDCMail():
    """
    This class searches for .eml (email) files in the current directory of the cif file.
    Each mail is parsed for CCDC number and unit cell.
    If the cell is the same as in the cif file. The deposition number (depnum) is
    set final.
    """

    def __init__(self, cif: CifContainer):
        eml_files = cif.fileobj.parent.glob('*.eml')
        self.depnum: int = 0
        self.mail_cell: Union[tuple, None] = None
        self.emlfile: Path = Path()
        for emlfile in eml_files:
            eml = False
            with suppress(Exception):
                eml = self.parse_emlfile(emlfile)
            if eml:
                self.emlfile = emlfile.resolve()
                if not self.mail_cell:
                    continue
                if not self.is_same_cell(cif, self.mail_cell):
                    self.depnum = 0
                    self.emlfile = Path()
            else:
                print('Mail parsing failed!')

    def __repr__(self):
        cell = 'None'
        if self.mail_cell:
            cell = ', '.join([str(x) for x in self.mail_cell])
        return 'CCDC-Number: {}\nCell from mail: {}\n.eml file name: {}'.format(self.depnum, cell, self.emlfile)

    def parse_emlfile(self, file: Path):
        m = email.message_from_string(file.read_text())
        encoding = m['Content-Transfer-Encoding']
        dirty = m.get_payload()
        mailbody = m.as_string()
        txt = mailbody.splitlines(keepends=False)
        if encoding == 'base64':
            mailbody = str(base64.decodebytes(bytes(dirty, 'ascii')))
            txt = html2text.html2text(mailbody).splitlines(keepends=False)
        for line in txt:
            spline = line.split()
            linelen = len(spline)
            if line.startswith('Deposition Number'):
                if linelen > 1:
                    self.depnum = int(spline[2])
            if line.startswith('Summary of Data CCDC'):
                if linelen > 3:
                    self.depnum = int(spline[4])
            if line.startswith('Unit Cell Parameters:'):
                if linelen > 9:
                    try:
                        self.mail_cell = (float(spline[4].split('(')[0]),
                                          float(spline[6].split('(')[0]),
                                          float(spline[8].split('(')[0]))
                        return True
                    except (TypeError, ValueError):
                        return False
        return True

    @staticmethod
    def is_same_cell(cif: CifContainer, cell: Union[list, tuple]):
        """
        """
        is_same = False
        for n in range(3):
            if round(cell[n], 4) == round(cif.cell[n], 4):
                is_same = True
            else:
                return False
        return is_same


if __name__ == '__main__':
    cif = CifContainer(
        Path('test-data/DK_zucker2_0m.cif'))
    ccdc = CCDCMail(cif)
