#!/usr/bin/bash

##edit this to location of svn repo on your system
export CONTURDIR=/unix/atlas4/yallup/contur

export RIVET_DATA_PATH=$CONTURDIR/modified_analyses/refdata
export RIVET_ANALYSIS_PATH=$CONTURDIR/modified_analyses/Analyses

export PYTHONPATH=${PYTHONPATH}:$CONTURDIR/AnalysisTools/contour
export PATH=${PATH}:$CONTURDIR/AnalysisTools/contour/bin/
