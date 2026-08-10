#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return. 
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
#
import re
from contextlib import suppress
from pathlib import Path

from finalcif.datafiles.utils import get_file_to_parse


class SaintListFile:
    _component_regex = re.compile(r'^\s*(\d+\.\d+\(\d+\))\s+\d+\s+\d+\s+\d+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s*$')
    _all_components_regex = re.compile(r'^\s*All\s+\d+\s+\d+\s+\d+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s*$')

    def __init__(self, name_patt: str, directory: Path | None = None, file_to_parse: Path | None = None):
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
        self._components: dict[str, tuple[int, float, float]] = {}
        self._all_components: tuple[int, float, float] | None = None
        if file_to_parse:
            self._fileobj = file_to_parse
        elif directory:
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
        in_summary = False
        for num, line in enumerate(text):
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

                A twinned crystal has one row per component, either in one summary or in a
                separate summary for every component (then also with a leading sample number):

                    1.1(1)      3665         0      3665    9.1422    0.7352     4.455    57.808
                    1.2(2)      2337         0      2337    9.1422    0.8216     4.455    51.257
                       All      6002         0      6002    9.1422    0.7352     4.455    57.808
                """
                in_summary = True
                continue
            if in_summary:
                in_summary = self._parse_summary_line(line)
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
            if line.startswith('Frames were acquired'):
                """
                Frames were acquired with BIS 2018.9.0.3/05-Dec-2018 && APEX3_2018.7-2
                    Rescan threshold is 95% of A/D conversion range
                """
                self.aquire_software = 'Bruker ' + ' '.join(line.split()[4:]).replace('&&', 'and')
        self._set_cell_measurement_values()

    def _parse_summary_line(self, line: str) -> bool:
        """
        Collects the component rows of a reflection summary. Returns False if the summary ended.
        """
        component = self._component_regex.match(line)
        if component:
            self._components[component.group(1)] = self._summary_values(line)
            return True
        if self._all_components_regex.match(line):
            self._all_components = self._summary_values(line)
            return True
        return not line.strip() or line.lstrip().startswith(("Component", "'RLV.Excl'"))

    @staticmethod
    def _summary_values(line: str) -> tuple[int, float, float]:
        spline = line.split()
        return int(spline[3]), float(spline[6]), float(spline[7])

    def _set_cell_measurement_values(self) -> None:
        """
        The 'All' row holds the values of all twin domains. Without it, all components have to
        be summed up, because otherwise only the first domain would be counted.
        """
        components = [self._all_components] if self._all_components else list(self._components.values())
        if not components:
            return
        self.cell_reflections = str(sum(x[0] for x in components))
        self.cell_res_min_2t = f'{min(x[1] for x in components):.3f}'
        self.cell_res_max_2t = f'{max(x[2] for x in components):.3f}'

    @property
    def cell_res_min_theta(self):
        return float(self.cell_res_min_2t) / 2.0

    @property
    def cell_res_max_theta(self):
        return float(self.cell_res_max_2t) / 2.0

    def __repr__(self):
        out = f'Version: {self.version}, file: {self.filename.name}\n'
        out += f'Number of samples: {self.nsamples} with {self.components_firstsample} components.\n'
        out += f'Used Reflections: {self.cell_reflections}\n'
        out += f'min thata: {self.cell_res_min_theta}\n'
        out += f'max theta: {self.cell_res_max_theta}\n'
        out += f'min 2 theta: {self.cell_res_min_2t}\n'
        out += f'max 2 theta: {self.cell_res_max_2t}\n'
        if self.aquire_software:
            out += f'Aquire software: {self.aquire_software}\n'
        out += f'Twin integration {self.is_twin}\n'
        if self.is_twin:
            out += 'With twin law: \n'
            for _, law in enumerate(self.twinlaw, 1):
                out += f"{law}:\n"
                out += '\n'.join(['{:>7.4f} {:>7.4f} {:>7.4f}'.format(*x) for x in self.twinlaw[law]])
                out += '\n'
        return out


if __name__ == "__main__":
    for name in ('TB_fs20_v1_0m._ls', 'test766_0m._ls', 'DK_Zucker2_0m._ls', 'DK_ML766_twin._ls'):
        print('#####')
        print(SaintListFile('*._ls', file_to_parse=Path('test-data') / name))
