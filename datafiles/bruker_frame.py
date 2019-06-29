from pathlib import Path
from pprint import pformat


class BrukerFrameHeader():
    def __init__(self, filename: str):
        self._fileobj = Path(filename)
        self.filename = self._fileobj.absolute()
        self.header = {}

        with open(self._fileobj) as file:
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
        tmp = self.header['CREATED'].split()[1]
        try:
            return (float(tmp) / 100.0) + 273.15
        except ValueError:
            return 293.15

    @property
    def kilovolts(self):
        tmp = self.header['SOURCEK']
        return round(float(tmp), 2)

    @property
    def milliwatt(self):
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
