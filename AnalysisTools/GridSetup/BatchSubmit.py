#!/usr/bin/python

import sys
import os
import string
import tarfile
import random
import errno
import time
import subprocess

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


for i in range(1100,2100,100):
    for j in range(100,1050,50):
        modelpath = 'mY_'+ str(i) + '_mX_' + str(j)
        copytree(pwd + '/GridPack',modelpath)
        #mkdir_p(str(modelpath))
        HerwigString = ''
        HC=open('HerwigCommand', 'r')

        HerwigString += 'read FRModel.model \n'
        HerwigString += 'set /Herwig/FRModel/Particles/Y1:NominalMass ' + str(i) + '.*GeV \n'
        HerwigString += 'set /Herwig/FRModel/Particles/Xm:NominalMass ' + str(j) + '.*GeV \n'
        HerwigString += str(HC.read())
        HC.close()
        RunCard = open(str(modelpath + '/LHC.in'), 'w')
        RunCard.write(str(HerwigString))
        RunCard.close()
        
        subprocess.call(["source /unix/cedar/software/sl6/Herwig-7.0.0/./bin/activate"], shell=True)
        #os.system('. /unix/cedar/software/sl6/Herwig-7.0.0/./bin/activate')
        #time.sleep(2)
        os.chdir(modelpath)
        os.system('Herwig read LHC.in')
        #time.sleep(2)

        batch_command = ''
        batch_command += '. /unix/cedar/software/sl6/Herwig-7.0.0/./bin/activate; '
        batch_command += 'cd ' + pwd + '/' + modelpath +'; '
        batch_command += 'Herwig run --seed='+str(i)+str(j)+' --tag='+str(modelpath)+' --numevents=100000 LHC.run;'
        batch_filename = str(modelpath)+'.sh'
        batch_submit = open(batch_filename, 'w')
        batch_submit.write(batch_command)
        batch_submit.close()

        os.system( "qsub -q medium " + batch_filename )
        #os.system( "rm -rf " + batch_filename )
        os.chdir(pwd)
