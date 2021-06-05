import requests

from cif.cod.parser import MyCODStructuresParser

"""
TODO: save table in settings and resfresh it during each COD login. Otherwise use token.
"""


class CODFetcher():
    def __init__(self, main_url: str = 'https://www.crystallography.net/cod-test/'):
        self._url = main_url + 'my_depositions.php'
        self.table_html = ''

    def get_token(self, username: str, password: str):
        post_data = {'username': username,
                     'password': password}
        r = requests.post(self._url, data=post_data)
        return self._extract_token(r.text)

    def get_table_data_by_token(self, token: str):
        post = {
            'CODSESSION': token,
        }
        r = requests.post(url=self._url, data=post)
        self.table_html = r.text

    def _extract_token(self, text: str, token=''):
        for line in text.splitlines():
            if 'CODSESSION' in line and '=' in line:
                token = line.split('=')[-1].split('"')[0]
                break
        return token


if __name__ == '__main__':
    f = CODFetcher()
    token = f.get_token(username='', password='')
    # print(token)
    f.get_table_data_by_token(token)
    p = MyCODStructuresParser()
    p.feed(f.table_html)
    print(p)
    print(p.token)
