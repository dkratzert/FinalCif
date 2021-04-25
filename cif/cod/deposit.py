from pathlib import Path
from pprint import pprint

import requests

from cif.cif_file_io import CifContainer

cif = CifContainer('/Users/daniel/Downloads/4315921.cif')

fileobj = open(cif.fileobj.absolute(), 'rb')


#url = 'https://www.crystallography.net/cod/cgi-bin/cif-deposit.pl'
url = 'https://www.crystallography.net/cod-test/cgi-bin/cif-deposit.pl'
test_url = 'https://www.crystallography.net/cod-test/cgi-bin/cif-deposit.pl'

data = {'username'       : Path('/Users/daniel/cod_username.txt').read_text(encoding='ascii'),
        'password'       : Path('/Users/daniel/cod_password.txt').read_text(encoding='ascii'),
        'user_email'     : 'dkratzert@gmx.de',
        'deposition_type': 'published',
        'author_name'    : 'Daniel Kratzert',
        'author_email'   : 'dkratzert@gmx.de',
        'output_mode'    : 'stdout',
        'filename'       : cif.fileobj.name,
        }

files = {'cif': fileobj}

if __name__ == '__main__':
    x = requests.post(test_url, files=files, data=data)
    print(x.text)
    # print(x.content)
    # print(x.headers)
    #pprint(x.request.headers)
    #pprint(x.request.body)
    print(x.status_code)
    fileobj.close()

