import os
import yoda
import rivet
from contur import TestingFunctions as ctr

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
    # Stolen from rivet-cmphistos
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

    CLs = []
    bgCount = []
    bgError = []
    sigCount = []
    sigError = []
    measCount = []
    measError = []

    # some special logic to deal with normalisation
    normFacSig = 0.0
    normFacRef = 0.0
    if ctr.isNorm(h)[0] == True:
        
        if has1D == False:
            print 'Found a normalised 2D scatter. Makes no sense. Ignoring it.',h
            return bgCount,bgError,sigCount,sigError,measCount,measError,CLs,normFacSig,normFacRef

        for point in refdata.points:
            normFacRef += point.y
        for point in sighisto.points:
            normFacSig += point.y
        normFacRef = ctr.isNorm(h)[1]
        import numpy as np
        if mc1D.sumW2() == 0:
            print 'Sum of weights is zero:',h
            return bgCount,bgError,sigCount,sigError,measCount,measError,CLs,normFacSig,normFacRef

        normFacSig = (float(mc1D.numEntries()) / float(Nev.numEntries()) * float(xsec.points[0].x))
                
    if has1D:
        if (mc1D.sumW()>0):
            mclumi = float(mc1D.numEntries())/mc1D.sumW()
            if (lumi/mclumi>2.0):
                # Note, this is usually in pb-1, but sometimes in fb-1.
                # Also, some analyses have factor of 2 because they are averaged over e and mu channels
                # How this works:
                # 1) Rivet scales the histos by xsec-per-event
                # 2) sumW = n_Gen * xsec-per-event = xsec
                # 3) so n_Gen/sumW = n_Gen/xsec = L_gen = mclumi
                print 'Warning! Effective MC lumi %.2f is substantially less than data lumi %.2f for %s' % (mclumi, lumi, h)
                print '--> consider generating more events.'
                    
    for i in range(0, refdata.numPoints):
        # Sigerror is used to store \tau, the ratio of MC Nev to "data" Nev
        # TODO check! (JMB) - looks to me like it stores the generated luminosity, not the ratio.
        if ctr.isNorm(h)[0] == True:
            test = 'LL'
            sigCount.append(mc1D.bins[i].sumW * lumi * normFacSig)
            bgCount.append(refdata.points[i].y * lumi * normFacRef * (refdata.points[i].xMax - refdata.points[i].xMin))
            bgError.append(refdata.points[i].yErrs[1] * lumi * normFacRef * (refdata.points[i].xMax - refdata.points[i].xMin))
            if mc1D.sumW() ==0:
                sigError.append(0.0)
            else:
                # TODO: shouldn't this be adjusted for normalised histos?
                sigError.append(float(mc1D.numEntries())/mc1D.sumW())
        else:
            if has1D:
                # Using CLs log-likeihood method, as in Contur paper. 
                test = 'LL'
                # error on signal will be estimated from event count, using poisson stats
                sigCount.append(mc1D.bins[i].sumW * lumi)
                bgCount.append(refdata.points[i].y * lumi * (refdata.points[i].xMax - refdata.points[i].xMin))
                bgError.append(refdata.points[i].yErrs[1] * lumi * (refdata.points[i].xMax - refdata.points[i].xMin))
                if mc1D.sumW() ==0:
                    sigError.append(0.0)
                else:
                    sigError.append(mclumi)
                                        
            else:
                # Using Chi2 test on two 2D plots. 
                # One is assumed to be the result of the measurement (measCount, measErr)
                # One is assumed to be the background-only scenario  (bgCount, bgErr)
                # One is assumed to be the signal+background scenario (sigCount, sigErr)
                # Currently only the ATLAS MET+JET measurement is done this way.
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
            print 'Warning! Ref data bin '+str(i)+" empty in "+h
            CLs.append(0)
                    
    return bgCount,bgError,sigCount,sigError,measCount,measError,CLs,normFacSig,normFacRef
