import visa
import numpy as np
import time, csv
from instrumental import instrument,list_instruments,u, Q_
from instrumental.drivers.spectrometers.thorlabs_ccs import CCS
paramsets = list_instruments()
ccs = instrument(paramsets[0])

initial_time = time.time()
inten, wavel = ccs.take_data(integration_time=None, num_avg=5, use_background=False)

np.savetxt('out.csv',wavel,delimiter=',')

elapsed_time = time.time() - initial_time
print(elapsed_time)
ccs.close()