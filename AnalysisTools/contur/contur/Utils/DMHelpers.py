import os, sys
import numpy as np

##quick function to return the pertubative unitarity bound
#the 1.0 is gdm, currently hardcoded, grab from model file/ directory info eventually
def pertUnit(mz):
    gdm=0.25
    return np.sqrt(np.pi/2) * (mz/gdm)
    #return gdm * mdm / np.sqrt(np.pi/2)


