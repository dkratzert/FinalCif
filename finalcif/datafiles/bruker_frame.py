#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
# 

import os
import re
from pathlib import Path
from pprint import pformat

from finalcif.tools.misc import isnumeric


class BrukerFrameHeader():
    def __init__(self, basename: str, searchpath: Path = Path(__file__).parent.parent):
        basename = re.sub(r'_[a-z]$', '', basename)
        frames = searchpath.glob('{}{}*.sfrm'.format('*' if basename else '', basename))
        frames = sorted(frames, key=os.path.getmtime, reverse=True)
        self._fileobj = None
        for fr in frames:
            if fr:
                self._fileobj = Path(fr)
        if not self._fileobj:
            raise FileNotFoundError
        self.filename = self._fileobj.resolve()
        self.header = {}
        if self._fileobj.is_file():
            with open(str(self._fileobj.resolve()), encoding='ascii', errors='ignore', mode='r') as file:
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
            return round((float(tmp) / 100.0) + 273.15, 2)
        except (ValueError, KeyError):
            return 293.15

    @property
    def kilovolts(self) -> float:
        tmp = self.header['SOURCEK']
        if isnumeric(tmp):
            return round(float(tmp), 2)
        else:
            return 0.0

    @property
    def milliamps(self) -> float:
        tmp = self.header['SOURCEM']
        if isnumeric(tmp):
            return round(float(tmp), 2)
        else:
            return 0.0


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
