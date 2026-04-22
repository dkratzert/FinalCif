=======
Options
=======

FinalCif has a configuration page accessible via the "Options" button. The options are
automatically saved and restored between sessions using a JSON file in the platform-specific
configuration directory.


General Options
---------------

The general options control the behavior of the report generation:

* **Without hydrogen atoms** – If checked, hydrogen atoms are omitted from the bonds and angles tables
  in the report document.
* **Without report text** – If checked, the report document will contain only the tables and no
  descriptive text.
* **ADP table** – If checked, the anisotropic displacement parameters table is included in the
  report document.
* **Use picometers** – If checked, all distances in the report are given in picometers instead of
  Ångströms and the unit cell volume is given in cubic nanometers.
* **Picture width** – The width of the structure picture in the report document (in centimeters).
* **Track changes** – If checked, FinalCif writes a separate CIF file tracking all changes
  made to the original CIF. This can be useful to quickly return to a previous state when
  starting from scratch.
* **Check for CSD duplicates** – If checked, CheckCIF online will also search the Cambridge Structural
  Database for duplicate structures.
* **Global font size** – Adjusts the font size used throughout the application. This setting
  is available in the main window via a spin box. Set it to 0 to use the system default.


CIF Output Order
----------------

The CIF output order page lets you control the order of CIF keywords in the saved CIF file.
This is accessible via the "CIF Order" button on the options page. The list shows all known CIF
keywords and can be rearranged by drag and drop. Essential keywords are highlighted.

You can import an ordering from an existing CIF file or export the current ordering to a CIF file.
The "Reset to defaults" button restores the built-in ordering. The CIF keyword order is also
stored in the templates export file, so it can be shared between installations.


Server URLs
-----------

Two server URLs can be configured:

* **CheckCIF server URL** – The URL of the IUCr CheckCIF server. The default is
  ``https://checkcif.iucr.org/cgi-bin/checkcif_hkl.pl``. Change this only if the IUCr changes
  the server address.
* **COD server URL** – The URL of the Crystallography Open Database upload server. The default is
  ``https://www.crystallography.net/cod/cgi-bin/cif-deposit.pl``.


Report Templates
----------------

The options page also provides a list of report templates. Report templates are Word documents
that control the layout and content of the generated report. See the :doc:`report` chapter
for details on how to create and use report templates.


Property Templates
------------------

Property templates define dropdown menus for common CIF keywords. They are located on the
options page. See the :doc:`templates` chapter for details.


Export and Import of All Templates
-----------------------------------

The "Export All Templates" and "Import All Templates" buttons on the options page allow you to
save and restore all templates (equipment, property, text, author and CIF order) at once.
Templates are exported as a JSON file, which can be shared between installations.
For backward compatibility, legacy files saved in the older pickle format (.dat) can still be imported.

