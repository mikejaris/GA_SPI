# GA_SPI
GA Single Pixel Imaging

A home for all of the various scripts used to conduct single pixel imaging experiments

AJ_DMD.py - library of functions to control the Ajile DMD.
- Requires the ajiledriver package

Test_AJ_DMD.py - exmaple file to use the AJ_DMD to perform single pixel imaging
- I recommend installing the package "spyrit" (pip install spyrit) to utilzie the built-in Walsh-Hadamard function instead of the scipy.signals.hadamard function

MCC_DAQ.py - library of functions to pull data from the measurement computing DAQ.
- Requires the mcculw package

TVAL3_CS.m - Matlab file to call the TVAL3 function to reconstruct images from under-sampled data.
- Requires the TVAL3 library & Octave (recommended) or Matlab
TVAL3.py - Python program that calls the TVAL3_CS program 
- Requires Octave to be installed on the machine and the oct2py python package to call it

pyunlocbox_CS_example.py - An alternative, standalone compressive sensing package with a variety of CS algorithims and solvers built in.
- Requires the pyunlocbox package
