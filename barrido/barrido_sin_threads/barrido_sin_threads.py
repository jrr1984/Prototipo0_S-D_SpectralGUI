import logging,threading,time
from logging.handlers import SocketHandler
from StageAndSpecWithReturn import StageAndSpec
import matplotlib.pyplot as plt
import numpy as np
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)
syst = StageAndSpec()
syst.connect()
initial_time = time.time()
num_avg=1
x_array_scan = np.arange(0.0,10+1,10)
y_array_scan = np.arange(0.0,10+1,10)
BE_thread = threading.Thread(target=syst.scan, args= (x_array_scan,y_array_scan,num_avg))
BE_thread.start()
log.info('Thread started')
keep_step= syst.step
intensity = []
wavelength = []
'''def storage_data():
    while thread.is_alive():
        yield syst.wavelength
        yield syst.intensity
storage_data()'''
def read(thread,q):
    t = 0
    while thread.is_set():
        q.put([syst.intensity, syst.wavelength])
        time.sleep(0.01)
    log.info('Done SAVING the data.')
BE_thread.join()
log.info('Length of wavelength: {}'.format(len(wavelength)))
elapsed_time =time.time() - initial_time
log.info('Time: {}, for num_avg: {}'.format(elapsed_time,num_avg))
syst.disconnect()
#syst.stop_program = True