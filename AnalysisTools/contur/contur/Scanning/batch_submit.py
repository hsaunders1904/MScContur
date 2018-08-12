#!/usr/bin/env python

import os
import subprocess
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from contur.Scanning.scan import run_scan
from contur.Scanning.scanning_functions import permission_to_continue, WorkingDirectory


def get_args():
    """Parse command line arguments"""
    parser = ArgumentParser(description=(
        "Run a parameter space scan and submit a batch job.\n"
        "Produces a scan directory containing: all files in given grid pack, "
        "a parameters file detailing the parameters used at that run point "
        "and a shell script to run Herwig that is then submitted to batch.\n"),
        formatter_class=ArgumentDefaultsHelpFormatter)
    # Positional arguments
    parser.add_argument("num_points", metavar="num_points",
                        help=("Number of points to sample within the parameter"
                              " space."))
    # Optional arguments
    parser.add_argument("-m", "--sample_mode", dest="sample_mode",
                        default="uniform", metavar="sample_mode",
                        help="Which sampling mode to use. {'uniform', "
                             "'random', 'weighted', 'bins'}")
    parser.add_argument("-o", "--out_dir", dest="out_dir", type=str,
                        metavar="output_dir", default="myscan00",
                        help="Specify the output directory name ")
    parser.add_argument('-p', '--param_file', dest='param_file',
                        default='param_file.dat', metavar='param_file',
                        help='File specifying parameter space.')
    parser.add_argument('-t', '--templates', dest='template_files', nargs='*',
                        default=['LHC.in'], metavar='template_files',
                        help='Template run card files.')
    parser.add_argument("-g", "--grid", dest="grid_pack", type=str,
                        default='GridPack', metavar='grid_pack',
                        help=("Provide additional grid pack. Set to 'none' to "
                              "not use one."))
    parser.add_argument('-r', '--rescan', dest='rescan', default=False,
                        help="Specify a .map file to resample points from.")
    parser.add_argument('-f', '--factor', default=None,
                        help=("Factor to use with resampling. If mode is "
                              "'weighted' CLs are raised by this factor to "
                              "calculate weightings."
                              "If mode is 'bins' this is the factor bins' "
                              "weights are multiplied by when a point is "
                              "sampled nearby (should be between 0 and 1, "
                              "smaller factor means more clustered points). "
                              "(bins default=0.66, weighted default=1."))
    parser.add_argument("-n", "--numevents", dest="num_events",
                        default='10000', metavar='num_events',
                        help="Number of events to generate in Herwig.")
    parser.add_argument('--seed', dest='seed', metavar='seed', default='101',
                        help="Seed for random number generator.")
    parser.add_argument('-s', '--scan_only', dest='scan_only', default=False,
                        action='store_true',
                        help='Only perform scan and do not submit batch job.')
    return parser.parse_args()


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

    template_doesnt_exist = False
    for template_file in args.template_files:
        if not os.path.exists(template_file):
            print("Template file '%s' does not exist!" % template_file)
            template_doesnt_exist = True
    if template_doesnt_exist:
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

    if args.rescan:
        if not args.factor:
            if args.sample_mode == 'weighted':
                args.factor = 1
            elif args.sample_mode == 'bins':
                args.factor = 0.66

    return valid_args


def gen_batch_command(directory_name, directory_path, args, setup_commands):
    """Generate commands to write to batch file"""

    # Setup Herwig environment
    batch_command = setup_commands['Herwig'] + ';\n'
    # Change directory to run point folder
    batch_command += 'cd ' + directory_path + ';\n'
    # Setup Contur environment
    batch_command += setup_commands['Contur'] + ';\n'
    # Create Herwig run card from LHC.in
    batch_command += 'Herwig read LHC.in;\n'
    # Run Herwig run card LHC.run
    batch_command += ('Herwig run LHC.run --seed=' + str(args.seed) +
                      ' --tag=runpoint_' + directory_name +
                      ' --jobs=2' +
                      ' --numevents=' + str(args.num_events) + ';\n')

    batch_filename = 'runpoint_' + directory_name + '.sh'

    return batch_command, batch_filename


def batch_submit(args, setup_commands):
    """Run parameter scan and submit shell scripts to batch"""
    # Make sure scan is not overwriting previous scans
    if os.path.isdir(args.out_dir):
        out_dir_copy = args.out_dir[:-2]
        counter = 1
        while os.path.isdir(args.out_dir):
            args.out_dir = out_dir_copy + "%02i" % counter
            counter += 1

    # Run parameter space scan and create run point directories
    run_scan(num_points=int(args.num_points),
             template_paths=args.template_files,
             grid_pack=args.grid_pack,
             output_dir=args.out_dir,
             sample_mode=args.sample_mode,
             rescan=args.rescan,
             param_file=args.param_file,
             seed=args.seed,
             factor=args.factor)

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

            print("Submitting: " + batch_command_path)
            if args.scan_only is False:
                with WorkingDirectory(directory_path):
                    # Changing working directory is necessary here since
                    # qsub reports are outputted to current working directory
                    subprocess.call(["qsub -q medium " + batch_command_path],
                                    shell=True)
