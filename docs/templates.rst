Templates
=========

FinalCif uses three different kinds of templates to simplify recurring tasks:

* Large text templates
    Each editable text field in the main table can hold text snippets as templates for reoccurring texts.
    The text template editor opens with a right-click on "Text Template" in the main table.
    This opens a new page where the first line shows the CIF key from the row of the previous mouse click.
    In the large text field below, you can type any text and apply it with the "Apply Text" button,
    or you compose any kind of text snippets in the input fields below.
    These fields can be saved with the "Save as Template" button. A saved template is indicated with
    light-blue background color in the respective edit field of the main table.

.. image:: pics/text_templates.png

The template editor for large text snippets.

    After you saved something as template, it will be loaded again on the next "Text Template"
    click on this same CIF key row. The trick here is that you can click the checkboxes before
    each text snippet to append the text of it to the "combined Text" field in click order.
    As any other templates in FinalCif, you can export/import them to CIF files.
    "Delete Template" deletes it from the configuration and will not show up again.
    So large text templates are usable either as a comfortable text editor and/or as template manager.


* Equipment and Author templates
    They are useful for definitions of parameters like the properties of a measurement device
    or the name and address of the crystallographer. Apply template by double-clicking on one row.
* Property templates
    Property templates define possible dropdown-menus for common CIF keywords like _cell_measurement_temperature.
    The template values are accessible as a dropdown behind the respective key in the main table of FinalCif.

.. image:: pics/templates.png

The templates selection and editor.

Templates can be edited anytime and they can be saved as a CIF file. You can use them for any cif keyword.
Just be creative...

.. image:: pics/property_templates.png

Template editor for crystallization methods.

For example the crystallographer information:

.. image:: pics/equipment_templates.png

Crystallographer details template.

Or just one keyword for only the absolute configuration information:

.. image:: pics/absolute_configuration.png

Absolute configuration template.


Sidenotes
---------

* As any other CIF, in order to import a template, it needs a \data_ keyword at the start.

* Templates may be multi-CIFs with multiple data\_ kewords for e.g. multiple machine definitions in one file.

