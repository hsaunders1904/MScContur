#!/usr/bin/python
import sys
import os
import subprocess
import shutil



### Adapt these settings ###




#import durham_batch as batch
import ucl_batch as batch

herwig_in_template = 'HerwigCommandHad' ## choose the template Herwig .in file to use

ParamSettingTemplate = """\
read FRModel.model
set /Herwig/FRModel/Particles/Y1:NominalMass {i}*GeV 
set /Herwig/FRModel/Particles/Xm:NominalMass {j}*GeV
"""

irange = range(105,107,1)
jrange = range(115,117,1)
numEv = 10000







### NO USER SETTINGS BELOW ###


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)

## grab these from the enviro rather than hardcoding twice
try:
    HerwigSetup = "source " + os.environ["HERWIG_ENV"] + "bin/activate"
    ConturSetup = "source " + os.environ["CONTURMODULEDIR"] + "/setupContur.sh"
except KeyError:
    sys.stderr.write("Herwing/Contur environment variables don't appear to have been initialised\n")
    sys.exit(1)

print "Herwig dir: ", os.environ["HERWIG_ENV"]
print "Contur dir: ", os.environ["CONTURMODULEDIR"]

pwd = os.getcwd()

for i in irange:
    for j in jrange:

        modelpath = 'mY_'+ str(i) + '_mX_' + str(j)
        copytree(pwd + '/GridPack',modelpath)
        print modelpath

        ## setting up Herwig for this particular run
        HerwigString = ParamSettingTemplate.format(i=i, j=j)

        HC=open(herwig_in_template, 'r')
        HerwigString += str(HC.read())
        HC.close()

        RunCard = open(str(modelpath + '/LHC.in'), 'w')
        RunCard.write(str(HerwigString))
        RunCard.close()

        os.chdir(modelpath)
        subprocess.call(['Herwig read LHC.in'], shell=True)

        ## writing and running the batch file based on the batch system required
        batch_filename = str(modelpath)+'.sh'
        batch.write_batch_file(batch_filename, modelpath, pwd, HerwigSetup, ConturSetup, numEv, i, j)
        batch.run_batch_file(batch_filename)

        os.chdir(pwd)
