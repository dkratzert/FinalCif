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


if __name__ == '__main__':
    sfrm = BrukerFrameHeader('test-data/apex_frame.sfrm')
    print(sfrm)

    print('#####')

    sfrm = BrukerFrameHeader('test-data/mo_DK_Zucker2_01_0001.sfrm')
    print(sfrm)
