#!usr/bin/env python

from matplotlib import rcParams
import numpy as np
#from matplotlib.ticker import MaxNLocator


WIDTH = 454.0
FACTOR = 1.0/2.0
figwidthpt =WIDTH*FACTOR
inchesperpt = 1.0 / 72.27

golden_ratio  = (np.sqrt(5) - 1.0) / 2.0

figwidthin  = figwidthpt * inchesperpt  # figure width in inches
figheightin = figwidthin * golden_ratio +0.8   # figure height in inches
fig_dims    = [figwidthin, figheightin] # fig dims as a list

document_fontsize = 10
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['font.size'] = document_fontsize
rcParams['axes.titlesize'] = document_fontsize
rcParams['axes.labelsize'] = document_fontsize
rcParams['xtick.labelsize'] = document_fontsize
rcParams['ytick.labelsize'] = document_fontsize
rcParams['legend.fontsize'] = document_fontsize
rcParams['text.usetex'] = True