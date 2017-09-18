import os
import yoda
import rivet
from contur import TestingFunctions as ctr
import contur.Utils as util


class conturFact(object):
    """Parent class to initialise a contur analysis, stores results at each point and handles I/O"""

    def __init__(self):
        self.masterDict = {}
        self.testVar = 1
        self.conturPoints=[]


    def addPoint(self, conturPoint):
        """Add all valid contur points to be sorted from an input file"""
        # self.masterDict.update({name, conturPoint})
        #self.masterDict[name] = conturPoint
        if conturPoint.__class__ != conturPoint:
            raise AssertionError("Must be adding a conturPoint")
        self.conturPoints.append(conturPoint)


    def __str__(self):
        return self.testVar

#
# class masterDict(conturFact):
#     """Dictionary to hold contur points"""
#     def __init__(self):
#         self.dict={}
#     @classmethod
#     def addPoint(self):
#         self.dict = 1


class histFact(object):
    """
    Take a yoda analysis object and structure a contur ready object
    This acts as a wrapper class for the underlying analysis object
    """

    #
    # background = False
    # scaleFactorSig=1
    # scaleFactorData=1
    # conturPoints = []
    # mcLumi = 0.0
    # lumi = 1.0
    # isScaled = False
    # ref = False
    # background = False
    # stack = yoda.Scatter2D


    def __init__(self, anaObj, xSec, nEv):
        # Construct with an input yoda aos and a scatter1D for the cross section and nEv
        self.signal = anaObj
        self.xsec = xSec
        self.nev = nEv

        # Initialize the members we always want to access
        self.background = False
        self.ref = False
        self.stack = yoda.Scatter2D
        self.lumi = 1
        self.isScaled = False
        self.scaleFactorData = 1
        self.scaleFactorSig = 1
        self.conturPoints = []
        self.mcLumi = 0.0

        # Call the internal functions on initialization
        # to fill the above members with what we want, these should all be private
        self.__getData()
        if self.__has1D():
            self.signal = yoda.mkScatter(self.signal)
        self.__getAux()
        self.__getMC()
        self.__getisScaled()
        # build stack for plotting
        # self.__buildStack()
        self.__doScale()
        self.__fillPoints()

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
                        float(self.signal.numEntries()) / float(self.nev.numEntries()) * float(self.xsec.x))
                except:
                    print "missing info for scalefactor calc"
            return True
        else:
            return False

    def __getisScaled(self):
        """Check if the data to compare to is normalized
        """
        self.isScaled, self.scaleFactorData, scaleMC = ctr.isNorm(self.signal.path)

    def __getData(self):
        """Looks up ref data"""
        refFiles = []
        rivet_data_dirs = rivet.getAnalysisRefPaths()
        for dirs in rivet_data_dirs:
            import glob
            refFiles.append(glob.glob(os.path.join(dirs, '*.yoda')))
        for fileList in refFiles:
            for f in fileList:
                aos = yoda.read(f)
                for path, ao in aos.iteritems():
                    if path.startswith('/REF/'):
                        if self.signal.path in path:
                            self.ref = ao

    def __getMC(self):
        """Lookup for any stored SM MC background calculation
        Currently doesn't exist so just return the refdata
        """
        try:
            self.background = self.ref.clone()
        except:
            print "no ref for histo"

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
        elif not self.background:
            return False
        else:
            self.stack = self.signal.clone()
            assert self.stack.numPoints == self.background.numPoints
            for i in range(0, len(self.stack.points)):
                self.stack.points[i].y = self.stack.points[i].y + self.background.points[i].y

    def __doScale(self):
        """Do the normalisation of the main attributes
        :return:
        """
        if self.signal.type != "Scatter2D":
            return False

        for i in range(0, len(self.signal.points)):
            self.signal.points[i].y = self.signal.points[i].y * self.scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin)
            self.signal.points[i].yErrs = (
                self.signal.points[i].yErrs[0] * self.scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin),
                self.signal.points[i].yErrs[1] * self.scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin)
            )
        for i in range(0, len(self.ref.points)):
            self.ref.points[i].y = self.ref.points[i].y * self.scaleFactorData * (
                self.ref.points[i].xMax - self.ref.points[i].xMin)
            self.ref.points[i].yErrs = (
                self.ref.points[i].yErrs[0] * self.scaleFactorData * (
                    self.ref.points[i].xMax - self.ref.points[i].xMin),
                self.ref.points[i].yErrs[1] * self.scaleFactorData * (
                    self.ref.points[i].xMax - self.ref.points[i].xMin)
            )
        for i in range(0, len(self.background.points)):
            # background should have a separate scalefactor later
            self.background.points[i].y = self.background.points[i].y * self.scaleFactorData * (
                self.background.points[i].xMax - self.background.points[i].xMin)
            self.background.points[i].yErrs = (
                self.background.points[i].yErrs[0] * self.scaleFactorData * (
                    self.background.points[i].xMax - self.background.points[i].xMin),
                self.background.points[i].yErrs[1] * self.scaleFactorData * (
                    self.background.points[i].xMax - self.background.points[i].xMin)
            )

            # def buildcontourPoint(self):

    def __fillPoints(self):
        """For now we just fill a conturPoint for each bin, if systematic correlations exist this can be improved"""
        if self.signal.type != "Scatter2D":
            return False
        for i in range(0, len(self.signal.points)):
            ctrPt = conturPoint()
            ctrPt.s =  self.signal.points[i].y
            ctrPt.bg = self.background.points[i].y
            ctrPt.bgErr =self.background.points[i].yErrs[1]
            ctrPt.nObs =self.ref.points[i].y
            # TODO check how we work mcLumi out
            ctrPt.sErr = self.mcLumi
            ctrPt.calcCLs()
            ctrPt.tags=self.signal.path
            ctrPt.pools=self.pool
            ctrPt.subpools=self.subpool
            self.conturPoints.append(ctrPt)


# class conturPoint(dict):
#     """
#     Defines a contur point, wrapper class for python dict to initialize necessary values and offer function call to update CLs
#     """
#
#     members = ["s", "sErr", "bg", "bgErr", "nobs"]
#     #CLs=0.0
#
#     def __init__(self):
#         dict.__init__(self)
#         #this is not quite write but initialize the dictionary with the default entries needed as empty lists
#
#         for m in self.members:
#             self.__setattr__(m,[])
#         self.CLs=0.0
#         #self.update(dict)
#         testVar=2
#
#     def calcCLs(self):
#         """Public function to recalculate CL of this contur point"""
#         #check points is well formed (equal arg lengths)
#         if not self.__checkConsistency():
#             self.CLs=0.0
#         else:
#             self.CLs = ctr.confLevel(self.s, self.bg, self.bgErr, self.sErr)
#
#
#     def __checkConsistency(self):
#         """Internal function to check if the point is well formed
#         Errors if unequal arg length and returns False if point is empty"""
#
#         ref = len(self[self.members[0]])
#         for m in self.members:
#             if len(self[m]) !=ref:
#                 raise AssertionError("Unequal lengths of arguments in conturpoint")
#
#         #If point is empty let it be known
#         if ref == 0:
#             return False
#         else:
#             return True
#
#     def __getattr__(self, name):
#         if name in self:
#             return self[name]
#         else:
#             raise AttributeError("No such attribute: " + name)
#
#     def __setattr__(self, name, item):
#         self[name] = item
#
#     def __delattr__(self, name):
#         if name in self:
#             del self[name]
#         else:
#             raise AttributeError("No such attribute: " + name)
#
#     def addPoint(self,point):
#         if point.__class__ != conturPoint:
#             raise AssertionError("Must be a conturPoint to add to conturPoint")
#         for k,v in point.iteritems():
#             self[k].extend(v)

#from collections import defaultdict

class conturPoint(object):
    members = ["s", "sErr", "bg", "bgErr", "nobs"]
    def __init__(self):
        #self.counts = dict.fromkeys(self.members,[])
        #self.counts=defaultdict(self.members)
        self.counts={}
        for m in self.members:
            self.counts[m]=[]
        self.CLs=0.0
        self._tags=[]
        self._pools=[]
        self._subpool=[]


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
        self._tags.extend(point.tags)


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
        self._tags.append(value)

    @property
    def pools(self):
        return self._pools
    @pools.setter
    def pools(self,value):
        self._pools.append(value)

    @property
    def subpools(self):
        return self._subpool
    @subpools.setter
    def subpools(self,value):
        self._subpool.append(value)


    def __repr__(self):
        return repr(self.counts)


for root, dirs, files in os.walk('.'):
    for name in files:
        fileliststatic = []
        conturFactory=conturFact()
        if '.yoda' in name and 'LHC' not in name:
            yodafile = os.path.join(root, name)
            fileliststatic = str(yodafile)
            refhistos, mchistos, xsec, Nev = util.getHistos(fileliststatic)
            hpaths = []
            m = conturFact()
            for aos in mchistos.values():
                for p in aos.keys():
                    if p and p not in hpaths:
                        hpaths.append(p)

            for k, v in mchistos.iteritems():
                for k2, v2 in v.iteritems():
                    if v2.type=="Scatter2D":
                        continue
                    if "count" in k2:
                        continue
                    try:
                        y=ctr.validHisto(v2.path)
                    except:
                        y=False
                        pass

                    if y:
                        histo = histFact(v2, xsec, Nev)
                        print histo.lumi
                        for p in histo.conturPoints:
                            print p.CLs
                        max_cl=[item.CLs for item in histo.conturPoints].index(max([item.CLs for item in histo.conturPoints]))
                        conturFactory.addPoint(histo.conturPoints[max_cl])
                        #    z=histo.conturPoints[0].addPoint(histo.conturPoints[2])
                        #m.addPoint(histo.conturPoints)
            print "done"
                        # contour=conturPoint(histo)
