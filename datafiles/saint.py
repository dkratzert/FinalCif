from pathlib import Path


class SaintListFile():
    def __init__(self, name_patt: str):
        self.cell_reflections = ''
        self.cell_res_min_2t = 0.0
        self.cell_res_max_2t = 0.0
        self.aquire_software = ''
        self.version = ''
        self.filename = Path('.')
        p = Path('./')
        saintfiles = p.glob(name_patt)
        for saintfile in saintfiles:
            if saintfile:
                self._fileobj = Path(saintfile)
                self.filename = self._fileobj.absolute()
                self.parse_file()

    def parse_file(self):
        text = self._fileobj.read_text(encoding='ascii', errors='ignore').splitlines(keepends=False)
        for num, line in enumerate(text):
            #spline = line.strip().split()
            if num == 0:
                self.version = line
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
                summary = text[num + 3].split() or text[num + 2].split()
                self.cell_reflections = summary[3] or 0
                self.cell_res_min_2t = summary[6] or 0.0
                self.cell_res_max_2t = summary[7] or 0.0
            if line.startswith('Frames were acquired'):
                """
                Frames were acquired with BIS 2018.9.0.3/05-Dec-2018 && APEX3_2018.7-2
                    Rescan threshold is 95% of A/D conversion range
                """
                self.aquire_software = 'Bruker ' + ' '.join(line.split()[4:])

    @property
    def cell_res_min_theta(self):
        return float(self.cell_res_min_2t) / 2.0

    @property
    def cell_res_max_theta(self):
        return float(self.cell_res_max_2t) / 2.0

    def __repr__(self):
        out = 'Version: {}\n'.format(self.version)
        out += 'Used Reflections: {}\n'.format(self.cell_reflections)
        out += 'min thata: {}\n'.format(self.cell_res_min_theta)
        out += 'max theta: {}\n'.format(self.cell_res_max_theta)
        out += 'min 2 theta: {}\n'.format(self.cell_res_min_2t)
        out += 'max 2 theta: {}\n'.format(self.cell_res_max_2t)
        if self.aquire_software:
            out += 'Aquire software: {}\n'.format(self.aquire_software)
        return out

if __name__ == "__main__":
    saint = SaintListFile('test-data/TB_fs20_v1_0m._ls')
    print(saint)

    print('#####')
    s = SaintListFile('test-data/Esser_JW316_01._ls')
    print(s)
