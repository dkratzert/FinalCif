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
        self.written_reflections = None
        self.hklfile = None
        self.transmission = None
        self.mu_r = None
        self.point_group_merge = 1
        self.filetype = 4
        self.domain = 1

    def __repr__(self):
        out = ''
        out += 'written refl.:\t{}\n'.format(self.written_reflections)
        out += 'transmission:\t{}\n'.format(self.transmission)
        out += 'Mu*r:\t\t\t{}\n'.format(self.mu_r)
        out += 'Merging:\t\t{}\n'.format(self.point_group_merge)
        out += 'hklfile:\t\t{}\n'.format(self.hklfile)
        out += 'HKL file type:\t{}\n'.format(self.filetype)
        out += 'Domain in hkl:\t{}\n'.format(self.domain)
        return out


class Sadabs():
    """
    This is a SADABS/TWINABS file parsing object.
    TODO: Add data structure that handles multiple refinements esp. in TWINABS
    """
    _refl_written_regex = re.compile(r'.*Corrected reflections written to file', re.IGNORECASE)
    _rint_regex = re.compile(r'^.*Rint\s=.*observations and')
    _rint3sig_regex = re.compile(r'^.*Rint\s=.*observations with')

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
        self.observations = None
        self.Rint_3sig = None
        self.observations_3sig = None
        self.input_files = []
        self.output = []
        self.batch_input = None
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
                #  Rint = 0.0873  for all   11683  observations and
                self.Rint = to_float(spline[2])
                self.observations = to_float(spline[5])
            if self._rint3sig_regex.match(line):
                #  Rint = 0.0376  for all   44606  observations with I > 3sigma(I)
                self.Rint = to_float(spline[2])
                self.observations_3sig = to_float(spline[5])
            if line.startswith(" Reading file"):
                self.input_files.append(spline[2])
            if line.startswith(" Reading batch"):
                self.input_files.append(spline[-1])
                self.batch_input = spline[2]
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

    @property
    def program(self):
        return self.version.split()[0].split('-')[0]

    def dataset(self, n):
        return self.output[n]

    def __repr__(self):
        out = 'Program:\t\t{}\n'.format(self.program)
        out += 'version:\t\t{}\n'.format(self.version)
        out += 'Input File:\t\t{}\n'.format(' '.join(self.input_files))
        out += 'Input Batch:\t{}\n'.format(self.batch_input)
        out += 'rint:\t\t\t{}\n'.format(self.Rint)
        out += 'components:\t\t{}\n'.format(self.twin_components)
        out += '\n'
        return out


if __name__ == '__main__':
    s = Sadabs('test-data/IK_WU19.abs')
    print(s)
    for dat in s:
        print(dat)

    print('###############\n\n')

    s = Sadabs(r'test-data/twin-4-5.abs')
    print(s)
    for dat in s:
        print(dat)

    print('###############\n\n')
    s = Sadabs(r'test-data/DK_Zucker2.abs')
    print(s)
    for dat in s:
        print(dat)
