#!/bin/bash

##edit this to location of svn repo on your system
export CONTURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export RIVET_DATA_PATH=$CONTURDIR/modified_analyses/refdata
export RIVET_ANALYSIS_PATH=$CONTURDIR/modified_analyses/Analyses

export PYTHONPATH=${PYTHONPATH}:$CONTURDIR/AnalysisTools/contour
export PATH=${PATH}:$CONTURDIR/AnalysisTools/contour/bin/
