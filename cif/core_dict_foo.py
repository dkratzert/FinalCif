import json
import pprint
from pathlib import Path

import gemmi


c = gemmi.cif.read_file('/Users/daniel/Downloads/cif_core.dic')
cdic = json.loads(c.as_json())

alldic = {}

for x in cdic.keys():
    if '_name' in cdic[x]:
        item = cdic[x]
        name = item['_name']
        if isinstance(item, dict):
            if isinstance(name, list):
                for n in name:
                    alldic[n] = ' '.join(cdic[x]['_definition'].split())
            else:
                alldic[name] = ' '.join(cdic[x]['_definition'].split())


pprint.pprint(alldic)

#Path('core_dict.py').write_text(pprint.pformat(alldic))
