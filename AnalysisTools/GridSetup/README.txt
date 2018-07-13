Instructions
============

The scanning and batch submitting is all done in the 'batch_submit_prof.py'
file.

batch_submit_prof.py
--------------------

- Must be called specifying the number of points to sample.

- You should check that the paths specified for variables 'herwig_setup' and
'contur_setup' point to the correct places.

- Reads parameter ranges from parameter file (usually called param_file.dat).
    --> Paramter file should be space separated with format:
        [paramter name] [min value] [max value]
        
- Will pick paramters inside the given ranges for the given number of points
and format the template file to include those parameters. Default sampling
mode is uniform but random is also available.

- Creates output directory (default is 'myscan', but any name can be specified
using the -o flag).

- Inside output directory n run point directories are created, numbered from 
0 to n.
    --> Each run point directory contains:
            - all files in the GridPack directory
            - the Herwig run card (the formatted template file)
            - params.dat file giving the parameter values used at that point
            - the shell script to submit to batch (runpoint_00xx.sh)

- The grid pack directory is by default 'GridPack' but any directory can be
specified using the -g flag. Or you can use '-g none' to not use one.

- If you only want to run a scan and not submit to batch (maybe to check it's 
running correctly after a change) you can use the -s or --scan_only flag.

'python batch_submit_prof.py --help' for more command line options.
