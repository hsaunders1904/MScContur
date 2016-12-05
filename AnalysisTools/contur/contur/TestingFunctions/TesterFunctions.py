#!usr/bin/env python

import os, sys
import numpy as np
import scipy.stats as sp
import math
from math import *


global mu_test
mu_test=1
#from contur.TestingFunctions import covariance_matrix as cv

def ML_mu_hat(n_obs,b_in,s_in):
#Maximum likelihood estimate for the strength parameter mu
    if fabs(s_in) <= 1E-5:
      return 0
    else:
      return (n_obs - b_in)/s_in

def gauss_exp(var, mean, db):
#defining the exponent of the gaussian for convenience in log likelihood
    if fabs(db) <= 1E-5:
      return 0
    else:
      return (var-mean)**2./(2.*db**2)

def ML_b_hat(n,mu,b_til, sig_in, db_in):
#Maximum likelihood estimate for the background count b
#form is the root of the polynomial in b derived from differentiating the log likelihood wrt b
# A(b^2) + B(b) + C = 0
    B=-(b_til - mu*sig_in - (db_in**2))
    C=(-b_til*mu*sig_in + (db_in**2)*(mu*sig_in-n))
    return (-B+(B**2 - 4*C)**0.5)*0.5

def n_exp(mu, b_hat, s_in):
#Expected count n, the mean of the poisson used to define event count
  return b_hat + s_in*mu

def Var_mu_comb(b_count,s_count,db_count, ds_count):
#Construct the inverse variance matrix from expected vals of the 2nd derivatives of the Log Likelihood
    Var_matrix_inv=np.zeros([(len(b_count)+len(s_count)+1),(len(b_count)+len(s_count)+1)])
#add exception handling if s=/=b
  #loop over all counts
    for i in range(0, len(b_count)+len(s_count)):
        if i < len(b_count):
            ##Construct all the inverse covar matrix from second derivatives of Likelihood function
            ##mu mu
            Var_matrix_inv[0,0] += s_count[i]**2/(mu_test*s_count[i]+b_count[i])
            ##mu b
            Var_matrix_inv[i+1,0]=Var_matrix_inv[0,i+1] = s_count[i]/(mu_test*s_count[i]+b_count[i])
            ##b b
            if db_count[i]**2 > 0.0:
                Var_matrix_inv[i+1,i+1]=1/(mu_test*s_count[i]+b_count[i]) + 1/db_count[i]**2
            else:
                Var_matrix_inv[i+1,i+1]=1/(mu_test*s_count[i]+b_count[i])
        if i>=(len(b_count)):
            ##mu s
            Var_matrix_inv[i+1,0]=Var_matrix_inv[0,i+1] = (mu_test*s_count[i-len(b_count)])/(mu_test*s_count[i-len(b_count)]+b_count[i-len(b_count)])
            ##s s
            if s_count[i-len(b_count)] >0.0:
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_count[i-len(b_count)]+b_count[i-len(b_count)]) + 1/s_count[i-len(b_count)]
            else:
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_count[i-len(b_count)]+b_count[i-len(b_count)])
        if i < len(s_count):
            ## b s
            Var_matrix_inv[len(b_count)+1+i,i+1] = Var_matrix_inv[i+1,len(b_count)+1+i] = mu_test/(mu_test*s_count[i]+b_count[i])
    if np.linalg.det(Var_matrix_inv) == 0:
        Var_matrix = np.zeros([(len(b_count)+1),(len(b_count)+1)])
  #Invert and return it
    else:
        Var_matrix = np.linalg.inv(Var_matrix_inv)
    return Var_matrix


def qMu_Asimov(mu_test,bCount,sCount,db):
#function to find the test statistic for a given value of mu
#take b_til as a variable to simulate oscilations about background mean
#first find the ML of mu and b
    result = 0
    for i in range(0,len(bCount)):
        mu_hat = ML_mu_hat(bCount[i],bCount[i],sCount[i])
        b_hat = ML_b_hat(bCount[i],mu_hat,bCount[i], sCount[i], db[i])
        if mu_hat > 1.0:
            return 0
        elif mu_hat < 0.:
            mu_hat=0
            b_hat = ML_b_hat(bCount[i],mu_hat,bCount[i],sCount[i],db[i])

        b_hat_hat = ML_b_hat(bCount[i],mu_test,bCount[i],sCount[i],db[i])

        N_exp_b_hat_hat = n_exp(mu_test, b_hat_hat,sCount[i])
        N_exp_b_hat = n_exp(mu_hat, b_hat,sCount[i])
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
            result = -2.*(gauss_exp(bCount[i],b_hat,db[i]) - gauss_exp(bCount[i],b_hat_hat,db[i]))
        else:
            # Otherwise, return the normal likelihood
            result += -2.*(bCount[i]*log(N_exp_b_hat_hat/N_exp_b_hat) + N_exp_b_hat - N_exp_b_hat_hat + gauss_exp(bCount[i],b_hat,db[i]) - gauss_exp(bCount[i],b_hat_hat,db[i]))
    return result


def confLevel(sigCount, bgCount, bgErr, sgErr,mu_test=1):
    varMat= Var_mu_comb(bgCount,sigCount,bgErr, sgErr)[0,0]
#    varMat= cv.chisq(bgCount,sigCount,bgErr, sgErr)
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

    ratioTest = False
    ##use the qMu_Asimov function to construct the ratio instead, should be equivalent input to Var_mu_comb
    if ratioTest:
        p_val=sp.halfnorm.sf(np.sqrt(q_mu_a))

    return float('%10.6f' % float(1-p_val))
