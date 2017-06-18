#!/bin/bash

export CONTURMODULEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export RIVET_DATA_PATH=$RIVET_DATA_PATH:$CONTURMODULEDIR/modified_analyses/refdata
export RIVET_ANALYSIS_PATH=$RIVET_ANALYSIS_PATH:$CONTURMODULEDIR/modified_analyses/Analyses
export RIVET_PLOT_PATH=$RIVET_PLOT_PATH:$CONTURMODULEDIR/modified_analyses/plotinfo
export RIVET_INFO_PATH=$RIVET_INFO_PATH:$CONTURMODULEDIR/modified_analyses/anainfo

export PYTHONPATH=$PYTHONPATH:$CONTURMODULEDIR/AnalysisTools/contur
export PATH=${PATH}:$CONTURMODULEDIR/AnalysisTools/contur/bin
