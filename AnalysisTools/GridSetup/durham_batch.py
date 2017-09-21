#!/usr/bin/python
import subprocess

## Modify for your username
batch_setup_file = """\
#!/bin/bash

#SBATCH --error="%j.err"                  # Direct STDERR here
#SBATCH --output="%j.out"                 # Direct STDOUT here
{HerwigSetup}
{ConturSetup}

cd {pwd}/{modelpath}
Herwig run --seed={i}{j} --tag={modelpath} -j 2 -N {numEv} LHC.run

exit 0
"""

def write_batch_file(batch_filename, modelpath, pwd, HerwigSetup, ConturSetup, numEv, i, j):
    batch_command = batch_setup_file.format(locals())
    with open(batch_filename, 'w') as batch_submit:
        batch_submit.write(batch_command)
    return batch_command

def run_batch_file(batch_filename):
    subprocess.call(["sbatch",batch_filename],shell=True )
