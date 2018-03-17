import os
import yoda
import re
import rivet
from contur import TestingFunctions as ctr
import contur.Utils as util
from conturPoint import conturPoint

ANALYSIS = re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)')
REFLOAD = False
refObj = {}


def init_ref():
    """Function to load all reference *.yoda data"""
    refFiles = []
    # refObj = {}
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
                    # TODO provide this information in the first place!
                    refObj[path] = ao
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

    def __init__(self, anaObj, xSec, nEv):
        # Construct with an input yoda aos and a scatter1D for the cross section and nEv
        self.signal = anaObj
        self.xsec = xSec
        self.nev = nEv

        # Initialize the public members we always want to access
        self._background = False
        self._ref = False
        self._stack = yoda.Scatter2D
        self._lumi = 1
        self._isScaled = False
        self._scaleFactorData = 1
        self._scaleFactorSig = 1
        self._conturPoints = []
        self._mcLumi = 0.0
        self._scaleMC = 1.0
        self._maxcl = -1
        self._maxbin = -1

        # Call the internal functions on initialization
        # to fill the above members with what we want, these should all be private
        self.__getData()
        self.__getAux()
        self.__getMC()
        self.__getisScaled()
        if self.__has1D():
            self.signal = yoda.mkScatter(self.signal)
        if self._ref:
            self.__doScale()
            self.__fillPoints()
        # build stack for plotting
        self.__buildStack()


    def __has1D(self):
        """Check type of input aos
        """
        if self.signal.type == 'Histo1D' or self.signal.type == 'Profile1D':
            if self.signal.sumW() == 0.0:
                self._mcLumi = 0.0
            else:
                self._mcLumi = float(self.signal.numEntries()) / float(self.signal.sumW())
            if self._isScaled:
                # if the Data is scaled, work out the signal scaling from number of events and generator xs
                try:
                    self._scaleFactorSig = (
                        float(self.signal.numEntries()) / float(self.nev.numEntries()) * float(self.xsec.points[0].x))

                except:
                    print "missing info for scalefactor calc"
            return True
        else:
            return False

    def __getisScaled(self):
        """Check if the data to compare to is normalized
        """
        self._isScaled, self._scaleFactorData, self._scaleMC = ctr.isNorm(self.signal.path)

    def __getData(self):
        """Looks up ref data"""
        if not REFLOAD:
            init_ref()
        for path, ao in refObj.iteritems():
            if self.signal.path in path:
                self._ref = ao

    def __getMC(self):
        """Lookup for any stored SM MC background calculation
        Currently doesn't exist so just return the refdata
        """
        try:
            self._background = self._ref.clone()
        except:
            print "No reference data found for histo: " + self.signal.path

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
                self._stack.points[i].y = self._stack.points[i].y + self._background.points[i].y

    def __doScale(self):
        """Perform the normalisation of the signal, reference and background data

        Scales signal
        """
        if self.signal.type != "Scatter2D":
            return False
        # for sig,ref,bg in zip(..,..,..):
        for i in range(0, len(self.signal.points)):
            self.signal.points[i].y = self.signal.points[i].y * self._lumi * self._scaleFactorSig * (
                self.signal.points[i].xMax - self.signal.points[i].xMin)
            self.signal.points[i].yErrs = (
                self.signal.points[i].yErrs[0] * self._lumi * self._scaleFactorSig * (
                    self.signal.points[i].xMax - self.signal.points[i].xMin),
                self.signal.points[i].yErrs[1] * self._lumi * self._scaleFactorSig * (
                    self.signal.points[i].xMax - self.signal.points[i].xMin)
            )
        for i in range(0, len(self._ref.points)):
            self._ref.points[i].y = self._ref.points[i].y * self._lumi * self._scaleFactorData * (
                self._ref.points[i].xMax - self._ref.points[i].xMin)
            self._ref.points[i].yErrs = (
                self._ref.points[i].yErrs[0] * self._lumi * self._scaleFactorData * (
                    self._ref.points[i].xMax - self._ref.points[i].xMin),
                self._ref.points[i].yErrs[1] * self._lumi * self._scaleFactorData * (
                    self._ref.points[i].xMax - self._ref.points[i].xMin)
            )
        for i in range(0, len(self._background.points)):
            # background should have a separate scalefactor later
            self._background.points[i].y = self._background.points[i].y * self._lumi * self._scaleFactorData * (
                self._background.points[i].xMax - self._background.points[i].xMin)
            self._background.points[i].yErrs = (
                self._background.points[i].yErrs[0] * self._lumi * self._scaleFactorData * (
                    self._background.points[i].xMax - self._background.points[i].xMin),
                self._background.points[i].yErrs[1] * self._lumi * self._scaleFactorData * (
                    self._background.points[i].xMax - self._background.points[i].xMin)
            )

    def __fillPoints(self):
        """Internal function to fill conturPoints list

        Fills the conturPoints attribute with all calculable conturPoints, requires reference data present and __doScale
        to have successfully run
        """
        if self.signal.type != "Scatter2D":
            return False
        # counter to track the maximum discrepant point
        clmax = 0.0
        for i in range(0, len(self.signal.points)):
            # need this as empty s is returning CL=1, this should be fixed in the limit setting functions
            if self.signal.points[i].y == 0.0:
                continue
            ctrPt = conturPoint()
            ctrPt.s = self.signal.points[i].y
            ctrPt.bg = self._background.points[i].y
            ctrPt.bgErr = self._background.points[i].yErrs[1]
            ctrPt.nObs = self._ref.points[i].y
            # TODO check how we work mcLumi out
            ctrPt.sErr = self._mcLumi
            ctrPt.calcCLs()

                
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
        """Stacked Signal+background yoda.Scatter2D"""
        return self._stack

    @property
    def lumi(self):
        """Analysis luminosity stored in staticDB

        Note: This can be quoted in pb or fb depending on the hepData record for an analysis.
        Either way this enters into the scale factor applied to the points as a separate factor
        multiplied with ScaleFactorSig/ScaleFactorData"""
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

