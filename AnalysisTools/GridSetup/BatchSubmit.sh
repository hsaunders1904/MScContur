#!/bin/bash

source ~/Documents/Herwig/bin/activate
source ~/Documents/CONTUR/setupContur.sh

exec python BatchSubmit.py "$@"
