import requests

from finalcif.cif.cod.website_parser import MyCODStructuresParser

"""
TODO: save table in settings and resfresh it during each COD login. Otherwise use token.
"""


class CODFetcher:
    def __init__(self, main_url: str):
        self.table_html = ''
        self.main_url = main_url
        self.authenticated = False

    @property
    def _url(self) -> str:
        return self.main_url + 'my_depositions.php'

    def get_token(self, username: str, password: str) -> str:
        post_data = {'username': username,
                     'password': password}
        try:
            r = requests.post(self._url, data=post_data)
        except requests.exceptions.ConnectionError as e:
            print(f'Getting auth token failed: {e}')
            return ''
        return self._extract_token(r.text)

    def get_table_data_by_token(self, token: str) -> None:
        post = {
            'CODSESSION': token,
        }
        try:
            r = requests.post(url=self._url, data=post)
        except requests.exceptions.ConnectionError:
            return None
        self.table_html = r.text

    def _extract_token(self, text: str, token: str = '') -> str:
        for line in text.splitlines():
            if "Deposited structures" in line:
                self.authenticated = True
            if 'CODSESSION' in line and '=' in line:
                token = line.split('=')[-1].split('"')[0]
                break
        return token


if __name__ == '__main__':
    f = CODFetcher(main_url='https://www.crystallography.net/cod/')
    token = f.get_token(username='', password='')
    # print(token)
    f.get_table_data_by_token(token)
    p = MyCODStructuresParser()
    p.feed(f.table_html)
    print(p)
    print(p.token)
