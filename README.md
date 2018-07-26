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
    
#### Set Up Environment
- Set up environments; mostly adding relevant folders to the system path such
  that you can execute the contur and Herwig commands from anywhere.
  
    `$ source /unix/cedar/software/sl6/Herwig-Tip/setupEnv.sh`
    
    `$ source contur/setupContur.sh`

- You need to do this every time you login.

#### Build Analyses Databases
- Build modified analyses

    `$ cd contur/modified_analyses/Analyses/`
    
    `$ chmod +x buildrivet.sh` <sub><sup>(give buildrivet.sh executable 
    permissions.)</sup></sub>
    
    `$ ./buildrivet.sh`
    
- Build database of static analysis information

    `$ cd contur` <sup><sub>Top level of repository</sub></sup>
    
    `$ make`

- You need only do this once.

#### Create Run Area     
- Create a run area seperate from the repository and copy over GridSetup
  area. This run area is where you will run everything from now on.
  
    `$ cd ~`
    
    `$ mkdir run-area`
    
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

- Build the model. Choose one of the example Herwig '.in' files and copy to
  the GridPack directory.
  
    `$ cd GridSetup/GridPack/`
    
    `$ cp DM_vector_mediator_HF_UFO/hf-1000-600-7_WEAK.in TestRun.in`
    
    `$ ufo2herwig DM_vector_mediator_HF_UFO`
    
    `$ make`
    
#### Run a Single Single Set of Analyses
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

    `$ cd GridSetup`
    
- Define a parameter space in 'param_file.dat'. This should be a space 
  seperated file formatted as:
  
    `[parameter] [minimum value] [maximum value]`
  
  You should check that the parameters defined are also defined at the top of 
  the LHC.in file within the same directory.
  
  The example model has parameters 'Xm', 'Y1', 'gYq', 'gYXm' defined in 
  'params_file.dat' and the LHC.in file has, at the top of the file:
      
      read FRModel.model
      set /Herwig/FRModel/Particles/Y1:NominalMass {Y1}
      set /Herwig/FRModel/Particles/Xm:NominalMass {Xm}
      set /Herwig/FRModel/FRModel:gYXm {gYXm}
      set /Herwig/FRModel/FRModel:gYq {gYq}

  If you wanted to add or remove parameters you must do this in both files.
  
- Run a scan over the parameter space defined in 'param_file.dat' and submit it
  to the batch farm. There are currently two sampling modes, uniform and
  random. Have a look at the command line options before running.
  
     `$ python batch_submit_prof.py --help`
     
     `$ python batch_submit_prof.py 20 -m random -N 500 --seed 101`
     
- This will produce a directory called 'myscan' containing 20 runpoint 
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
  
    `$ cd run-area/`
    
    `$ contur -g GridSetup/` 

- Plot a heatmap.

    `$ cd ANALYSIS/`
    
    `$ contur-plot --help`
    
    `$ contur-plot xxxx.map Xm Y1 gYq -g 200 -s 100 -t "My First Heatmap"`
    
    
## Authors
Jonathan Butterworth, David Grellscheid, Michael Krämer, Björn Sarrazin, 
David Yallup, with others contributing to specific studies and credited on 
those pages.
