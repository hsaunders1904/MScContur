#!/usr/bin/env bash                                                             

# Execute to build all Rivet routines in this directory                         
cd $CONTURMODULEDIR/modified_analyses/Analyses
rm -f *.so
rivet-buildplugin Rivet-ConturOverload.so --std=c++11 *.cc
