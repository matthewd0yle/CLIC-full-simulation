#!/bin/bash
# Does a basic CLIC simulation and reconstruction.


# Checks to see if already sourced
if [ -z "$ILCSOFT" ]
then
    echo Sourcing ILCSOFT
    source /cvmfs/clicdp.cern.ch/iLCSoft/builds/2019-04-17/x86_64-slc6-gcc62-opt/init_ilcsoft.sh
fi

ddsim --steeringFile clic_steer.py --compactFile CLIC_o3_v14/CLIC_o3_v14.xml --enableGun --gun.particle mu- --gun.energy 10*GeV  --gun.distribution uniform --outputFile mySimOutputFile.slcio --numberOfEvents 100

Marlin --InitDD4hep.DD4hepXMLFile="CLIC_o3_v14/CLIC_o3_v14.xml" --global.LCIOInputFiles="mySimOutputFile.slcio"  myEditedClicReconstruction.xml
