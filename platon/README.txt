
THIS RESEARCH PROGRAM MAY BE USED FREE OF CHARGE FOR USE WITHIN THE
ACADEMIC COMMUNITY AND NOT FOR PROFIT WITHOUT EXPLICIT PERMISSION.
COMMERCIAL USERS SHOULD APPLY BY FILLING OUT AN APPLICATION FORM.
https://www.platonsoft.nl/platon/applform.pdf
IT IS TO BE UNDERSTOOD THAT THE AUTHOR OR HIS UNIVERSITY CANNOT BE
HELD RESPONSIBLE FOR ANY PROBLEMS CAUSED BY ERRORS IN THE CODE.
PLEASE REPORT ENCOUNTERED ISSUES TO ITS AUTHOR WITH ASSOCIATED DATA



This directory contains a special 'command-line only' PLATON version
=====================================================================
(not for general distribution ! useful only for structure validation
as part of Bruker Software.)

Static LINUX executable : platon_special_linux

Linux Compilation Instructions (or use compiled version):

- copy the files platon.f, zs2057.cif and zs2057.fcf
  to a new directory, e.g. /usr/local/platon

- Compile: gfortran -static -o platon platon.f 

- Copy the platon executable to a globally accessible location
  e.g. /usr/local/bin

- run structure validation from the command line with either

  platon -u zs2057.cif or platon -U zs2057.cif 

  the validation result in on the files zs2057.chk and zs2057.ckf

- Example validation output is in this directory

- Documentation can be found in CIF-VALIDATION.pdf and FCF-VALIDATION.pdf
  
Version 26/06/15

