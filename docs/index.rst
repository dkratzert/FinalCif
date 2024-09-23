.. FinalCif documentation master file, created by
   sphinx-quickstart on Fri Apr 17 19:57:46 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
FinalCif
========

FinalCIF simplifies the process of preparing CIF files for publication, which usually involves
tedious manual work. It automatically gathers necessary information from the work folder,
but also allows for easy manual input of missing details. In ideal cases, it takes just one
click to create a publication-ready file—though it’s always wise to review the file afterwards.
No software is flawless!

.. _available_APEX: https://www.youtube.com/watch?v=XihJ9t_rTPY
.. |available_APEX| replace:: **available within APEX**

Since the end of 2024, a special version of FinalCif has been |available_APEX|_, part of the
Bruker software suite. Instead of gathering information from the work folder, this version directly
accesses the APEX database to complete the CIF data. Therefore, if you're using APEX, it's recommended
to do all your work within APEX to ensure all information is centrally and fully available.
Despite its integration with APEX, this version of FinalCif will remain independent of Bruker AXS.
It will continue to support CIF files from any other company's software as well.

Transferring work between two APEX computers is simple—either archive and restore the sample as a .zip
file within APEX, or import the [sample name].xml file from the frames folder. They contain every database
information of a sample.





`Back to the FinalCif home page <https://dkratzert.de/finalcif.html>`_


.. toctree::

   description
   install
   templates
   loops
   checkcif
   report
   deposition
   sources
   homepage

