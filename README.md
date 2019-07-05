# CLIC-full-simulation
This repo is an attempt to get the full CLIC simulation and reconstruction pipeline working. This is done with the aim of testing possible improvements to the detector design.



## Setup
The setup is largely based on the iLCSoft CLICPerformance repo, which in turn built using several other iLCSoft projects. The easiest way to set up the required software is via cvmfs. If properly setup, this can be done via the following command:

```
source /cvmfs/clicdp.cern.ch/iLCSoft/builds/2019-04-17/x86_64-slc6-gcc62-opt/init_ilcsoft.sh
```

Work was done on the 2019-04-17 build, but in principle any reasonably recent or future build should also work.



## Simulation
Simulation of the particles interacting with the detector is conducted via ddsim. An example usage is as follows:

```
ddsim \
--steeringFile $ILCSOFT/ClicPerformance/HEAD/examples/lcio_particle_gun.py \
--compactFile $ILCSOFT/lcgeo/HEAD/CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml \
--enableGun --gun.particle mu- --gun.energy 10*GeV --gun.distribution uniform \
--outputFile mySimOutputFile.slcio --numberOfEvents 100
```

Where **steeringFile** corresponds to the file that produces the initial particles, **compactFile** describes the geometry and design of the detector and the other arguments are reasonably self explanatory. The compact files come in the format **CLIC_o\<option\>_v\<version\>**.


  
  
  






