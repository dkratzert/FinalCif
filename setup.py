#  ----------------------------------------------------------------------------
#  "THE BEER-WARE LICENSE" (Revision 42):
#  daniel.kratzert@ac.uni-freiburg.de> wrote this file.  As long as you retain
#  this notice you can do whatever you want with this stuff. If we meet some day,
#  and you think this stuff is worth it, you can buy me a beer in return.
#  Dr. Daniel Kratzert
#  ----------------------------------------------------------------------------

from setuptools import setup

setup(
    name='FinalCif',
    version='41',
    packages=['cif', 'gui', 'tools', 'report', 'report.gui', 'datafiles'],
    url='https://www.xs3.uni-freiburg.de/research/finalcif',
    license='Beerware',
    author='Daniel Kratzert',
    author_email='daniel.kratzert@ac.uni-freiburg.de',
    description='https://www.xs3.uni-freiburg.de/research/finalcif'
)
