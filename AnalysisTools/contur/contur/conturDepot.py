import os
import yoda
import re
import rivet
from contur import TestingFunctions as ctr
from conturPoint import conturPoint
from histFactory import ANALYSIS


class conturDepot(object):
    """Parent class to initialise a contur analysis, send yoda files for processing and store and categorize resul

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
                        #Remove the point if it ends up in a group
                        # Tags need to store which histo contribute to this point.
                        for y in self.conturPoints:
                             if y.subpools == k and a in y.tags:
                                 result[k].addPoint(y)  
                                 if len(result[k].tags) > 0:
                                     result[k].tags += ","
                                 result[k].tags += y.tags
                        v.calcCLs()
                        v.pools=p
                        v.tags=result[k].tags
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

