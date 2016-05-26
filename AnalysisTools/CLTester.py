#! /usr/bin/env python

"""\
%prog - generate histogram comparison plots

USAGE:
 %prog [options] yodafile1[:'PlotOption1=Value':'PlotOption2=Value':...] [path/to/yodafile2 ...] [PLOT:Key1=Val1:...]

where the plot options are described in the make-plots manual in the HISTOGRAM
section.
"""

import rivet, yoda, sys, os
rivet.util.check_python_version()
rivet.util.set_process_name(os.path.basename(__file__))

#############################################################################################
### Here some of the leftover functions from cmp-histos, some are used some aren't, can be cleaned up


class Plot(dict):
    "A tiny Plot object to help writing out the head in the .dat file"
    def __repr__(self):
        return "# BEGIN PLOT\n" + "\n".join("%s=%s" % (k,v) for k,v in self.iteritems()) + "\n# END PLOT\n\n"


def sanitiseString(s):
    #s = s.replace('_','\\_')
    #s = s.replace('^','\\^{}')
    #s = s.replace('$','\\$')
    s = s.replace('#','\\#')
    s = s.replace('%','\\%')
    return s


def getCommandLineOptions():
    "Parse command line options"
    from optparse import OptionParser, OptionGroup
    parser = OptionParser(usage=__doc__)

    parser.add_option("--no-rivet-refs", dest="RIVETREFS", action="store_false",
                      default=True, help="don't use Rivet reference data files")
    parser.add_option('-o', '--outdir', dest='OUTDIR',
                      default='.', help='write data files into this directory')
    parser.add_option("--hier-out", action="store_true", dest="HIER_OUTPUT", default=True,
                      help="write output dat files into a directory hierarchy which matches the analysis paths")
    parser.add_option('--plotinfodir', dest='PLOTINFODIRS', action='append',
                      default=['.'], help='directory which may contain plot header information (in addition '
                      'to standard Rivet search paths)')

    stygroup = OptionGroup(parser, "Plot style")
    # stygroup.add_option("--refid", dest="REF_ID",
    #                     default="REF", help="ID of reference data set (file path for non-REF data)")
    stygroup.add_option("--linear", action="store_true", dest="LINEAR",
                        default=False, help="plot with linear scale")
    stygroup.add_option("--mc-errs", action="store_true", dest="MC_ERRS",
                        default=False, help="show vertical error bars on the MC lines")
    stygroup.add_option("--no-ratio", action="store_false", dest="RATIO",
                        default=True, help="disable the ratio plot")
    stygroup.add_option("--rel-ratio", action="store_true", dest="RATIO_DEVIATION",
                        default=False, help="show the ratio plots scaled to the ref error")
    stygroup.add_option("--no-plottitle", action="store_true", dest="NOPLOTTITLE",
                        default=False, help="don't show the plot title on the plot "
                        "(useful when the plot description should only be given in a caption)")
    stygroup.add_option("--style", dest="STYLE", default="default",
                        help="change plotting style: default|bw|talk")
    stygroup.add_option("-c", "--config", dest="CONFIGFILES", action="append", default=["~/.make-plots"],
                        help="additional plot config file(s). Settings will be included in the output configuration.")
    parser.add_option_group(stygroup)

    selgroup = OptionGroup(parser, "Selective plotting")
    # selgroup.add_option("--show-single", dest="SHOW_SINGLE", choices=("no", "ref", "mc", "all"),
    #                     default="mc", help="control if a plot file is made if there is only one dataset to be plotted "
    #                     "[default=%default]. If the value is 'no', single plots are always skipped, for 'ref' and 'mc', "
    #                     "the plot will be written only if the single plot is a reference plot or an MC "
    #                     "plot respectively, and 'all' will always create single plot files.\n The 'ref' and 'all' values "
    #                     "should be used with great care, as they will also write out plot files for all reference "
    #                     "histograms without MC traces: combined with the -R/--rivet-refs flag, this is a great way to "
    #                     "write out several thousand irrelevant reference data histograms!")
    # selgroup.add_option("--show-mc-only", "--all", action="store_true", dest="SHOW_IF_MC_ONLY",
    #                     default=False, help="make a plot file even if there is only one dataset to be plotted and "
    #                     "it is an MC one. Deprecated and will be removed: use --show-single instead, which overrides this.")
    # # selgroup.add_option("-l", "--histogram-list", dest="HISTOGRAMLIST",
    # #                     default=None, help="specify a file containing a list of histograms to plot, in the format "
    # #                     "/ANALYSIS_ID/histoname, one per line, e.g. '/DELPHI_1996_S3430090/d01-x01-y01'.")
    selgroup.add_option("-m", "--match", action="append",
                        help="Only write out histograms whose $path/$name string matches these regexes. The argument "
                        "may also be a text file.",
                        dest="PATHPATTERNS")
    selgroup.add_option("-M", "--unmatch", action="append",
                        help="Exclude histograms whose $path/$name string matches these regexes",
                        dest="PATHUNPATTERNS")
    parser.add_option_group(selgroup)

    return parser


def getHistos(filelist):
    """Loop over all input files. Only use the first occurrence of any REF-histogram
    and the first occurrence in each MC file for every MC-histogram."""
    refhistos = {}
    mchistos = {}
    #for infile in filelist:
    mchistos.setdefault(filelist, {})
    analysisobjects = yoda.read(filelist, patterns=opts.PATHPATTERNS, unpatterns=opts.PATHUNPATTERNS)
    for path, ao in analysisobjects.iteritems():
            ## Conventionally don't plot data objects whose names start with an underscore
        if os.path.basename(path).startswith("_"):
            continue
        if path.startswith('/REF/'):
            if not refhistos.has_key(path):
                refhistos[path] = ao
        else:
            if not mchistos[filelist].has_key(path):
                mchistos[filelist][path] = ao
    return refhistos, mchistos


def getRivetRefData(refhistos, anas=None):
    "Find all Rivet reference data files"
    rivet_data_dirs = rivet.getAnalysisRefPaths()
    dirlist = []
    for d in rivet_data_dirs:
        if anas is None:
            import glob
            dirlist.append(glob.glob(os.path.join(d, '*.yoda')))
        else:
            dirlist.append([os.path.join(d, a+'.yoda') for a in anas])
    for filelist in dirlist:
        # TODO: delegate to getHistos?
        for infile in filelist:
            analysisobjects = yoda.read(infile, patterns=opts.PATHPATTERNS, unpatterns=opts.PATHUNPATTERNS)
            for path, ao in analysisobjects.iteritems():
                if path.startswith('/REF/'):
                    if not refhistos.has_key(path):
                        refhistos[path] = ao


def parseArgs(args):
    """Look at the argument list and split it at colons, in order to separate
    the file names from the plotting options. Store the file names and
    file specific plotting options."""
    filelist = []
    plotoptions = {}
    for a in args:
        asplit = a.split(':')
        path = asplit[0]
        filelist.append(path)
        plotoptions[path] = []
        has_title = False
        for i in xrange(1, len(asplit)):
            ## Add 'Title' if there is no = sign before math mode
            if '=' not in asplit[i] or ('$' in asplit[i] and asplit[i].index('$') < asplit[i].index('=')):
                asplit[i] = 'Title=%s' % asplit[i]
            if asplit[i].startswith('Title='):
                has_title = True
            plotoptions[path].append(asplit[i])
        if path != "PLOT" and not has_title:
            plotoptions[path].append('Title=%s' % sanitiseString(os.path.basename( os.path.splitext(path)[0] )) )
    return filelist, plotoptions


def setStyle(ao, style):
    """Set default plot styles (color and line width) colors borrowed from Google Ngrams"""
    LINECOLORS = ['{[HTML]{EE3311}}',  # red (Google uses 'DC3912')
                  '{[HTML]{3366FF}}',  # blue
                  '{[HTML]{109618}}',  # green
                  '{[HTML]{FF9900}}',  # orange... weirdly this screws up if the F is lower-case!
                  '{[HTML]{990099}}']  # lilac
    LINESTYLES = ['solid',
                  'dashed',
                  'dashdotted',
                  'dotted']

    if opts.STYLE == 'talk':
        ao.setAnnotation('LineWidth', '1pt')
    if opts.STYLE == 'bw':
        LINECOLORS = ['black!90',
                      'black!50',
                      'black!30']

    c = style % len(LINECOLORS)
    s = (style / len(LINECOLORS)) % len(LINESTYLES)

    ao.setAnnotation('LineStyle', '%s' % LINESTYLES[s])
    ao.setAnnotation('LineColor', '%s' % LINECOLORS[c])


def setOptions(ao, options):
    "Set arbitrary annotations"
    for opt in options:
        key, val = opt.split('=', 1)
        ao.setAnnotation(key, val)


# TODO: move to rivet.utils
def mkoutdir(outdir):
    "Function to make output directories"
    if not os.path.exists(outdir):
        try:
            os.makedirs(outdir)
        except:
            msg = "Can't make output directory '%s'" % outdir
            raise Exception(msg)
    if not os.access(outdir, os.W_OK):
        msg = "Can't write to output directory '%s'" % outdir
        raise Exception(msg)
        
def writeOutput(output, h, root):
    "Choose output file name and dir"
    hparts = h.strip("/").split("/")
    if opts.HIER_OUTPUT:
        ana = "_".join(hparts[:-1]) if len(hparts) > 1 else "ANALYSIS"
        outdir = os.path.join(root, ana)
        outfile = '%s.dat' % hparts[-1]
    else:
        outdir = opts.OUTDIR
        outfile = '%s.dat' % "_".join(hparts)
    mkoutdir(outdir)
    outfilepath = os.path.join(outdir, outfile)
    f = open(outfilepath, 'w')
    f.write(output)
    f.close()

def writeOutputHier(output, h):
    "Choose output file name and dir"
    hparts = h.strip("/").split("/")
    if opts.HIER_OUTPUT:
        ana = "_".join(hparts[:-1]) if len(hparts) > 1 else "ANALYSIS"
        outdir = os.path.join(opts.OUTDIR, ana)
        outfile = '%s.dat' % hparts[-1]
    else:
        outdir = opts.OUTDIR
        outfile = '%s.dat' % "_".join(hparts)
    # outdir = opts.OUTDIR
    # outfile=output
    mkoutdir(outdir)
    outfilepath = os.path.join(outdir, outfile)
    f = open(outfilepath, 'w')
    for item in output:
        f.write(str(item) + "\n")
    #f.write(output)
    f.close()

#############################################################################################
### Here store aditional static data we dont get from rivet, this can be improved greatly..
anapool=['ATLAS_7_JETS','ATLAS_7_Zjj','ATLAS_7_Wjj_mu','CMS_7_JETS','CMS_7_Wjj','CMS_7_Zjj','ATLAS_8_JETS','ATLAS_7_Wjj_EL','ATLAS_7_GAMMA','ATLAS_7_Z_GAMMA','ATLAS_7_W_GAMMA_MU','ATLAS_7_W_GAMMA_EL','ATLAS_7_ZZ','ATLAS_7_GAMMAGAMMA']
##This is really bad, but set up an arbitrary number of subpool tags to iterate over, this should just be done on the fly for each analysis!
subpools=['R1','R2','R3','R4']
def LumiFinder(h):
    #ananame = h.strip("/").split("/")[0]
    lumi = -1
    anatype=''
    subpool=''
    if 'ATLAS_2014_I1325553' in h:
        lumi = 4500
        anatype=anapool[0]
    elif 'ATLAS_2014_I1268975' in h:
        lumi = 4500
        anatype=anapool[0]
        R1=['d01-x01-y01','d01-x01-y02','d01-x01-y03','d01-x01-y04','d01-x01-y05','d01-x01-y06']
        R2=['d02-x01-y01','d02-x01-y02','d02-x01-y03','d02-x01-y04','d02-x01-y05','d02-x01-y06']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]
    elif 'ATLAS_2014_I1326641' in h:
        lumi = 4510
        anatype=anapool[0]
    elif 'ATLAS_2013_I1230812' in h:
        #Z+jets
        blacklist=['d02','d04','d06','d08']
        lumi = 4600
        anatype=anapool[1]
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
#    elif 'ATLAS_2013_I1217863' in h:
#        lumi = 4600
    elif 'ATLAS_2012_I1093738' in h:
        lumi = 37
        anatype=anapool[8]
    elif 'ATLAS_2012_I1083318' in h:
        lumi = 36
    elif 'ATLAS_2011_I945498' in h:
        lumi = 36
    elif 'ATLAS_2011_I921594' in h:
        lumi = 35
    elif 'ATLAS_2011_S9128077' in h:
        lumi = 2.4
    elif 'CMS_2014_I1298810' in h:
        lumi = 5000
        anatype=anapool[3]
        blacklist=['d13','d14','d15','d16','d17','d18']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
        R1=['d01-x01-y01','d02-x01-y01','d03-x01-y01','d04-x01-y01','d05-x01-y01','d06-x01-y01']
        R2=['d07-x01-y01','d08-x01-y02','d09-x01-y01','d10-x01-y01','d11-x01-y01','d12-x01-y01']
        for poolmember in R1:
            if poolmember in h:
                subpool = subpools[0]
        for poolmember in R2:
            if poolmember in h:
                subpool = subpools[1]

    elif 'ATLAS_2013_I1244522' in h:
        lumi = 37
    elif 'ATLAS_2014_I1306294' in h:
        lumi = 4600
    elif 'CMS_2013_I1256943' in h:
        lumi = 5200
    elif 'CMS_2015_I1310737' in h:
        lumi = 4900
        anatype=anapool[5]
    elif 'CMS_2014_I1303894' in h:
        lumi = 5000
        anatype=anapool[4]
    elif 'ATLAS_2014_I1319490_MU' in h:
        lumi = 4600
        anatype=anapool[2]
    elif 'ATLAS_2014_I1319490_EL' in h:
        lumi = 4600
        anatype=anapool[7]
    elif 'ATLAS_2015_I1394679' in h:
        ##this analysis uses y units of fb
        lumi =20.3
        anatype=anapool[6]
    elif 'ATLAS_2014_I1307243' in h:
        lumi = -1
        anatype=anapool[0]
        whitelist=['d13','d14','d15','d16','d17','d18','d19','d20','d21','d22','d23','d24','d25','d26','d27','d28']
        for plotkey in whitelist:
            if plotkey in h:
                lumi = 4500
    elif 'ATLAS_2013_I1263495' in h:
        lumi = 4600
        anatype =anapool[8]
    elif 'ATLAS_2013_I1217863_Z' in h:
        lumi = 4.6
        anatype= anapool[9]
        blacklist=['d17','d18','d20']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2013_I1217863_W_MU' in h:
        lumi = 4.6
        anatype= anapool[10]
        blacklist=['d15','d16','d19']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2013_I1217863_W_EL' in h:
        lumi = 4.6
        anatype= anapool[11]
        blacklist=['d15','d16','d19']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2012_I1203852' in h:
        lumi = 4.600
        anatype= anapool[12]
        blacklist=['d03','d04','d05','d06','d07','d08']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1
    elif 'ATLAS_2012_I1199269' in h:
        lumi = 4900
        anatype=anapool[13]
        blacklist=['d04']
        for plotkey in blacklist:
            if plotkey in h:
                lumi = -1

    return lumi,anatype,subpool

#############################################################################################
### Now the testing functions, the bulk of this is for the MC tester that no longer works without changing
### the CLs calculation use


import yoda, optparse, sys, math
import numpy as np
import os
import scipy.stats as sp
import scipy.misc as fact
from scipy.optimize import minimize, brentq
from math import *

def n_exp(mu, b_hat):
#Expected count n, the mean of the poisson used to define event count
  return b_hat + s0*mu

def n_exp_model(mu, b_hat, s_in):
#Expected count n, the mean of the poisson used to define event count
  return b_hat + s_in*mu

def ML_b_hat(n,mu,b_til):
#Maximum likelihood estimate for the background count b
#form is the root of the polynomial in b derived from differentiating the log likelihood wrt b
# A(b^2) + B(b) + C = 0
    B=-(b_til - mu*s0 - (db**2))
    C=(-b_til*mu*s0 + (db**2)*(mu*s0-n))
    return (-B+(B**2 - 4*C)**0.5)*0.5

def ML_b_hat_model(n,mu,b_til, sig_in, db_in):
#Maximum likelihood estimate for the background count b
#form is the root of the polynomial in b derived from differentiating the log likelihood wrt b
# A(b^2) + B(b) + C = 0
    B=-(b_til - mu*sig_in - (db_in**2))
    C=(-b_til*mu*sig_in + (db_in**2)*(mu*sig_in-n))
    return (-B+(B**2 - 4*C)**0.5)*0.5


def ML_mu_hat(n_obs,b_in,s_in):
#Maximum likelihood estimate for the strength parameter mu
    if fabs(s_in) <= 1E-5:
      return 0
    else:
      return (n_obs - b_in)/s_in

def gauss_exp(var, mean):
#defining the exponent of the gaussian for convenience in log likelihood
    if fabs(db) <= 1E-5:
      return 0
    else:
      return (var-mean)**2./(2.*db**2)

def gauss_exp_model(var, mean, db):
#defining the exponent of the gaussian for convenience in log likelihood
    if fabs(db) <= 1E-5:
      return 0
    else:
      return (var-mean)**2./(2.*db**2)

def qMu_Asimov(mu_test,bCount,sCount,db):
#function to find the test statistic for a given value of mu
#take b_til as a variable to simulate oscilations about background mean
#first find the ML of mu and b
    result = 0
    for i in range(0,len(bCount)):
        mu_hat = ML_mu_hat(bCount[i],bCount[i],sCount[i])
        b_hat = ML_b_hat_model(bCount[i],mu_hat,bCount[i], sCount[i], db[i])
        if mu_hat > 1.0:
            return 0
        elif mu_hat < 0.:
            mu_hat=0
            b_hat = ML_b_hat_model(bCount[i],mu_hat,bCount[i],sCount[i],db[i])

        b_hat_hat = ML_b_hat_model(bCount[i],mu_test,bCount[i],sCount[i],db[i])

        N_exp_b_hat_hat = n_exp_model(mu_test, b_hat_hat,sCount[i])
        N_exp_b_hat = n_exp_model(mu_hat, b_hat,sCount[i])
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
            result = -2.*(gauss_exp_model(bCount[i],b_hat,db[i]) - gauss_exp_model(bCount[i],b_hat_hat,db[i]))
        else:
            # Otherwise, return the normal likelihood
            result += -2.*(bCount[i]*log(N_exp_b_hat_hat/N_exp_b_hat) + N_exp_b_hat - N_exp_b_hat_hat + gauss_exp_model(bCount[i],b_hat,db[i]) - gauss_exp_model(bCount[i],b_hat_hat,db[i]))
    return result

    #return mu_hat
  # mu_hat = ML_mu_hat(n,b_til,s0)
  # #print "muhat", mu_hat
  # b_hat = ML_b_hat(n,mu_hat,b_til)
  # if mu_hat > 1.0:
  #   return 0
  # # if mu_hat < 0, fix mu_hat = 0 and re-evaluate best b_hat
  # elif mu_hat < 0.:
  #   mu_hat = 0
  #   b_hat = ML_b_hat(n,mu_hat,b_til)
  #
  # # Now, Maximise at the hypothesised mu
  # # b_hat_hat, the b that maximizes the likelihood for the hypothesised mu
  #
  # b_hat_hat = ML_b_hat(n, muprime,b_til)
  #
  # # Having this, formulate the profile likelihood
  # # First, evaluate n_exp for N_exp_hat and N_exp_hat_hat
  # N_exp_b_hat_hat = n_exp(muprime, b_hat_hat)
  # N_exp_b_hat = n_exp(mu_hat, b_hat)
  #
  # # If any n_exp is almost zero, it should be set to zero
  # if (N_exp_b_hat < 0) and (fabs(N_exp_b_hat) < 1E-5):
  #   N_exp_b_hat = 0
  # if (N_exp_b_hat_hat < 0) and (fabs(N_exp_b_hat_hat) < 1E-5):
  #   N_exp_b_hat_hat = 0
  #
  # # If any expected value is really negative, there has been a problem somewhere
  # if (N_exp_b_hat < 0) or (N_exp_b_hat_hat < 0):
  #   exit("ERROR: In S95 calculation, profile likelihood asked for nexp < 0!")
  #   N_exp_b_hat = N_exp_b_hat_hat =0
  # result = 0
  #
  # # If any expected value is zero both must be zero
  # if N_exp_b_hat*N_exp_b_hat_hat == 0:
  #   #if N_exp_b_hat != 0 or N_exp_b_hat_hat != 0:
  #   #  exit("ERROR: In S95 calculation, profile likelihood asked for impossible maximisation parameteres!")
  #   # In that case, the result is only the likelihood w.r.t the nuisance parameters
  #   result = -2.*(gauss_exp(b_til,b_hat) - gauss_exp(b_til,b_hat_hat))
  # else:
  #   # Otherwise, return the normal likelihood
  #   result = -2.*(n*log(N_exp_b_hat_hat/N_exp_b_hat) + N_exp_b_hat - N_exp_b_hat_hat + gauss_exp(b_til,b_hat) - gauss_exp(b_til,b_hat_hat))
  # return result


def qMu_MC(n,b_til):
#function to find the test statistic for a given value of mu
#take b_til as a variable to simulate oscilations about background mean
#first find the ML of mu and b
  mu_hat = ML_mu_hat(n,b_til,s0)
  #print "muhat", mu_hat
  b_hat = ML_b_hat(n,mu_hat,b_til)
  if mu_hat > 1.0:
    return 0
  # if mu_hat < 0, fix mu_hat = 0 and re-evaluate best b_hat
  elif mu_hat < 0.:
    mu_hat = 0
    b_hat = ML_b_hat(n,mu_hat,b_til)

  # Now, Maximise at the hypothesised mu
  # b_hat_hat, the b that maximizes the likelihood for the hypothesised mu

  b_hat_hat = ML_b_hat(n, muprime,b_til)

  # Having this, formulate the profile likelihood
  # First, evaluate n_exp for N_exp_hat and N_exp_hat_hat
  N_exp_b_hat_hat = n_exp(muprime, b_hat_hat)
  N_exp_b_hat = n_exp(mu_hat, b_hat)

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
    result = -2.*(gauss_exp(b_til,b_hat) - gauss_exp(b_til,b_hat_hat))
  else:
    # Otherwise, return the normal likelihood
    result = -2.*(n*log(N_exp_b_hat_hat/N_exp_b_hat) + N_exp_b_hat - N_exp_b_hat_hat + gauss_exp(b_til,b_hat) - gauss_exp(b_til,b_hat_hat))
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
  b_hat_obs_mu=ML_b_hat(n_obs,mu_test_in,b0)
  b_hat_obs_0=ML_b_hat(n_obs,0,b0)

  # Run pseudo experiments for the nuisance parameters.
  qMu_pseu_sig = []
  qMu_pseu_bkg = []

  #using the most likely background count for each hypothesis, calc the expected count for each hypothesis
  #_sig is sig+bkg (mu=1) hypothesis, _bkg is the background only hypothesis
  n_exp_sig = n_exp(mu_test_in,b_hat_obs_mu)
  n_exp_bkg = n_exp(0.,b_hat_obs_0)
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


#############################################################################################
### This is the main function used for extracting the variance in the strength parameter for constructing the CLs

def Var_mu(mu,b_hat,s_in,db_in):
#Construct the inverse variance matrix from expected vals of the 2nd derivatives of the Log Likelihood
  Var_matrix_inv=np.zeros([2,2])
  #mu mu
  Var_matrix_inv[0,0]=s_in**2/(mu*s_in+b_hat)
  #mu b, b mu
  Var_matrix_inv[1,0]=Var_matrix_inv[0,1]=s_in/(mu*s_in+b_hat)
  #b b
  Var_matrix_inv[1,1]=1/(mu*s_in+b_hat) + 1/db_in**2
  
  #This needs to be changed, sometimes the matrix was non invertable (mostly for plots not used such as ratios or those
  #with some normalisation) a quick fix was to set the var mat to 0 and clean up downstream
  
  if Var_matrix_inv[0,0] * Var_matrix_inv[1,1] - Var_matrix_inv[1,0] * Var_matrix_inv[0,1] == 0:
        Var_matrix = np.zeros([2,2])
  #Invert and return it
  else:
        Var_matrix = np.linalg.inv(Var_matrix_inv)
  return Var_matrix

#############################################################################################
### A modified version of the above to build a combined likelihood

def Var_mu_comb(b_count,s_count,db_count, ds_count):
#Construct the inverse variance matrix from expected vals of the 2nd derivatives of the Log Likelihood
    Var_matrix_inv=np.zeros([(len(b_count)+len(s_count)+1),(len(b_count)+len(s_count)+1)])
#add exception handling is s=/=b
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

def findItem(theList, item):
   return [(ind, theList[ind].index(item)) for ind in xrange(len(theList)) if item in theList[ind]]

def confLevel(sigCount, bgCount, bgErr, sgErr):
    varMat= Var_mu_comb(bgCount,sigCount,bgErr, sgErr)[0,0]
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

    return float('%10.6f' % float(1-p_val))

#         varMat = Var_mu_comb(gathered_pool[key][4],gathered_pool[key][3],gathered_pool[key][5])[0,0]
#         q_mu_a= qMu_Asimov(mu_test,gathered_pool[key][4],gathered_pool[key][3],gathered_pool[key][5])
#         mu_hat = 0
#         if varMat ==0:
#             gathered_pool[key][2].append(0)
#         else:
#             q_mu=0
#             p_val=0
#             q_mu = (mu_test-mu_hat)**2/(varMat)
#             if 0 < q_mu <= (mu_test**2)/(varMat):
#                 p_val=sp.halfnorm.sf(np.sqrt(q_mu))
#             elif q_mu > (mu_test**2)/(varMat):
#                 p_val=sp.halfnorm.sf( (q_mu + (mu_test**2/varMat))/(2*mu_test/(np.sqrt(varMat))) )

#--------------------------------------------------------------------------------------------


if __name__ == '__main__':
    #need an empty dict to store our results
    scatterpoints ={}
    ## Command line parsing
    parser = getCommandLineOptions()
    opts, args = parser.parse_args()

    ## Split the input file names and the associated plotting options
    ## given on the command line into two separate lists
    filelist, plotoptions = parseArgs(args)
    ## Remove the PLOT dummy file from the file list
    if "PLOT" in filelist:
        filelist.remove("PLOT")

    ## Read the .plot files
    plotdirs = opts.PLOTINFODIRS + [os.path.abspath(os.path.dirname(f)) for f in filelist]
    plotparser = rivet.mkStdPlotParser(plotdirs, opts.CONFIGFILES)

    masterDict={}
    heatMap={}
    for anatype in anapool:
        masterDict[anatype] =[]

   # fileliststatic= []
    for root, dirs, files in os.walk('.'):
        for name in files:
            fileliststatic = []
            if 'hidden' in root:
                continue
            if '.yoda' in name and 'LHC' not in name:
                #if "1000_mX_800" not in name:
                #    continue
                #else:
                yodafile = os.path.join(root, name)
                fileliststatic = str(yodafile)
            else:
                continue
            refhistos, mchistos = getHistos(fileliststatic)
            hpaths = []
            for aos in mchistos.values():
                for p in aos.keys():
                    if p and p not in hpaths:
                        hpaths.append(p)

            getRivetRefData(refhistos)

            mapPoints={}
    ## Now loop over all MC histograms and plot them
    # TODO: factorize much of this into a rivet.utils mkplotfile(mchists, refhist, kwargs) function
            for h in hpaths:
				#Manually store additional plot in a function called LumiFinder, if a Lumi isn't stored vs an 
				#analysis name then use that info to veto testing
                if LumiFinder(h)[0] == -1:
                    continue
                #Use this switch to view individual analyses
                #if '/ATLAS_2014_I1268975' not in h:
                #    continue
        #print 'Currently looking at', h
        ## A list of all analysis objects to be plotted
                anaobjects = []

        ## Plot object for the PLOT section in the .dat file
                plot = Plot()
                plot['Legend'] = '1'
                plot['MainPlot'] = '0'
                plot['RatioPlotYMin'] = '1'
                plot['LogY'] = '1'
                for key, val in plotparser.getHeaders(h).iteritems():
                    plot[key] = val
                if plotoptions.has_key("PLOT"):
                    for key_val in plotoptions["PLOT"]:
                        key, val = [s.strip() for s in key_val.split("=")]
                        plot[key] = val
                if opts.LINEAR:
                    plot['LogY'] = '0'
                if opts.NOPLOTTITLE:
                    plot['Title'] = ''

                if opts.STYLE == 'talk':
                    plot['PlotSize'] = '8,6'
        #elif opts.STYLE == 'bw':
        #    if opts.RATIO:
        #        plot['RatioPlotErrorBandColor'] = 'black!10'

        ## DrawOnly is needed to keep the order in the Legend equal to the
        ## order of the files on the command line
                drawonly = []

        ## Check if we have reference data for the histogram
                ratioreference = None
                if refhistos.has_key('/REF' + h):
                    refdata = refhistos['/REF' + h]
                    refdata.setAnnotation('ErrorBars', '1')
                    refdata.setAnnotation('PolyMarker', '*')
                    refdata.setAnnotation('ConnectBins', '0')
                    refdata.setAnnotation('Title', 'Data')
                    if opts.RATIO:
                        ratioreference = '/REF'+h
                    anaobjects.append(refdata)
                    drawonly.append('/REF' + h)

                if opts.RATIO and opts.RATIO_DEVIATION:
                    plot['RatioPlotMode'] = 'deviation'

        ## Loop over the MC files to plot all instances of the histogram
                styleidx = 0
                #for infile in filelist:
                mcpath='/'+fileliststatic
            # if infile == "PLOT":
            #     continue  ##< This isn't a real file!
                if mchistos.has_key(fileliststatic) and mchistos[fileliststatic].has_key(h):
                ## Default linecolor, linestyle
                    setStyle(mchistos[fileliststatic][h], styleidx)
                    styleidx += 1
                if opts.MC_ERRS:
                    mchistos[fileliststatic][h].setAnnotation('ErrorBars', '1')
                ## Plot defaults from .plot files
                for key, val in plotparser.getHistogramOptions(h).iteritems():
                    mchistos[fileliststatic][h].setAnnotation(key, val)
                ## Command line plot options
                setOptions(mchistos[fileliststatic][h], {}) # plotoptions[fileliststatic])
                mchistos[fileliststatic][h].setAnnotation('Path', mcpath + h)

                print 'testing: ' + h
                lumi = LumiFinder(h)[0]
                if lumi > 0:
					#make some empty arrays, not all of these are used, can definitely be optimised and cleaned up but used for de
					#bugging for now
                    sighisto=yoda.core.mkScatter(mchistos[fileliststatic][h])
                    # q_mu_MC=np.zeros([refdata.numPoints,4])
                    # varmat=np.zeros([refdata.numPoints,1])
                    # q_mu=np.zeros([refdata.numPoints,1])
                    # mu_hat=np.zeros([refdata.numPoints,1])
                    # p_val=np.zeros([refdata.numPoints,1])
                    #varmat=[0]*refdata.numPoints
                    #varmat=[]
                    CLs=[]
                    sigCount = []
                    bgCount = []
                    bgError = []
                    sigError = []
                    #fill test results for each bin
                    #out=np.zeros([refdata.numPoints,1])
                    for i in range(0,refdata.numPoints):
                        global mu_test
                        mu_test=1
                        mu_hat=0
                        varmat=0
                        sigCount.append(sighisto.points[i].y*lumi)
                        bgCount.append(refdata.points[i].y*lumi)
                        bgError.append(refdata.points[i].yErrs[1]*lumi)
                        sigError.append(sighisto.points[i].yErrs[1]*lumi)
                        ##cater for the case where the refdata bin is empty, occurs notably in ATLAS_2014_I1307243
                        if refdata.points[i].y > 0:
                            varmat=Var_mu(mu_test,ML_b_hat_model(refdata.points[i].y*lumi,mu_test,refdata.points[i].y*lumi,sighisto.points[i].y*lumi,refdata.points[i].yErrs[1]*lumi),sighisto.points[i].y*lumi,refdata.points[i].yErrs[1]*lumi)[0,0]
                            mu_hat=ML_mu_hat(refdata.points[i].y*lumi,refdata.points[i].y*lumi,sighisto.points[i].y*lumi)
                            if varmat==0:
							#a bit dodgey, but due to rounding, sometimes the inverse variance matrix is non invertable, so
							#its coded to just pass back 0, in this case the CL should be 0 not 1 so manually set it
							#the covar matrix shouldn't ever legitametly be 0 unless something is wrong...
                                CLs.append(0)
                            else:
							#otherwise construct the CL as per Cowan et al
                                q_mu=0
                                p_val=0
                                q_mu=(mu_test-mu_hat)**2/(varmat)

                                if 0 < q_mu <= (mu_test**2)/(varmat):
                                    p_val=sp.halfnorm.sf(np.sqrt(q_mu))
                                elif q_mu > (mu_test**2)/(varmat):
                                    p_val=sp.halfnorm.sf( (q_mu + (mu_test**2/varmat))/(2*mu_test/(np.sqrt(varmat))) )

                                CLs.append(float('%10.6f' % float(1-p_val)))
                        else:
                            CLs.append(0)

                    for i in range(0,refdata.numPoints):
                        sighisto.points[i].y=sighisto.points[i].y+refdata.points[i].y
                        sighisto.points[i].yErrs =((refdata.points[i].yErrs[1])**2 + (sighisto.points[i].yErrs[1])**2 )**0.5
                        sighisto.title=str(max(CLs))
                    anaobjects.append(sighisto)
                else:
                    anaobjects.append(mchistos[fileliststatic][h])
                drawonly.append(mcpath + h)
                if opts.RATIO and ratioreference is None:
                    ratioreference = mcpath + h

                plot['DrawOnly'] = ' '.join(drawonly).strip()
                if opts.RATIO and len(drawonly) > 1:
                    plot['RatioPlot'] = '1'
                    plot['RatioPlotReference'] = ratioreference


                plot['RatioPlotYMin'] = '1'
                ## Now create the output. We can't use "yoda.writeFLAT(anaobjects, 'foobar.dat')" because
                ## the PLOT and SPECIAL blocks don't have a corresponding analysis object.
                #os.mkdir(h)
                output = ''
                output += str(plot)

                ## Special
                special = plotparser.getSpecial(h)
                if special:
                    output += "\n"
                    output += "# BEGIN SPECIAL %s\n" % h
                    output += special
                    output += "# END SPECIAL\n\n"


                from cStringIO import StringIO
                sio = StringIO()
                yoda.writeFLAT(anaobjects, sio)
                output += sio.getvalue()
        ## Write everything into a file
        # creates the ratio plots
                writeOutput(output, h, root)
        #store the results in a dictionary for sorting (the yoda files are unsorted so everything comes in in a random order
            # mapPoints = {}

                # if h not in scatterpoints:
                #     scatterpoints[h] = [(float(name.strip('.yoda').split('_')[1]),float(name.strip('.yoda').split('_')[3]),float(max(CLs)) , sigCount[CLs.index(max(CLs))], bgCount[CLs.index(max(CLs))] , bgError[CLs.index(max(CLs))], LumiFinder(h)[2] , h.split('/')[1] )]
                # else:
                #     scatterpoints[h].append((float(name.strip('.yoda').split('_')[1]),float(name.strip('.yoda').split('_')[3]), float(max(CLs)), sigCount[CLs.index(max(CLs))], bgCount[CLs.index(max(CLs))] , bgError[CLs.index(max(CLs))], LumiFinder(h)[2] , h.split('/')[1] ))


##All these extra count checks are to stop any plots with no count in most likely bin from being entered
##into liklihood calc, should be fixed upstream
                if LumiFinder(h)[2]:
                    tempKey = ''
                    tempKey= h.split('/')[1] +'_'+LumiFinder(h)[2]
                    if tempKey not in mapPoints and bgCount[CLs.index(max(CLs))]>0.0:
                        mapPoints[tempKey] = [float(name.strip('.yoda').split('_')[1]),float(name.strip('.yoda').split('_')[3]), float(max(CLs)) , [sigCount[CLs.index(max(CLs))]], [bgCount[CLs.index(max(CLs))]] , [bgError[CLs.index(max(CLs))]], [sigError[CLs.index(max(CLs))]]]
                    elif bgCount[CLs.index(max(CLs))] > 0.0:
                        mapPoints[tempKey][3].append(sigCount[CLs.index(max(CLs))])
                        mapPoints[tempKey][4].append(bgCount[CLs.index(max(CLs))])
                        mapPoints[tempKey][5].append(bgError[CLs.index(max(CLs))])
                        mapPoints[tempKey][6].append(sigError[CLs.index(max(CLs))])
                else:
                    if h not in mapPoints and bgCount[CLs.index(max(CLs))]>0.0:
                        mapPoints[h] = [float(name.strip('.yoda').split('_')[1]),float(name.strip('.yoda').split('_')[3]), float(max(CLs)) , [sigCount[CLs.index(max(CLs))]], [bgCount[CLs.index(max(CLs))]] , [bgError[CLs.index(max(CLs))]],[sigError[CLs.index(max(CLs))]]]
            for key in mapPoints:
                tempName = LumiFinder(key)[1]
                mapPoints[key][2] = confLevel(mapPoints[key][3],mapPoints[key][4],mapPoints[key][5], mapPoints[key][6])
                if not masterDict[tempName]:
                    masterDict[tempName].append(mapPoints[key][:])
                else:
                    _overWriteFlag = False
                    _pointExistsFlag = False
                    for listelement in masterDict[tempName]:
                        if mapPoints[key][0] == listelement[0] and mapPoints[key][1] == listelement[1]:
                            _pointExistsFlag = True
                            if mapPoints[key][2] > listelement[2]:
                                masterDict[tempName][masterDict[tempName].index(listelement)] = mapPoints[key][:]
                                #listelement = mapPoints[key][:]
                                _overWriteFlag=True
                    if _overWriteFlag == False and _pointExistsFlag == False:
                        masterDict[tempName].append(mapPoints[key][:])


                # else if mapPoints[key][]
                # else if mapPoints[key][2] > masterDict[tempName]
                #
                # masterDict[]
    import pickle
    for key in masterDict:
        if masterDict[key]:
            masterDict[key].sort(key=lambda x: x[0])
            writeOutputHier(masterDict[key],key+"test")
            with open("./ANALYSIS/"+key+'.map', 'w') as f:
                pickle.dump(masterDict[key], f)
    #     for key in heatmap:
#         heatmap[key].sort(key=lambda x: x[0])
#         writeOutputHier(heatmap[key],key)
#         writeOutputHier(data,"combined")
#         temp = []
#         temp =  zip(zip(*heatmap[key])[0],zip(*heatmap[key])[1],zip(*heatmap[key])[2])
#         temp.sort(key=lambda x: x[0])
#         with open("./ANALYSIS/"+key+'.map', 'w') as f:
#             pickle.dump(temp, f)
#         with open("./ANALYSIS/combined.map",'w') as f:
#             pickle.dump(data, f)
        #print scatterpoints
print 'g'

#
#     for key in scatterpoints:
#         writeOutputHier(scatterpoints[key],"combined"+key)
#
#
#         #outfile=open(str('.'+h+'.plot'), 'w')
#         #outfile.write(str(plot))
#     #print "break"
#
#     #make a new dictionary to combine the analysis pools
#     heatmap = {}
#     pool = {}
#     for an_type in anapool:
# #        pool=[]
#         for key in scatterpoints.keys():
# 			#also store the pools in the lumi finder function
#             if LumiFinder(key)[2]:
#                 continue
#             if LumiFinder(key)[1] == an_type:
#                 if an_type not in heatmap:
#                     heatmap[an_type] = scatterpoints[key][:]
#                     #for each plot in each analysis in each pool, run through and update the value stored against the pool and which plot said value came from
#                 for i in range(0,len(scatterpoints[key])):
#                     for j in range(0,len(heatmap[an_type])):
#                         if scatterpoints[key][i][0] == heatmap[an_type][j][0] and scatterpoints[key][i][1] == heatmap[an_type][j][1] and scatterpoints[key][i][2]>=heatmap[an_type][j][2]:
#
#                             #if LumiFinder(key):
#
#                             heatmap[an_type][j]=list(heatmap[an_type][j])
#                             heatmap[an_type][j][2:5] = scatterpoints[key][i][2:5]
#
#                             # heatmap[an_type][j][2] = scatterpoints[key][i][2]
#                             # heatmap[an_type][j][3] = scatterpoints[key][i][3]
#                             # heatmap[an_type][j][4] = scatterpoints[key][i][4]
#                             # heatmap[an_type][j][5] = scatterpoints[key][i][5]
#                             if len(heatmap[an_type][j])==6:
#                                 #heatmap[an_type][j].append(key.split('/')[2])
#                                 heatmap[an_type][j].append(key)
#                             else:
#                                 #heatmap[an_type][j][3]=key.split('/')[2]
#                                 heatmap[an_type][j][6]=key
#                 # if LumiFinder(key)[2]:
#                 #     ##Special logic for jet measurements/ any measurements w. well defined kinematic regions
#                 #     if an_type not in pool:
#                 #         for subpool_type in subpools:
#                 #         ##slice out each subpool
#                 #             scatterpoints.keys()
#
#     # aim here is to gather all the keys at each xy point to a single group as a list of counts for a given xy
#     # with key as analysis+pool
#     for key in scatterpoints:
#         if LumiFinder(key)[2]:
#             for point in scatterpoints[key]:
#                 tempkey =  point[6]+"_"+point[7]
#                 if tempkey not in pool:
#                     pool[tempkey]=point[:]
#                 elif point[2] >= pool[key][2]:
#                     pool[key]=point[:]
#
#     gathered_pool = {}
#     #this is crap but I'm really not sure how to do this in a pythonic way so I'm bruteforcing it
#     #want to organise measurements w. combinable bins s.t. the best combination can be picked out for a particular pool
#     for key in pool:
#         poolstring = str(pool[key][7]+"_"+pool[key][6])
#         if poolstring not in gathered_pool:
#             gathered_pool[poolstring] = pool[key][:2]
#             ##this is really crap
#             gathered_pool[poolstring] =list(gathered_pool[poolstring])
#             gathered_pool[poolstring].append([])
#             gathered_pool[poolstring].append([pool[key][3]])
#             gathered_pool[poolstring].append([pool[key][4]])
#             gathered_pool[poolstring].append([pool[key][5]])
#            # gathered_pool[poolstring] = [list(elem) for elem in gathered_pool[poolstring]]
#             #gathered_pool[poolstring].append[poolkey]
#         for i in range(0, len(gathered_pool[poolstring])):
#
#             #if
#
#             if gathered_pool[poolstring][0]==pool[key][0] and gathered_pool[poolstring][1]==pool[key][1]:
#                 gathered_pool[poolstring][3].append(pool[key][3])
#                 gathered_pool[poolstring][4].append(pool[key][4])
#                 gathered_pool[poolstring][5].append(pool[key][5])
#         else:
#             templist=[]
#             templist.append(list(pool[key][:2]))
#             ##this is really crap
#             templist.append([])
#             templist.append([pool[key][3]])
#             templist.append([pool[key][4]])
#             templist.append([pool[key][5]])
#             gathered_pool[poolstring].append(templist)
#
#     for key in gathered_pool:
#         varMat = Var_mu_comb(gathered_pool[key][4],gathered_pool[key][3],gathered_pool[key][5])[0,0]
#         q_mu_a= qMu_Asimov(mu_test,gathered_pool[key][4],gathered_pool[key][3],gathered_pool[key][5])
#         mu_hat = 0
#         if varMat ==0:
#             gathered_pool[key][2].append(0)
#         else:
#             q_mu=0
#             p_val=0
#             q_mu = (mu_test-mu_hat)**2/(varMat)
#             if 0 < q_mu <= (mu_test**2)/(varMat):
#                 p_val=sp.halfnorm.sf(np.sqrt(q_mu))
#             elif q_mu > (mu_test**2)/(varMat):
#                 p_val=sp.halfnorm.sf( (q_mu + (mu_test**2/varMat))/(2*mu_test/(np.sqrt(varMat))) )
#
#             gathered_pool[key][2].append(float('%10.6f' % float(1-p_val)))
#
#     for key in gathered_pool:
#         for an_type in anapool:
#             if an_type in LumiFinder(key):
#                 if an_type not in heatmap:
#                     heatmap[an_type] = gathered_pool[key][:]
#                 #elif
#
#
#
#
#     print 'g'
#
#
#     # for subpool in subpools:
#     #    print 'g'
#     #
#     # for key in pool:
#     #     temp1=[]
#     #     temp2=[]
#
#
#     #pool = dict((k,v) for k, v in pool.iteritems() if v[6]=="R1" and v[7]=='ATLAS_2014_I1268975')
#
#
#     # print 'g'
#
#
#
# #############################################################################################
# #### Now we perform the analysis again, in order to construct a combined Likelihood, s.t. the p value behaves correctly
# #### In terms of convergence for many combined signicances (cannot correctly calc signifiances by combining each channels
# #### Independent significance
#
#     # data = zip(zip(*heatmap[heatmap.keys()[0]])[0],zip(*heatmap[heatmap.keys()[0]])[1],zip(*heatmap[heatmap.keys()[0]])[2])
#     # for i in range(0,len(data)):
#     #     data[i]=list(data[i])
#     #     data[i][2] = 0.0
#
#     data = heatmap[heatmap.keys()[0]][:]
#     for i in range(0,len(data)):
#         data[i]=list(data[i])
#         data[i][2] = []
#         data[i][3] = []
#         data[i][4] = []
#         data[i][5] = []
#         data[i][6] = []
#
#     for key in heatmap:
#         for i in range(0,len(heatmap[key])):
#             for j in range(0,len(data)):
#                 if heatmap[key][i][0] == data[j][0] and heatmap[key][i][1] == data[j][1]:
#                     ##append signal counts
#                     data[j][3].append(heatmap[key][i][3])
#                     ##append bkg counts
#                     data[j][4].append(heatmap[key][i][4])
#                     ##append bkg errors
#                     data[j][5].append(heatmap[key][i][5])
#                     ##append analysis used for this
#                     data[j][6].append(heatmap[key][i][6])
#         print 'break'
#
#     for i in range(0,len(data)):
#         #### here we copy the p value logic from before, this should be factored into a function that takes varmat as an arg
#         ####
#         #print zip(*data)[4]
#         #data[i][4] = [ML_b_hat_model(x,mu_test,x,data[i][3][data[i][4].index(x)],data[i][5][data[i][4].index(x)] ) for x in data[i][4]]
#         varMat = Var_mu_comb(data[i][4],data[i][3],data[i][5])[0,0]
#         q_mu_a= qMu_Asimov(mu_test,data[i][4],data[i][3],data[i][5])
#         mu_hat = 0
#         if varMat ==0:
#             data[i][2].append(0)
#         else:
#             q_mu=0
#             p_val=0
#             q_mu = (mu_test-mu_hat)**2/(varMat)
#             if 0 < q_mu <= (mu_test**2)/(varMat):
#                 p_val=sp.halfnorm.sf(np.sqrt(q_mu))
#             elif q_mu > (mu_test**2)/(varMat):
#                 p_val=sp.halfnorm.sf( (q_mu + (mu_test**2/varMat))/(2*mu_test/(np.sqrt(varMat))) )
#
#             data[i][2].append(float('%10.6f' % float(1-p_val)))
#
#
    # import pickle
    # #dump out the final pool heatmaps in human and python readable format
    # for key in heatmap:
    #     heatmap[key].sort(key=lambda x: x[0])
    #     writeOutputHier(heatmap[key],key)
    #     writeOutputHier(data,"combined")
    #     temp = []
    #     temp =  zip(zip(*heatmap[key])[0],zip(*heatmap[key])[1],zip(*heatmap[key])[2])
    #     temp.sort(key=lambda x: x[0])
    #     with open("./ANALYSIS/"+key+'.map', 'w') as f:
    #         pickle.dump(temp, f)
    #     with open("./ANALYSIS/combined.map",'w') as f:
    #         pickle.dump(data, f)

#
#
# #############################################################################################
# ### Old plotting stuff, now factored into a different script
#
#
#         #np.save("./ANALYSIS/"+key,heatmap[key])
# #        for point in pool[an_type]
# #        for key in (y for y in scatterpoints.keys() if LumiFinder(y)[1] == an_type):
# #            print key
# #    import matplotlib.pyplot as plt
# #    import colormaps as cmaps
# #    import pylab
#
# #   for anakey in range(0, (len(scatterpoints.keys()))):
# #       currentkey = scatterpoints.keys()[anakey]
# #       writeOutputHier(scatterpoints[currentkey], currentkey)
#
# #       np.save("."+currentkey,scatterpoints[currentkey])
#         # dx=25
#         # dy=50
#         #
#         # data=np.zeros([3,len(scatterpoints[currentkey])])
#         # for i in range(0,len(scatterpoints[currentkey])):
#         #     data[0,i]=(int(scatterpoints[currentkey][i][1]))
#         #     data[1,i]=(int(scatterpoints[currentkey][i][0]))
#         #     data[2,i]=((scatterpoints[currentkey][i][2]))
#         # #print "break"
#         # np.save("."+currentkey, data)
#         # x_grid_min= data[0,:].min()-dx
#         # y_grid_min= data[1,:].min()-dy
#         # x_grid_max=data[0,:].max()+dx
#         # y_grid_max=data[1,:].max()+dy
#         #
#         # yy,xx =np.mgrid[y_grid_min:y_grid_max+dy:2*dy,x_grid_min:x_grid_max+dx:2*dx]
#         # c=np.zeros([len(xx[0,:])-1,len(yy[:,0])-1])
#         #
#         #
#         # for i in range(0,len(data[1,:])):
#         #     xcounter=0
#         #     ycounter=0
#         #     for xarg2 in xx[1]:
#         #         if data[0,i] > xarg2:
#         #             xcounter+=1
#         #     for yarg2 in yy[:,xcounter]:
#         #         if data[1,i] > yarg2:
#         #             ycounter+=1
#         #     c[xcounter-1][ycounter-1]=data[2,i]
#         #
#         #
#         # fig = plt.figure(figsize=(12, 8))
#         # ax = fig.add_subplot(1,1,1)
#         # #plt.pcolormesh(xx,yy,zz,cmap="seismic", vmin=0, vmax=1)
#         # plt.pcolormesh(xx,yy,c.T,cmap=cmaps.magma_r, vmin=0, vmax=1)
#         # plt.axis([x_grid_min, x_grid_max, y_grid_min, y_grid_max])
#         #
#         # plt.rc('text', usetex=True)
#         # plt.rc('font', family='lmodern')
#         # plt.xlabel(r"$M_{\chi}$ [GeV]", fontsize=16)
#         # plt.ylabel(r"$M_{Z'}$ [GeV]", fontsize=16)
#         # plt.rc('text', usetex=False)
#         # plt.rc('font', family='sans')
#         # plt.title(str(currentkey),y=1.02)
#         # plt.colorbar().set_label("CL of exclusion")
#         # plt.savefig("."+str(currentkey)+".pdf")
#         # plt.savefig("."+str(currentkey)+".png")
