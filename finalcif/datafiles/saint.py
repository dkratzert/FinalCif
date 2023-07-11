#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#
from contextlib import suppress
from pathlib import Path

from finalcif.datafiles.utils import get_file_to_parse


class SaintListFile():
    def __init__(self, name_patt: str, directory: Path = None):
        self.cell_reflections = ''
        self.cell_res_min_2t = 0.0
        self.cell_res_max_2t = 0.0
        self.aquire_software = ''
        self.version = ''
        self.is_twin = False
        self.twinlaw = {}
        self.nsamples = 1
        self.components_firstsample = 1
        self.filename = Path('')
        if directory:
            self._fileobj = get_file_to_parse(name_pattern=name_patt, base_directory=directory)
        else:
            self._fileobj = get_file_to_parse(name_pattern=name_patt, base_directory=Path('.'))
        if self._fileobj:
            self.filename = self._fileobj.resolve()
            try:
                self.parse_file()
            except Exception as e:
                print('Unable to parse saint list file:', e)

    def parse_file(self):
        text = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
        summary = None
        orientation = 0
        for num, line in enumerate(text):
            # spline = line.strip().split()
            if num == 0:
                self.version = line
            if line.startswith('Refinement includes'):
                with suppress(IndexError):
                    self.nsamples = int(line.split()[2])
                with suppress(IndexError, ValueError):
                    self.components_firstsample = int(text[num + 1].split()[3])
            if line.startswith('Reflection Summary:'):
                """
                Reflection Summary:
                'RLV.Excl' are reflections excluded after cycle 1 because RLV error exceeded 0.0250:
                 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
                    1.1(1)      9478         0      9478    8.7419    0.7731     4.660    54.727
                    
                Or in *_01._ls:
                
                Reflection Summary:
                 Component     Input  RLV.Excl      Used  WorstRes   BestRes   Min.2Th   Max.2Th
                    1.1(1)       202         0       202    6.9242    1.2823     5.884    32.178
                """
                summary = True
            if summary and line.lstrip().startswith('1.1(1)'):
                summary = line.split()
                if len(summary) == 8:
                    self.cell_reflections = summary[3] or 0
                    self.cell_res_min_2t = summary[6] or 0.0
                    self.cell_res_max_2t = summary[7] or 0.0
                summary = False
            # This is the twin case:
            if summary and line.lstrip().startswith('All'):
                summary = line.split()
                if len(summary) == 8:
                    self.cell_reflections = summary[3] or 0
                    self.cell_res_min_2t = summary[6] or 0.0
                    self.cell_res_max_2t = summary[7] or 0.0
                # essential to prevent wrong parsing:
                summary = False
            if line.startswith("Orientation ('UB') matrix"):
                orientation += 1
            if line.startswith('Twin Law'):
                self.is_twin = True
                # S.C(F) -> S Sample number, C Combonent number, F number in the file
                try:
                    twin = []
                    transform = text[num + 1].strip()
                    twin.append([float(x) for x in text[num + 2].split()])
                    twin.append([float(x) for x in text[num + 3].split()])
                    twin.append([float(x) for x in text[num + 4].split()])
                    self.twinlaw[transform] = twin
                except (KeyError, ValueError):
                    print('Could not determine twin law fro m._ls file.')
                    pass
            if summary and orientation == 2:
                summary = False
            if line.startswith('Frames were acquired'):
                """
                Frames were acquired with BIS 2018.9.0.3/05-Dec-2018 && APEX3_2018.7-2
                    Rescan threshold is 95% of A/D conversion range
                """
                self.aquire_software = 'Bruker ' + ' '.join(line.split()[4:]).replace('&&', 'and')

    @property
    def cell_res_min_theta(self):
        return float(self.cell_res_min_2t) / 2.0

    @property
    def cell_res_max_theta(self):
        return float(self.cell_res_max_2t) / 2.0

    def __repr__(self):
        out = 'Version: {}, file: {}\n'.format(self.version, self.filename.name)
        out += 'Number of samples: {} with {} components.\n'.format(self.nsamples, self.components_firstsample)
        out += 'Used Reflections: {}\n'.format(self.cell_reflections)
        out += 'min thata: {}\n'.format(self.cell_res_min_theta)
        out += 'max theta: {}\n'.format(self.cell_res_max_theta)
        out += 'min 2 theta: {}\n'.format(self.cell_res_min_2t)
        out += 'max 2 theta: {}\n'.format(self.cell_res_max_2t)
        if self.aquire_software:
            out += 'Aquire software: {}\n'.format(self.aquire_software)
        out += 'Twin integration {}\n'.format(self.is_twin)
        if self.is_twin:
            out += 'With twin law: \n'
            for n, law in enumerate(self.twinlaw, 1):
                out += "{}:\n".format(law)
                out += '\n'.join(['{:>7.4f} {:>7.4f} {:>7.4f}'.format(*x) for x in self.twinlaw[law]])
                out += '\n'
        return out


if __name__ == "__main__":
    saint = SaintListFile(name_patt='*._ls', directory='test-data/TB_fs20_v1_0m._ls')
    print(saint)

    print('#####')
    s = SaintListFile('*._ls', directory='test-data/Esser_JW316_01._ls')
    print(s)

    print('#####')
    s = SaintListFile('*._ls', directory='test-data/test766_0m._ls')
    print(s)

    print('#####')
    s = SaintListFile('*_0[?]m._ls', directory=r'D:\GitHub\FinalCif\test-data\DK_Zucker2_0m._ls')
    print(s)

    paths = Path(r'D:\frames').rglob('*_0*m._ls')
    l = Path(r'D:\refltest.txt')
    content = []
    for p in paths:
        s = SaintListFile(name_patt='*_0*m._ls', directory=p.resolve())
        content.append(s.cell_reflections)
    l.write_text('\n'.join(content))
