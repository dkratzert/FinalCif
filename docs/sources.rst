
Source code
===========


In case you want to play with the source code and make your own modifications to FinalCif, 
get the `code from Github <https://github.com/dkratzert/FinalCif>`_

In order to run FinalCif from the source code directly, you need to install only Python3 >= 3.6:
https://www.python.org/

Then clone the repository from GitHub:

.. code-block::

   git clone https://github.com/dkratzert/FinalCif.git
   cd FinalCif

Create a virtual environment and activate it:

.. code-block::

    C:\Python38\python3.exe -m venv venv
    
    venv\Scripts\activate.bat    

After activation, install all necessary packages using pip:

.. code-block::

    pip install -r requirements.txt

I am always open for suggestions by users. Please tell me if something does not work as expected!

FinalCif uses the great `gemmi cif parser <https://gemmi.readthedocs.io/en/latest/index.html>`_.
It needs `MSVC++ 14 <https://visualstudio.microsoft.com/de/vs/features/cplusplus>`_ in order to compile in Windows.
For Linux and MacOS, a regular installatin of the GCC compiler is sufficient.