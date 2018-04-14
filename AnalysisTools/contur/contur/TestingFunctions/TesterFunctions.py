#!usr/bin/env python

import os, sys
import numpy as np
import scipy.stats as spstat
import math
from math import *
import scipy.optimize as spopt

global mu_test
mu_test=1

def Min_function(x, n_obs, b_obs, s_obs, db, ds):
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
        d_lnL_ds += ds / x[1]
    if s_obs > 0.0:
        d_lnL_ds -= ds/s_obs
    return [d_lnL_db,d_lnL_ds]


def Min_find(n_obs, b_obs, s_obs, db, ds):
    #Min find just runs the root finding on the Min_function so just needs to pass through the arguments
    # s_hat_hat is called x_1, b_hat_hat is x_0
    # func_0 being the first entry in vector, corresponds to dlnL/db
    # func_1 dlnL/ds
    return spopt.root(Min_function, [b_obs, s_obs], args=(n_obs, b_obs, s_obs, db, ds))



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

def Covar_Matrix(b_count,s_count,db_count, tau):
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
            res = Min_find(b_count[i], b_count[i], s_count[i], db_count[i], tau[i]).x
        else:
            res = Min_find(b_count[i-len(b_count)], b_count[i-len(b_count)], s_count[i-len(b_count)], db_count[i-len(b_count)], tau[i-len(b_count)]).x
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
                Var_matrix_inv[i+1,i+1]=(mu_test**2)/(mu_test*s_hat_hat+b_hat_hat) + tau[i-len(b_count)]/(s_hat_hat**2)
                
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

def chisquare(background, signal, measurement, error, mu_test):
    # returns the Chi2 based on comparing the data (measurement) to a possible signal (sigCount - scaled by a mu_test. Could be zero.)
    # and a background prediction (bgCounts - could be identical to n_obs) and a total uncertainty (error).
    # Each argument is a list of values, the returned chi2 is the result of comparing them all.
    chis= 0.0
    for i in range(0,len(background)):
         if error[i]>0.0:
            chis+=((float(mu_test*signal[i]+background[i]-measurement[i]))**2.0)/(float(error[i])**2.0)
    return chis


def confLevel(signal, background, measurement, sgErr, bgErr, measErr, tau, mu_test=1, test='LL'):

    # Does not make use of measurement or error (assumed=data).
    # Does not make use of sigErr (uses tau to get MC stats)

    # 'test' argument decides what statistical test will be used.
    # 'LL' means the CLs likelihood is used (as in contur paper) (poisson error assumption 
    # 'LLA' as LL, but use the qMu_Asimov function to construct the ratio instead, should be equivalent to LL
    # (TODO: add another one here to use the MC method instead of asymptotic/Asimov?)
    # 'CS' means the Chi2 goodness-of-fit is used (Gaussian error assumption)

    # tau is (or will be) the ratio of MC to data events in the plot under consideration.
 
    p_val=1.0

    # We need to know most likely mu, aka mu_hat. In current assumption (data=SM) this is known to be 0
    # TODO: this function expects floats, not lists.
    # mu_hat = ML_mu_hat(n_obs,bgCount,signal)
    mu_hat = 0

    if test=='LL':

        # When we call the varMatrix, this needs to be passed an additional argument for the measurement
        # currently uses mu_test which is hard coded to 1
        # This function should be called twice, once at mu_test=1 and once at mu_test=0

        varMat= Covar_Matrix(background,signal,bgErr,tau)[0,0]

        # NOTE: I believe the biggest restructing needed is to take the min_find out of this Covar_matrix, if I have things correct in my head then
        # recipe is as follows:
        # Work out b_hat_hat and s_hat_hat here in this function, using mu_hat as an additional argument to these functions,
        # we need to call this covar matrix twice at the tested mu values, but b_hat_hat and s_hat_hat should be the same in both cases

        mu_hat = 0
        if varMat <=0:
            return 0
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

        q_mu_a = qMu_Asimov(mu_test,background,signal,bgErr)
        p_val=2.0*spstat.norm.sf(np.sqrt(q_mu_a))

    elif test=='CS':

        #print 'using the Chi2 test on cross section plots'

        totalErr = measErr
        # Include the MCstats
        for i in range(0, len(measErr)):
            totalErr[i] = np.sqrt(measErr[i]**2+sgErr[i]**2)


        # chisquare function above takes argument (background, signal, measurement, total_uncertainty)
        # Here we are assuming measurement = background, and the measurement error dominates.
        chisq_p_sb = spstat.norm.sf(np.sqrt(chisquare( background,signal,measurement,totalErr, 1)))

        #Explicitly find p_b rather than just use two, no cost to evaluate a norm.sf of 0!
        chisq_p_b = 1-spstat.norm.sf(np.sqrt(chisquare( background,signal,measurement,totalErr, 0)))
        #return this value 'cls' to get the confidence interval using a simple chi square fit
        p_val=chisq_p_sb/(1-chisq_p_b)

        #print 'Chi2 sb, b, p_val', chisq_p_sb, chisq_p_b, p_val

    elif test=='CSR':

        #print 'using the Chi2 test on ratio plots'

        # chisquare function above takes argument (background, signal, measurement, total_uncertainty)
        # TODO: fix this for ratios. Is this really needed? What would change?
        chisq_p_sb = spstat.norm.sf(np.sqrt(chisquare( background,signal,measurement,totalErr, 1)))

        #Explicitly find p_b rather than just use two, no cost to evaluate a norm.sf of 0!
        chisq_p_b = 1-spstat.norm.sf(np.sqrt(chisquare( background,signal,measurement,totalErr, 0)))
        #return this value 'cls' to get the confidence interval using a simple chi square fit
        p_val=chisq_p_sb/(1-chisq_p_b)

         #print 'Chi2 sb, b, p_val', chisq_p_sb, chisq_p_b, p_val

    else:
        print 'Unrecognised test type ', test
        

    
     #print 'returning', float('%10.6f' % float(1-p_val))
    
    return float('%10.6f' % float(1-p_val))
