#!/usr/bin/env bash
mydir="$( dirname "${BASH_SOURCE[0]}" )"

# some cd commands issue terminal instructions, so pipe them away
export CONTURMODULEDIR="$( cd "$mydir" 2>&1 > /dev/null && echo "$PWD" )"

export RIVET_DATA_PATH=$RIVET_DATA_PATH:$CONTURMODULEDIR/modified_analyses/refdata:$CONTURMODULEDIR/modified_analyses/Theory
export RIVET_ANALYSIS_PATH=$RIVET_ANALYSIS_PATH:$CONTURMODULEDIR/modified_analyses/Analyses
export RIVET_PLOT_PATH=$RIVET_PLOT_PATH:$CONTURMODULEDIR/modified_analyses/plotinfo
export RIVET_INFO_PATH=$RIVET_INFO_PATH:$CONTURMODULEDIR/modified_analyses/anainfo

export PYTHONPATH=$PYTHONPATH:$CONTURMODULEDIR/AnalysisTools/contur
export PATH=$CONTURMODULEDIR/AnalysisTools/contur/bin:${PATH}
