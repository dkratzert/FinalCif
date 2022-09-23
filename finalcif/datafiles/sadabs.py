#!python
import dataclasses
#  Copyright (c)  2019 by Daniel Kratzert
import re
from pathlib import Path
from typing import Optional

from finalcif.datafiles.utils import get_file_to_parse
from finalcif.tools.misc import to_float, to_int


#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#

@dataclasses.dataclass
class Transmission():
    tmin: float = None
    tmax: float = None

    def __repr__(self):
        return f'min: {self.tmin}, max: {self.tmax}'


class Dataset():
    def __init__(self):
        self.written_reflections: Optional[int] = None
        self.hklfile: Optional[str] = None
        self.transmission = Transmission()
        self.mu_r: Optional[str] = None
        self.point_group_merge: Optional[str] = '1'
        self.filetype: Optional[int] = 4
        self.domain: str = '1'
        self.numerical: bool = False

    def __repr__(self):
        out = f''
        out += f'written refl.:\t{self.written_reflections}\n'
        out += f'transmission:\t{self.transmission}\n'
        out += f'Mu*r:\t\t\t{self.mu_r}\n'
        out += f'Merging:\t\t{self.point_group_merge}\n'
        out += f'hklfile:\t\t{self.hklfile}\n'
        out += f'HKL file type:\t{self.filetype}\n'
        out += f'Domain in hkl:\t{self.domain}\n'
        out += f'Abs. type:\t\t{"multi-scan" if not self.numerical else "numerical"}'
        out += '\n'
        return out


class Sadabs():
    """
    This is a SADABS/TWINABS file parsing object.
    """
    _refl_written_regex = re.compile(r'.*Corrected reflections written to file', re.IGNORECASE)
    _rint_regex = re.compile(r'^.*Rint\s=.*observations and')
    _rint3sig_regex = re.compile(r'^.*Rint\s=.*observations with')

    def __init__(self, basename: str = '', searchpath: Path = Path(__file__).parent.parent, fileobj: Path = None):
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
            self._fileobj = get_file_to_parse(name_pattern=basename, base_directory=searchpath)
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
                self.Rint_3sig = to_float(spline[2])
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
                    transmissions = [float(x) for x in spline[-2:]]
                    self.dataset(n).transmission.tmin = min(transmissions)
                    self.dataset(n).transmission.tmax = max(transmissions)
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
        out = f'Program:\t\t{self.program}\n'
        out += f'version:\t\t{self.version}\n'
        out += f'Abs File:\t\t{self.filename.name}\n'
        out += f'raw input File:\t{" ".join(self.input_files)}\n'
        out += f'Input Batch:\t{self.batch_input}\n'
        out += f'Rint:\t\t\t{self.Rint}\n'
        out += f'Rint-3sig:\t\t{self.Rint_3sig}\n'
        out += f'components:\t\t{self.twin_components}\n'
        out += '\n'
        return out


if __name__ == '__main__':
    print('###############\n\n')
    # s = Sadabs(fileobj=Path(r'tests/statics/1163_67_1_rint_matt.abs'))
    s = Sadabs(fileobj=Path(r'tests/examples/work/cu_BruecknerJK_153F40.abs'))
    print(s)
    for dat in s:
        print(dat)
