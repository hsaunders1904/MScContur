#!/usr/bin/env python

import os, sys
import numpy as np
from math import *
import subprocess

mapPoints = []

for root, dirs, files in os.walk('.'):
       for name in files:
           tempPoints= []
                   #walk and look for .map files
           if '1.log' in name:
               #if '1900_mX_600' not in name:
               #    continue
               widthstring = os.system('grep -i "Y1.*Width" */' + name)
               #widthstring = subprocess.call(['grep -i "Y1.*Width" */' + name])
               tempStr=''
               #print widthstring.strip('-1.log').split('_')
               tempStr = subprocess.Popen('grep -i "Y1.*Width" */' + name,stdout=subprocess.PIPE, shell=True).communicate()[0]
               #name.strip('-1.log').split('_')
               if tempStr:
               #if subprocess.Popen('grep -i "Y1.*Width" */' + name,stdout=subprocess.PIPE, shell=True).communicate()[1] == None:
                    tempPoints.append(int(name.strip('-1.log').split('_')[1]))
                    tempPoints.append(int(name.strip('-1.log').split('_')[3]))
                    tempPoints.append(float(tempStr.strip('\n').split(':')[3])/float(name.strip('-1.log').split('_')[1]))
                    #print tempPoints
                    mapPoints.append(tempPoints)

print 'mY: ' + str(zip(*mapPoints)[0][zip(*mapPoints)[2].index(max(zip(*mapPoints)[2]))]) + ' mX: ' + str(zip(*mapPoints)[1][zip(*mapPoints)[2].index(max(zip(*mapPoints)[2]))]) + ' max width/M: ' + str(max(zip(*mapPoints)[2])) 
