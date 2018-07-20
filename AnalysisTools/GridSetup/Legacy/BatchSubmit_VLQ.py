#!/usr/bin/python

import sys
import os
import string
import tarfile
import random
import errno
import time
import subprocess
import numpy as np

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

import shutil

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

pwd = os.getcwd()
i=0
k=0

HerwigSetup="source /unix/cedar/software/sl6/Herwig-Release-fix/setupEnv.sh"
ConturSetup="source /home/jmb/svn-managed/contur/setupContur.sh"

for i in range(600,2200,200):
    for j in range(0,11,1):
        modelpath = 'mB_'+ str(i) + '_xibph_' + str(j)
        copytree(pwd + '/GridPack',modelpath)
        
        HerwigString = ''
        HC=open('HerwigCommandWeak8', 'r')
        HerwigString += 'read FRModel.model \n'
        HerwigString += 'set /Herwig/FRModel/Particles/bp:NominalMass ' + str(i) + '.*GeV \n'
        HerwigString += 'set /Herwig/FRModel/FRModel:xibph ' + str(j/10.0) + ' \n'
        HerwigString += 'set /Herwig/FRModel/FRModel:xibpz ' + str(1-(j/10.0)) + ' \n'
        #HerwigString += 'set /Herwig/FRModel/FRModel:xibph ' + str(j) + ' \n'
        #HerwigString += 'set /Herwig/FRModel/FRModel:xibpz ' + str(1-j) + ' \n'
        HerwigString += str(HC.read())
        HC.close()
        RunCard = open(str(modelpath + '/LHC-FRModel.in'), 'w')
        RunCard.write(str(HerwigString))
        RunCard.close()

        subprocess.call([HerwigSetup], shell=True)
        subprocess.call([ConturSetup], shell=True)
        os.chdir(modelpath)
        subprocess.call(['Herwig read LHC-FRModel.in'], shell=True)
        batch_command = ''
        batch_command += HerwigSetup + '; '
        batch_command += 'cd ' + pwd + '/' + modelpath +'; '
        batch_command += ConturSetup + "; "
        numEv=500000
        batch_command += 'Herwig run --seed='+str(i)+str(j)+' --tag='+str(modelpath)+' --jobs=2 --numevents='+ str(numEv) +' LHC-FRModel.run;'
        batch_filename = str(modelpath)+'.sh'
        batch_submit = open(batch_filename, 'w')
        batch_submit.write(batch_command)
        batch_submit.close()
        subprocess.call([ "qsub -q long " + batch_filename],shell=True )
        os.chdir(pwd)

