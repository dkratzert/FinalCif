#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------
import urllib3

mainurl = "https://xs3-data.uni-freiburg.de/finalcif/"


def get_current_version():
    http = urllib3.PoolManager()
    r = http.request('GET', '{}version.txt'.format(mainurl))
    if r.status == 200:
        return int(r.data.decode('ascii'))
    else:
        return 0


if __name__ == '__main__':
    v = get_current_version()
    print(v)
