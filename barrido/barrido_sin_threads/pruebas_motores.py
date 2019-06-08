from thor_stepm import ThorlabsStageWithStepMotors
import numpy as np
from instrumental import instrument,list_instruments,u, Q_
from instrumental.drivers.spectrometers.thorlabs_ccs import CCS
import time

syst = ThorlabsStageWithStepMotors()
syst.set_stage()
#time.sleep(0.5)
syst.get_motor_travel_limits()
#paramsets = list_instruments()
#ccs = instrument(paramsets[0])


'''import numpy as np
def meander_scan(x_array_scan, y_array_scan):
    for ndx, y in enumerate(y_array_scan):
        if ndx % 2:
            for x in reversed(x_array_scan):
                yield x, y
        else:
            for x in x_array_scan:
                yield x, y

x_array = np.arange(0.0,3.0,1.0)
y_array = np.arange(0.0,3.0,1.0)
for x,y in meander_scan(x_array,y_array):
    print(x,y)
    #syst.move_to_x_y(x,y)
    #a,b =ccs.take_data(integration_time=None, num_avg=5, use_background=False)
'''
syst.close()
#ccs.close()