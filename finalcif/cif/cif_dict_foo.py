import json
import pprint
from pathlib import Path
from xml.sax.saxutils import escape as escape

import gemmi


def format_definition(definition: str):
    # Removes space characters in front of each line.
    newdef = ''
    padding = 13
    for n, line in enumerate(definition.splitlines(keepends=True)):
        # Remove the spaces at start:
        if len(line) > (padding - 1) and not line[:padding].strip():
            if n:
                line = line[padding + 1:]
            else:
                line = line[padding:]
        newdef += line
    return newdef


def process_cif_dict(cdic):
    """
    Creates a dictionary with cif keywords as key and help text as value.
    """
    alldic = {}
    for x in cdic.keys():
        if '_name' in cdic[x]:
            item = cdic[x]
            name = item['_name']
            if isinstance(item, dict) and not '[]' in name:
                definition = escape(item['_definition'])
                example = item.get('_example', '')
                example_detail = item.get('_example_detail', '')
                enumeration = item.get('_enumeration', '')
                enumeration_detail = item.get('_enumeration_detail', '')
                if example:
                    if isinstance(example, list) and not enumeration_detail:
                        example = '\n'.join([str(x) for x in example])
                    if isinstance(example, list) and enumeration_detail:
                        example = '\n'.join(
                            ["{}\t\t{}\n".format(str(x), str(y)) for x, y in zip(example, example_detail)])
                    example = format_definition(escape(str(example)))
                    definition = '{}\n\n<h3>Example:</h3>\n{}'.format(definition, example)
                if enumeration:
                    if isinstance(enumeration, list) and not enumeration_detail:
                        enumeration = '\n'.join([str(x) for x in enumeration])
                    if isinstance(enumeration, list) and enumeration_detail:
                        enumeration = '\n'.join(
                            ["{}\n\t{}\n".format(str(x), str(y)) for x, y in zip(enumeration, enumeration_detail)])
                    enumeration = format_definition(escape(str(enumeration)))
                    definition = '{}\n\n<h3>Example:</h3>\n{}'.format(definition, enumeration)
                if isinstance(name, list):
                    for n in name:
                        # For keys like 'atom_site_aniso_b_[]' where the name has several subnames:
                        alldic[n] = '<pre><h2>{}</h2>{}</pre>'.format(n, format_definition(definition))
                else:
                    alldic[name] = '<pre><h2>{}</h2>{}</pre>'.format(name, format_definition(definition))
    return alldic


def load_cif_as_dictionary(link, path_to_cif):
    if not path_to_cif.exists():
        get_dictionary_cif(link, path_to_cif)
    c = gemmi.cif.read_file(str(path_to_cif))
    cdic = json.loads(c.as_json())
    return cdic


def get_dictionary_cif(link, path_to_cif):
    import requests
    r = requests.get(link, timeout=10)
    path_to_cif.write_text(r.text)


if __name__ == '__main__':
    main_path = Path.home()

    core_path = main_path.joinpath('cif_core.dic.txt')
    twin_path = main_path.joinpath('cif_twinning.dic.txt')
    modulation_path = main_path.joinpath('cif_modulation.dic.txt')
    powder_path = main_path.joinpath('cif_powder.dic.txt')
    restraints_path = main_path.joinpath('cif_restraints.dic.txt')

    core_link = 'https://www.iucr.org/__data/iucr/cif/dictionaries/cif_core_2.4.5.dic'
    twin_link = 'https://www.iucr.org/__data/iucr/cif/dictionaries/cif_twinning_1.0.dic'
    modulation_link = 'https://www.iucr.org/__data/iucr/cif/dictionaries/cif_ms_1.0.1.dic'
    powder_link = 'https://www.iucr.org/__data/iucr/cif/dictionaries/cif_pd_1.0.1.dic'
    restraints_link = 'https://www.iucr.org/__data/iucr/cif/dictionaries/cif_core_restraints_1.0.dic'

    print('Downloading core dictionary')
    core_dic = load_cif_as_dictionary(link=core_link, path_to_cif=core_path)
    print('Downloading twin dictionary')
    twin_dic = load_cif_as_dictionary(link=twin_link, path_to_cif=twin_path)
    print('Downloading modulation dictionary')
    modulation_dic = load_cif_as_dictionary(link=modulation_link, path_to_cif=modulation_path)
    print('Downloading powder dictionary')
    powder_dic = load_cif_as_dictionary(link=powder_link, path_to_cif=powder_path)
    print('Downloading restraints dictionary')
    restraints_dic = load_cif_as_dictionary(link=restraints_link, path_to_cif=restraints_path)

    core_results = process_cif_dict(core_dic)
    twin_results = process_cif_dict(twin_dic)
    mod_results = process_cif_dict(modulation_dic)
    powder_results = process_cif_dict(powder_dic)
    restraints_results = process_cif_dict(restraints_dic)

    # pprint.pprint(core_results)

    Path('finalcif/cif/core_dict.py').write_text(r"cif_core = " + pprint.pformat(core_results, width=100))
    Path('finalcif/cif/twin_dict.py').write_text(r"twinning_dict = " + pprint.pformat(twin_results, width=100))
    Path('finalcif/cif/modulation_dict.py').write_text(r"modulation_dict = " + pprint.pformat(mod_results, width=100))
    Path('finalcif/cif/powder_dict.py').write_text(r"powder_dict = " + pprint.pformat(powder_results, width=100))
    Path('finalcif/cif/restraints_dict.py').write_text(
        r"restraints_dict = " + pprint.pformat(restraints_results, width=100))
