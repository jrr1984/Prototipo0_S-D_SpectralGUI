# Create your own Python Script.
# Make use of the objects _gui (of type IUserInterface), _deviceMgr (of type IDeviceManager) and _script (of type IScriptEngine) 
#import clr;
#import ThorlabsSpectrum;
#from ThorlabsSpectrum import *;
#from System import *;
#import matplotlib.pyplot as plt
#%matplotlib inline
import time
from thor_stepm import ThorlabsStageWithStepMotors
from instrumental import u, Q_
from instrumental import instrument,list_instruments
from instrumental.drivers.spectrometers.thorlabs_ccs import CCS
paramsets = list_instruments()
paramsets
ccs = instrument(paramsets[0])
ccs