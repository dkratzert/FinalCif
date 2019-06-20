from pathlib import Path


class SaintListFile():
    def __init__(self, filename: str):
        self._fileobj = Path(filename)
        self.filename = self._fileobj.absolute()
        self.cell_reflections = 0
        self.cell_res_min_2t = 0.0
        self.cell_res_max_2t = 0.0
        self.version = ''
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
                """
                #print(text[num + 3])
                summary = text[num + 3].split()
                self.cell_reflections = summary[3]
                self.cell_res_min_2t = summary[6]
                self.cell_res_max_2t = summary[7]

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
        return out

if __name__ == "__main__":
    saint = SaintListFile('test-data/TB_fs20_v1_0m._ls')
    print(saint)
