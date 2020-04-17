FinalCif
========

Finalize CIF files without hassle.

Essentially, you must have the corresponding CIF file for FinalCif in its original 'work' folder, which contains
all other files such as SAINT list files, SADABS list file, SHELX list files, etc. that led to this cif file.
The main table of FinalCif has three columns. The most left contains the information from the .cif file. Data from
other sources like the .p4p file is displayed in the middle column and user information can be put into the right-most
column. The data typed by the user always rules out the other information. The two different templates on the left
can be used to fill in author information or machine models (top) as well as to create dropdown menus for specific
CIF keywords (bottom). Any keyword not already in the CIF file will be added by the template. In the dropdown menus,
you can be creative to specify the crystallization conditions with a template...
The CIF keywords with a question mark as value are at the beginning of the table and the keywords with values are below.
Various possibilities of Checkcif are available, online with html or pdf result and offline.
The button "save cif file" saves the current file under 'name'-finalcif.cif. FinalCif will never make Changes to the
original CIF file.
The FinalCif executable accepts a file name as first argument in order to open .cif files from
other programs like ShelXle.

# TODO:
.. image:: picture.png

**A workflow example**


* Open a cif file in a work folder.
* Check and edit the remaining items.
* Do a html checkcif (it also saves an image for the report). Probaly correct last items like the moiety formula and  explain alerts with the validation response form editor in the same window.
* Do a pdf checkcif
* Submit the CIF to the CCDC
* Drag&drop the CCDC deposit reply email into the work folder
* Click on „Make Tables“
