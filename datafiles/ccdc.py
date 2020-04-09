from email import message
from pathlib import Path
from typing import Union

from cif.cif_file_io import CifContainer


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
        for x in eml_files:
            if self.parse_emlfile(x):
                if not self.is_same_cell(cif, self.mail_cell):
                    self.depnum = 0

    def parse_emlfile(self, file: Path):
        m = message.Message()
        m.set_payload(file.read_bytes())
        for line in m.as_string().splitlines(keepends=False):
            spline = line.split()
            linelen = len(spline)
            if line.startswith('Deposition Number'):
                if linelen > 1:
                    self.depnum = spline[2]
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
    def is_same_cell(cif: CifContainer, cell):
        """

        :param cif:
        :param cell:
        :return:

        >>> cif = CifContainer(Path('test-data/DK_zucker2_0m.cif'))
        >>> ccdc = CCDCMail(cif)
        >>> ccdc.is_same_cell(cif, [7.716, 8.664, 10.812])
        True
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
