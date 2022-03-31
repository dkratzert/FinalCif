# -*- encoding: utf-8 -*-

#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
# 


"""
This file reads Bruker p4p files into a data structure.
"""
import os
import re
from pathlib import Path


def read_file_to_list(p4pfile: str) -> list:
    """
    Reads a file and returns a list without line endings.
    """
    p4plist = []
    try:
        p4plist = Path(p4pfile).read_text().splitlines(keepends=False)
    except IOError as e:
        print(e)
        print('*** CANNOT READ FILE {} ***'.format(p4pfile))
    return p4plist


class P4PFile():

    def __init__(self, basename: str = '', searchpath: Path = Path(__file__).parent.parent):
        self.fileid = None
        self.siteid = None
        self.chem = None
        self.cell = None
        self.cellsd = None
        self.ort1 = None
        self.ort2 = None
        self.ort3 = None
        self.zeros = None
        self.source = None
        self.volume = None
        self.ortmatrix = None
        self._temperature = 0.0
        self.crystal_color = ''
        self.crystal_size = ['', '', '']
        self.morphology = ''
        self._radiation_type = ''
        self.wavelen = ''
        self.filename = Path()
        basename = re.sub(r'_[a-z]$', '', basename)
        p4p_files = searchpath.glob('{}{}*_0m.p4p'.format('*' if basename else '', basename))
        if not p4p_files:
            p4p_files = Path(os.curdir).resolve().glob('*.p4p')
        for p4p in p4p_files:
            if p4p:
                self.filename = p4p
                self.p4plist = read_file_to_list(str(self.filename))
                try:
                    self.parse_p4p()
                except Exception:
                    raise ValueError('*** p4p not readable ***')
        if not p4p_files:
            print('No p4p file found')

    def parse_p4p(self):
        for line in self.p4plist:
            spline = line.split()
            card = spline[0]
            if card == "CELL" and len(spline) > 5:
                self.cell = [float(x) for x in spline[1:7]]
                if len(spline) > 6:
                    self.volume = float(spline[7])
            if card == "FILEID":
                self.fileid = spline[1:]
            if card == 'CELLSD':
                self.cellsd = self.to_float_list(spline[1:])
            if card == "ORT1":
                self.ort1 = self.to_float_list(spline[1:])
            if card == "ORT2":
                self.ort2 = self.to_float_list(spline[1:])
            if card == "ORT3":
                self.ort3 = self.to_float_list(spline[1:])
            # if all([self.ort1, self.ort2, self.ort3]):
            #    self.ortmatrix = Matrix([self.ort1, self.ort2, self.ort3])
            if card == "CHEM":
                self.chem = spline[1]
            if card == 'SOURCE':
                self._radiation_type = spline[1]
                self.wavelen = spline[2]
            if card == 'MORPH':
                self.morphology = spline[1]
            if card == 'CCOLOR':
                self.crystal_color = spline[1]
            if card == 'CSIZE':
                # CSIZE  0.080        0.100        0.330        ?            -173.140
                self.crystal_size = spline[1:4]
                try:
                    # in Kelvin:
                    self._temperature = float(spline[-1]) + 273.15
                except ValueError:
                    pass

    @staticmethod
    def to_float_list(items):
        return [float(x) for x in items]

    @property
    def radiation_type(self):
        return self._radiation_type.capitalize()

    @property
    def temperature(self):
        return round(self._temperature, 2)


if __name__ == '__main__':
    p4p = P4PFile(searchpath=Path('./test-data/test1.p4p'))
    print(p4p.cell)
    print(p4p.cellsd)
    print(p4p.volume)
    print(p4p.ortmatrix)
    print(p4p.chem)
