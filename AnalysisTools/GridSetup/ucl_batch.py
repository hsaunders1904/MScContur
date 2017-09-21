#!/usr/bin/python
import subprocess

batch_setup_file = """\
{HerwigSetup};
cd {pwd}/{modelpath};
{ConturSetup};
Herwig run --seed={i}{j} --tag={modelpath} -j 2 -N {numEv} LHC.run;
"""


def write_batch_file(batch_filename, modelpath, pwd, HerwigSetup, ConturSetup, numEv, i, j):
    batch_command = batch_setup_file.format(locals())
    batch_filename = "{}.sh".format(modelpath)
    with open(batch_filename, 'w') as batch_submit:
        batch_submit.write(batch_command)
    return batch_command

def run_batch_file(batch_filename):
    subprocess.call(["qsub","-q","medium",batch_filename],shell=True )
