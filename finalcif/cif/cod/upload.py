#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------

import requests

from finalcif import VERSION


def upload_cif(deposit_url, data, files):
    # pprint(data)
    # pprint(files)
    r = requests.post(deposit_url, data=data, files=files, headers={'User-Agent': 'FinalCif/{}'.format(VERSION)})
    return r
