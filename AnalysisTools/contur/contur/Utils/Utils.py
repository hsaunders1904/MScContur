import os
import yoda
import rivet
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

