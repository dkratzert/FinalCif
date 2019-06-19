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


class Dataset():
    def __init__(self):
        self.rint = None
        self.line = None
        self.domain = None
        self.written_reflections = None
        self.hklfile = None
        self.observations = None
        self.Rint_3sig = None
        self.observations_3sig = None
        self.transmission = None
        self.mu_r = None
        self.version = 'SADABS'
        self.point_group_merge = 1
        self.filetype = 4
        self.domain = 1

    # def __getattribute__(self, item):
    #    try:
    #        return self.item
    #    except AttributeError:
    #        return None


class Sadabs():
    """
    This is a SADABS/TWINABS file parsing object.
    TODO: Add data structure that handles multiple refinements esp. in TWINABS
    """
    _refl_written_regex = re.compile(r'.*Corrected reflections written to file', re.IGNORECASE)
    _rint_regex = re.compile(r'^.*Rint\s=.*observations and')

    def __init__(self, filename):
        """
        >>> s = Sadabs(r'test-data/IK_WU19.abs')  # this is a sadabs file
        >>> s.twin_components
        0
        >>> s.dataset(0).hklfile
        'IK_WU19_0m.hkl'
        >>> s.dataset(0).Rint  # the WR2(int)
        0.0472
        >>> s.dataset(0).transmission
        [0.7135, 0.7459]
        >>> s.dataset(0).version
        'SADABS-2016/2 - Bruker AXS area detector scaling and absorption correction'
        >>> s.dataset(0).written_reflections
        152800

        >>> s = Sadabs(r'test-data/twin-4-5.abs')  # this is a twinabs file
        >>> s.dataset(0).transmission
        [0.605537, 0.744178]
        >>> s.dataset(0).Rint
        0.0873
        >>> s.dataset(0).hklfile
        'twin5.hkl'
        >>> s.twin_components
        2
        >>> s.version
        'TWINABS - Bruker AXS scaling for twinned crystals - Version 2012/1'
        >>> s.dataset(0).written_reflections
        2330
        """
        self._fileobj = Path(filename)
        self.version = None
        self.twin_components = 1
        self.Rint = None
        self.input_files = [] 
        self.output = []
        self.parse_file()

    def parse_file(self):
        n = 0
        filetxt = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
        hklf5 = False
        # TODO: input files: "Reading file IK_WU19_0m.raw", but remind the 01, 02, etc. raw files
        for line in filetxt:
            spline = line.split()
            if line.startswith(' PART 3'):
                if self.version.startswith('SADABS'):
                    self.output.append(Dataset())
            if self._rint_regex.match(line):
                # Rint = 0.0873  for all   11683  observations and
                self.Rint = to_float(spline[2])
            if line.startswith(' wR2(int)'):
                self.Rint = to_float(spline[2])
            if 'SADABS' in line or 'TWINABS' in line:
                self.version = line.lstrip().strip()
            if 'twin components' in line:
                self.twin_components = to_int(spline[0])
            if line.startswith(" Additional spherical absorption correction"):
                self.dataset(n).mu_r = spline[-1]  # This is always last
                n += 1
            if line.startswith(' Reflections merged according'):
                self.dataset(n).point_group_merge = spline[-1]
            if line.startswith(' HKLF 5 dataset constructed'):
                # This can be before "Corrected reflections written" in case of hklf5 files
                if self.version.startswith('TWINABS'):
                    hklf5 = True
                    self.output.append(Dataset())
                self.dataset(n).filetype = to_int(spline[1])
                self.dataset(n).domain = spline[-1]
            if self._refl_written_regex.match(line):  # This is always first
                #     2330 Corrected reflections written to file IK_KG_CF_3_0m_5.hkl
                if self.version.startswith('TWINABS') and not hklf5:
                    self.output.append(Dataset())
                self.dataset(n).written_reflections = to_int(spline[0])
                self.dataset(n).hklfile = spline[-1]
            if "Estimated minimum and maximum transmission" in line \
                    or 'Minimum and maximum apparent transmission' in line:
                try:
                    self.dataset(n).transmission = [float(x) for x in spline[-2:]]
                except ValueError:
                    pass

    def __iter__(self):
        return iter(x for x in self.output)

    def dataset(self, n):
        return self.output[n]


if __name__ == '__main__':
    s = Sadabs('test-data/IK_WU19.abs')
    print('version:', s.version)
    print('rint:', s.Rint)
    print('components:', s.twin_components)
    print('')
    for dat in s:
        print('written reflections:', dat.written_reflections)
        print('hklfile:', dat.hklfile)
        print('transmission:', dat.transmission)
        print('Mu*r:', dat.mu_r)
        print('file type:', dat.filetype)
        print('\n')

    print('###############')

    s = Sadabs(r'test-data/twin-4-5.abs')
    print('version:', s.version)
    print('rint:', s.Rint)
    print('components:', s.twin_components)
    print('')
    for dat in s:
        print('written reflections:', dat.written_reflections)
        print('hklfile:', dat.hklfile)
        print('transmission:', dat.transmission)
        print('Mu*r:', dat.mu_r)
        print('Merging:', dat.point_group_merge)
        print('file type:', dat.filetype)
        print('\n')
