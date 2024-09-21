.. FinalCif documentation master file, created by
   sphinx-quickstart on Fri Apr 17 19:57:46 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========
FinalCif
========

Usually, CIF files need some extra tedious work to get them ready for publication.
Finalcif tries to collects all the information from a work folder needed in order
to finalize a CIF file for publication. But also information that is not at hand automatically
can be filled in conveniently.
In ideal cases, it takes one click to have a publication-ready file. But check the file
thoroughly afterwards, no software is perfect!

Since the end of 2024, a special version of FinalCif has been available within APEX, part of the
Bruker software suite. Instead of gathering information from the work folder, this version directly
accesses the APEX database to complete the CIF data. Therefore, if you're using APEX, it's recommended
to do all your work within APEX to ensure all information is centrally and fully available.
The work from one computer can be easily transferred to another by either archiving and restoring the respective
sample as a .zip file within APEX, or by importing the [sample name].xml file from each frames folder.



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

