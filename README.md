# Contur

Contur is a procedure and toolkit designed to set limits on theories Beyond the
Standard Model using measurements at particle colliders. The original procedure
is defined in a
[white paper](https://link.springer.com/article/10.1007%2FJHEP03%282017%29078)
, which should be used as a reference for this method.

Contur produces a combined limit derived from comparisons between theoretical
simulations and data at the particle-level. That is, the theory simulates a
fully-exclusive final state, and the data have been corrected for detector
effects.

Contur exploits the fact that particle-level differential measurements made in
fiducial regions of phase-space have a high degree of model-independence.
These measurements can therefore be compared to BSM physics implemented in
Monte Carlo generators in a very generic way, allowing a wider array of final
states to be considered than is typically the case. The Contur approach should
be seen as complementary to the discovery potential of direct searches, being
designed to eliminate inconsistent BSM proposals in a context where many (but
perhaps not all) measurements are consistent with the Standard Model. The
Contur method is highly scaleable to other models and future measurements and
we intend to reflect these developments in these pages.

More information can be found at
[https://contur.hepforge.org/](https://contur.hepforge.org/).

## Running Contur

To run contur locally you will need to install [Herwig](https://herwig.hepforge.org/),
[Rivet](https://rivet.hepforge.org/) and [Yoda](https://yoda.hepforge.org/).
These can all be installed together using the Herwig bootstrap you can download
[here](https://herwig.hepforge.org/downloads.html). You will then need to
change the *setupContur.sh* script to point to the correct directories.

You will also need a Python 2.7 environment.

If you are running on the cluster (recommended) all this is already set up for
you.

#### Sign on to PC
- Log on to plus1 and then on to a pc. You need the '-X' to do plotting.

    `$ ssh -X username@plus1.hep.ucl.ac.uk`

    `$ ssh -X pcXXX`

#### Check Out Repository
- Check out code from repository.

    `$ hg clone https://bitbucket.org/heprivet/contur/`
    
  or

    `$ git clone https://github.com/hsaunders1904/MScContur`


#### Set Up Environment
- Set up environments; mostly adding relevant folders to the system path such
  that you can execute the contur commands from anywhere.
  
    `$ source contur/setupContur.sh`

- You need to do this every time you login.

- You also need to make sure the 'herwigSetup.sh' file contains the path to the
  Herwig setup script (on the UCL cluster this should be
  /unix/cedar/software/sl6/Herwig-Tip/setupEnv.sh), then source this.
  
    `$ source herwigSetup.sh`

#### Build Analyses Databases
- Build modified analyses

    `$ cd contur/modified_analyses/Analyses/`

    `$ source buildrivet.sh`

- Build database of static analysis information

    `$ cd contur`

    `$ make`

- You need only do this once.

#### Create Run Area     
- Create a run area seperate from the repository and copy over GridSetup
  area. This run area is where you will run everything from now on.

    `$ cd ~`

    `$ cp -r contur/AnalysisTools/GridSetup/ run-area/`

#### Choose a Model
- Choose a model. The standard run area contains two simplified dark matter
  models installed as default.

    > DM_vector_mediator_UFO is the model used in the first contur paper.

    > DM_vector_mediator_HF_UFO is the same model but with Z' coupling to all
generations of quark.

  The following instructions are specific to running Herwig with one of these
  models, a recommended first step. If you are running a different model or
  generator, you'll have to modify your actions here; for a single run, once
  you have the yoda file from rivet, the procedure should be the same again.

  For convenience, we have two ways of running, specific to the simple DM model
  but can be modified.
  Example Herwig .in files are provided in the model directories; see the

    > First Way: (see for example .in files with HAD in the name) runs
    inclusive generation of BSM particles.

    > Second Way: (see for example .in files with WEAK in the name) forces
     associated production modes of weak bosons, and leptonic decays of those
     bosons.

- Build the UFO model using Herwig's 'ufo2herwig' command.

    `$ cd run-area/GridPack/`
    
    `$ ufo2herwig DM_vector_mediator_HF_UFO/`
    
    `$ make`

#### Run a Single Single Set of Analyses
- Copy one of the .in files from inside the model to the top level of the
  grid pack.
  
    `$ cp DM_vector_mediator_HF_UFO/hf-1000-600-7_HAD.in TestRun.in`
    
- Build the Herwig run card (LHC.run).

    `$ Herwig read TestRun.in`

- Run the Herwig run card, specifying the number of events to generate. This
  can take a while so, as a first test, running around 200 events is fine.

    `$ Herwig run LHC.run -N 200`

- This will produce the file LHC.yoda containing the results of the Herwig run.
  Analyse this with contur. You can also specify which statistical test to use
  with the -t flag, e.g. '-t CS' for chi-squared test. (Run 'contur --help' to
  see more options).

    `$ contur LHC.yoda -t CS`

- The contur script will output a plots folder and an ANALYSIS folder and
  print some other information.

- Generate 'contur-plots' directory containing histograms and an index.html
  file to view them all. Whilst still in the GridPack directory, run:

    `$ contur-mkhtml LHC.yoda`

#### Run a Batch Job to Generate Heatmaps
- Go to base directory of copied over run area.

    `$ cd run-area`

- Define a parameter space in 'param_file.dat'. This should be a space
  seperated file formatted as:

    `[parameter] [minimum value] [maximum value]`

  You should check that the parameters defined are also defined at the top of
  the LHC.in file within the same directory.

  The example model has parameters 'Xm', 'Y1', 'gYq', defined in
  'params_file.dat' and the LHC.in file has, at the top of the file:

      read FRModel.model
      set /Herwig/FRModel/Particles/Y1:NominalMass {Y1}
      set /Herwig/FRModel/Particles/Xm:NominalMass {Xm}
      set /Herwig/FRModel/FRModel:gYXm {gYXm}

  If you wanted to add or remove parameters you must do this in both files.
  
- You can check that your model is built correctly and necessary files are
  present to by executing 'pytest' in the run-area directory.
  
    `$ pytest`
  

- Run a scan over the parameter space defined in 'param_file.dat' and submit it
  to the batch farm. There are currently two sampling modes, uniform and
  random. Have a look at the command line options before running.

     `$ batch-submit --help`

     `$ batch-submit 27 -N 1000 --seed 101`

- This will produce a directory called 'myscan00' containing 27 runpoint
  directories and file 'sampled_points.txt' that specifies the parameter
  values used at each run point.

- Within each run point directory there will be a 'runpoint_xxxx.sh' script.
  This is what is submitted to the batch farm. You need to wait for the farm
  to finish the job before continuing. You can check the progress using the
  'qstat' command.

- When the batch job is complete there should, in every run point directory, be
  files 'LHC-runpoint_xxx-1.yoda' and 'LHC-runpoint_xxxx-2.yoda'.

- Analyse results with contur. Resulting .map file will be outputted to
  ANALYSIS folder.

    `$ contur -g msycan00/`

- Plot a heatmap.

    `$ cd ANALYSIS/`

    `$ contur-plot --help`

    `$ contur-plot xxxx.map Xm Y1 gYq -s 100 -t "My First Heatmap"`

#### Re-scanning

- To scan new points based on a previous scan's results use batch submit again
  but specify the previous run's .map file.
    $ batch-submit 20 -r ANALYSIS/myscan00.map

- This will generate directory 'myscan01'; when the batch is complete you can
  run Contur's analysis on this directory
  
    `$ contur -g myscan01/`

- This will ouptut 'myscan01.map' inside the ANALYSIS directory. You can then
  merge the two map files and plot the joint results.
  
    `$ cd ANALYSIS/`
    
    `$ merge-map myscan00.map myscan01.map -o merged.map`
    
    `$ contur-plot Xm Y1 gYq -s 100 -t "My First Merged Heatmap"`


#### Running Tests

- You can run tests on some of Contur's code using pytest.

    `$ cd contur/AnalysisTools/contur/`
    
    `$ pytest`

- Currently this runs tests on the code responsible for the batch submitting
  process.

## Authors
Jonathan Butterworth, David Grellscheid, Michael Krämer, Björn Sarrazin,
David Yallup, Harry Saunders, with others contributing to specific studies and 
credited on those pages.
