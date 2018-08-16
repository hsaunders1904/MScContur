# AnalysisTools

This directory contains the run area and the main Contur code.

## GridSetup
This is the run area. Copy this directory to a new location and set up your
model to begin a run. It is not advised to run anything inside this directory
if you haven't copied it elsewhere; unless you're happy cleaning up the grid
pack.

## contur
Inside the 'contur' directory is the main contur code. The 'bin' directory
contains the package's executables; this will be added to your system path when
../setupContur.sh. Inside the 'contur' directory are the main utilities and
functions imported by the executables.

## Tests
To run contur's tests cd into 'contur' and run:

`$ pytest`
