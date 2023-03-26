=============
Installation
=============

Windows
--------
Start the installer (FinalCif-setup-x64-vXX.exe) and click next until finished.

Linux
-----

Thanks to Andrius Merkys, Debian and Ubuntu have FinalCif in their official distribution.


Any System
----------

Alternatively, there is a pypi package for FinalCif:

Since version 118, there is a `pypi <https://pypi.org/project/finalcif>`_ package for installation in a Python environment.
Do the following steps in order to install and run FinalCif in any Python environment:

.. code-block::

    >> python -m venv venv        <-- creates a virtual environment
    >> source venv/bin/activate   (Windows: venv\Scripts\activate.bat)  <-- Activates the environment
    >> pip install finalcif
    >> finalcif

Next time, only

.. code-block::

    >> source venv/bin/activate   (Windows: venv\Scripts\activate.bat)
    >> finalcif
is necessary.