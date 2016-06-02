#!usr/bin/env python

import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import colormaps as cmaps
import pickle
import scipy.stats as sp
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
                    print tempPoints
                    mapPoints.append(tempPoints)

dx = 50
dy = 50

x_grid_min= min(zip(*mapPoints)[1])-dx
y_grid_min= min(zip(*mapPoints)[0])-dy
x_grid_max= max(zip(*mapPoints)[1])+dx
y_grid_max= max(zip(*mapPoints)[0])+dy

yy,xx =np.mgrid[y_grid_min:y_grid_max+dy:2*dy,x_grid_min:x_grid_max+dx:2*dx]
c=np.zeros([len(xx[0,:])-1,len(yy[:,0])-1])


for i in range(0,len(zip(*mapPoints)[1])):
    xcounter=0
    ycounter=0
    for xarg2 in xx[1]:
        if zip(*mapPoints)[1][i] > xarg2:
            xcounter+=1
    for yarg2 in yy[:,xcounter]:
        if zip(*mapPoints)[0][i] > yarg2:
            ycounter+=1
    c[xcounter-1][ycounter-1]=zip(*mapPoints)[2][i]


fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1,1,1)
#plt.pcolormesh(xx,yy,zz,cmap="seismic", vmin=0, vmax=1)
plt.pcolormesh(xx,yy,c.T,cmap=cmaps.magma, vmin=min(zip(*mapPoints)[2]), vmax=max(zip(*mapPoints)[2]))
plt.axis([x_grid_min, x_grid_max, y_grid_min, y_grid_max])

plt.rc('text', usetex=True)
plt.rc('font', family='lmodern')#, size=10)
plt.xlabel(r"$M_{DM}$ [GeV]")
plt.ylabel(r"$M_{z'}$ [GeV]")
#plt.rc('text', usetex=False)
#plt.rc('font', family='sans')
#, fontsize=12
plt.title("Total Width to mediator mass ratio",y=1.01)

plt.colorbar().set_label(r"$\Gamma / M_{z'}$")
plt.savefig("combinedCL.pdf")
plt.savefig("combinedCL.png")



print 'exit'