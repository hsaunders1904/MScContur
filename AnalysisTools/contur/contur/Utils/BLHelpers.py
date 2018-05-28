import os, sys
import numpy as np

mh1 = 125.0
vev = 246.0


# inverse of mzprime
def xfromMzp(mzp):
    return 10.0*np.log10(mzp)

# LEP bound in x as function of y
# 
def LEPLimit(ylab):  
#  MZ'/g' > 6.9  so MZ' = g' * 6.9 TeV
    ret = []
    for val in ylab:
        mzp = val*6900
        if mzp > 200.:
            ret.append(xfromMzp(mzp))
        else:
            ret.append(np.nan)
    return ret


# ATLAS bound in x as function of y
# 
def ATLASLimit(ylab):    

#log10 g'/g = k M + c;  M = (log10(g'/g)-c)/k 
#0.1 = 2900 = -1
#1.0 = 5000 =  0
# so 5000k = -c,    -1 = 2900k + c = -2100k;    k = 1/2100, c = -5000/2100
#    sqrt(g'^2 + g^2) (SM) = 0.74
    k = 1.0/2100
    c = -50.0/21.0
    ret = []
    for val in ylab:
        mzp = (np.log10(val/.74)-c)/k
        if mzp > 150.:
            ret.append(xfromMzp(mzp))
        else:
            ret.append(np.nan)
    return ret

# Borexino bound in x as function of y
def BorexinoLimit(ylab):  
#  MZ'/g' > 250  so MZ' = g' * 250 GeV
    return xfromMzp(ylab*250)



# --------------------------------------------------------------------
# theory limits on B-L model
def bl3theory(mzp,g1p,mh2,sa):
    alpha=np.arcsin(sa)

    vacon = VaCon(lambda1(mh2,mzp,g1p,alpha),lambda2(mh2,mzp,g1p,alpha),lambda3(mh2,mzp,g1p,alpha))
    percon = PerCon(lambda1(mh2,mzp,g1p,alpha),lambda2(mh2,mzp,g1p,alpha),lambda3(mh2,mzp,g1p,alpha))
    vapercon = VaperCon(lambda1(mh2,mzp,g1p,alpha),lambda2(mh2,mzp,g1p,alpha),lambda3(mh2,mzp,g1p,alpha))

    return vacon, percon, vapercon


def xev(MZP,gBL):
	x = MZP/(2*gBL)
	return x
def lambda1(Mh2,MZP,gBL,Alpha):
	lambda11= (1/(4*vev**2))* ((mh1**2 + Mh2**2) - np.cos(2*Alpha)*(Mh2**2-mh1**2))
 	return lambda11
def lambda2(Mh2,MZP,gBL,Alpha):
	lambda11= (1/(4*xev(MZP,gBL)**2))* ((mh1**2 + Mh2**2) + np.cos(2*Alpha)*(Mh2**2-mh1**2))
 	return lambda11
def lambda3(Mh2,MZP,gBL,Alpha):
	lambda11= (1/(2*vev*xev(MZP,gBL))* (np.sin(2*Alpha)*(Mh2**2-mh1**2)))
 	return lambda11
def VaCon(lambda1,lambda2,lambda3):
	if ((4*lambda1*lambda2-lambda3>0) and lambda1>0 and lambda2>0):
		return 1
	else:
		return 0
def PerCon(lambda1,lambda2,lambda3):
	if ((abs(lambda1)<1) and (abs(lambda2)<1) and (abs(lambda3)<1)):
		return 1
	else:
		return 0
def VaperCon(lambda1,lambda2,lambda3):
	if ((abs(lambda1)<1) and (abs(lambda2)<1) and (abs(lambda3)<1) and (4*lambda1*lambda2-lambda3>0) and lambda1>0 and lambda2>0):
		return 1
	else:
		return 0





