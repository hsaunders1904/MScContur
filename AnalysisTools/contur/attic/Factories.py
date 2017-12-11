import os
import yoda
import re
import rivet
from contur import TestingFunctions as ctr
import contur.Utils as util
import pandas as pd


ANALYSIS=re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)')

REFLOAD=False
refObj={}
def init_ref():
    """Function to load all reference data into memory
    Here reference data can be either experimental data or theoretical prediction"""
    refFiles=[]
    #refObj = {}
    print "Gathering all reference Data"
    rivet_data_dirs = rivet.getAnalysisRefPaths()
    for dirs in rivet_data_dirs:
        import glob
        refFiles.append(glob.glob(os.path.join(dirs, '*.yoda')))
    for fileList in refFiles:
        for f in fileList:
            aos = yoda.read(f)
            for path, ao in aos.iteritems():
                if path.startswith('/REF/'):
                    refObj[path] = ao
                if path.startswith('/THY/'):
                    #TODO provide this information in the first place!
                    refObj[path] = ao
    global REFLOAD
    REFLOAD = True

class conturFact(object):
    """Parent class to initialise a contur analysis, stores results at each point and handles I/O
    #TODO Add a model point info that can be set to group all added conturPoints  by parameter space point
    additionally, this will be needed to do grid runs

    The sortedPoints and ctPt variables would then be inside dictionaries with a key for each parameter space
    point
    """

    def __init__(self):
        self.masterDict = {}
        self.conturPoints=[]
        self._sortedPoints=[]
        self._ctPt=conturPoint()

    def addPoint(self, ctPt):
        """Add all valid contur points to be sorted from an input file"""
        # self.masterDict.update({name, conturPoint})
        #self.masterDict[name] = conturPoint
        if ctPt.__class__ != conturPoint:
            raise AssertionError("Must be adding a conturPoint")
        self.conturPoints.append(ctPt)

    def sortPoints(self):
        """Function call to sort conturPoints"""
        pools=[]
        [pools.append(x) for x in [item.pools for item in self.conturPoints] if x not in pools]
        for p in pools:
            anas=[]
            [anas.append(x) for x in [ANALYSIS.search(item.tags).group() for item in self.conturPoints if item.tags and item.pools == p] if x not in anas]
            for a in anas:
                subpools = []
                [subpools.append(x) for x in [item.subpools for item in self.conturPoints if item.pools == p and a in item.tags ] if x not in subpools ]
                if subpools[0]:
                    result={}
                    for sp in subpools:
                        result[sp]=conturPoint()
                    for k,v in result.iteritems():
                        #remove the point if it ends up in a group
                        [result[k].addPoint(y) for y in self.conturPoints if y.subpools == k and a in y.tags ]
                        v.calcCLs()
                        v.pools=p
                        v.tags=a
                    #add the max subpool back into the list of points with the pool tag set but no subpool
                    [self.conturPoints.append(v) for k,v in result.iteritems()] # if v.CLs == max([z.CLs for z in result.values()])

        for p in pools:
            [self._sortedPoints.append(item) for item in self.conturPoints if item.CLs == max([x.CLs for x in self.conturPoints if x.pools==p]) and item.pools == p and item.pools not in [x.pools for x in self._sortedPoints]]
        #once all the points are sorted and the representative of each pool is put into _sortedPoints, work out the final exclusion
        self.buildFinal()


    def buildFinal(self):
        """Function to build the final contur point out of the safe combination of all input points"""
        for x in self._sortedPoints:
            self._ctPt.addPoint(x)
        self._ctPt.calcCLs()

    @property
    def sortedPoints(self):
        return self._sortedPoints
    @property
    def conturPoint(self):
        return self._ctPt

    def __repr__(self):
        return repr(self._ctPt)



class histFact(object):
    """
    Take a yoda analysis object and structure a contur ready object
    This acts as a wrapper class for the underlying analysis object
    """

    def __init__(self, anaObj, xSec, nEv):
        # Construct with an input yoda aos and a scatter1D for the cross section and nEv
        self.signal = anaObj
        self.xsec = xSec
        self.nev = nEv

        # Initialize the members we always want to access
        self._background = False
        self.ref = False
        self.stack = yoda.Scatter2D
        self.lumi = 1
        self.isScaled = False
        self.scaleFactorData = 1
        self.scaleFactorSig = 1
        self.conturPoints = []
        self.mcLumi = 0.0
        self.scaleMC = 1.0

        # Call the internal functions on initialization
        # to fill the above members with what we want, these should all be private
        self.__getData()
        self.__getAux()
        self.__getMC()
        self.__getisScaled()
        if self.__has1D():
            self.signal = yoda.mkScatter(self.signal)
        # build stack for plotting
        # self.__buildStack()
        if self.ref:
            self.__doScale()
            self.__fillPoints()

    @property
    def _background(self):
        return self._background

    def __has1D(self):
        """Check type of input aos
        """
        if self.signal.type == 'Histo1D' or self.signal.type == 'Profile1D':
            if self.signal.sumW()==0.0:
                self.mcLumi=0.0
            else:
                self.mcLumi = float(self.signal.numEntries()) / float(self.signal.sumW())
            if self.isScaled:
                # if the Data is scaled, work out the signal scaling from number of events and generator xs
                try:
                    self.scaleFactorSig = (
                        float(self.signal.numEntries()) / float(self.nev.numEntries()) * float(self.xsec.points[0].x))

                except:
                    print "missing info for scalefactor calc"
            return True
        else:
            return False

    def __getisScaled(self):
        """Check if the data to compare to is normalized
        """
        self.isScaled, self.scaleFactorData, self.scaleMC = ctr.isNorm(self.signal.path)

    def __getData(self):
        """Looks up ref data"""
        if not REFLOAD:
            init_ref()
        for path,ao in refObj.iteritems():
            if self.signal.path in path:
                self.ref = ao


    def __getMC(self):
        """Lookup for any stored SM MC background calculation
        Currently doesn't exist so just return the refdata
        """
        try:
            self._background = self.ref.clone()
        except:
            print "No reference data found for histo: " + self.signal.path

    def __getAux(self):
        """Sets member variables from static lookup tables
        :return:
        """
        self.lumi, self.pool, self.subpool = ctr.LumiFinder(self.signal.path)

    def __buildStack(self):
        """Build the signal/background stack for plotting
        """
        if self.signal.type != "Scatter2D":
            return False
        elif not self._background:
            return False
        else:
            self.stack = self.signal.clone()
            assert self.stack.numPoints == self._background.numPoints
            for i in range(0, len(self.stack.points)):
                self.stack.points[i].y = self.stack.points[i].y + self._background.points[i].y

    def __doScale(self):
        """Do the normalisation of the main attributes
        :return:
        """
        if self.signal.type != "Scatter2D":
            return False
# for sig,ref,bg in zip(..,..,..):
        for i in range(0, len(self.signal.points)):
            self.signal.points[i].y = self.signal.points[i].y * self.lumi * self.scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin)
            self.signal.points[i].yErrs = (
                self.signal.points[i].yErrs[0] * self.lumi * self.scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin),
                self.signal.points[i].yErrs[1] * self.lumi * self.scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin)
            )
        for i in range(0, len(self.ref.points)):
            self.ref.points[i].y = self.ref.points[i].y * self.lumi * self.scaleFactorData * (
                self.ref.points[i].xMax - self.ref.points[i].xMin)
            self.ref.points[i].yErrs = (
                self.ref.points[i].yErrs[0] * self.lumi * self.scaleFactorData * (
                    self.ref.points[i].xMax - self.ref.points[i].xMin),
                self.ref.points[i].yErrs[1] * self.lumi * self.scaleFactorData * (
                    self.ref.points[i].xMax - self.ref.points[i].xMin)
            )
        for i in range(0, len(self._background.points)):
            # background should have a separate scalefactor later
            self._background.points[i].y = self._background.points[i].y * self.lumi * self.scaleFactorData * (
                self._background.points[i].xMax - self._background.points[i].xMin)
            self._background.points[i].yErrs = (
                self._background.points[i].yErrs[0] * self.lumi * self.scaleFactorData * (
                    self._background.points[i].xMax - self._background.points[i].xMin),
                self._background.points[i].yErrs[1] * self.lumi * self.scaleFactorData * (
                    self._background.points[i].xMax - self._background.points[i].xMin)
            )

    def __fillPoints(self):
        """For now we just fill a conturPoint for each bin, if systematic correlations exist this can be improved"""
        if self.signal.type != "Scatter2D":
            return False
        for i in range(0, len(self.signal.points)):
            ctrPt = conturPoint()
            #need this as empty s is returning CL=1, this should be fixed in the limit setting functions
            if self.signal.points[i].y == 0.0:
                continue
            ctrPt.s = self.signal.points[i].y
            ctrPt.bg = self._background.points[i].y
            ctrPt.bgErr =self._background.points[i].yErrs[1]
            ctrPt.nObs =self.ref.points[i].y
            # TODO check how we work mcLumi out
            ctrPt.sErr = self.mcLumi
            ctrPt.calcCLs()
            ctrPt.tags=self.signal.path
            ctrPt.pools=self.pool
            ctrPt.subpools=self.subpool
            self.conturPoints.append(ctrPt)


class conturBucket(object):
    """ A conturBucket is a collection of conturPoints that forms a combined test

    """
    members = ["s", "sErr", "bg", "bgErr", "nobs", "nobsErr","CLs","tags","pool","subpool"]
    def __init__(self):
        self.bucket=pd.DataFrame(columns=self.members)
        print "break"
    #def addPoint(self):
    #    self.bucket



class conturPoint(object):
    """ A conturPoint is a container for the counts that an observable forms
    histFactory creates a series of conturPoints from any well formed conturPoints
    """

    members = ["s", "sErr", "bg", "bgErr", "nobs"]
    def __init__(self):
        #self.counts = dict.fromkeys(self.members,[])
        #self.counts=defaultdict(self.members)
        self.counts={}
        for m in self.members:
            self.counts[m]=[]
        self.CLs=0.0
        self._tags=''
        self._pools=''
        self._subpool=''


    def calcCLs(self):
        """Public function to recalculate CL of this contur point"""
        #check points is well formed (equal arg lengths)
        if not self.__checkConsistency():
            self.CLs=0.0
        else:
            self.CLs = ctr.confLevel(self.s, self.bg, self.bgErr, self.sErr)


    def __checkConsistency(self):
        """Internal function to check if the point is well formed
        Errors if unequal arg length and returns False if point is empty"""
        ref = len(self.counts[self.counts.keys()[0]])
        for k,v in self.counts.iteritems():
            if len(v) !=ref:
                raise AssertionError("Unequal lengths of arguments in conturpoint")
        if ref == 0:
            return False
        else:
            return True

    def addPoint(self,point):
        if point.__class__ != conturPoint:
            raise AssertionError("Must be a conturPoint to add to conturPoint")
        for k,v in point.counts.iteritems():
            self.counts[k].extend(v)
        #self._tags.extend(point.tags)


    @property
    def s(self):
        """Signal count"""
        return self.counts["s"]
    @s.setter
    def s(self,value):
        self.counts["s"].append(value)

    @property
    def sErr(self):
        return self.counts["sErr"]
    @sErr.setter
    def sErr(self, value):
        self.counts["sErr"].append(value)

    @property
    def bg(self):
        return self.counts["bg"]
    @bg.setter
    def bg(self, value):
        self.counts["bg"].append(value)

    @property
    def bgErr(self):
        return self.counts["bgErr"]
    @bgErr.setter
    def bgErr(self, value):
        self.counts["bgErr"].append(value)

    @property
    def nObs(self):
        return self.counts["nobs"]
    @nObs.setter
    def nObs(self, value):
        self.counts["nobs"].append(value)

    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self,value):
        self._tags=value

    @property
    def pools(self):
        return self._pools
    @pools.setter
    def pools(self,value):
        self._pools=value

    @property
    def subpools(self):
        return self._subpool
    @subpools.setter
    def subpools(self,value):
        self._subpool=value


    def __repr__(self):
        return repr(self.counts)

