.. _document-sources:

========================
Running from Source Code
========================


In case you want to play with the source code and make your own modifications to FinalCif, 
get the `code from Github <https://github.com/dkratzert/FinalCif>`_.

In order to run FinalCif from the source code directly, you need to install Python3 >= 3.7 but >= 3.9 is advisable:
https://www.python.org/

Until now, I was just too lazy to build proper Linux packages and therefore only single-file executables
made with `pyinstaller <https://www.pyinstaller.org/>` exist. They are large and run sub-optimal in different
Linux distributions.

But for Ubuntu, there is an installer script that does all steps necessary for an installation from source automatically.
Apart from the Python installation, the script should work in any Linux or MacOS distribution:

First go into the directory where you like to have FinalCif, e.g.:

.. code-block:: bat

    cd /home/username/Downloads

Load the script:

.. code-block:: bat

    wget https://raw.githubusercontent.com/dkratzert/FinalCif/master/scripts/finalcif-start.sh

Make it executable:

.. code-block:: bat

    chmod u+x ./finalcif-start.sh

Install Python3.9:

.. code-block:: bat

    ./finalcif-start.sh -pyinst

Install FinalCif:

.. code-block:: bat

    ./finalcif-start.sh -install

Run FinalCif:

.. code-block:: bat

    ./finalcif-start.sh


Manual install from source
--------------------------

Clone the repository from GitHub:

.. code-block:: bat

   git clone https://github.com/dkratzert/FinalCif.git
   cd FinalCif

Create a virtual environment and activate it:

.. code-block:: bat

    C:\Python39\python3.exe -m venv venv
    venv\Scripts\activate.bat
    (in Linux: source venv/bin/activate)

After activation, install all necessary packages using pip:

.. code-block:: bat

    pip install -r requirements.txt


I am always open for suggestions by users. Please tell me if something does not work as expected!

FinalCif uses the great `gemmi CIF parser <https://gemmi.readthedocs.io/en/latest/index.html>`_ for all CIF reading
and writing operations.