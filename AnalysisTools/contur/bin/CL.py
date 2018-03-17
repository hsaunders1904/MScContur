from contur import TestingFunctions as ctr
from contur import Utils as util
import rivet
import yoda
import sys
import os
import pickle


def init_dict():
    ''' Initialises the master dictionary using the analysis pool '''

    masterDict = {}
    for anatype in ctr.anapool:
        masterDict[anatype] = []

    return masterDict

def grid_add_to_dict(masterDict, mapPoints):
    ''' Adds the results of each cell in the  grid run to the dictionary '''

    for key in mapPoints:
	tempName = ctr.LumiFinder(key)[1]
	mapPoints[key][2] = ctr.confLevel(mapPoints[key][3],mapPoints[key][4],mapPoints[key][5], mapPoints[key][6])
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

    return masterDict


def contur_analysis(infile, opts, grid=False, x=0, y=0):
    ''' Main untounched analysis function. '''

    # need empty dicts to store our results
    scatterpoints = {}
    masterDict = {}
    heatMap = {}

    plotdirs = [os.path.abspath(os.path.dirname(f)) for f in infile]
    plotparser = util.mkStdPlotParser(plotdirs, )

    # get reference histograms,
    #     mchistos = mc plots,
    #     xsec     = generated xsec and its uncertainty,
    #     Nev      = sum of weights, sum of squared weight, number of events
    refhistos, mchistos, xsec, Nev = util.getHistos(infile)

    hpaths = []
    for aos in mchistos.values():
        for p in aos.keys():
            if p and p not in hpaths:
                hpaths.append(p)

    util.getRivetRefData(refhistos)

    mapPoints = {}
    for h in hpaths:
        try:
            refdata = refhistos['/REF%s' % h]
        except KeyError:
            sys.stderr.write('Ignoring %s, no refdata found.\n'%h)
            continue

        # Manually store additional plot in a function called LumiFinder, if a Lumi isn't stored vs an
        # analysis name then use that info to veto testing
        # LumiFinder also returns -1 for vetoed/blacklisted histograms
        lumi = ctr.LumiFinder(h)[0]
        if lumi <=0:
            continue

        # Use this switch to view individual analyses
        mcpath='/'+infile

        if mchistos[infile][h].type == 'Histo1D':
            # Most of the time we deal with 1D histos
            has1D = True
            mc1D = mchistos[infile][h]
            mc1D.setAnnotation('Path', mcpath + h)
            sighisto = yoda.core.mkScatter(mchistos[infile][h])
        else:
            has1D = False
            mchistos[infile][h].setAnnotation('Path', mcpath + h)
            sighisto = mchistos[infile][h]

        # fill test results for each bin for this histogram
        bgCount,bgError,sigCount,sigError,measCount,measError,CLs,normFacSig,normFacRef = util.fillResults(refdata,h,lumi,has1D,mc1D,sighisto,Nev,xsec)
        if (len(CLs)==0):
            CLs.append(0)

        ## DrawOnly is needed to keep the order in the Legend equal to the
        ## order of the files on the command line
        anaobjects = []
        drawonly = []

        ## Check if we have reference data for the histogram
        ratioreference = None
        if refhistos.has_key('/REF' + h):
            refdata = refhistos['/REF' + h]
            refdata.setAnnotation('ErrorBars', '1')
            refdata.setAnnotation('PolyMarker', '*')
            refdata.setAnnotation('ConnectBins', '0')
            refdata.setAnnotation('Title', 'Data')
            #if ctr.isNorm(h)[0] == True:
            #    refdata.setAnnotation('Scale', str(normFacRef))
            #if opts.RATIO:
            #    ratioreference = '/REF'+h
            anaobjects.append(refdata)
            drawonly.append('/REF' + h)

        drawonly.append(mcpath + h)

        for i in range(0, refdata.numPoints):
            if ctr.isNorm(h)[0] == True:
                sighisto.points[i].y=(sighisto.points[i].y*normFacSig+refdata.points[i].y*normFacRef)*1/normFacRef
                sighisto.points[i].yErrs =((refdata.points[i].yErrs[1])**2 + (sighisto.points[i].yErrs[1])**2 )**0.5
            elif has1D:
                sighisto.points[i].y=sighisto.points[i].y+refdata.points[i].y
                sighisto.points[i].yErrs =((refdata.points[i].yErrs[1])**2 + (sighisto.points[i].yErrs[1])**2 )**0.5
            # if there was no 1D plot, assume we had an already-made ratio (ATLAS MET)

        # write the bin number of the most significant bin, and the bin number for the plot legend
        sighisto.title='[%s] %5.2f' % ( CLs.index(max(CLs))+1, max(CLs) )
        sighisto.setAnnotation('LineColor', 'red')
        anaobjects.append(sighisto)
        plot = util.Plot()
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
        util.writeOutput2(output, h, opts.OUTPUTDIR)
        # All these extra count checks are to stop any plots with no count in most likely bin from being entered
        # into liklihood calc, should be fixed upstream

        # See if any additional grouping is needed 'subpool'
        max_cl = CLs.index(max(CLs))
        if ctr.LumiFinder(h)[2]:
            tempKey = h.split('/')[1] + '_' + ctr.LumiFinder(h)[2]
            if tempKey not in mapPoints and bgCount[max_cl] > 0.0:
                if(grid):
                    mapPoints[tempKey] = [float(x),float(y), float(max(CLs)) , [sigCount[CLs.index(max(CLs))]],
                                         [bgCount[CLs.index(max(CLs))]] , [bgError[CLs.index(max(CLs))]], [sigError[CLs.index(max(CLs))]],str(h)]
                else:
                    mapPoints[tempKey] = [float(max(CLs)),[ sigCount[max_cl] ],[ bgCount[max_cl]  ],[ bgError[max_cl]  ],[ sigError[max_cl] ], str(h)]

            elif bgCount[max_cl] > 0.0:
                corr = 0
                if(grid): corr = 2

                mapPoints[tempKey][1+corr].append(sigCount[max_cl])
                mapPoints[tempKey][2+corr].append(bgCount[max_cl])
                mapPoints[tempKey][3+corr].append(bgError[max_cl])
                mapPoints[tempKey][4+corr].append(sigError[max_cl])
                mapPoints[tempKey][5+corr] += "," + (str(h))
        else:
            if h not in mapPoints and bgCount[max_cl] > 0.0:
                if(grid):
                    mapPoints[h] = [float(x),float(y), float(max(CLs)) , [sigCount[CLs.index(max(CLs))]],
                                         [bgCount[CLs.index(max(CLs))]] , [bgError[CLs.index(max(CLs))]], [sigError[CLs.index(max(CLs))]],str(h)]
                else:
                    mapPoints[h] = [float(max(CLs)),[ sigCount[max_cl] ],[ bgCount[max_cl]  ],[ bgError[max_cl]  ],[ sigError[max_cl] ], str(h)]

        # End of the loop over histograms.

    return mapPoints

def output_grid(masterDict, opts):
    for key in masterDict:
        if masterDict[key]:
            masterDict[key].sort(key=lambda x: x[0])
            util.writeOutput(masterDict[key],key + ".dat")
            with open(opts.ANALYSISDIR+"/"+key+'.map', 'w') as f:
                pickle.dump(masterDict[key], f)


def output_single(mapPoints, opts):
    """
    Scan through all points and fill each category, stored in masterDict,
    with the counts from each grouping if it is more sensitive than the
    Previous fill
    """
    masterDict = init_dict()

    for key, pts in mapPoints.iteritems():
        poolname = ctr.LumiFinder(key)[1]
        # Need to recalculate this for cases with subpools.
        pts[0] = ctr.confLevel(pts[1], pts[2], pts[3], pts[4])
        if not masterDict[poolname]:
            masterDict[poolname].append(pts[:])
        else:
            for listelement in masterDict[poolname]:
                if pts[0] > listelement[0]:
                    masterDict[poolname][masterDict[poolname].index(listelement)] = pts[:]

    sigfinal=[]
    bgfinal=[]
    bgerrfinal=[]
    sigerrfinal=[]
    for key in masterDict:
        if masterDict[key]:
            sigfinal.extend(map(list,zip(*masterDict[key])[1])[0])
            bgfinal.extend(map(list,zip(*masterDict[key])[2])[0])
            bgerrfinal.extend(map(list,zip(*masterDict[key])[3])[0])
            sigerrfinal.extend(map(list,zip(*masterDict[key])[4])[0])
            masterDict[key].sort(key=lambda x: x[0])
            util.writeOutput(masterDict[key], key + ".dat")
            with open(opts.ANALYSISDIR + "/" + key + '.map', 'w') as f:
                pickle.dump(masterDict[key], f)

    if len(sigfinal)>0:
        # Open the summary file for writing.
        sumfn = open(opts.ANALYSISDIR+"/Summary.txt", 'w')

        # Calculate the confidence level from the list of independent signal and
        # background values.
        # TODO: when we have mixed methods for doing this, the numbers in the lists
        # stored in masterDict have different meanings, so this is broken!
        pccl = 100.*ctr.confLevel(sigfinal, bgfinal, bgerrfinal,sigerrfinal)

        result = "Combined CL exclusion for these plots is %.1f %%" % pccl
        sumfn.write(result)
        for anapool in masterDict:
            if masterDict[anapool]:
                sumfn.write("\n"+anapool)
                sumfn.write("\n"+str(masterDict[anapool][0][5]))

        sumfn.close()
        print(result)
        print "Based on " +str(len(sigfinal))+ " found counting tests"
        print "\nMore details output to ", opts.ANALYSISDIR, " folder"
