.. _document-sources:

========================
Running from Source Code
========================


In case you want to play with the source code and make your own modifications to FinalCif,
get the `code from GitHub <https://github.com/dkratzert/FinalCif>`_.

In order to run FinalCif from the source code directly, you need Python >= 3.12:
https://www.python.org/

The recommended way to manage dependencies is `uv <https://docs.astral.sh/uv/>`_.


Quick start with uv
--------------------

Clone the repository and install all dependencies:

.. code-block:: bash

    git clone https://github.com/dkratzert/FinalCif.git
    cd FinalCif
    uv sync --all-extras --dev

Compile the UI files (needed after changes to .ui files):

.. code-block:: bash

    uv run python scripts/compile_ui_files.py

Run FinalCif:

.. code-block:: bash

    uv run finalcif

Run the tests:

.. code-block:: bash

    QT_QPA_PLATFORM=offscreen uv run pytest tests/

On Linux, you may need to install system packages for the Qt platform plugin:

.. code-block:: bash

    sudo apt install libegl1 libgl1 libxkbcommon0


Manual install with pip
-----------------------

Clone the repository from GitHub:

.. code-block:: bash

   git clone https://github.com/dkratzert/FinalCif.git
   cd FinalCif

Create and activate a virtual environment:

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate.bat

Install the package in development mode:

.. code-block:: bash

    pip install -e ".[dev]"

Compile the UI files:

.. code-block:: bash

    python scripts/compile_ui_files.py

Run FinalCif:

.. code-block:: bash

    finalcif

I am always open for suggestions by users. Please tell me if something does not work as expected!

FinalCif uses the great `gemmi CIF parser <https://gemmi.readthedocs.io/en/latest/index.html>`_ for all CIF reading
and writing operations.