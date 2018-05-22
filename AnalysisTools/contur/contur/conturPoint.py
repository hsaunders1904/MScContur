import os
import yoda
import re
import rivet
from contur import TestingFunctions as ctr
import contur.Utils as util



class conturPoint(object):
    """ A container for counts derived from an observable.

    Currently to replicate some of the older functionality, this object is a wrapper for a list
    of counts forming a single test. This can then either be derived from a single observable or
    from a group of observables considered uncorrelated.
    The eventual design will be to reduce conturPoint to the information corresponding to a single
    observable. The combination/correlation information will then be handled by conturBucket, a meta object for
    collections of conturPoints
    """

    members = ["s", "sErr", "bg", "bgErr", "meas", "measErr", "isRatio", "kev"]
    def __init__(self):
        #self.counts = dict.fromkeys(self.members,[])
        #self.counts=defaultdict(self.members)
        self.counts={}
        for m in self.members:
            self.counts[m]=[]
        self.CLs=0.0
        self.p_b=0.0
        self.p_sb=0.0
        self._tags=''
        self._pools=''
        self._subpool=''


    def calcCLs(self, TestMethod):
        """Recalculate CLs of this conturPoint

        Currently only operates under asymptotic approximation and assumes all observables added to the point
        are uncorrelated
        """
        #check points is well formed (equal arg lengths)
        if not self.__checkConsistency():
            self.CLs=0.0
        else:
            self.CLs, self.p_sb, self.p_b = ctr.confLevel(self.s, self.bg, self.meas, self.sErr, self.bgErr, self.measErr, self.isRatio, self.kev, 1, TestMethod)

    def __checkConsistency(self):
        """Internal function to check if the point is well formed

        Errors if unequal arg length and returns False if point is empty
        """

        ref = len(self.counts[self.counts.keys()[0]])
        for k,v in self.counts.iteritems():
            if len(v) !=ref:
                raise AssertionError("Unequal lengths of arguments in conturpoint")
        if ref == 0:
            return False
        else:
            return True

    def addPoint(self,point):
        """Placeholder function to replicate functionality of combining observables

        Appends another conturPoint to this instance, errors if types don't match
        """
        if point.__class__ != conturPoint:
            raise AssertionError("Must be a conturPoint to add to conturPoint")
        for k,v in point.counts.iteritems():
            self.counts[k].extend(v)
        #self._tags.extend(point.tags)


    @property
    def s(self):
        """Signal Count
        """
        return self.counts["s"]
    @s.setter
    def s(self,value):
        """Set the Signal count

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        """
        self.counts["s"].append(value)

    @property
    def sErr(self):
        """MC error on signal

        TODO:Clarify how we treat this, currently this value actually represents the ratio of signal luminosity
        to data luminosity
        """
        return self.counts["sErr"]
    @sErr.setter
    def sErr(self, value):
        """Set the MC error on signal

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        TODO:Clarify how we treat this, currently this value actually represents the ratio of signal luminosity
        to data luminosity
        """
        self.counts["sErr"].append(value)

    @property
    def kev(self):
        """Ratio of generated MC events to expected Data events for this point

        This is needed only for estimating the MC statistical uncertainty, so should be small
        TODO: check the way it is actually used in TesterFunctions.
        """
        return self.counts["kev"]
    @kev.setter
    def kev(self,value):
        """Set the number of generted events

        """
        self.counts["kev"].append(value)


    @property
    def bg(self):
        """Background count
        """
        return self.counts["bg"]
    @bg.setter
    def bg(self, value):
        """Set the Background count

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        """
        self.counts["bg"].append(value)

    @property
    def bgErr(self):
        """Background error
        """
        return self.counts["bgErr"]
    @bgErr.setter
    def bgErr(self, value):
        """Set the Background error

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        """
        self.counts["bgErr"].append(value)

    @property
    def meas(self):
        """Observed count
        """
        return self.counts["meas"]
    @meas.setter
    def meas(self, value):
        """Set the Observed count

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        """
        self.counts["meas"].append(value)

    @property
    def measErr(self):
        """Observed count
        """
        return self.counts["measErr"]
    @measErr.setter
    def measErr(self, value):
        """Set the Observed count

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        """
        self.counts["measErr"].append(value)

    @property
    def isRatio(self):
        """is this a ratio (true) or a xsec (false)
        """
        return self.counts["isRatio"]
    @isRatio.setter
    def isRatio(self, value):
        """Set the isRatio

        Always appends a new value to the stored list, deleting/modifying values done manually
        (although should be avoided)
        """
        self.counts["isRatio"].append(value)

    @property
    def tags(self):
        """Analysis tag defining the conturPoint

        Use the Rivet analysis ID to define the origin of the observables
        """
        return self._tags
    @tags.setter
    def tags(self,value):
        """Set the analysis tag

        In contrast to the observable this is a set variable, if combinations of multiple analyses are made this
        should be updated
        """
        self._tags=value

    @property
    def pools(self):
        """Analysis Pool associated to the tags

        Analysis pool defines statistically correlated (overlapping datasets) groupings of analysis
        """
        return self._pools
    @pools.setter
    def pools(self,value):
        """Set the analysis pool

        This is automatically set when reading in a histogram, and is used for combinations
        """
        self._pools=value

    @property
    def subpools(self):
        """Analysis subpool

        An additional tag to identify subgrouping available with a pool, eventually this info
        will only be available on the conturPoint but won't be stored in a bucket
        """
        return self._subpool
    @subpools.setter
    def subpools(self,value):
        """Set the analysis subpool

        """
        self._subpool=value




    def __repr__(self):
        return repr(self.counts)
