#!/home/hs/anaconda3/envs/contur/bin/python


import os
import sys
import subprocess
import optparse

from scan import run_scan

op = optparse.OptionParser(usage=__doc__)
op.add_option("-g", "--grid", dest="grid_pack", metavar="DIR",
              default='GridPack', help="provide additional gridpack")
op.add_option("-o", "--out_dir", dest="out_dir", metavar="DIR",
              default="myscan",
              help="specify the output directory name (default: %default)")
op.add_option("-N", "--numevents", dest="num_events", metavar="INT",
              default=10000, help="Number of events to generate in Herwig.")
op.add_option("-n", "--num_points", dest="num_points", metavar="INT",
              default=None,
              help="Number of points to sample within the parameter space.")
op.add_option("-m", "--sample_mode", dest="sample_mode", default="uniform",
              help="Which sampling mode to use. {'uniform', 'random'}")
op.add_option('-s', '--scan_only', dest='scan_only', default=False,
              action='store_true',
              help='Only perform scan and do not submit batch job.')
op.add_option('-p', '--param_file', dest='param_file',
              default='param_file.dat',
              help='File specifying parameter space.')
op.add_option('-t', '--template', dest='template_file', default='LHC.in',
              help='Template run card file.')
op.add_option('--seed', dest='seed', metavar='INT', default=None,
              help="Seed for random number generator.")
opts, args = op.parse_args()

if opts.num_points is None:
    print("You must specify the number of points to sample.\n"
          "Use the -n flag.\n")
    sys.exit()
if opts.seed:
    opts.seed = int(opts.seed)
if opts.grid_pack.lower() == 'none':
    opts.grid_pack == None

run_scan(num_points=int(opts.num_points),
         template_paths=[opts.template_file],
         grid_pack=opts.grid_pack,
         output_dir=opts.out_dir,
         sample_mode=opts.sample_mode,
         param_file=opts.param_file,
         seed=opts.seed)

herwig_setup = "source /unix/cedar/software/sl6/Herwig-Tip/setupEnv.sh"
contur_setup = "source $HOME/contur/setupContur.sh"

contur_setup = contur_setup.replace('$HOME', os.environ['HOME'])
if not os.path.exists(contur_setup.strip('source ')):
    print("Warning: The path to 'setupContur.sh' does not exist!\n"
          "%s" % contur_setup)
if not os.path.exists(herwig_setup.strip('source ')):
    print("Warning: The path to the Herwig setup script 'setupEnv.sh' does not"
          " exist!\n%s" % herwig_setup)

pwd = os.getcwd()
for directory in os.listdir(opts.out_dir):
    directory_name = os.path.join(opts.out_dir, directory)
    if os.path.isdir(directory_name):
        if opts.scan_only is False:
            subprocess.call([herwig_setup], shell=True)
            subprocess.call([contur_setup], shell=True)
        os.chdir(directory_name)

        if opts.seed:
            seed = opts.seed
        else:
            seed = str(int(directory))

        # Setup Herwig environment
        batch_command = herwig_setup + '; \n'
        # Change directory to run point folder
        batch_command += 'cd ' + os.path.join(pwd, directory_name) + '; \n'
        # Setup Contur environment
        batch_command += contur_setup + '; \n'
        # Create Herwig run card from LHC.in
        batch_command += 'Herwig read LHC.in; \n'
        # Run Herwig run card LHC.run
        batch_command += ('Herwig run LHC.run --seed=' + str(int(directory)) +
                          ' --tag=runpoint_' + directory +
                          ' --jobs=2' +
                          ' --numevents=' + str(opts.num_events) + '; \n')

        batch_filename = 'runpoint_' + directory + '.sh'
        with open(batch_filename, 'w') as batch_submit:
            batch_submit.write(batch_command)
        if opts.scan_only is False:
            subprocess.call(["qsub -q medium " + batch_filename], shell=True)
        os.chdir(pwd)
