#!usr/bin/env python

"""A simplified version of a MC toys based likelihood calculator
"""

import yoda, optparse, sys, math
import numpy as np
import os
import scipy.stats as sp
import scipy.misc as fact
from scipy.optimize import minimize, brentq
from math import *
import TesterFunctions as tf

def qMu_MC(n,b_til):
#function to find the test statistic for a given value of mu
#take b_til as a variable to simulate oscilations about background mean
#first find the ML of mu and b
  mu_hat = tf.ML_mu_hat(n,b_til,s0)
  #print "muhat", mu_hat
  b_hat = tf.ML_b_hat(n,mu_hat,b_til)
  if mu_hat > 1.0:
    return 0
  # if mu_hat < 0, fix mu_hat = 0 and re-evaluate best b_hat
  elif mu_hat < 0.:
    mu_hat = 0
    b_hat = tf.ML_b_hat(n,mu_hat,b_til)

  # Now, Maximise at the hypothesised mu
  # b_hat_hat, the b that maximizes the likelihood for the hypothesised mu

  b_hat_hat = tf.ML_b_hat(n, muprime,b_til)

  # Having this, formulate the profile likelihood
  # First, evaluate n_exp for N_exp_hat and N_exp_hat_hat
  N_exp_b_hat_hat = tf.n_exp(muprime, b_hat_hat)
  N_exp_b_hat = tf.n_exp(mu_hat, b_hat)

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
    result = -2.*(tf.gauss_exp(b_til,b_hat) - tf.gauss_exp(b_til,b_hat_hat))
  else:
    # Otherwise, return the normal likelihood
    result = -2.*(n*log(N_exp_b_hat_hat/N_exp_b_hat) + N_exp_b_hat - N_exp_b_hat_hat + tf.gauss_exp(b_til,b_hat) - tf.gauss_exp(b_til,b_hat_hat))
  return result


def qMu_obs_MC(n_obs, b0_in, db_in, s0_in,mu_test_in):
#build the observed test statistic then run MC pseudoexperiments to estimate the pdf from the number of events exceeding the observed mu
  global b0, s0, db, muprime # Passes this to nexp function
  b0 = b0_in
  s0 = s0_in
  db = db_in
  muprime = mu_test_in
  # Find observed test statistic
  qMu_obs = qMu_MC(n_obs,b0)

  #define how many pseudo experiments to run
  nPseudo=1500
  NSIG = nPseudo * 5 # You need more signal MC as only few will pass
  NBKG = nPseudo

  # Find values for the nuisance parameters (in both hypotheses), which are most likely according to the observation
  b_hat_obs_mu=tf.ML_b_hat(n_obs,mu_test_in,b0)
  b_hat_obs_0=tf.ML_b_hat(n_obs,0,b0)

  # Run pseudo experiments for the nuisance parameters.
  qMu_pseu_sig = []
  qMu_pseu_bkg = []

  #using the most likely background count for each hypothesis, calc the expected count for each hypothesis
  #_sig is sig+bkg (mu=1) hypothesis, _bkg is the background only hypothesis
  n_exp_sig = tf.n_exp(mu_test_in,b_hat_obs_mu)
  n_exp_bkg = tf.n_exp(0.,b_hat_obs_0)
  if n_exp_sig<0:
    return 0
  if n_exp_bkg<0:
    return 0
  #Randomly generate outcomes based on the expected count
  n_pseu_sig = np.random.poisson(n_exp_sig, NSIG)
  b_pseu_sig = np.random.normal(b_hat_obs_mu, db, NSIG)
  #print "b_mu:", b_pseu_sig, "\t n_mu:", n_pseu_sig
  n_pseu_bkg = np.random.poisson(n_exp_bkg, NBKG)
  b_pseu_bkg = np.random.normal(b_hat_obs_0, db, NBKG)
  #print "b_0:", b_pseu_bkg, "\t n_0:", n_pseu_bkg

  #Determine how many pseudo experiments would have been as positive as the observed experiment.
  #ps = (relative number of positive signal+background pseudoexperiments)
  #1-pb = (relative number of positive background pseudoexperiments)
  #CLs = ps/(1-pb)
  #Errors are determined as Poissonian MC errors
  positive_sig = 0
  positive_bkg = 0
  for i in range(NSIG):
    if qMu_MC(n_pseu_sig[i],b_pseu_sig[i]) >= qMu_obs:
      positive_sig += 1
  for i in range(NBKG):
    if qMu_MC(n_pseu_bkg[i],b_pseu_bkg[i]) >= qMu_obs:
      positive_bkg += 1

  ps = positive_sig/float(NSIG)
  d_ps = sqrt(positive_sig)/float(NSIG)
  oneminus_pb = positive_bkg/float(NBKG)
  d_oneminus_pb = sqrt(positive_bkg)/float(NBKG)
  #print str(ps)+"     "+str(oneMinusPb)
  if oneminus_pb == 0:
    CLs = 1.0
    dCLs = 1.0
  else:
    CLs = ps/oneminus_pb
    if CLs == 0.0:
      dCLs = 1.0
    else:
      dCLs = sqrt((d_ps/oneminus_pb)**2+(ps*d_oneminus_pb/oneminus_pb**2)**2)

  del n_pseu_sig
  del n_pseu_bkg
  del b_pseu_sig
  del b_pseu_bkg

  return (ps, oneminus_pb, CLs, dCLs)


def qMu_obs(n_obs, b0_in, db_in, s0_in,mu_test_in):
  # Build the observed test statistic for a given strength parameter
  global b0, s0, db, muprime # Passes these global variables to other functions
  b0 = b0_in
  s0 = s0_in
  db = db_in
  muprime = mu_test_in
  # Find observed test statistic
  qMu_obs = qMu_MC(n_obs,b0)
  return(qMu_obs)

