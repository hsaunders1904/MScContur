import os
import yoda
import rivet
import plotinfo
from contur import TestingFunctions as ctr

def writeBanner():
    """Write Ascii banner"""
    print "Running Contur v1.0 Release \n"
    print "Mail to developers: contur (at) projects.hepforge.org \n"

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

def writeOutputHier(output, h):
    "Choose output file name and dir"
    hparts = h.strip("/").split("/")
    ana = "ANALYSIS"
    outdir = os.path.join('.', ana)
    mkoutdir(outdir)
    outfilepath = os.path.join(outdir, output)
    f = open(outfilepath, 'w')
    for item in output:
        f.write(str(item) + "\n")
    #f.write(output)
    f.close()

def writeOutput(output, h):
    mkoutdir("ANALYSIS")
    f = open("./ANALYSIS/"+h, 'w')
    for item in output:
        f.write(str(item) + "\n")
    f.close()

def writeOutput2(output, h, outdir):
    "Choose output file name and dir"
    hparts = h.strip("/").split("/")
    #outdir = opts.OUTPUTDIR
    outfile = '%s.dat' % "_".join(hparts)
    mkoutdir(outdir)
    outfilepath = os.path.join(outdir, outfile)
    f = open(outfilepath, 'w')
    f.write(output)
    f.close()

def getHistos(filelist):
    """Loop over all input files. Only use the first occurrence of any REF-histogram
    and the first occurrence in each MC file for every MC-histogram."""
    # return reference histograms,
    #        mchistos = mc plots, 
    #        xsec     = generated xsec and its uncertainty,    
    #        Nev      = sum of weights, sum of squared weight, number of events
    # (derived from rivet-cmphistos)
    refhistos = {}
    mchistos = {}
    xsec = {}
    Nev = {}
    # for infile in filelist:
    mchistos.setdefault(filelist, {})
    analysisobjects = yoda.read(filelist)
    print len(analysisobjects), "analysisobjects in", filelist
    for path, ao in analysisobjects.iteritems():
        if path.startswith('/_EVTCOUNT'):
            Nev = ao
        if path.startswith('/_XSEC'):
            xsec = ao
            # Conventionally don't plot data objects whose names start with an
            # underscore
        if os.path.basename(path).startswith("_"):
            continue
        if path.startswith('/REF/'):
            if path not in refhistos:
                refhistos[path] = ao
        else:
            if path not in mchistos[filelist]:
                mchistos[filelist][path] = ao
    return refhistos, mchistos, xsec, Nev




def getRivetRefData(refhistos, anas=None):
    "Find all Rivet reference data files"
    rivet_data_dirs = rivet.getAnalysisRefPaths()
    dirlist = []
    for d in rivet_data_dirs:
        if anas is None:
            import glob
            dirlist.append(glob.glob(os.path.join(d, '*.yoda')))
        else:
            dirlist.append([os.path.join(d, a + '.yoda') for a in anas])
    for filelist in dirlist:
        # TODO: delegate to getHistos?
        for infile in filelist:
            analysisobjects = yoda.read(infile)
            for path, ao in analysisobjects.iteritems():
                if path.startswith('/REF/'):
                    if path not in refhistos:
                        refhistos[path] = ao


def fillResults(refdata,h,lumi,has1D,mc1D,sighisto,Nev,xsec):
# Function to fill and return the background, signal and error counts
# from histogram h, along with the measured values from refdata, CLs
# exclusion, and the normalisation factors (if required). 
# It big and messy, needs work, but is at least factored out here
# so the same code can be used in CLTest and CLTestSingle
#
# Input
# -----
# refdata -- reference data plot with measured values
# h       -- name of plot being considered
# lumi    -- luminosity used in the measurement
# has1D   -- flag to say whether there is a 1D histogram present (sometimes there may be only 2D scatters)
# mc1D    -- the 1D histogram for the signal (if has1D)
# sighisto - the signal scatter plot (2D) 
# Nev     -- for the signal: sumW, sumW2, number of events
# xsec    -- for the signal: xsec, uncertainties
#

    CLs = []
    bgCount = []
    bgError = []
    sigCount = []
    sigError = []
    measCount = []
    measError = []

    # Scale factor to apply to the BSM points 
    normFacSig = 1.0
    # Scale factor to apply to the measured points (reference histogram)
    normFacRef = 1.0
    
    normalised, factor, scaleMC = ctr.isNorm(h)

    if normalised:
        # Set up the normalisation values. 
        
        if has1D == False:
            print 'Found a normalised 2D scatter. Makes no sense. Ignoring it.',h
            return bgCount,bgError,sigCount,sigError,measCount,measError,CLs,normFacSig,normFacRef
        
        # number to scale the background data by during combination with signal.
        # If rivet has generated area-normalised plots, this will typically be the integrated cross section in the plot.
        # However, it can also be a simple scale factor to take into account e.g. branching ratio corrections in W/Z measurements
        normFacRef = factor
        
        import numpy as np
        
         #print h, scaleMC

        # number to scale the signal by during combination with background
        # if rivet generated normalised histograms, signal is normalised by its cross section 
        # (generated xsec * fraction appearing in histo)
        if (scaleMC == 1 and Nev.numEntries()>0):
            print "scaling MC for", h
             #print mc1D.numEntries(), Nev.numEntries(), xsec.points[0].x
            normFacSig = (float(mc1D.numEntries()) / float(Nev.numEntries()) * float(xsec.points[0].x))
            
    if has1D:
        # do a check on the generated luminosity
        
        if (mc1D.sumW()>0):
            
            mclumi = float(mc1D.numEntries())/(mc1D.sumW()*normFacSig)
            #mclumi = float(Nev.numEntries()) / float(xsec.points[0].x)
            #print mc1D.numEntries(), mc1D.sumW(), normFacSig, mclumi
            #print h,' mclumi=',mclumi
            if (lumi/mclumi>2.0):
                # Note, this is usually in pb-1, but sometimes in fb-1.
                # Also, some analyses have factors of 2 because they are averaged over e and mu channels
                # There can also be bin-width effects (e.g. in 3D cross sections)
                # How this works:
                # 1) Rivet scales the histos by xsec-per-event (sometimes with bin width effects too)
                # 2) sumW = n_Gen * xsec-per-event = xsec
                # 3) so n_Gen/sumW = n_Gen/xsec = L_gen = mclumi
                print 'Warning! Effective MC lumi %.2f appears substantially less than data lumi %.2f for %s' % (mclumi, lumi, h)
                print 'This may be a bin width effect, but if not, consider generating more events.'
        else:
            print h, ' has zero MC entries'
            mclumi = 0

# Loop over the data points.
                    
    for i in range(0, refdata.numPoints):
        # Sigerror is used to store \tau, the ratio of MC Nev to "data" Nev
        # TODO check! (JMB) - looks to me like it stores the generated luminosity without scale factor 
        # (ie num entries/sumweights), not the ratio.
        if has1D:
            test = 'LL'
            sigCount.append(mc1D.bins[i].sumW * lumi * normFacSig)
            bgCount.append(refdata.points[i].y * lumi * normFacRef * (refdata.points[i].xMax - refdata.points[i].xMin))
            bgError.append(refdata.points[i].yErrs[1] * lumi * normFacRef * (refdata.points[i].xMax - refdata.points[i].xMin))
            if mc1D.sumW() ==0:
                sigError.append(0.0)
            else:
                sigError.append(float(mclumi)*normFacSig)
 
        else:
            # Using Chi2 test on two 2D plots. 
            # One is assumed to be the result of the measurement (measCount, measErr)
            # One is assumed to be the background-only scenario  (bgCount, bgErr)
            # One is assumed to be the signal+background scenario (sigCount, sigErr)
            # Currently only the ATLAS MET+JET measurement is done this way.
            print 'Why are we here?' 
            print refdata
            test = 'CSR'
            print 'values:', i, sighisto.points[i].y, refdata.points[i].y, refdata.points[i].yErrs[1] 
            sigCount.append(sighisto.points[i].y)
            bgCount.append(refdata.points[i].y)
            bgError.append(refdata.points[i].yErrs[1])
                
            # TODO: at the moment, the 'CS' option is used for comparing ratio plots with and without BSM. The vast majority of the
            # uncertainty is correlated and comes from the background, so we are ignoring the (uncorrelated) signal
            # uncertainty here.
            sigError.append(0.0)
                
        # cater for the case where the refdata bin is empty,
        # occurs notably in ATLAS_2014_I1307243
        if refdata.points[i].y > 0:
            CLs.append(ctr.confLevel([sigCount[i]], [bgCount[i]], [bgError[i]], [sigError[i]], 1, test))
        else:
             #print 'Warning! Ref data bin '+str(i)+" empty in "+h
            CLs.append(0)

                    
    return bgCount,bgError,sigCount,sigError,measCount,measError,CLs,normFacSig,normFacRef


def writeHistoDat(mcpath, plotparser, outdir, histo):
    """Write a .dat file for the histogram in the output directory, for later display."""

    anaobjects = []
    drawonly = []
    mcpath = "/"+mcpath

    ## Check if we have reference data for the histogram
    ratioreference = None
    if histo.ref:

        ## unfortunuately this has been scale by bin width and lumi...
        #refdata = histo.background

        refdata = histo.refplot

        sigback = histo.stack
        h = sigback.path

        sigback.setAnnotation('Path', mcpath+h)

        refdata.setAnnotation('ErrorBars', '1')
        refdata.setAnnotation('PolyMarker', '*')
        refdata.setAnnotation('ConnectBins', '0')
        refdata.setAnnotation('Title', 'Data')
        
        anaobjects.append(refdata)
        drawonly.append('/REF' + h)

        drawonly.append(mcpath + h)

        # write the bin number of the most significant bin, and the bin number for the plot legend
        if histo.maxbin > 0:
            sigback.title='[%s] %5.2f' % ( histo.maxbin, histo.conturPoints[histo.maxcl].CLs )

        sigback.setAnnotation('LineColor', 'red')
        anaobjects.append(sigback)
        plot = plotinfo.Plot()
        plot['DrawOnly'] = ' '.join(drawonly).strip()
        plot['Legend'] = '1'
        plot['MainPlot'] = '1'
        plot['RatioPlotYMin'] = '1'
        plot['LogY'] = '1'
        plot['RatioPlot'] = '1'

        for key, val in plotparser.getHeaders(h).iteritems():
            # Get any updated attributes from plotinfo files
             plot[key] = val
        
        ratioreference = '/REF'+h
        plot['RatioPlotReference'] = ratioreference
        output = ''
        output += str(plot)
        from cStringIO import StringIO
        sio = StringIO()
        yoda.writeFLAT(anaobjects, sio)
        output += sio.getvalue()
        
        hparts = h.strip("/").split("/")
        
        outfile = '%s.dat' % "_".join(hparts)
        mkoutdir(outdir)
        outfilepath = os.path.join(outdir, outfile)
        f = open(outfilepath, 'w')
        f.write(output)
        f.close()

