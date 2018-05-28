import os
import yoda
import rivet
import plotinfo
from contur import TestingFunctions as ctr

#set the version here globally
global version
version = " Beta pre-release"

def writeBanner():
    """Write Ascii banner"""
    print "Running Contur ",version, "\n"
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

def writeOutput(output, h):
    mkoutdir("ANALYSIS")
    f = open("./ANALYSIS/"+h, 'w')
    for item in output:
        f.write(str(item) + "\n")
    f.close()


def getHistos(filelist):
    """Loop over all input files. Only use the first occurrence of any REF-histogram
    and the first occurrence in each MC file for every MC-histogram."""
    # return reference histograms,
    #        mchistos = mc plots, 
    #        xsec     = generated xsec and its uncertainty,    
    #        Nev      = sum of weights, sum of squared weight, number of events
    # (derived from rivet-cmphistos)
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
            # Reference histograms are read elsewhere.
            continue
        else:
            if path not in mchistos[filelist]:
                mchistos[filelist][path] = ao
    return mchistos, xsec, Nev


def writeHistoDat(mcpath, plotparser, outdir, nostack, histo):
    """Write a .dat file for the histogram in the output directory, for later display."""

    anaobjects = []
    drawonly = []
    mcpath = "/"+mcpath

    ## Check if we have reference data for the histogram
    ratioreference = None
    if histo.ref:

        refdata = histo.refplot
        background = histo.bgplot

        if nostack:
            sigback = histo.sigplot
        else:
            sigback = histo.stack

        h = sigback.path

        sigback.setAnnotation('Path', mcpath+h)

        refdata.setAnnotation('ErrorBars', '1')
        refdata.setAnnotation('PolyMarker', '*')
        refdata.setAnnotation('ConnectBins', '0')
        refdata.setAnnotation('Title', 'Data')
    
        background.setAnnotation('LineColor', 'green')
        anaobjects.append(background)
        anaobjects.append(refdata)

        drawonly.append('/REF' + h)
        drawonly.append(mcpath + h)
        drawonly.append('/THY' + h)

        # write the bin number of the most significant bin, and the bin number for the plot legend
        if histo.maxbin > 0:
            sigback.title='[%s] %5.2f' % ( histo.maxbin, histo.conturPoints[histo.maxcl].CLs )

        sigback.setAnnotation('LineColor', 'red')
         #sigback.setAnnotation('ErrorBars', '1')

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


def mkScatter2D(s1):
    """ Make a Scatter2D from a Scatter1D by treating the points as y values and adding dummy x bins."""

    rtn = yoda.Scatter2D()

    xval = 0.5
    for a in s1.annotations:
        rtn.setAnnotation(a, s1.annotation(a))

    rtn.setAnnotation("Type", "Scatter2D");

    for point in s1.points:
        
        ex_m = xval-0.5
        ex_p = xval+0.5

        y = point.x
        ey_p = point.xMax - point.x
        ey_m = point.x    - point.xMin
        
        pt = yoda.Point2D(xval, y, (0.5,0.5), (ey_p,ey_m))
        rtn.addPoint(pt)
        xval = xval + 1.0

    return rtn

def walklevel(some_dir, level=1):
    """Like os.walk but can specify a level to walk to
    useful for managing directories a bit better

    https://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
    """
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

