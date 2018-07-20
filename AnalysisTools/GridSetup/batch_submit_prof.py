#!/home/hs/anaconda3/envs/contur/bin/python

import os
import sys
import subprocess
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from scan import run_scan

herwig_setup = "source /unix/cedar/software/sl6/Herwig-Tip/setupEnv.sh"
contur_setup = "source $HOME/contur/setupContur.sh"


def get_args():
    parser = ArgumentParser(description=(
        "Run a parameter space scan and submit a batch job.\n"
        "Produces a scan directory containing: all files in given grid pack, "
        "a parameters file detailing the parameters used at that run point "
        "and a shell script to run Herwig that is then submitted to batch.\n"),
        formatter_class=ArgumentDefaultsHelpFormatter)
    # Positional arguments
    parser.add_argument("num_points", default=None, metavar="num_points",
                        help=("Number of points to sample within the parameter"
                              " space."))
    # Optional arguments
    parser.add_argument("-m", "--sample_mode", dest="sample_mode",
                        default="uniform", metavar="sample_mode",
                        help="Which sampling mode to use. {'uniform', "
                             "'random'}")
    parser.add_argument("-o", "--out_dir", dest="out_dir", type=str,
                        metavar="output_dir", default="myscan",
                        help=("specify the output directory name "))
    parser.add_argument('-p', '--param_file', dest='param_file',
                        default='param_file.dat', metavar='param_file',
                        help='File specifying parameter space.')
    parser.add_argument('-t', '--templates', dest='template_files', nargs='*',
                        default=['LHC.in'], metavar='template_files',
                        help='Template run card files.')
    parser.add_argument("-g", "--grid", dest="grid_pack", type=str,
                        default='GridPack', metavar='grid_pack',
                        help=("Provide additional gridpack. Set to 'none' to "
                              "not use one."))
    parser.add_argument("-N", "--numevents", dest="num_events",
                        default='10000', metavar='num_events',
                        help="Number of events to generate in Herwig.")
    parser.add_argument('--seed', dest='seed', metavar='seed', default=None,
                        help="Seed for random number generator.")
    parser.add_argument('-s', '--scan_only', dest='scan_only', default=False,
                        action='store_true',
                        help='Only perform scan and do not submit batch job.')
    args = parser.parse_args()

    if args.seed:
        args.seed = int(args.seed)
    if args.grid_pack.lower() == 'none':
        args.grid_pack = None
    return args


def check_setup_files(contur_setup, herwig_setup):
    """Check that Contur and Herwig setup scripts exist"""
    contur_setup = contur_setup.replace('$HOME', os.environ['HOME'])
    if not os.path.exists(contur_setup.strip('source ')):
        print("Warning: The path to 'setupContur.sh' does not exist!\n"
              "%s" % contur_setup)
    if not os.path.exists(herwig_setup.strip('source ')):
        print("Warning: The path to the Herwig setup script 'setupEnv.sh' "
              "does not exist!\n%s" % herwig_setup)


def gen_batch_command(directory_name, directory_path, args):
    """Write shell script to submit to batch"""
    if args.seed:
        seed = str(args.seed)
    else:
        seed = str(int(directory_name))

    # Setup Herwig environment
    batch_command = herwig_setup + ';\n'
    # Change directory to run point folder
    batch_command += 'cd ' + directory_path + ';\n'
    # Setup Contur environment
    batch_command += contur_setup + ';\n'
    # Create Herwig run card from LHC.in
    batch_command += 'Herwig read LHC.in;\n'
    # Run Herwig run card LHC.run
    batch_command += ('Herwig run LHC.run --seed=' + seed +
                      ' --tag=runpoint_' + directory_name +
                      ' --jobs=2' +
                      ' --numevents=' + str(args.num_events) + ';\n')

    batch_filename = 'runpoint_' + directory_name + '.sh'

    return batch_command, batch_filename


def batch_submit(args):

    check_setup_files(contur_setup, herwig_setup)

    # Run parameter space scan and create run point directories
    run_scan(num_points=int(args.num_points),
             template_paths=args.template_files,
             grid_pack=args.grid_pack,
             output_dir=args.out_dir,
             sample_mode=args.sample_mode,
             param_file=args.param_file,
             seed=args.seed)

    for directory_name in os.listdir(args.out_dir):
        directory_path = os.path.abspath(os.path.join(args.out_dir,
                                                      directory_name))
        if os.path.isdir(directory_path):
            # if args.scan_only is False:
            #     subprocess.call([herwig_setup], shell=True)
            #     subprocess.call([contur_setup], shell=True)

            command, filename = gen_batch_command(directory_name,
                                                  directory_path, args)
            batch_command_path = os.path.join(directory_path, filename)
            with open(batch_command_path, 'w') as batch_file:
                batch_file.write(command)

            if args.scan_only is False:
                subprocess.call(["qsub -q medium " + filename], shell=True)


if __name__ == '__main__':
    args = get_args()
    batch_submit(args)
