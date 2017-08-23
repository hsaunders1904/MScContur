import os
import yoda
import rivet
from contur import TestingFunctions as ctr
import contur.Utils as util


class histFact(object):
    """
    Take a yoda analysis object and structure a contur ready object
    This acts as a wrapper class for the underlying analysis object
    """
    def __init__(self, anaObj,xSec,nEv):
        #Construct with an input yoda aos and a scatter1D for the cross section and nEv
        self.aos = anaObj
        self.xsec= xSec
        self.nev=nEv

        #Initialize the members we always want to access
        self.background=False
        self.ref=False
        self.signal=yoda.Scatter2D
        self.lumi=1
        self.isScaled=False
        self.scaleFactorData=1
        self.scaleFactorSig=1

        #Call the internal functions to fill the above members with what we want
        self.getData()
        if self.has1D():
            self.aos=yoda.mkScatter(self.aos)
        self.getAux()
        self.getMC()
        self.getisScaled()
        self.buildStack()

    def has1D(self):
        """Check type of input aos
        """
        if self.aos.type == 'Histo1D' or self.aos.type=='Profile1D':
            if self.isScaled:
                #if the Data is scaled, work out the signal scaling from number of events and generator xs
                try:
                    self.scaleFactorSig=(float(self.aos.numEntries()) / float(self.nev.numEntries()) * float(self.xsec.x))
                except:
                    print "missing info for scalefactor calc"
            return True
        else:
            return False

    def getisScaled(self):
        """Check if the data to compare to is normalized
        """
        self.isScaled,self.scaleFactorData = ctr.isNorm(self.aos.path)


    def getData(self):
        """Looks up ref data"""
        refFiles=[]
        rivet_data_dirs = rivet.getAnalysisRefPaths()
        for dirs in rivet_data_dirs:
            import glob
            refFiles.append(glob.glob(os.path.join(dirs, '*.yoda')))
        for fileList in refFiles:
            for f in fileList:
                aos=yoda.read(f)
                for path, ao in aos.iteritems():
                    if path.startswith('/REF/'):
                        if self.aos.path in path:
                            self.ref=ao
    def getMC(self):
        """Lookup for any stored SM MC background calculation
        Currently doesn't exist so just return the refdata
        """
        try:
            self.background=self.ref
        except:
            print "no ref for histo"

    def getAux(self):
        """Sets member variables from static lookup tables
        :return:
        """
        self.lumi,self.pool,self.subpool = ctr.LumiFinder(self.aos.path)

    def buildStack(self):
        """Build the signal/background stack for plotting
        """
        if self.aos.type!="Scatter2D":
            return False
        elif not self.background:
            return False
        else:
            self.signal=self.aos.clone()
            assert self.signal.numPoints == self.background.numPoints
            for p in self.signal.points:
                p.y=p.y


class conturPoint(histFact):
    """
    Defines a contur point, an object extracted from a histogram that is then used in the conturFactory to build combinations
    """


for root, dirs, files in os.walk('.'):
    for name in files:
        fileliststatic = []
        if '.yoda' in name and 'LHC' not in name:
            yodafile = os.path.join(root, name)
            fileliststatic = str(yodafile)
            refhistos, mchistos, xsec, Nev = util.getHistos(fileliststatic)
            hpaths = []
            for aos in mchistos.values():
                for p in aos.keys():
                    if p and p not in hpaths:
                        hpaths.append(p)
            for k, v in mchistos.iteritems():
                for k2, v2 in v.iteritems():
                    histo = histFact(v2,xsec,Nev)
                    print histo.lumi
                    print histo.has1D()
                    histo.getData()
