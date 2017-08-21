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

HerwigSetup="source /unix/cedar/software/sl6/Herwig-7.1.0/setupEnv.sh"
ConturSetup="source /home/jmb/svn-managed/contur/setupContur.sh"

for i in range(100,3100,100):
    for j in range(100,2100,100):
        i = int(i)
        j = int(j)
        modelpath = 'mY_'+ str(i) + '_mX_' + str(j)
        copytree(pwd + '/GridPack',modelpath)
        #mkdir_p(str(modelpath))
        HerwigString = ''
        HC=open('HerwigCommandWeak', 'r')

        HerwigString += 'read FRModel.model \n'
        HerwigString += 'set /Herwig/FRModel/Particles/Y1:NominalMass ' + str(i) + '.*GeV \n'
        HerwigString += 'set /Herwig/FRModel/Particles/Xm:NominalMass ' + str(j) + '.*GeV \n'
        HerwigString += str(HC.read())
        HC.close()
        RunCard = open(str(modelpath + '/LHC.in'), 'w')
        RunCard.write(str(HerwigString))
        RunCard.close()
        
        subprocess.call([HerwigSetup], shell=True)
        subprocess.call([ConturSetup], shell=True)
        os.chdir(modelpath)
        subprocess.call(['Herwig read LHC.in'], shell=True)
        batch_command = ''
        batch_command += HerwigSetup + '; '
        batch_command += 'cd ' + pwd + '/' + modelpath +'; '
        batch_command += ConturSetup + "; "
        if i < 1500:
            numEv=30000
        else:
            numEv=5000
        batch_command += 'Herwig run --seed='+str(i)+str(j)+' --tag='+str(modelpath)+' --jobs=5 --numevents='+ str(numEv) +' LHC.run;'
        batch_filename = str(modelpath)+'.sh'
        batch_submit = open(batch_filename, 'w')
        batch_submit.write(batch_command)
        batch_submit.close()

        subprocess.call([ "qsub -q medium " + batch_filename],shell=True )
        os.chdir(pwd)
