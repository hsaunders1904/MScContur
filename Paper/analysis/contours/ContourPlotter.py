#!usr/bin/env python
import os, sys
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib as mpl
import colormaps as cmaps
import pickle
import scipy.stats as sp
import pylab as plab


import math
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator



def Var_mu_comb(b_count,s_count,db_count, ds_count):
#Construct the inverse variance matrix from expected vals of the 2nd derivatives of the Log Likelihood
    Var_matrix_inv=np.zeros([(len(b_count)+len(s_count)+1),(len(b_count)+len(s_count)+1)])
#add exception handling if s=/=b
  #loop over all counts
    for i in range(0, len(b_count)+len(s_count)):
      # if mu_test*s_count[i]+b_count[i] == 0:
      #     print 'g'
      #mu mu
        #Var_matrix_inv[0,0] += s_count[i]**2/(mu_test*s_count[i]+b_count[i])
      #mu b_i/b_i mu
        if i < len(b_count):
            Var_matrix_inv[0,0] += s_count[i]**2/(mu_test*s_count[i]+b_count[i])
            Var_matrix_inv[i+1,0]=Var_matrix_inv[0,i+1] = s_count[i]/(mu_test*s_count[i]+b_count[i])
            if db_count[i]**2 > 0.0:
                Var_matrix_inv[i+1,i+1]=1/(mu_test*s_count[i]+b_count[i]) + 1/db_count[i]**2
            else:
                Var_matrix_inv[i+1,i+1]=1/(mu_test*s_count[i]+b_count[i])
        if i>=(len(b_count)):
            Var_matrix_inv[i+1,0]=Var_matrix_inv[0,i+1] = (mu_test*s_count[i-len(b_count)])/(mu_test*s_count[i-len(b_count)]+b_count[i-len(b_count)])
            if ds_count[i-len(b_count)]**2 >0.0:
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_count[i-len(b_count)]+b_count[i-len(b_count)]) + 1/ds_count[i-len(b_count)]**2
            else:
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_count[i-len(b_count)]+b_count[i-len(b_count)])
        if i < len(s_count):
            Var_matrix_inv[len(b_count)+1+i,i+1] = Var_matrix_inv[i+1,len(b_count)+1+i] = mu_test/(mu_test*s_count[i]+b_count[i])
    if np.linalg.det(Var_matrix_inv) == 0:
        Var_matrix = np.zeros([(len(b_count)+1),(len(b_count)+1)])
  #Invert and return it
    else:
        Var_matrix = np.linalg.inv(Var_matrix_inv)
    return Var_matrix


def confLevel(sigCount, bgCount, bgErr, sgErr):
    varMat= Var_mu_comb(bgCount,sigCount,bgErr, sgErr)[0,0]
#    q_mu_a = qMu_Asimov(mu_test,bgCount,sigCount,bgErr)
    mu_hat = 0
    if varMat ==0:
        return 0
    else:
        q_mu=0
        p_val=0
        q_mu = (mu_test-mu_hat)**2/(varMat)
        if 0 < q_mu <= (mu_test**2)/(varMat):
            p_val=sp.halfnorm.sf(np.sqrt(q_mu))
        elif q_mu > (mu_test**2)/(varMat):
            p_val=sp.halfnorm.sf( (q_mu + (mu_test**2/varMat))/(2*mu_test/(np.sqrt(varMat))) )


    return float('%10.6f' % float(1-p_val))


maps={}
global mu_test
mu_test=1

for root, dirs, files in os.walk('.'):
       for name in files:

		   #walk and look for .map files
           if '.map' in name and 'svn' not in name:
               with open(name,'r+b') as f:
                maps[name.strip(".map")] = pickle.load(f)

#copy the first map in the dictionary, and make it into a blank canvas

data = maps['ATLAS_7_JETS'][:]
for i in range(0,len(data)):
    data[i]=list(data[i])
    data[i][2] = 1.0
    data[i][3] = []
    data[i][4] = []
    data[i][5] = []
    data[i][6] = []
i=0
for key in maps:
    i+=1
    for i in range(0,len(maps[key])):
        for j in range(0,len(data)):
            if maps[key][i][0] == data[j][0] and maps[key][i][1] == data[j][1]:
                data[j][3].extend(maps[key][i][3])
                data[j][4].extend(maps[key][i][4])
                data[j][5].extend(maps[key][i][5])
                data[j][6].extend(maps[key][i][6])

for listelement in data:
    data[data.index(listelement)][2]= confLevel(listelement[3],listelement[4],listelement[5],listelement[6])

# temp = []
# temp =  zip(zip(*data)[0],zip(*data)[1],zip(*data)[2])
# temp.sort(key=lambda x: x[0])
# writeOutput(temp,"combinedCL.dat")


#### for some reason I hadcoded the grid width, easy enough to work out
##in fact this whole plotting script is a bit weird and could be done better I think
dx = 50
dy = 50

x_grid_min= min(zip(*data)[1])-dx
y_grid_min= min(zip(*data)[0])-dy
x_grid_max= max(zip(*data)[1])+dx
y_grid_max= max(zip(*data)[0])+dy

yy,xx =np.mgrid[y_grid_min:y_grid_max+dy:2*dy,x_grid_min:x_grid_max+dx:2*dx]
c=np.zeros([len(xx[0,:])-1,len(yy[:,0])-1])


for i in range(0,len(zip(*data)[1])):
    xcounter=0
    ycounter=0
    for xarg2 in xx[1]:
        if zip(*data)[1][i] > xarg2:
            xcounter+=1
    for yarg2 in yy[:,xcounter]:
        if zip(*data)[0][i] > yarg2:
            ycounter+=1
    c[xcounter-1][ycounter-1]=zip(*data)[2][i]

contourXaxis=[]
contourYaxis=[]
x=min(zip(*data)[1])
y=min(zip(*data)[0])
#lets make a second grid for contouring
#for x in range(0, min(zip(*data)[1]), dx*2):
while x <= max(zip(*data)[1]):
    contourXaxis.append(x)
    x= x+ dx*2
while y <= max(zip(*data)[0]):
    contourYaxis.append(y)
    y= y+ dy*2


MP_LINEWIDTH = 2.4
MP_TICKSIZE = 10.

WIDTH = 454.0
FACTOR = 1.0/2.0
figwidthpt =WIDTH*FACTOR
inchesperpt = 1.0 / 72.27

golden_ratio  = (np.sqrt(5) - 1.0) / 2.0

figwidthin  = figwidthpt * inchesperpt  # figure width in inches
figheightin = figwidthin * golden_ratio +0.2   # figure height in inches
fig_dims    = [figwidthin, figheightin] # fig dims as a list



def pertUnit(mz):
    return np.sqrt(np.pi/2) * (mz/1.0)

#rcParams['figure.figsize'] = figsize()

#return figsize
document_fontsize = 10
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['font.size'] = document_fontsize
rcParams['axes.titlesize'] = document_fontsize
rcParams['axes.labelsize'] = document_fontsize
rcParams['xtick.labelsize'] = document_fontsize
rcParams['ytick.labelsize'] = document_fontsize
rcParams['legend.fontsize'] = document_fontsize
rcParams['text.usetex'] = True

#fig = plt.figure(figsize=(8, 6))
#fig = plab.figure(figsize=fig_dims)
fig=plab.figure(figsize=fig_dims)
ax = fig.add_subplot(1,1,1)
my_locator_x = MaxNLocator(5)
my_locator_y = MaxNLocator(4)
minorLocator_x = MaxNLocator(10)
minorLocator_y = MaxNLocator(19)
ax.yaxis.set_major_locator(my_locator_y)
ax.xaxis.set_major_locator(my_locator_x)
ax.xaxis.set_minor_locator(minorLocator_x)
ax.yaxis.set_minor_locator(minorLocator_y)

#plt.pcolormesh(xx,yy,zz,cmap="seismic", vmin=0, vmax=1)
#plab.pcolormesh(xx,yy,c.T,cmap=cmaps.magma, vmin=0, vmax=1)
plab.axis([min(zip(*data)[1]), max(zip(*data)[1]), min(zip(*data)[0]), max(zip(*data)[0])])
#CS=plab.contour(contourXaxis,contourYaxis,c.T,levels=[0.95],label="CL")

CS=plab.contourf(contourXaxis,contourYaxis,c.T,levels=[0.95,1.0],label="CL",cmap=cmaps.magma)



CS2=plab.contour(CS, colors = 'black')

#CS2=plab.contour(contourXaxis,contourYaxis,c.T,levels=[0.95,1.0], colors = 'black')

#
# plab.rc('axes', linewidth=MP_LINEWIDTH)
# plab.subplot(111)
# for tick in plab.gca().xaxis.get_major_ticks():
#   tick.label1.set_fontsize(20.)
#   tick.tick1line.set_markeredgewidth(MP_LINEWIDTH)
#   tick.tick2line.set_markeredgewidth(MP_LINEWIDTH)
#   tick.tick1line.set_markersize(0.5*MP_TICKSIZE)
#   tick.tick2line.set_markersize(0.5*MP_TICKSIZE)
y=np.array(contourYaxis)
x=pertUnit(y)
plab.plot(x,y,color='black')
ax.fill_between(x,y,1.,facecolor='navy',alpha=0.8)

fmt={}
strs=['95\% CL','CL']
for l , s in zip(CS2.levels, strs):
    fmt[l]=s

#manual_loc=[(800,1300),(400,300)]

#plab.clabel(CS2, CS2.levels[::2], inline=1, fmt=fmt, fontsize=10, manual=manual_loc)
#txt = plab.text(700,1100,'95\% CL',backgroundcolor='white')
#plab.clabel(CS2, inline=1, fontsize=10, manual=manual_loc)
#plab.rc('text', usetex=True)
#### plab.rc('font', family='cm', size=10)
#plab.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plab.xlabel(r"$M_{DM}$ [GeV]")
plab.ylabel(r"$M_{Z'}$ [GeV]",x=1.01)
artists, labels = CS.legend_elements()
plab.legend(artists, labels, handleheight=2,loc=2)


#plt.legend(handles=[CS])
#plt.rc('text', usetex=False)
#plt.rc('font', family='sans')
#, fontsize=12
#plab.title("CL Contour",y=1.01)
#legend = ax.legend(loc='upper center', shadow=True)
#plab.colorbar(ticks=[0,0.5,1.0]).set_label("CL of exclusion")
fig.tight_layout(pad=0.1)
fig.savefig('figure.pdf')
plab.savefig("contour.pdf")
plab.savefig("contour.png")


print "end"
