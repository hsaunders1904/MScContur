# -*- coding: utf-8 -*-
"""
Created on 29/06/18

@author: HarryS
"""

from scanning_functions import *


def run_scan(num_points, template_path, grid_pack, seed=101,
             output_dir='myscan00', sample_mode='uniform', rescan=False,
             param_file='param_file.dat', factor=None):
    """
    Run a scan over parameter space defined in param_file.dat using a
    given sampling mode and write relevant run cards and param files.

    Parameters
    ----------

    num_points: int
        Number of points to sample.

    template_paths: list
        List of template files (eg. LHC.in).

    grid_pack: str or None
        Path to directory containing the model grid pack.

    seed: int (default = 101)
        Seed for random number generator to get reproducibility.

    output_dir: str (default = 'myscan')
        Path to output scan results to.

    sample_mode: str ['uniform', 'random'] (default = 'uniform')
        The mode to sample in.
            Uniform: Sample points uniformly within parameter space. The
                     number of points sampled^(1/number of dimensions)
                     must be an integer.
            Random: Randomly sample the parameter space

    param_file: str (default = 'param_file.dat')
        Path to space seperated file containing parameters and their
        value ranges.
        Eg.
            Xm 50 100
            Y1 75 150

    rescan: str
        Path to a .map file containing a previous Contur run's results.

    """
    check_param_consistency(param_file, template_path)

    np.random.seed(seed)

    # Read in run card template files
    templates = read_template_file(template_path)

    # Param dict has parameter names as keys and then each item is a
    # dictionary with keys 'range' and 'values'
    param_dict = read_param_ranges(param_file)

    # Generate parameter values depending on sampling mode
    param_dict, num_points = generate_points(
        num_points, sample_mode, param_dict, map_file=rescan, factor=factor)
    make_directory(output_dir)
    for run_point in range(num_points):
        # Run point directories are inside the output directory and hold
        # the necessary files to run Herwig with the param_dict associated
        # with that point
        run_point_path = make_run_point_directory(run_point, output_dir)

        # Write params.dat file inside run point directory. This is purely to
        # record what the param_dict are at this run point
        write_param_file(param_dict, run_point_path, run_point)

        # Write run card template files formatted with parameter values
        write_template_files(templates, param_dict, run_point, run_point_path,
                             param_file)

        # Copy across all files in GridPack
        if grid_pack:
            copy_tree(grid_pack, run_point_path)

    # Write all sampled points and their run points to a .dat file
    write_sampled_points(output_dir)
