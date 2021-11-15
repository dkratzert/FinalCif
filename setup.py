#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  dkratzert@gmx.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

from setuptools import setup, find_packages

from tools.version import VERSION

setup(
    name='FinalCif',
    version=str(VERSION),
    #packages=['cif', 'gui', 'tools', 'report', 'report.gui', 'datafiles', 'displaymol', 'icon', 'template'],
    packages=find_packages(),
    url='https://dkratzert.de/finalcif.html',
    license='Beerware',
    author='Daniel Kratzert',
    author_email='dkratzert@gmx.de',
    description='https://dkratzert.de/finalcif.html'
)
