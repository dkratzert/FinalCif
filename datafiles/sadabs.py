#!python

#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
# 

#  Copyright (c)  2019 by Daniel Kratzert
import re
from pathlib import Path

from datafiles.utils import get_file_to_parse
from tools.misc import to_float, to_int


class Dataset():
    def __init__(self):
        self.written_reflections = None
        self.hklfile = None
        self.transmission = None
        self.mu_r = None
        self.point_group_merge = 1
        self.filetype = 4
        self.domain = 1
        self.numerical = False

    def __repr__(self):
        out = ''
        out += 'written refl.:\t{}\n'.format(self.written_reflections)
        out += 'transmission:\t{}\n'.format(self.transmission)
        out += 'Mu*r:\t\t\t{}\n'.format(self.mu_r)
        out += 'Merging:\t\t{}\n'.format(self.point_group_merge)
        out += 'hklfile:\t\t{}\n'.format(self.hklfile)
        out += 'HKL file type:\t{}\n'.format(self.filetype)
        out += 'Domain in hkl:\t{}\n'.format(self.domain)
        out += 'Abs. type:\t\t{}'.format('multi-scan' if not self.numerical else 'numerical')
        out += '\n'
        return out


class Sadabs():
    """
    This is a SADABS/TWINABS file parsing object.
    """
    _refl_written_regex = re.compile(r'.*Corrected reflections written to file', re.IGNORECASE)
    _rint_regex = re.compile(r'^.*Rint\s=.*observations and')
    _rint3sig_regex = re.compile(r'^.*Rint\s=.*observations with')

    def __init__(self, basename: str = '', fileobj: Path = None):
        """
        """
        self.faces = False
        self.version = ''
        self.twin_components = 1
        self.Rint = None
        self.observations = None
        self.Rint_3sig = None
        self.observations_3sig = None
        self.input_files = []
        self.datasets = []
        self.batch_input = None
        self.filename = Path('')
        if basename:
            self._fileobj = get_file_to_parse(name_pattern=basename, base_directory='.')
        else:
            self._fileobj = get_file_to_parse(fileobj=fileobj)
        if self._fileobj:
            self.filename = self._fileobj.resolve()
            self.parse_file()

    def parse_file(self):
        n = 0
        filetxt = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
        hklf5 = False
        for line in filetxt:
            spline = line.split()
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
            if line.startswith(' Crystal faces:'):
                self.faces = True
            if 'SADABS' in line or 'TWINABS' in line:
                self.version = line.lstrip().strip() + ": Krause, L., Herbst-Irmer, R., Sheldrick G.M. & Stalke D., " \
                                                       "J. Appl. Cryst. 48 (2015) 3-10"
            if 'twin components' in line:
                self.twin_components = to_int(spline[0])
            if line.startswith(' Reflections merged according'):
                self.dataset(n).point_group_merge = spline[-1]
            if line.startswith(' HKLF 5 dataset constructed'):
                # This can be before "Corrected reflections written" in case of hklf5 files
                if self.version.startswith('TWINABS'):
                    hklf5 = True
                    self.datasets.append(Dataset())
                self.dataset(n).filetype = to_int(spline[1])
                self.dataset(n).domain = spline[-1]
            if self._refl_written_regex.match(line):  # This is always first
                #     2330 Corrected reflections written to file IK_KG_CF_3_0m_5.hkl
                #   275136 Corrected reflections written to file sad_noface_u.hkl
                if not hklf5:
                    self.datasets.append(Dataset())
                self.dataset(n).written_reflections = to_int(spline[0])
                self.dataset(n).hklfile = spline[-1]
            if "Estimated minimum and maximum transmission" in line \
                    or 'Minimum and maximum apparent transmission' in line:
                try:
                    self.dataset(n).transmission = [float(x) for x in spline[-2:]]
                except ValueError:
                    pass
            # This is always last:
            if line.startswith(" Additional spherical absorption correction"):
                self.dataset(n).mu_r = spline[-1]
                self.dataset(n).numerical = self.faces
                n += 1
            # do not:
            # if line.startswith(' Unique HKLF'):
            #    n += 1

    def __iter__(self):
        return iter(x for x in self.datasets)

    @property
    def program(self):
        return self.version.split()[0].split('-')[0]

    def dataset(self, n):
        try:
            return self.datasets[n]
        except IndexError:
            return Dataset()

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
    print('###############\n\n')
    s = Sadabs(fileobj=Path(r'/Volumes/nifty/test_workordner/test766-twin/work/test766.abs'))
    print(s)
    for dat in s:
        print(dat)
