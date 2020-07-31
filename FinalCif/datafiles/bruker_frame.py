#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
# 

import os
from pathlib import Path
from pprint import pformat

from FinalCif.cif.cif_file_io import CifContainer


class BrukerFrameHeader():
    def __init__(self, basename: str, cif: CifContainer):
        self.cif = cif
        p = self.cif.fileobj.parent
        frames = p.glob(basename + '*.sfrm')
        frames = sorted(frames, key=os.path.getmtime, reverse=True)
        self._fileobj = None
        if not frames:
            frames = Path(os.curdir).absolute().glob('*.sfrm')
        for fr in frames:
            if fr:
                self._fileobj = Path(fr)
        if not self._fileobj:
            raise FileNotFoundError
        self.filename = self._fileobj.absolute()
        self.header = {}
        if self._fileobj.is_file():
            with open(str(self._fileobj.absolute()), encoding='ascii', errors='ignore', mode='r') as file:
                for n in range(96):
                    l = file.read(80).strip()
                    key = l[:7].strip()
                    self.header[key] = l[8:].strip()  # value

    def __repr__(self):
        return pformat(self.header, indent=2, width=120)

    @property
    def radiation_type(self):
        return self.header['TARGET']

    @property
    def program(self):
        return self.header['PROGRAM']

    @property
    def detector_type(self):
        return self.header['DETTYPE'].split()[0]

    @property
    def measure_date(self):
        dt = ' '.join(self.header['CREATED'].split())
        return dt

    @property
    def temperature(self):
        try:
            tmp = self.header['LOWTEMP'].split()[1]
            return (float(tmp) / 100.0) + 273.15
        except (ValueError, KeyError):
            return 293.15

    @property
    def kilovolts(self):
        tmp = self.header['SOURCEK']
        return round(float(tmp), 2)

    @property
    def milliamps(self):
        tmp = self.header['SOURCEM']
        return round(float(tmp), 2)


if __name__ == '__main__':
    sfrm = BrukerFrameHeader('test-data/apex_frame.sfrm')
    print(sfrm)

    print('#####')

    sfrm = BrukerFrameHeader('test-data/mo_DK_Zucker2_01_0001.sfrm')
    print(sfrm)
    print(sfrm.radiation_type)

    print('#####')

    sfrm = BrukerFrameHeader('test-data/cu_Ylid_Shutterless_01_0001.sfrm')
    print(sfrm)
    print(sfrm.radiation_type)
    print(sfrm.measure_date)
