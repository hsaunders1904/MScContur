import os, sys
import numpy as np
import matplotlib.pyplot as plt
import colormaps as cmaps
import pickle
import scipy.stats as sp
from math import *

def gauss_exp_model(var, mean, db):
#defining the exponent of the gaussian for convenience in log likelihood
    if fabs(db) <= 1E-5:
      return 0
    else:
      return (var-mean)**2./(2.*db**2)

def ML_b_hat_model(n,mu,b_til, sig_in, db_in):
#Maximum likelihood estimate for the background count b
#form is the root of the polynomial in b derived from differentiating the log likelihood wrt b
# A(b^2) + B(b) + C = 0
    B=-(b_til - mu*sig_in - (db_in**2))
    C=(-b_til*mu*sig_in + (db_in**2)*(mu*sig_in-n))
    return (-B+(B**2 - 4*C)**0.5)*0.5

def n_exp_model(mu, b_hat, s_in):
#Expected count n, the mean of the poisson used to define event count
  return b_hat + s_in*mu

def ML_mu_hat(n_obs,b_in,s_in):
#Maximum likelihood estimate for the strength parameter mu
    if fabs(s_in) <= 1E-5:
      return 0
    else:
      return (n_obs - b_in)/s_in

def qMu_Asimov(mu_test,bCount,sCount,db):
#function to find the test statistic for a given value of mu
#take b_til as a variable to simulate oscilations about background mean
#first find the ML of mu and b
    result = 0
    for i in range(0,len(bCount)):
        mu_hat = ML_mu_hat(bCount[i],bCount[i],sCount[i])
        b_hat = ML_b_hat_model(bCount[i],mu_hat,bCount[i], sCount[i], db[i])
        if mu_hat > 1.0:
            return 0
        elif mu_hat < 0.:
            mu_hat=0
            b_hat = ML_b_hat_model(bCount[i],mu_hat,bCount[i],sCount[i],db[i])

        b_hat_hat = ML_b_hat_model(bCount[i],mu_test,bCount[i],sCount[i],db[i])

        N_exp_b_hat_hat = n_exp_model(mu_test, b_hat_hat,sCount[i])
        N_exp_b_hat = n_exp_model(mu_hat, b_hat,sCount[i])
        # If any n_exp is almost zero, it should be set to zero
        if (N_exp_b_hat < 0) and (fabs(N_exp_b_hat) < 1E-5):
            N_exp_b_hat = 0
        if (N_exp_b_hat_hat < 0) and (fabs(N_exp_b_hat_hat) < 1E-5):
            N_exp_b_hat_hat = 0

        # If any expected value is really negative, there has been a problem somewhere
        if (N_exp_b_hat < 0) or (N_exp_b_hat_hat < 0):
            exit("ERROR: In S95 calculation, profile likelihood asked for nexp < 0!")
            N_exp_b_hat = N_exp_b_hat_hat =0
            result = 0

        # If any expected value is zero both must be zero
        if N_exp_b_hat*N_exp_b_hat_hat == 0:
            #if N_exp_b_hat != 0 or N_exp_b_hat_hat != 0:
            #  exit("ERROR: In S95 calculation, profile likelihood asked for impossible maximisation parameteres!")
            # In that case, the result is only the likelihood w.r.t the nuisance parameters
            result = -2.*(gauss_exp_model(bCount[i],b_hat,db[i]) - gauss_exp_model(bCount[i],b_hat_hat,db[i]))
        else:
            # Otherwise, return the normal likelihood
            result += -2.*(bCount[i]*log(N_exp_b_hat_hat/N_exp_b_hat) + N_exp_b_hat - N_exp_b_hat_hat + gauss_exp_model(bCount[i],b_hat,db[i]) - gauss_exp_model(bCount[i],b_hat_hat,db[i]))
    return result


def Var_mu_comb(b_count,s_count,db_count, ds_count):
#Construct the inverse variance matrix from expected vals of the 2nd derivatives of the Log Likelihood
    Var_matrix_inv=np.zeros([(len(b_count)+len(s_count)+1),(len(b_count)+len(s_count)+1)])
#add exception handling is s=/=b
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
    q_mu_a = qMu_Asimov(mu_test,bgCount,sigCount,bgErr)
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

data = maps[maps.keys()[0]][:]
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

                #data[j][2] = float(data[j][2]) + float(maps[key][i][2]) ** 2
                #continue

#for i in range(0,len(data)):
#    data[i][2]= np.sqrt(float(data[i][2]))

#### for some reason I hadcoded the grid width, easy enough to work out
##in fact this whole plotting script is a bit weird and could be done better I think
dx = 25
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


fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1,1,1)
#plt.pcolormesh(xx,yy,zz,cmap="seismic", vmin=0, vmax=1)
plt.pcolormesh(xx,yy,c.T,cmap=cmaps.magma_r, vmin=0, vmax=1)
plt.axis([x_grid_min, x_grid_max, y_grid_min, y_grid_max])

plt.rc('text', usetex=True)
plt.rc('font', family='lmodern')
plt.xlabel(r"$M_{\chi}$ [GeV]", fontsize=16)
plt.ylabel(r"$M_{Z'}$ [GeV]", fontsize=16)
plt.rc('text', usetex=False)
plt.rc('font', family='sans')

plt.title("ATLAS + CMS Combined",y=1.02)

plt.colorbar().set_label("CL of exclusion")
plt.savefig("combined.pdf")
plt.savefig("combined.png")


print "end"
