# Running a Batch Job

Submit a batch job in order to generate heat maps by running:

    $ python batch_submit_prof.py number_of_points [options]

## batch_submit_prof.py

- Must be called specifying the number of points to sample.

- You should check that the paths specified for variables 'herwig_setup' and
'contur_setup' at the top of the script point to the correct places.

- Reads parameter ranges from parameter file (usually called param_file.dat).

    - Paramter file should be space separated with format:
    
        `[paramter name] [min value] [max value]`
        
- Will pick paramters inside the given ranges for the given number of points
and format the template file to include those parameters. Default sampling
mode is uniform but random is also available.

- Creates output directory (default is 'myscan', but any name can be specified
using the `-o` flag).

- Inside output directory n run point directories are created, numbered from 
0 to n.

    Each run point directory contains:
    
    - all files in the GridPack directory
            
    - the Herwig run card (the formatted template file)
    - params.dat file giving the parameter values used at that point
    - the shell script to submit to batch (runpoint_00xx.sh)

- The grid pack directory is by default 'GridPack' but any directory can be
specified using the `-g` flag. Or you can use `-g none` to not use one.

- If you only want to run a scan and not submit to batch (maybe to check it's 
running correctly after a change) you can use the `-s` or `--scan_only` flag.

`$ python batch_submit_prof.py --help` for more command line options.


## Testing

- To run tests, simply run, in the terminal in the same directory as this file.

	`$ pytest`
   

- There are 4 test modules, two test your run environment the others are unit 
  tests for batch_submit_prof:

    - tests/test_environment.py: This will run tests to make sure your 
      environment is set up correctly, i.e. correct paths are in your system 
      and python path. 

    - tests/test_grid.py: This will test your GridPack directory throwing 
      errors if it is not compiled properly. It also checks your param_file.dat
      file is formatted correctly.

    - tests/test_scanning_functions.py: Unit tests for scanning_funtions.py.

    - tests/test_batch_submit.py: Unit tests for batch_submit_prof.py. Checks 
      all the correct files are produced etc.
      
- If you only want to run, say tests in 'test_grid.py', you can specify this
  using pytest's `-k` flag:
  
    `$ pytest -k test_grid`
    
  This searches for test functions whose strings match the given argument. So
  individual test functions can also be run this way.

