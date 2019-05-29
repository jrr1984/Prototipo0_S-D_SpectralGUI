import matplotlib.pyplot as plt
import threading
import visa
import time
rm = visa.ResourceManager()
rm.list_resources()
from instrumental import instrument,list_instruments,u, Q_
from instrumental.drivers.spectrometers.thorlabs_ccs import CCS
paramsets = list_instruments()
ccs = instrument(paramsets[0])

num_avg = 10
integration_time = '0.01 seconds'
ccs.set_integration_time(integration_time)
integration_time = Q_(integration_time)
wait_time = integration_time/100

start_time =time.time()
for i in range(num_avg):
            time.sleep(integration_time.to('s').magnitude)
            ccs.start_single_scan()
            while not ccs.is_data_ready():
                time.sleep(wait_time.to('s').magnitude)
            temp = ccs.get_scan_data()
            if i == 0:
                data = temp
            else:
                data = data + temp
            if sum(temp >= (1.0 - 1e-5)):
                raise Warning('Raw data is saturated')
y = data / num_avg
x = ccs._wavelength_array
end_time = time.time() -start_time
print(end_time)
plt.plot(x,y)
plt.show()
'''
for i in range(1):
    init = time.time()
    y,x = ccs.take_data(integration_time='0.01 seconds', num_avg=5, use_background=False,
                  max_attempts=10)
    final= time.time() - init
    print(final)
    plt.plot(x,y)
    plt.show()'''
'''init = time.time()
y,x = ccs.take_data(integration_time='0.01 seconds', num_avg=1, use_background=False,
              max_attempts=10)
final= time.time() - init
print(final)
plt.plot(x,y)
plt.show()'''