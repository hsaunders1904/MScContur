#!/bin/sh
#
# Contur "smoke test".
#
# Runs Herwig (which must already be available) and performs a confidence-limit
# calculation for a single point in model parameter space.
#
# Uses Contur installation within which the script exists by default.
# Set $CONTURMODULEDIR to make it use a different installation.
#

# Check environment
if type Herwig >/dev/null 2>&1; then
  echo "Found Herwig, so assuming environment is OK."
else
  echo "Didn't find Herwig, so environment is not set up correctly."
  echo "This script requires Herwig, Rivet and Yoda to be configured,"
  echo "e.g. by typing this command on the UCL HEP cluster:"
  echo
  echo "source /unix/cedar/software/sl6/Herwig-7.1.0/setupEnv.sh"
  exit 1
fi

# Create output directory after checking it doesn't already exist.
if [ "$#" -ne 1 ]; then
  echo "Script needs single argument, giving output directory."
  exit 1
fi
CONTURRUNDIR=`readlink -fm "$1"`
if [ -e "$CONTURRUNDIR" ]; then
  echo "Output directory already exists: $CONTURRUNDIR"
  echo "Exiting."
  exit 1
fi
echo "Creating output directory: $CONTURRUNDIR"
mkdir -p "$CONTURRUNDIR"
LOGFILE="$CONTURRUNDIR/simple-test.log"

# Use existing $CONTURMODULEDIR if set, or default to the top-level directory of this installation.
RELDIRNAME=`dirname $0`/..
DEFAULTCONTURMODULEDIR=`readlink -fm $RELDIRNAME`
CONTURMODULEDIR=${CONTURMODULEDIR:-$DEFAULTCONTURMODULEDIR}

# Compile modified Rivet analyses
source "$CONTURMODULEDIR"/setupContur.sh
cd "$CONTURMODULEDIR"/modified_analyses/Analyses
echo "Compiling modified Rivet analyses"
rivet-buildplugin RivetMyAnalyses.so *.cc -std=c++11 >> $LOGFILE

# Update database
cd "$CONTURMODULEDIR"
echo "Updating database"
make >> $LOGFILE

# Copy scripts into run directory
echo "Copying scripts into run directory"
cd $CONTURRUNDIR
cp -r $CONTURMODULEDIR/AnalysisTools/GridSetup/* .
cd GridPack/

# Create Herwig model file from UFO (Universal FeynRules Output)
#   see: https://herwig.hepforge.org/tutorials/bsm/ufo.html
echo "Create Herwig model file from UFO"
ufo2herwig DM_vector_mediator_UFO/ >> $LOGFILE
make >> $LOGFILE

# Make Herwig steering file by prepending lines to snippet provided
echo "Making Herwig steering file"
cat <<EOF > TestRun.in
read FRModel.model
set /Herwig/FRModel/Particles/Y1:NominalMass 1000.*GeV
set /Herwig/FRModel/Particles/Xm:NominalMass 600.*GeV
EOF
cat ../HerwigCommandHad >> TestRun.in

# Read Herwig steering and generate some events
echo "Reading Herwig steering"
Herwig read TestRun.in >> $LOGFILE
echo "Generating events"
Herwig run LHC.run -N 2000 # let stdout go to console so user can see progress

# Do confidence limit calculation
#   creates directories plots/ and ANALYSIS/
echo "Doing confidence limit calculation"
CLTestSingle LHC.yoda >> $LOGFILE

# Plot data and MC
#   makes directory contur-plots/ containing index.html and subdirectories with
#   .dat, .png and .pdf files for each analysis:
echo "Making plots"
contur-mkhtml LHC.yoda >> $LOGFILE 2>&1

# Final report
CONTURPLOTDIR=$CONTURRUNDIR/GridPack/contur-plots
echo
echo "Test complete"
echo "Plots are in directory $CONTURPLOTDIR"
echo "Detailed logs are in $LOGFILE"
