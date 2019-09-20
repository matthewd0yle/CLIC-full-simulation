# CLIC-full-simulation
This repo is an attempt to get the full CLIC simulation and reconstruction pipeline working. This is done with the aim of testing possible improvements to the detector design.



## Setup
The setup is largely based on the iLCSoft CLICPerformance repo, which in turn built using several other iLCSoft projects. The easiest way to set up the required software is via cvmfs. If properly setup, this can be done via the following command:

```
source /cvmfs/clicdp.cern.ch/iLCSoft/builds/2019-09-04/x86_64-slc6-gcc62-opt/init_ilcsoft.sh
```

Work was done on the 2019-09-04 build, but in principle any reasonably recent or future build should also work.



## Simulation
Simulation of the particles interacting with the detector is conducted via ddsim. An example usage is as follows:

```
ddsim \
--steeringFile $ILCSOFT/ClicPerformance/HEAD/examples/lcio_particle_gun.py \
--compactFile $ILCSOFT/lcgeo/HEAD/CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml \
--enableGun --gun.particle mu- --gun.energy 10*GeV --gun.distribution uniform \
--outputFile mySimOutputFile.slcio --numberOfEvents 100
```

Where **steeringFile** corresponds to the file that defines the parameters of the simulation, **compactFile** describes the geometry and design of the detector and the other arguments are reasonably self explanatory. The compact files come in the format **CLIC\_o**_(option)_**\_v**_(version)_. The resultant .slcio file can then be reconstructed.



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
--InitDD4hep.DD4hepXMLFile="$lcgeo_DIR/CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml" \
--global.LCIOInputFiles="mySimOutputFile.slcio" \
myEditedClicReconstruction.xml
```

This process will produce a .root file, which can then be easily analysed. It also creates full *.slcio* files of both the simulated and reconstructed particles, allowing for the possibility of more in depth analysis.



## Automation
There are three scripts designed to automate the full simulation and automation process. **myFullRunScript.sh** does a full simulation reconstruction cycle on the custom CLIC model, simulating a number of single muon gun events. **fileBasedRunScript** is similar, but instead of a muon gun it takes a *.stdhep* input file to allow the simulation of more complicated events. **condorTopRunsScript** is a file based script specifically designed for use with HTCondor.

Simulating the detection of a single top anti-top event can take several minutes. As a result, obtaining sufficient data by directly running the scripts can take an excessively long time. One way around this issue is by running several parallel simulations on DICE and then combining the resultant file. This can be done by submitting **topFullRun.job** with HTCondor, which will in turn execute **condorTopRunsScript** independently on a number of machines, transferring the necessary files. In order for the script to execute successfully, the directory TopRuns must exist and contain the following file structure:

```
TopRuns
 -run0
 -run1
 -run2
 ...
```
The output of each run will be placed in the relevant run directory. In addition to the standard output, the files *output*, *error* and *log* will be produced. *output* contains that what would usually be printed to the console, *error* contains any error messages and *log* gives information about the program's execution on DICE.

The files produced on DICE can then be merged with the **MergeTrees.ipynb** interactive Jupyter notebook or the **MergeTrees.py** python script, which is based on the former. They are written in Python 3 and require a version of ROOT compiled to work with such. They may work in Python 2, but this has not been tested.


## Analysis
Analysis is done using the **Analysis.ipynb** Jupyter notebook, which as before is written in Python 3. This notebook produces a number of plots to enable the analysis of the simulation and reconstruction process. By following the structure provided, it should be reasonably easy to produce further plots as required.




