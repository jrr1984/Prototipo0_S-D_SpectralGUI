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
num_avg=1
dx = 1.0
dy=1.0
x_array_scan = np.arange(0.0,dx*(10+1),dx)
y_array_scan = np.arange(0.0,dy*(10+1),dy)
BE_thread = threading.Thread(target=syst.scan_meander, args=(x_array_scan,y_array_scan,num_avg))
BE_thread.start()
storage_thread = threading.Thread(target = syst.storage_thread, args=(BE_thread,))
storage_thread.start()
BE_thread.join()
storage_thread.join()
syst.disconnect()
elapsed_time = time.time() - initial_time
log.info('TOTAL TIME: {}'.format(elapsed_time))
