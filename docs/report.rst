Report Document
===============

FinalCif is able to render a nice looking report document as MS Word format from the information contained in the CIF.
For a complete report, you have to finish the CIF first.
It is also advisable to deposit the file before the report generation in order to have the CCDC number
listed in the report text.

.. image:: pics/finalcif_report.png

CCDC Number
-----------
There are two ways of introducing the CCDC number into the .cif file:

* Click on the template 'CCDC Number' and insert the number into the '_database_code_depnum_ccdc_archive' field manually.
* Drag&Drop the deposition response email from the CCDC into the work folder and reload the .cif file.


Picture
-------
FinalCif can add an picture of your structure to the report document. 

* Either by previously performing an html check cif. Then it automatically adds a picture from the checkcif report, as in the example above.
* Or you can add any other picture with the "Picture for Tables" button.

Customizing the Report
----------------------

.. image:: pics/report_options.png
    :width: 600

Do you have specific expectations regarding the appearance of the structure report?
With self-defined templates this is possible in FinalCif. You can find example templates
at https://github.com/dkratzert/FinalCif. It is easier to change them than to create them from scratch.

The templates are an ordinary MS Word document (more specific: Office Open XML, https://de.wikipedia.org/wiki/Office_Open_XML)
So you can use them with MS Word, Openoffice or Libre Office abd others.

FinalCif uses the Jinja2 template language to exchange specific instructions in the templates with
values from the CIF file and other precalculated information.

In the templates, you have two different types of information to add:

A variable, starting with {{ and ending with }}, for example: {{ a_variable }}
This would insert the content of the variable at this point in the document during the report generation.

A block, starting with {% and ending with %}, for example 
| {% if a_variable %}} Put this text here {% endif %}

This would put the text enclosed in the block into the document depending if either a_variable is has a value or not.

| The second possibility for blocks is to iterate over values of a dictionary:
| {% for atom in atomlist %}
| {{ atom.label }}
| {% enfor %}

{%tr is used to generate table rows.

Data Available for the Report
-----------------------------

| 'cif'                   :  Gives you access to the full CIF information, use it like {{ cif._exptl_crystal_density_diffrn }}
| 'options'               : A dictionary with {'without_h': True, 'atoms_table': True, 'text': True, 'bonds_table': True},
| 'space_group'           : The space group formated as formula object
| 'structure_figure'      : a picture selected with the 'Picture for Report' button
| 'crystallization_method': The value of '_exptl_crystal_recrystallization_method'
| 'sum_formula'           : The formated version of '_chemical_formula_sum' with subscripted numbers
| 'itnum'                 : the space group number from the international tables
| 'crystal_size'          : The crystal size as X x Y x Z
| 'crystal_colour'        : The crystal colour
| 'crystal_shape'         : The crystal shape
| 'radiation'             : The radiation type used like MoK_alpha
| 'wavelength'            : The wavelength in nm
| 'theta_range'           : The theta range
| 'diffr_type'            : The measurement device type
| 'diffr_device'          : The measurement device
| 'diffr_source'          : The radiation source
| 'monochromator'         : The monochromator
| 'detector'              : The detector model
| 'lowtemp_dev'           : The low-temperature device
| 'index_ranges'          : The preformatted index ranges
| 'indepentent_refl'      : The number of independent reflections
| 'r_int'                 : The r_int of the data
| 'r_sigma'               : The r_sigma of the data
| 'completeness'          : The completeness of the data
| 'theta_full'            : The resolution of the dataset in degree theta
| 'data'                  : the value of '_refine_ls_number_reflns'
| 'restraints'            : The value of '_refine_ls_number_restraints'
| 'parameters'            : The value of '_refine_ls_number_parameters'
| 'goof'                  : The value of '_refine_ls_goodness_of_fit_ref'
| 'ls_R_factor_gt'        : The value of '_refine_ls_R_factor_gt'
| 'ls_wR_factor_gt'       : The value of '_refine_ls_wR_factor_gt'
| 'ls_R_factor_all'       : The value of '_refine_ls_R_factor_all'
| 'ls_wR_factor_ref'      : The value of '_refine_ls_wR_factor_ref'
| 'diff_dens_min'         : The minimum residual density in e/A^3
| 'diff_dens_max'         : The maximum residual density in e/A^3
| 'exti'                  : The extinction coefficient
| 'flack_x'               : The value of the flack X parameter
| 'integration_progr'     : The name of the integration program used
| 'abstype'               : The value of '_exptl_absorpt_correction_type'
| 'abs_details'           : The name of the absortion correction program used
| 'solution_method'       : The structure solution method used
| 'solution_program'      : The name of the structure solution program
| 'refinement_prog'       : The name of the refinement program
| 'atomic_coordinates'    : The atomic coordinates
| 'bonds'                 : The bonds with lengths
| 'angles'                : The bond angles
| 'ba_symminfo'           : The symmetry operations used to generate equivalent atoms in the angles list
| 'torsions'              : The torsion angles
| 'torsion_symminfo'      : The symmetry operations used to generate equivalent atoms in the torsion angles list
| 'hydrogen_bonds'        : The hydrogen bonds (in case there are some defined with HTAB)
| 'hydrogen_symminfo'     : The symmetry operations used to generate equivalent atoms in the hydrogen bonds list
| 'literature'            : A list of citations to the above used programs


**This information from the 'cif' variable can also be useful:**
| res_file_data             : The SHELX res file text
| is_centrosymm             : It true if the space group of the structure is centrosymmetric
| atoms                     : The list of atoms with 'label', 'type', 'x', 'y', 'z', 'part', 'occ', 'u_eq'
| hydrogen_atoms_present    : Is true if hydrogen atoms are present in the structure
| disorder_present          : Is true if atoms in parts are present in the structure
| cell                      : The unit cell
| bonds                     : The list of bonds as 'label1', 'label2', 'dist', 'symm'
| angles                    : The list of angles as 'label1', 'label2', 'label3', 'angle_val', 'symm1', 'symm2'
| torsion_angles            : The list of torsion angles as 'label1', 'label2', 'label3', 'label4', 'torsang', 'symm1', 'symm2', 'symm3', 'symm4'
| hydrogen_bonds            : The list of hydrogen atoms involved in HTAB listings as 'label_d', 'label_h', 'label_a', 'dist_dh', 'dist_ha', 'dist_da', 'angle_dha', 'symm'
| test_res_checksum         : True if the checksum of the SHELX .res file fits to the file content.
| test_hkl_checksum         : True if the checksum of the SHELX .hkl file fits to the file content.

The above is not limited to the templates of FinalCif. It is also possible to insert template tags into any other Word document and replace them with values from a CIF file. There are no limits to the imagination.


Further information for programmers:
`https://docxtpl.readthedocs.io/en/latest/ <https://docxtpl.readthedocs.io/en/latest/>`_