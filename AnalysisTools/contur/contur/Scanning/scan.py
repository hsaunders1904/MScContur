# -*- coding: utf-8 -*-
"""
Created on 29/06/18

@author: HarryS
"""

from scanning_functions import *


def run_scan(param_dict, args):
    """
    Given points defined in param_dict run create run point directories
    and populate with Herwig .in file and params.dat file.

    Parameters
    ----------

    param_dict: dict
        Dictionary with parameter names as keys each containing another
        dictionary with keys 'range' and 'values'.

    args: argparse.Namespace object
        Argparse object with attributes containing command line options.

    Returns
    -------

    None

    """

    # Read in run card template files
    template = read_template_file(args.template_file)

    make_directory(args.out_dir)
    for run_point in range(args.num_points):
        # Run point directories are inside the output directory and hold
        # the necessary files to run Herwig with the param_dict associated
        # with that point
        run_point_path = make_run_point_directory(run_point, args.out_dir)

        # Write params.dat file inside run point directory. This is purely to
        # record what the param_dict are at this run point
        write_param_file(param_dict, run_point_path, run_point)

        # Write run card template files formatted with parameter values
        write_template_files(template, param_dict, run_point,
                             run_point_path, args.param_file)

    # Write all sampled points and their run points to a .dat file
    write_sampled_points(args.out_dir)
