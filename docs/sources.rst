========================
Running from Source Code
========================


In case you want to play with the source code and make your own modifications to FinalCif, 
get the `code from Github <https://github.com/dkratzert/FinalCif>`_

In order to run FinalCif from the source code directly, you need to install only Python3 >= 3.7:
https://www.python.org/

For Ubuntu, there is an installer script that makes all steps necessary for installation automatically:

First go into the directory where you like to have FinalCif:

cd /home/username/

Load the script:
wget https://raw.githubusercontent.com/dkratzert/FinalCif/master/scripts/finalcif-start.sh

Make it executable:
chmod u+x ./finalcif-start.sh

Install Python3.9:
./finalcif-start.sh -pyinst

Install FinalCif:
./finalcif-start.sh -install

Run FinalCif:
./finalcif-start.sh


Manual install
--------------

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

FinalCif uses the great `gemmi cif parser <https://gemmi.readthedocs.io/en/latest/index.html>`_ for all CIF reading
and writing operations.