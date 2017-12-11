import numpy as np
from scipy import stats as sp

def covariance_matrix(s,b,sigma,muprime=0,mu=1,tau=100): 
# what about n when b is a simulated background?
# two gaussian terms?
    """
        Build the covariance matrix from signal and background counts s and b.
        db is the uncertainty on background data.
    """

    assert( len(b) == len(s) == len(sigma) )

    matrix_size = len(b) + len(s) + 1

    V_inv = np.zeros((matrix_size,matrix_size),dtype=np.float64)
#add exception handling if s=/=b
  
    ## create inverse covariance matrix V^-1
    for i in range(len(b)):
        common_factor = (muprime*s[i]+b[i])/(mu*s[i]+b[i])**2
        print common_factor

        offset = len(b)+1
        
        ##Construct all the inverse covar matrix from second derivatives of Likelihood function

        ## mu mu
        V_inv[0,0] += s[i]**2 * common_factor

        ## mu b
        V_inv[i+1,0] = V_inv[0,i+1] = s[i] * common_factor

        ## mu s
        V_inv[i+offset,0]=V_inv[0,i+offset] = -b[i] * common_factor + 1

        ## b b
        V_inv[i+1,i+1] = common_factor
        if sigma[i]**2 > 0.0:
            V_inv[i+1,i+1] += 1.0/sigma[i]**2
            
        ## s s
        V_inv[i+offset,i+offset]= mu**2 * common_factor
        if s[i] > 0.0:
            V_inv[i+offset,i+offset] += tau/s[i]

        ## b s mixed        
        V_inv[i+offset,i+1] = V_inv[i+1,i+offset] = mu * common_factor
        
    print "before inversion"
    print V_inv

    if np.linalg.det(V_inv) == 0:
        print "Zero determinant"
        return np.zeros((matrix_size,matrix_size))
    else:
        return np.linalg.inv(V_inv)

def chisq(s,b,sigma,mu=1,tau=100):
    i = 0
    bPlusS = b[i] + s[i]
    justB  = b[i]

    chisq = (bPlusS - justB)**2 /  sigma[i]**2  # + MC err ** 2

    return chisq


if __name__ == "__main__":

    args = [[9.e1],[40.],[8.]]

    mu = 1
    muprime = 0

    mat = covariance_matrix(*args,mu=1,muprime=0)
    print mat

    #print chisq(*args)

    sigma_muhat_sq = mat[0,0]
    sigma_muhat    = np.sqrt(sigma_muhat_sq)

    print 'sigma_muhat', sigma_muhat

    # Cowan sect. 3.7
    q_mu = (mu-muprime)**2/sigma_muhat_sq

    if q_mu <= mu**2/sigma_muhat_sq:
        # should always be here
        F_arg = np.sqrt(q_mu) - (mu-muprime)/sigma_muhat
    else:
        F_arg = (q_mu - (mu**2 - 2*mu*muprime)/sigma_muhat_sq)/(2*mu/sigma_muhat)

    p_val = sp.halfnorm.sf( F_arg )

    print
    print 'DATA    ',args[1]
    print 'ERR     ',args[2]
    print
    print 'SIGNAL  ',args[0]
    print
    print 'Significance',F_arg

    print 'p',p_val, "BSM ruled out" if p_val < 0.95 else "BSM allowed"

    print chisq(*args)
