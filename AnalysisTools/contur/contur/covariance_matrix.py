import numpy as np

def covariance_matrix(s_count,b_count,db_count,mu_test,n_count,k_count): 
# what about n when b is a simulated background?
# two gaussian terms?
    """
        Build the covariance matrix from signal and background counts s and b.
        db is the uncertainty on background data.
    """

    assert( len(b_count) == len(s_count) == len(db_count) )

    matrix_size = len(b_count) + len(s_count) + 1

    Var_matrix_inv = np.zeros((matrix_size,matrix_size),dtype=np.float64)
#add exception handling if s=/=b
  
    ## create inverse covariance matrix V^-1
    for i in range(len(b_count)):
        squared_bracket = (mu_test*s_count[i]+b_count[i])**2
        print squared_bracket

        offset = len(b_count)+1
        
        ##Construct all the inverse covar matrix from second derivatives of Likelihood function

        ## mu mu
        Var_matrix_inv[0,0] += n_count[i]*s_count[i]**2 / squared_bracket

        ## mu b
        Var_matrix_inv[i+1,0] = Var_matrix_inv[0,i+1] = n_count[i]*s_count[i] / squared_bracket

        ## mu s
        Var_matrix_inv[i+offset,0]=Var_matrix_inv[0,i+offset] = -n_count[i]*b_count[i] / squared_bracket + 1

        ## b b
        Var_matrix_inv[i+1,i+1] = n_count[i]/squared_bracket
        if db_count[i]**2 > 0.0:
            Var_matrix_inv[i+1,i+1] += 1.0/db_count[i]**2
            
        ## s s
        Var_matrix_inv[i+offset,i+offset]= n_count[i]*mu_test**2/squared_bracket
        if s_count[i] > 0.0:
            Var_matrix_inv[i+offset,i+offset] += k_count[i]/s_count[i]**2

        ## b s mixed        
        Var_matrix_inv[i+offset,i+1] = Var_matrix_inv[i+1,i+offset] = mu_test*n_count[i]/squared_bracket
        
    print "before inversion"
    print Var_matrix_inv

    if np.linalg.det(Var_matrix_inv) == 0:
        print "Zero determinant"
        return np.zeros((matrix_size,matrix_size))
    else:
        return np.linalg.inv(Var_matrix_inv)

if __name__ == "__main__":
    mat = covariance_matrix([5.],[40.],[10],1.,[40.],[5.])
    print mat