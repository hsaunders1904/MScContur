#!usr/bin/env python

import os, sys
import numpy as np
import scipy.stats as spstat
import math
from math import *
import scipy.optimize as spopt

global mu_test
mu_test=1

def Min_function(x, n_obs, b_obs, s_obs, db, kev):
    # defines the functional form of vector function Min_function[0] corresponds to dlnL/db
    # Min_function[1] corresponds to dlnL/ds
    # takes argument x=[b_hat_hat, s_hat_hat]

    #Here mu_hat is passed and included into the functional form of the first derivatives, it's set to 1 in the current assumption
    #so doesn't appear
    # the if statement form of this is just to prevent any term blowing up if the denominator is near 0

    d_lnL_db = 0.0
    d_lnL_ds = 0.0
    if fabs((x[0] + x[1])) > 0.0:
        d_lnL_db += n_obs / (x[0] + x[1]) - 1
        d_lnL_ds += n_obs / (x[0] + x[1]) - 1
    if fabs(db) >= 1e-5:
        d_lnL_db += (b_obs - x[0]) / db**2
    if x[1] > 0.0:
        d_lnL_ds += kev / x[1]
    if s_obs > 0.0:
        d_lnL_ds -= kev / s_obs
    return [d_lnL_db,d_lnL_ds]


def Min_find(n_obs, b_obs, s_obs, db, k):
    #Min find just runs the root finding on the Min_function so just needs to pass through the arguments
    # s_hat_hat is called x_1, b_hat_hat is x_0
    # func_0 being the first entry in vector, corresponds to dlnL/db
    # func_1 dlnL/ds
    return spopt.root(Min_function, [b_obs, s_obs], args=(n_obs, b_obs, s_obs, db, k))



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
#Maximum likelihood estimate for the background count b, assuming s is not a nuisance parameter
#form is the root of the polynomial in b derived from differentiating the log likelihood wrt b
# A(b^2) + B(b) + C = 0
    B=-(b_til - mu*sig_in - (db_in**2))
    C=(-b_til*mu*sig_in + (db_in**2)*(mu*sig_in-n))
    return (-B+(B**2 - 4*C)**0.5)*0.5

def n_exp(mu, b_hat, s_in):
#Expected count n, the mean of the poisson used to define event count
  return b_hat + s_in*mu

def Covar_Matrix(b_count,s_count,db_count, kev):
#Construct the inverse variance matrix from expected vals of the 2nd derivatives of the Log Likelihood

    # start with a matrix full of zeros
    Var_matrix_inv=np.zeros([(len(b_count)+len(s_count)+1),(len(b_count)+len(s_count)+1)])


#add exception handling if s=/=b
  #loop over all counts
    for i in range(0, len(b_count)+len(s_count)):
        #Call function to simultaneously minimise s and b at the specified ML mu (always 0)
        #if min not found return the input s and b

        #Major restructing here, these min_finds can be factored out to the main conf level function as we only need to work these out once
        #The big change in the code needed here is to sort out the form of the second derivatives, which are all correct in the paper
        # I used a cancellation of n and mu.s+b here which was fine before but as we separate these two counts, the form of these needs 
        #to be updated to reflect as in the paper
        

        if i < (len(b_count)):
            if b_count[i]<0:
                b_count[i]=0
            res = Min_find(b_count[i], b_count[i], s_count[i], db_count[i], kev[i]).x
        else:
            if b_count[i-len(b_count)]<0:
                b_count[i-len(b_count)]=0
            res = Min_find(b_count[i-len(b_count)], b_count[i-len(b_count)], s_count[i-len(b_count)], db_count[i-len(b_count)], kev[i-len(b_count)]).x

        b_hat_hat = res[0]
        s_hat_hat = res[1]

        if i < len(b_count):
            ##Construct all the inverse covar matrix from second derivatives of Likelihood function
            ##mu mu

            Var_matrix_inv[0,0] += s_hat_hat**2/(mu_test*s_hat_hat+b_hat_hat)
            ##mu b
            Var_matrix_inv[i+1,0]=Var_matrix_inv[0,i+1] = s_hat_hat/(mu_test*s_hat_hat+b_hat_hat)
            ##b b
            if db_count[i]**2 > 0.0:
                Var_matrix_inv[i+1,i+1]=1/(mu_test*s_hat_hat+b_hat_hat) + 1/db_count[i]**2
            else:
                Var_matrix_inv[i+1,i+1]=1/(mu_test*s_hat_hat+b_hat_hat)
        if i>=(len(b_count)):
            ##mu s
            Var_matrix_inv[i+1,0]=Var_matrix_inv[0,i+1] = (mu_test*s_hat_hat)/(mu_test*s_hat_hat+b_hat_hat)
            ##s s
            if s_hat_hat >0.0:
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_hat_hat+b_hat_hat) + kev[i-len(b_count)]/(s_hat_hat**2)
                
            else:
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_hat_hat+b_hat_hat)
        if i < len(s_count):
            ## b s
            Var_matrix_inv[len(b_count)+1+i,i+1] = Var_matrix_inv[i+1,len(b_count)+1+i] = mu_test/(mu_test*s_hat_hat+b_hat_hat)
            
#    print 'inv matrix '+str(Var_matrix_inv[0,0])
#    print 'det '+str(np.linalg.det(Var_matrix_inv))

    if np.linalg.det(Var_matrix_inv) == 0:
        Var_matrix = np.zeros([(len(b_count)+1),(len(b_count)+1)])
  #Invert and return it
    else:
        Var_matrix = np.linalg.inv(Var_matrix_inv)

#    print 'matrix '+str(Var_matrix[0,0])

    return Var_matrix


def qMu_Asimov(mu_test,bCount,sCount,db):
#function to find the test statistic for a given value of mu
#take b_til as a variable to simulate oscilations about background mean
#first find the ML of mu and b
    result = 0
    for i in range(0,len(bCount)):
        # trap negative backgorund counts (!)
        if bCount[i]<0:
            bCount[i]=0
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

def chisquare(background, signal, measurement, error, sigerr, mu_test):
    # returns the Chi2 based on comparing the data (measurement) to a possible signal (sigCount - scaled by a mu_test. Could be zero.)
    # and a background prediction (background - could be identical to measurement) and a total uncertainty (error).
    # Each argument is a list of values, the returned chi2 is the result of comparing them all.
    chis= 0.0
    for i in range(0,len(background)):
         if error[i]>0.0 or sigerr[i]*mu_test>0.0:
             chis+=((float(mu_test*signal[i]+background[i]-measurement[i]))**2.0)/(float(error[i])**2+(mu_test*sigerr[i])**2)
    return chis


def confLevel(signal, background, measurement, sgErr, bgErr, measErr, kev, mu_test=1, test='LL'):

    # 'test' argument decides what statistical test will be used.
    # 'LL' means the CLs likelihood is used (as in contur paper) (poisson error assumption 
    # 'LLA' as LL, but use the qMu_Asimov function to construct the ratio instead, should be equivalent to LL
    # (TODO: add another one here to use the MC method instead of asymptotic/Asimov?)
    # 'CS' means the Chi2 goodness-of-fit is used (Gaussian error assumption)

    # kev is the actual number of generated events in the bin
 
    p_val=1.0
    p_sb =1.0
    p_b  =1.0

    # We need to know most likely mu, aka mu_hat. In current assumption (data=SM) this is known to be 0
    # TODO: this function expects floats, not lists.
    # mu_hat = ML_mu_hat(n_obs,bgCount,signal)
    mu_hat = 0
    
     #print "background", background
 
    if test=='LL':

        # prevent zeros getting in there, otherwise the matrix barfs and returns 100% exclusion
        if not np.any(signal):
            return 0, 0, 0

        # always assume background = measurement
        varMat= Covar_Matrix(measurement,signal,measErr,kev)[0,0]
         #print "varMat", varMat

        mu_hat = 0
        if varMat <=0:
            return 0, 0, 0 
        else:
            q_mu=0
            p_val=0
            q_mu = (mu_test-mu_hat)**2/(varMat)
            if 0 < q_mu <= (mu_test**2)/(varMat):
                ##Constant factor of 2 arises due to CL_s procedure and represents 1/spstat.norm(0)
                # Here rather than a factor of 2, the p_val in the null hypothesis needs to be worked out,
                # this 2 arises since CLs = 1-( p_(s+b)/1-p_b)
                # 1/(1-p_b) = 1/ (1-0.5) = 2
                # To evaluate this properly, the procedure above needs to be run again, but under the null hypothesis, i.e where mu_test is 0

                p_val=2.0*spstat.norm.sf(np.sqrt(q_mu))
            elif q_mu > (mu_test**2)/(varMat):
                p_val=2.0*spstat.norm.sf( (q_mu + (mu_test**2/varMat))/(2*mu_test/(np.sqrt(varMat))) )
            

    elif test=='LLA':

        # always assume background = measurement
        q_mu_a = qMu_Asimov(mu_test,measurement,signal,measErr)
        p_val=2.0*spstat.norm.sf(np.sqrt(q_mu_a))

    elif test[:2]=='CS':

        #print "using the Chi2 test on cross section plots"
        totalErr = []

        for i in range(0, len(measErr)):
            totalErr.append(np.sqrt(bgErr[i]**2+measErr[i]**2))

        # chisquare function above takes argument (background, signal, measurement, total_uncertainty)
        # signal + background
        chisq_p_sb = spstat.norm.sf(np.sqrt(chisquare( background,signal,measurement,totalErr,sgErr,1)))
        # background only
        chisq_p_b = spstat.norm.sf(np.sqrt(chisquare( background,signal,measurement,totalErr,sgErr,0)))

        #return this value 'cls' to get the confidence interval using a simple chi square fit
        p_val=chisq_p_sb/(1-chisq_p_b)

         #print "Prob. bg only, s+b, p, cls", chisq_p_b, chisq_p_sb, p_val, 1.0-p_val
        p_b =  chisq_p_b
        p_sb = chisq_p_sb

    else:
        print 'Unrecognised test type ', test
        

    
    # print 'returning', float('%10.6f' % float(1-p_val))
    

    return float('%10.6f' % float(1-p_val)), p_sb, p_b
