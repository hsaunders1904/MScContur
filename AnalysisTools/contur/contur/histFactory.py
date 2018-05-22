import os
import yoda
import re
import rivet
import numpy as np
from contur import TestingFunctions as ctr
import contur.Utils as util
from conturPoint import conturPoint

ANALYSIS = re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)')
REFLOAD = False
refObj = {}
scaledYet = {}

def init_ref():
    """Function to load all reference data and theory *.yoda data"""
    refFiles = []
    global scaledYet
    print "Gathering all reference Data (and Theory, if available)"
    rivet_data_dirs = rivet.getAnalysisRefPaths()
    for dirs in rivet_data_dirs:
        import glob
        refFiles.append(glob.glob(os.path.join(dirs, '*.yoda')))
    for fileList in refFiles:
        for f in fileList:
            aos = yoda.read(f)
            for path, ao in aos.iteritems():
                if ao.type!="Scatter2D":
                    ao = yoda.mkScatter(ao)
                if ao.type=="Scatter1D":
                     ao = util.mkScatter2D(ao)
                if path.startswith('/REF/'):
                    refObj[path] = ao
                    scaledYet[path] = False
                if path.startswith('/THY/'):
                    refObj[path] = ao
                    scaledYet[path] = False


    global REFLOAD
    REFLOAD = True

class histFactory(object):
    """Processes and decorates yoda AnalysisObjects to a testable format, filling candidate conturPoints

    This object is initialised with 3 arguments:
    anaObj - A yoda analysis object (see https://yoda.hepforge.org/pydoc/)
    xSec - Total MC Generator XS
    nEv - Total MC Generated Events

    Returns metadata attributes and a formated list of conturPoints
    """

    def __init__(self, anaObj, xSec, nEv, TestMethod, GridMode):

        # Construct with an input yoda aos and a scatter1D for the cross section and nEv
        self.signal = anaObj
        self.xsec = xSec
        self.nev = nEv
        # Overall effective integrated luminosity may be recalculated plot by plot because units change.
        self._mcLumi = float(nEv.numEntries())/xSec.point(0).x
 
        # Initialize the public members we always want to access
        self._has1Dhisto = False
        self._background = False
        self._ref = False
        self._stack = yoda.Scatter2D
        self._refplot = yoda.Scatter2D
        self._sigplot = yoda.Scatter2D
        self._bgplot = yoda.Scatter2D
        self._lumi = 1
        self._isScaled = False
        self._scaleFactorData = 1
        self._scaleFactorSig = 1
        self._conturPoints = []
        self._scaleMC = 1.0
        self._maxcl = -1
        self._maxbin = -1
        self._testMethod = TestMethod

        # Call the internal functions on initialization
        # to fill the above members with what we want, these should all be private
        self.__getData()
        self.__getAux()
        self.__getMC()
        self.__getisScaled()


        # Determine the type of object we have, and build a 2D scatter from it if it is not one already
        # Also recalculate MCLumi, and scalefactor, if appropriate
        if self.signal.type == 'Histo1D' or self.signal.type == 'Profile1D' or self.signal.type == 'Counter':
            
            self._has1Dhisto = True

            if self._isScaled:
                # if the plot is area normalised (ie scaled), work out the factor from number of events and generator xs
                # (this is just the integrated cross section associated with the plot)
                try:
                    self._scaleFactorSig = (
                        float(self.xsec.points[0].x)) * float(self.signal.numEntries()) / float(self.nev.numEntries())
                except:
                    print "missing info for scalefactor calc"

            # effective MClumi has to be calculated plot-by-plot because units change and some plots are symmetrised (in which
            # there will be a factor of two between this the mclumi from (number of generated events/xsec) )
            if self.signal.sumW() != 0.0:
                self._mcLumi = float(self.signal.numEntries()) / (float(self.signal.sumW())*self._scaleFactorSig)

            self.signal = yoda.mkScatter(self.signal)
            # Make sure it is actually a Scatter2D - mkScatter makes Scatter1D from counter.   
            if self.signal.type == 'Scatter1D':
                self.signal = util.mkScatter2D(self.signal) 

            
        if not GridMode:
        #Public member function to build plots needed for direct histogram visualisation
        #avoid calling YODA.clone() unless we have to
        #Must be called before scaling.
            self.doPlot()            

        if self._ref:
            # don't scale histograms that came in as 2D scatters
            if self._has1Dhisto:
                self.__doScale()
            self.__fillPoints()

           #print "initialised histfactory:", self._ref.path 
           #print self._ref.points[0], self.background.points[0]


    def __getisScaled(self):
        """Check if the data to compare to is normalized
        """
        self._isScaled, self._scaleFactorData, self._scaleMC = ctr.isNorm(self.signal.path)

    def __getData(self):
        """Looks up ref data"""
        if not REFLOAD:
            init_ref()
        for path, ao in refObj.iteritems():
            if self.signal.path in path and "/REF/" in path:
                self._ref = ao

    def __getMC(self):
        """Lookup for any stored SM MC background calculation
        If doesn't exist, just return the refdata
        """
        if not REFLOAD:
            init_ref()

        gotTh = False    
        if "T" in self._testMethod:

            for path, ao in refObj.iteritems():
                if self.signal.path in path and "/THY/" in path:
                    gotTh = True
                    print "got theory", path
                    self._background = ao

        if not gotTh:            
            try:
                self._background = self._ref.clone()
            except:
                print "No reference data found for histo: " + self.signal.path


    def doPlot(self):
        """Public member function to build yoda plot members for interactive runs"""
        self._bgplot = self._background.clone()
        self._refplot = self._ref.clone()
        # build stack for plotting, for histogrammed data
        if self._has1Dhisto:
            self.__buildStack()
        else:
            self._stack = self.signal.clone()
        self._sigplot = self.signal.clone()

    def __getAux(self):
        """Sets member variables from static lookup tables
        :return:
        """
        self._lumi, self.pool, self.subpool = ctr.LumiFinder(self.signal.path)

    def __buildStack(self):
        """Build the signal/background stack for plotting
        """

        if self.signal.type != "Scatter2D":
            return False
        elif not self._background:
            return False
        else:
            self._stack = self.signal.clone()
            assert self._stack.numPoints == self._background.numPoints

            for i in range(0, len(self._stack.points)):
                self._stack.points[i].y = self._stack.points[i].y*self._scaleFactorSig/self._scaleFactorData + self._background.points[i].y
                self._stack.points[i].yErrs = (
                    self._stack.points[i].yErrs[0]*self._scaleFactorSig/self._scaleFactorData + self._background.points[i].yErrs[0], 
                    self._stack.points[i].yErrs[1]*self._scaleFactorSig/self._scaleFactorData + self._background.points[i].yErrs[1])

    def __doScale(self):
        """Perform the normalisation of the signal, reference and background data

        Scales signal
        """

        if self.signal.type != "Scatter2D":
            return False

        # turn the published plots into numbers of events expected to appear in the measurement
        # Factors needed are the bin width and the integrated lumi for which the measurement are made, and
        # for plots which were area normalised in rivet, the integrated cross section associated with the plot, to undo that.

        # @TODO is there any reason why we can't do all this in the same loop? Surely the
        # number of points, binwidths etc have to be the same?

        for i in range(0, len(self.signal.points)):
            binWidth = self.signal.points[i].xMax - self.signal.points[i].xMin
            self.signal.points[i].y = self.signal.points[i].y * self._lumi * self._scaleFactorSig * binWidth
            # the current error on the signal derives from the MC stats. There should also be
            # a term due the stat uncertainty on the number of events predicted for this LHC lumi.
            # At this point, y has been scaled to be number of events, so calculate this here (Poisson) and add it in quadrature
            statErr2 = np.absolute(self.signal.points[i].y)
            yErr0 = np.sqrt( (self.signal.points[i].yErrs[0] * self._lumi * self._scaleFactorSig * binWidth)**2 + statErr2 ) 
            yErr1 = np.sqrt( (self.signal.points[i].yErrs[1] * self._lumi * self._scaleFactorSig * binWidth)**2 + statErr2 ) 
            self.signal.points[i].yErrs = ( yErr0, yErr1 )

        # for grid running - only scale the REF/Background data once!    
        global scaledYet 
        if not scaledYet[self._ref.path]:
            for i in range(0, len(self._ref.points)):
                binWidth = self._ref.points[i].xMax - self._ref.points[i].xMin
                self._ref.points[i].y = self._ref.points[i].y * self._lumi * self._scaleFactorData * binWidth                
                self._ref.points[i].yErrs = (
                    self._ref.points[i].yErrs[0] * self._lumi * self._scaleFactorData * binWidth,
                    self._ref.points[i].yErrs[1] * self._lumi * self._scaleFactorData * binWidth
                    )

            for i in range(0, len(self._background.points)):
                # background should have a separate scalefactor later
                binWidth = self._background.points[i].xMax - self._background.points[i].xMin
                self._background.points[i].y = self._background.points[i].y * self._lumi * self._scaleFactorData * binWidth                
                self._background.points[i].yErrs = (
                    self._background.points[i].yErrs[0] * self._lumi * self._scaleFactorData * binWidth,
                    self._background.points[i].yErrs[1] * self._lumi * self._scaleFactorData * binWidth
                    )
        scaledYet[self._ref.path] = True


    def __fillPoints(self):
        """Internal function to fill conturPoints list

        Fills the conturPoints attribute with all calculable conturPoints, requires reference data present and __doScale
        to have successfully run

        Takes into account the requested Test Method

        """
        if self.signal.type != "Scatter2D":
            return False
        # counter to track the maximum discrepant point
        clmax = 0.0

        for i in range(0, len(self.signal.points)):

            # don't trust unfolded zero (or less!) bins                    
            if self._ref.points[i].y<=0:
                continue

            ctrPt = conturPoint()
            ctrPt.s = self.signal.points[i].y
            ctrPt.sErr = self.signal.points[i].yErrs[1]
            ctrPt.meas = self._ref.points[i].y
            ctrPt.measErr = self._ref.points[i].yErrs[1]

            if "T" in self._testMethod:
                # Using theory if it is there
                ctrPt.bg = self._background.points[i].y
                if "D" in self._testMethod or "THY" in self._background.path:
                    ctrPt.bgErr = self._background.points[i].yErrs[1]
                else:
                    ctrPt.bgErr = 0.0
            else:    
                # Not using theory
                ctrPt.bg = self._ref.points[i].y
                if "D" in self._testMethod:
                    ctrPt.bgErr = self._ref.points[i].yErrs[1]
                else:
                    ctrPt.bgErr = 0.0


            ctrPt.kev  = self.signal.points[i].y*self._mcLumi/self._lumi

            if self._has1Dhisto:
                ctrPt.isRatio = False
            else:
                ctrPt.isRatio = True

            ctrPt.calcCLs(self._testMethod)
            
            ctrPt.tags = self.signal.path
            ctrPt.pools = self.pool
            ctrPt.subpools = self.subpool
            self._conturPoints.append(ctrPt)
            if ctrPt.CLs > clmax:
                clmax = ctrPt.CLs
                self._maxcl = len(self._conturPoints)-1
                self._maxbin = i+1

    @property
    def maxcl(self):
        """The index of the most discrepant point for this plot"""
        return self._maxcl

    @property
    def maxbin(self):
        """The bin number of the most discrepant point for this plot"""
        return self._maxbin

    @property
    def background(self):
        """Background scaled yoda.Scatter2D used as input to a conturPoint"""
        return self._background

    @property
    def ref(self):
        """Bool representing if ref data was found for a given analysis object"""
        return self._ref

    @property
    def stack(self):
        """Stacked, unscaled Signal+background for plotting yoda.Scatter2D"""
        return self._stack

    @property
    def sigplot(self):
        """Signal for plotting (without event number scaling) yoda.Scatter2D"""
        return self._sigplot

    @property
    def refplot(self):
        """unscaled reference data yoda.Scatter2D"""
        return self._refplot

    @property
    def bgplot(self):
        """unscaled reference data yoda.Scatter2D"""
        return self._bgplot

    @property
    def lumi(self):
        """Analysis luminosity stored in staticDB

        Note: This can be quoted in pb or fb depending on the hepData record for an analysis.
        Either way this enters into the scale factor applied to the points as a separate factor
        multiplied with ScaleFactorSig or ScaleFactorData"""
        return self._lumi

    @property
    def isScaled(self):
        """Bool representing if there is additional scaling applied on top of luminosity"""
        return self._isScaled

    @property
    def scaleFactorSig(self):
        """Scale factor applied to the signal histogram/scatter"""
        return self._scaleFactorSig

    @property
    def scaleFactorData(self):
        """Scale factor applied the reference"""
        return self._scaleFactorData

    @property
    def conturPoints(self):
        """List of conturPoints found in each analysis object"""
        return self._conturPoints

    @property
    def mcLumi(self):
        """Generated Monte Carlo luminosity, this is derived but used to work out
        the poisson uncertainty on the generated signal"""
        return self._stack

    @property
    def scaleMC(self):
        """Separate MC ScaleFactor"""
        return self._stack

