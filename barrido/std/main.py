import logging,threading,time
from logging.handlers import SocketHandler
from std.StageAndSpec import System
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)
import numpy as np
import time, threading
initial_time=time.time()
syst = System()
syst.connect()
num_avg=5
<<<<<<< HEAD
dx = 500.0 #en micrones, luego son pasados a mm
dy = 500.0
x_array_scan = np.arange(0.0,dx*(25+1),dx)
y_array_scan = np.arange(0.0,dy*(25+1),dy)
=======
dx = 1.0
dy=1.0
x_array_scan = np.arange(0.0,dx*(5+1),dx)
y_array_scan = np.arange(0.0,dy*(5+1),dy)
>>>>>>> 1e383a0fc81b85c7118b87981badb0bf45d62af9
BE_thread = threading.Thread(target=syst.scan_meander, args=(x_array_scan,y_array_scan,num_avg))
BE_thread.start()
storage_thread = threading.Thread(target = syst.storage_thread, args=(BE_thread,))
storage_thread.start()
BE_thread.join()
BE_total_time = time.time() - initial_time
log.info('MEASUREMENT Thread done, it took: {}.'.format(BE_total_time))
storage_thread.join()
<<<<<<< HEAD
storage_total_time = time.time() - initial_time
log.info('STORAGE Thread done, it took: {}.'.format(storage_total_time))
=======
storage_total_time = time.time() - BE_total_time
log.info('STORAGE Thread done, it took: {} + {}.'.format(BE_total_time,storage_total_time))
>>>>>>> 1e383a0fc81b85c7118b87981badb0bf45d62af9
syst.disconnect()
elapsed_time = time.time() - initial_time
log.info('TOTAL TIME: {}'.format(elapsed_time))
