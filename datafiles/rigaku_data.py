from pathlib import Path

import gemmi

loop_crystal_faces = ['_exptl_crystal_face', ['_index_h', '_index_k', '_index_l', '_perp_dist']]
loop_oxdiff_faces = ['_exptl_oxdiff_crystal_face', ['_indexfrac_h', '_indexfrac_k', '_indexfrac_l', '_x', '_y', '_z']]


class RigakuData():

    def __init__(self, cifod: Path):
        self.fileobj = cifod
        self.filename = cifod.name
        self.open_cif()
        self.sources = {}
        print('Reading {}'.format(str(self.fileobj.absolute())))
        self.exclude_keys = [
            '_cell_length_a',
            '_cell_length_b',
            '_cell_length_c',
            '_cell_angle_alpha',
            '_cell_angle_beta',
            '_cell_angle_gamma',
            '_space_group_IT_number',
            '_space_group_crystal_system',
            '_space_group_name_H-M_alt',
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
        print('Getting data from .cif_od file.')
        #self.sources['_oxdiff_exptl_absorpt_empirical_details'] = ('', '')
        #self.sources['_diffrn_measurement_details'] = ('', '')
        for item in self.block:
            if item.pair is not None:
                key, value = item.pair
                if key not in self.exclude_keys:
                    # print(key, gemmi.cif.as_string(value))
                    self.sources[key] = (gemmi.cif.as_string(value), self.fileobj.name)
            # loops currently dont work:
            '''if item.loop is not None:
                print('loop')
                tags = item.loop.tags
                table = self.block.find(tags)
                loop = []
                loop.append([tag for tag in tags])
                #print([tag for tag in tags])
                #print('table columns, rows:', table.width(), len(table))
                row = [x for x in table]
                for r in row:
                    print([x for x in r])
                    loop.append([x for x in r])
                print(loop)
                self.loops.append(loop)'''
