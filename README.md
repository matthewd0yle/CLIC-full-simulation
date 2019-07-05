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

Where **steeringFile** corresponds to the file that produces the initial particles, **compactFile** describes the geometry and design of the detector and the other arguments are reasonably self explanatory. The compact files come in the format **CLIC\_o**_(option)_**\_v**_(version)_. The resultant .slcio file can then be reconstructed.



## Reconstruction
Reconstruction is done via Marlin and a corresponding XML steering file. Marlin steering files follow the general structure:

```XML
...
  <execute>
    <processor name="MyProcessor1"/>
    <processor name="MyProcessor2"/>
    </execute>

  <global>
    <parameter name="MyParameter1" value="1" />
    <parameter name="MyParameter2" value="2" />
  </global>
  
  <processor name="MyProcessor1" type="MyProcessorType1">
    <parameter name="MyProcessor1ParameterX" type="float" value="0.5"/>
  </processor>
  
  <processor name="MyProcessor2" type="MyProcessorType2">
    <parameter name="MyProcessor2ParameterY" type="bool" value="false"/>
  </processor>

...
```
The file can then be executed using the Marlin command as follows:
```
Marlin myEditedClicReconstruction.xml
```
Values within the steering file can overridden from the terminal by adding the argument in the format **--**_(processor)_**.**_(parameter)_.
For example:

```
Marlin \
--InitDD4hep.DD4hepXMLFile="$lcgeo_DIR/CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml"  \
--global.LCIOInputFiles="mySimOutputFile.slcio"\
myEditedClicReconstruction.xml
```

This process will produce a .root file, which can then be analysed.

## Analysis
#### **TO DO**




