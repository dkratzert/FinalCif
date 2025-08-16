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

