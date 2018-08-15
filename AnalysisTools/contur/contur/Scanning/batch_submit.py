#!/usr/bin/env python

import os
import subprocess
from argparse import ArgumentParser

from contur.Scanning.scan import run_scan
from contur.Scanning.scanning_functions import permission_to_continue, WorkingDirectory


def get_args():
    """Parse command line arguments"""
    parser = ArgumentParser(description=(
        "Run a parameter space scan and submit a batch job.\n"
        "Produces a scan directory containing: all files in given grid pack, "
        "a parameters file detailing the parameters used at that run point "
        "and a shell script to run Herwig that is then submitted to batch.\n"
        "Can specify to run a 'rescan' on an old .map file using the -r "
        "option."))
    # Positional arguments
    parser.add_argument("num_points", metavar="num_points",
                        help=("Number of points to sample within the parameter"
                              " space."))
    # Optional arguments
    parser.add_argument("-m", "--sample_mode", dest="sample_mode",
                        default=None, metavar="sample_mode",
                        help="Which sampling mode to use. {'uniform', "
                             "'random', 'weighted', 'bins'}\n"
                             "'weighted' and 'bins' only valid alongside "
                             "'--rescan' option")
    parser.add_argument("-o", "--out_dir", dest="out_dir", type=str,
                        metavar="output_dir", default="myscan00",
                        help="Specify the output directory name ")
    parser.add_argument('-p', '--param_file', dest='param_file',
                        default='param_file.dat', metavar='param_file',
                        help='File specifying parameter space.')
    parser.add_argument('-t', '--template', dest='template_file',
                        default='LHC.in', metavar='template_file',
                        help='Template run card files.')
    parser.add_argument("-g", "--grid", dest="grid_pack", type=str,
                        default='GridPack', metavar='grid_pack',
                        help=("Provide additional grid pack. Set to 'none' to "
                              "not use one."))
    parser.add_argument('-r', '--rescan', dest='rescan', default=False,
                        help="Specify a .map file to resample points from.")
    parser.add_argument('-cf', '--cl_focus', type=float, default=0.95,
                        help=("Specify a CL value to focus re-sampling points "
                              "around. Only available with rescan option. "
                              "For 'bins' mode this is the maximum CL value "
                              "that will be sample, for 'weighted' mode this "
                              "is the centre of the probability distribution. "
                              "Must be between 0 and 1."))
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
                        default='30000', metavar='num_events',
                        help="Number of events to generate in Herwig.")
    parser.add_argument('--seed', dest='seed', metavar='seed', default='101',
                        help="Seed for random number generator.")
    parser.add_argument('-s', '--scan_only', dest='scan_only', default=False,
                        action='store_true',
                        help='Only perform scan and do not submit batch job.')
    args = parser.parse_args()

    if not args.sample_mode:
        if not args.rescan:
            args.sample_mode = 'uniform'
        else:
            args.sample_mode = 'bins'

    if args.rescan:
        if not args.factor:
            if args.sample_mode == 'weighted':
                args.factor = 1
            elif args.sample_mode == 'bins':
                args.factor = 0.66

    return args


def valid_arguments(args):
    """Check that command line arguments are valid; return True or False"""
    valid_args = True
    try:
        args.num_points = int(args.num_points)
    except ValueError:
        print("Number of points '%s' cannot be converted to integer!"
              % args.num_points)
        valid_args = False

    if args.sample_mode not in ['uniform', 'random', 'weighted', 'bins']:
        print("Invalid sample mode! Must be 'uniform' or 'random', or if "
              "rescanning weighted or bins.")
        valid_args = False

    if args.sample_mode in ['weighted', 'bins'] and not args.rescan:
        print("Mode '%s' is only available when performing a rescan."
              % args.sample_mode)
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

    if args.rescan:
        if not os.path.isfile(args.rescan):
            print("No such file %s to use for rescan!" % args.rescan)
            valid_args = False

    if args.cl_focus != 0.95 and not args.rescan:
        print("You must be performing a rescan to use the cl_focus option!")
        valid_args = False

    elif not (0 <= args.cl_focus <= 1):
        print("'cl_focus' focus option must be a float between greater than 0 "
              "and less than or equal to 1.")

    return valid_args


def gen_batch_command(directory_name, directory_path, args, setup_commands):
    """Generate commands to write to batch file"""
    # Setup Herwig environment
    batch_command = setup_commands['Herwig'] + ';\n'
    # Setup Contur environment
    batch_command += setup_commands['Contur'] + ';\n'
    # Change directory to run point folder
    batch_command += 'cd ' + directory_path + ';\n'
    # Create Herwig run card from LHC.in
    batch_command += 'Herwig read %s;\n' % args.template_file
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

    # Run parameter space scan and create run point directories
    run_scan(num_points=int(args.num_points),
             template_path=args.template_file,
             grid_pack=args.grid_pack,
             output_dir=args.out_dir,
             sample_mode=args.sample_mode,
             rescan=args.rescan,
             param_file=args.param_file,
             seed=args.seed,
             factor=args.factor,
             cl_focus=args.cl_focus)

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
