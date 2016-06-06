#!usr/bin/env python

import os, sys
import numpy as np
import scipy.stats as sp
import math

global mu_test
mu_test=1


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