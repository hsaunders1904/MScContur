Prerequisites:
Require a working and sourced install of Professor,
https://professor.hepforge.org/

Make a dummy gridpack, gridpacks contail model information for actually running the event generator. Initially we don't proceed to this step so just:
mkdir GridPack
touch GridPack/Model.model

Make a dummy folder and dummy model file just to ensure we have the capability to include additional files to the generator when actually running.

A copy of prof2-sample has been made from the professor bin dir to the pwd, this is now editable so it's easier to disect what is going on.

The sample command we need to replicate is included in profcommand.sh, so:
. profcommand.sh

This makes a folder named myscan containing what we need,
Read Professor documentation etc. to figure out what this has done. We want to replicate this functionality without needing the Professor install as a first step,
The professor command should mostly be python file manipulation contained in prof2-sample, so we can extract that into a standalone python script