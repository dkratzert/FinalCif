#!python
#  Copyright (c)  2019 by Daniel Kratzert
import re
from pathlib import Path


def to_float(st):
    if isinstance(st, list):
        try:
            return [float(x) for x in st[-2:]]
        except ValueError:
            return None
    else:
        try:
            return float(st)
        except ValueError:
            return None


def to_int(st):
    if isinstance(st, list):
        try:
            return [int(x) for x in st[-2:]]
        except ValueError:
            return None
    else:
        try:
            return int(st)
        except ValueError:
            return None


class Sadabs():
    """
    This is a SADABS/TWINABS file parsing object.
    TODO: Add data structure that handles multiple refinements esp. in TWINABS
    """
    _written_refl_regex = re.compile(r'.*Corrected reflections written to file', re.IGNORECASE)
    _rint_regex = re.compile(r'^.*Rint\s=.*observations and')

    def __init__(self, filename):
        """
        >>> s = Sadabs(r'scxrd/testfiles/IK_WU19.abs')
        >>> s.parse_file()
        >>> s.components

        >>> s.hklfile
        'IK_WU19_0m.hkl'
        >>> s.Rint

        >>> s.transmission
        [0.7135, 0.7459]
        >>> s.version
        'SADABS-2016/2 - Bruker AXS area detector scaling and absorption correction'
        >>> s.written_reflections
        152800

        >>> s = Sadabs(r'scxrd/testfiles/IK_KG_CF_3.abs')
        >>> s.parse_file()
        >>> s.transmission
        [0.605537, 0.744178]
        >>> s.Rint
        0.0873
        >>> s.hklfile
        'IK_KG_CF_3_0m_5.hkl'
        >>> s.components
        2
        >>> s.version
        'TWINABS - Bruker AXS scaling for twinned crystals - Version 2012/1'
        >>> s.written_reflections
        2330
        """
        self._fileobj = Path(filename)
        self.written_reflections = None
        self.hklfile = None
        self.Rint = None
        self.version = None
        self.components = None
        self.transmission = None

    def parse_file(self):
        for line in self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False):
            spline = line.split()
            if self._written_refl_regex.match(line):
                #     2330 Corrected reflections written to file IK_KG_CF_3_0m_5.hkl
                self.written_reflections = to_int(spline[0])
                self.hklfile = spline[-1]
            if self._rint_regex.match(line):
                # Rint = 0.0873  for all   11683  observations and
                self.Rint = to_float(spline[2])
            if 'SADABS' in line or 'TWINABS' in line:
                self.version = line.lstrip().strip()
            if 'twin components' in line:
                self.components = to_int(spline[0])
            if "Estimated minimum and maximum transmission" in line \
                    or 'Minimum and maximum apparent transmission' in line:
                try:
                    self.transmission = [float(x) for x in spline[-2:]]
                except ValueError:
                    pass


if __name__ == '__main__':
    s = Sadabs(r'scxrd/testfiles/IK_WU19.abs')
    s.parse_file()
    print('written reflections:', s.written_reflections)
    print('hklfile:', s.hklfile)
    print('rint:', s.Rint)
    print('version:', s.version)
    print('components:', s.components)
    print('transmission:', s.transmission)
    print('\n')
    s = Sadabs(r'scxrd/testfiles/IK_KG_CF_3.abs')
    s.parse_file()
    print('written reflections:', s.written_reflections)
    print('hklfile:', s.hklfile)
    print('rint:', s.Rint)
    print('version:', s.version)
    print('components:', s.components)
    print('transmission:', s.transmission)
