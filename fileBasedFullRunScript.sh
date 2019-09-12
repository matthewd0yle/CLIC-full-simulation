#!/bin/bash
# Does a basic CLIC simulation and reconstruction.


# Checks to see if already sourced
if [ -z "$ILCSOFT" ]
then
    echo Sourcing ILCSOFT
    source /cvmfs/clicdp.cern.ch/iLCSoft/builds/2019-04-17/x86_64-slc6-gcc62-opt/init_ilcsoft.sh
fi

ddsim --compactFile CLIC_o3_vCustom/CLIC_o3_v14.xml --inputFile whizard.001.stdhep --outputFile mySimOutputFile.slcio --numberOfEvents 10

Marlin --InitDD4hep.DD4hepXMLFile="CLIC_o3_vCustom/CLIC_o3_v14.xml" --global.LCIOInputFiles="mySimOutputFile.slcio"  myEditedClicReconstruction.xml
