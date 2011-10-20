#!/bin/bash
# Work out which directory the script is stored in
DIR="$( cd -P "$( dirname "$0" )" && pwd )"
# Tell python where to find the extra modules I've included
#export PYTHONPATH=$DIR/lib/python
# Change to my directory, in case we were being run from somewhere else
cd $DIR
# Run the project
cd spellorama
python project.py

