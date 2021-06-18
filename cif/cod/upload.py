import requests

from tools.version import VERSION


def upload_cif(deposit_url, data, files):
    r = requests.post(deposit_url, data=data, files=files, headers={'User-Agent': 'FinalCif/{}'.format(VERSION)})
    return r
