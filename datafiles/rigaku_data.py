from pathlib import Path

import gemmi


class RigakuData():

    def __init__(self, cifod: Path):
        self.fileobj = cifod
        self.filename = cifod.name
        self.open_cif()
        self.sources = {}
        self.exclude_keys = [
            '_cell_length_a',
            '_cell_length_b',
            '_cell_length_c',
            '_cell_angle_alpha',
            '_cell_angle_beta',
            '_cell_angle_gamma',
        ]
        self.loops = []
        self.get_sources()

    def open_cif(self):
        try:
            self.doc = gemmi.cif.read_file(str(self.fileobj.absolute()))
            self.block = self.doc.sole_block()
        except Exception as e:
            print('Unable to read file:', e)
            raise

    def __getitem__(self, item):
        result = self.block.find_value(item)
        return result if result else ''

    def get_sources(self):
        for item in self.block:
            if item.pair is not None:
                key, value = item.pair
                if key not in self.exclude_keys:
                    self.sources[key.lower()] = (gemmi.cif.as_string(value), self.fileobj.name)

            if item.loop is not None:
                tags = item.loop.tags
                table = self.block.find(tags)
                loop = []
                loop.append([tag for tag in tags])
                #print([tag for tag in tags])
                #print('table columns, rows:', table.width(), len(table))
                row = [x for x in table]
                for r in row:
                    #print([x for x in r])
                    loop.append([x for x in r])
                #print(loop)
                self.loops.append(loop)
