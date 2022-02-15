#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Daniel Kratzert <dkratzert@gmx.de> wrote this file.  As long as you retain
#   this notice you can do whatever you want with this stuff. If we meet some day,
#   and you think this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
import sys
from shutil import which

addr = """Albert-Ludwigs-Universität Freiburg
Institut für Anorganische und Analytische Chemie
Albertstraße 21
Freiburg i. Br.
79104
Germany"""


def get_platon_exe() -> str:
    if sys.platform.startswith('win'):
        platon_exe = r'C:\pwt\platon.exe'
    else:
        platon_exe = which('platon')
    return platon_exe