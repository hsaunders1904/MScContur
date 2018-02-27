#!/usr/bin/env bash                                                             

# Execute to build all Rivet routines in this directory                         

rm -f *.so
rivet-buildplugin Rivet-ConturOverload.so --std=c++11 *.cc
