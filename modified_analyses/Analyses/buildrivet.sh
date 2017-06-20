#!/usr/bin/env bash                                                             

# Execute to build all Rivet routines in this directory                         

for routine in *.cc; do
    rivet-buildplugin Rivet${routine%.cc}.so --std=c++11 $routine
done