import os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import colormaps as cmaps
import pickle
import scipy.stats as sp
from math import *

def writeOutput(output, h):
    f = open(h, 'w')
    for item in output:
        f.write(str(item) + "\n")
    f.close()


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
           if '.map' in name:
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

temp = []
temp =  zip(zip(*data)[0],zip(*data)[1],zip(*data)[2])
temp.sort(key=lambda x: x[0])
writeOutput(temp,"combinedCL.dat")


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


fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(1,1,1)
#plt.pcolormesh(xx,yy,zz,cmap="seismic", vmin=0, vmax=1)
plt.pcolormesh(xx,yy,c.T,cmap=cmaps.magma, vmin=0, vmax=1)
plt.axis([x_grid_min, x_grid_max, y_grid_min, y_grid_max])

plt.rc('text', usetex=True)
plt.rc('font', family='lmodern')#, size=10)
plt.xlabel(r"$M_{DM}$ [GeV]")
plt.ylabel(r"$M_{z'}$ [GeV]")
#plt.rc('text', usetex=False)
#plt.rc('font', family='sans')
#, fontsize=12
plt.title("ATLAS + CMS Combined all channels",y=1.01)

plt.colorbar().set_label("CL of exclusion")
plt.savefig("combinedCL.pdf")
plt.savefig("combinedCL.png")


print "end"
