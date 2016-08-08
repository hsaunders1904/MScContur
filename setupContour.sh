#!/bin/bash

export CONTURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export RIVET_DATA_PATH=$CONTURDIR/modified_analyses/refdata
export RIVET_ANALYSIS_PATH=$CONTURDIR/modified_analyses/Analyses
export RIVET_PLOT_PATH=$CONTURDIR/modified_analyses/plotinfo
export RIVET_REF_PATH=$CONTURDIR/modified_analyses/anainfo

export PYTHONPATH=${PYTHONPATH}:$CONTURDIR/AnalysisTools/contour
export PATH=${PATH}:$CONTURDIR/AnalysisTools/contour/bin/
