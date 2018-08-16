#!/usr/bin/env python

import os
import subprocess
import numpy as np
from argparse import ArgumentParser

from contur.Scanning.scan import run_scan
from contur.Scanning.scanning_functions import *


def get_args():
    """Parse command line arguments"""
    parser = ArgumentParser(description=(
        "Run a parameter space scan and submit a batch job.\n"
        "Produces a scan directory containing: a parameters file detailing the "
        "parameters used at that run point and a shell script to run Herwig "
        "that is then submitted to batch.\n"
        "\n"
        "Can specify to run a 'rescan' on an old .map file using the -r "
        "option. When re-scanning 'weighted' and 'bin' modes are available.\n"
        "Weighted samples randomly from grid with weights derived from map "
        "file. 'bins' uses histogram bins and weights to sample around and "
        "below a CL level specified by the user with the '-cf' option."))
    # Positional arguments
    parser.add_argument("num_points", metavar="num_points", type=int,
                        help=("Number of points to sample within the parameter"
                              " space."))
    # Optional arguments
    parser.add_argument("-m", "--sample_mode", dest="mode",
                        default=None, metavar="mode",
                        help="Which sampling mode to use. {'uniform', "
                             "'random', 'weighted', 'bins'}\n"
                             "'weighted' and 'bins' only valid alongside "
                             "'--rescan' option\n (if rescan default='bins' "
                             "else default='uniform'")
    parser.add_argument("-o", "--out_dir", dest="out_dir", type=str,
                        metavar="output_dir", default="myscan00",
                        help="Specify the output directory name "
                             "(default=myscan00).")
    parser.add_argument('-p', '--param_file', dest='param_file', type=str,
                        default='param_file.dat', metavar='param_file',
                        help='File specifying parameter space '
                             '(default=param_file.dat).')
    parser.add_argument('-t', '--template', dest='template_file',
                        default='LHC.in', metavar='template_file',
                        help='Template Herwig .in file (default=LHC.in).')
    parser.add_argument("-g", "--grid", dest="grid_pack", type=str,
                        default='GridPack', metavar='grid_pack',
                        help=("Provide additional grid pack. Set to 'none' to "
                              "not use one (default=GridPack)."))
    parser.add_argument('-r', '--rescan', dest='map_file', default=False,
                        help="Specify a .map file to resample points from "
                             "(default=False).")
    parser.add_argument('-cf', '--cl_focus', type=float, default=0.95,
                        help=("Specify a CL value to focus re-sampling points "
                              "around. Only available with rescan option. "
                              "For 'bins' mode this is the maximum CL value "
                              "that will be sample, for 'weighted' mode this "
                              "is the centre of the probability distribution. "
                              "Must be between 0 and 1 (default=0.95)."))
    parser.add_argument('-f', '--factor', default=None, type=float,
                        help=("Factor to use with resampling. If mode is "
                              "'weighted' CLs are raised by this factor to "
                              "calculate weightings."
                              "If mode is 'bins' this is the factor bins' "
                              "weights are multiplied by when a point is "
                              "sampled nearby (should be between 0 and 1, "
                              "smaller factor means more clustered points). "
                              "(bins default=0.66, weighted default=1."))
    parser.add_argument("-n", "--numevents", dest="num_events",
                        default='30000', metavar='num_events', type=int,
                        help="Number of events to generate in Herwig "
                             "(default=30,000).")
    parser.add_argument('--seed', dest='seed', metavar='seed', default=101,
                        type=int,
                        help="Seed for random number generator (default=101).")
    parser.add_argument('-s', '--scan_only', dest='scan_only', default=False,
                        action='store_true',
                        help='Only perform scan and do not submit batch job '
                             '(default=False).')
    args = parser.parse_args()

    if not args.mode:
        if not args.map_file:
            args.mode = 'uniform'
        else:
            args.mode = 'bins'

    if args.map_file:
        if not args.factor:
            if args.mode == 'weighted':
                args.factor = 1
            elif args.mode == 'bins':
                args.factor = 0.66

    return args


def valid_arguments(args):
    """
    Check that command line arguments are valid; return True or False.
    This function is also responsible for formatting some arguments e.g.
    converting the GridPack path to an absolute path."""
    valid_args = True
    try:
        args.num_points = int(args.num_points)
    except ValueError:
        print("Number of points '%s' cannot be converted to integer!"
              % args.num_points)
        valid_args = False

    if args.mode not in ['uniform', 'random', 'weighted', 'bins']:
        print("Invalid sample mode! Must be 'uniform' or 'random', or, if "
              "rescanning weighted or bins.")
        valid_args = False

    if args.mode in ['weighted', 'bins'] and not args.map_file:
        print("Mode '%s' is only available when performing a rescan."
              % args.mode)
        valid_args = False

    if not os.path.exists(args.param_file):
        print("Param file '%s' does not exist!" % args.param_file)
        valid_args = False

    if not os.path.exists(args.template_file):
        print("Template file '%s' does not exist!" % args.template_file)
        valid_args = False

    if args.grid_pack.lower() == 'none':
        args.grid_pack = None
    else:
        args.grid_pack = os.path.abspath(args.grid_pack)
        if not os.path.isdir(args.grid_pack):
            print("No such grid pack directory '%s'!" % args.grid_pack)
            valid_args = False

    try:
        int(args.num_events)
    except ValueError:
        print("Number of events '%s' cannot be converted to integer!"
              % args.num_events)
        valid_args = False

    try:
        args.seed = int(args.seed)
    except ValueError:
        print("Seed '%s' cannot be converted to integer!" % args.seed)
        valid_args = False

    if args.map_file:
        if not os.path.isfile(args.map_file):
            print("No such file %s to use for rescan!" % args.map_file)
            valid_args = False

    if args.cl_focus != 0.95 and not args.map_file:
        print("You must be performing a rescan to use the cl_focus option!")
        valid_args = False

    elif not (0 <= args.cl_focus <= 1):
        print("'cl_focus' focus option must be a float between greater than 0 "
              "and less than or equal to 1.")
        valid_args = False

    return valid_args


def gen_batch_command(directory_name, directory_path, args, setup_commands):
    """Generate commands to write to batch file"""
    # Setup Herwig environment
    batch_command = setup_commands['Herwig'] + ';\n'
    # Setup Contur environment
    batch_command += setup_commands['Contur'] + ';\n'
    # Change directory to run point folder
    batch_command += 'cd ' + directory_path + ';\n'
    # Create Herwig run card from LHC.in. Pass it the the full grid pack
    # directory path to read model files from
    batch_command += ('Herwig read %s -I %s -L %s;\n' %
                      (args.template_file, args.grid_pack, args.grid_pack))
    # Run Herwig run card LHC.run
    run_card_name = os.path.splitext(args.template_file)[0] + '.run'
    batch_command += ('Herwig run ' + run_card_name +
                      ' --seed=' + str(args.seed) +
                      ' --tag=runpoint_' + directory_name +
                      ' --jobs=2' +
                      ' --numevents=' + str(args.num_events) + ';\n')

    batch_filename = 'runpoint_' + directory_name + '.sh'

    return batch_command, batch_filename


def batch_submit(args, setup_commands):
    """Run parameter scan and submit shell scripts to batch"""
    # Make sure scan is not overwriting previous scans
    if os.path.isdir(args.out_dir):
        out_dir_basename = args.out_dir[:-2]
        counter = 1
        while os.path.isdir(args.out_dir):
            args.out_dir = out_dir_basename + "%02i" % counter
            counter += 1

    check_param_consistency(args.param_file, args.template_file)

    np.random.seed(args.seed)

    # Param dict has parameter names as keys and then each item is a
    # dictionary with keys 'range' and 'values'
    param_dict = read_param_ranges(args.param_file)

    # Generate parameter values depending on sampling mode
    param_dict, num_points = generate_points(args, param_dict)

    # Create run point directories
    run_scan(param_dict, args)

    for directory_name in os.listdir(args.out_dir):
        directory_path = os.path.abspath(
            os.path.join(args.out_dir, directory_name))
        if os.path.isdir(directory_path):
            command, filename = gen_batch_command(
                directory_name, directory_path, args, setup_commands)
            batch_command_path = os.path.join(directory_path, filename)
            # Write batch file command (commands to run Herwig)
            with open(batch_command_path, 'w') as batch_file:
                batch_file.write(command)

            if args.scan_only is False:
                print("Submitting: " + batch_command_path)
                with WorkingDirectory(directory_path):
                    # Changing working directory is necessary here since
                    # qsub reports are outputted to current working directory
                    subprocess.call(["qsub -q medium " + batch_command_path],
                                    shell=True)
