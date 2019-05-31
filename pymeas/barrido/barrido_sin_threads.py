import logging
from logging.handlers import SocketHandler
from StageAndSpecWithReturn import StageAndSpec
import numpy as np

log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)

syst = StageAndSpec()
syst.connect()
import time

initial_time = time.time()
num_avg=5
dx = 1
dy=1
x_array_scan = np.arange(0.0,dx*(10+1),dx)
y_array_scan = np.arange(0.0,dy*(10+1),dy)
log.info('ANTES DEL SCAN')
#x,y = syst.generate_positions_list(dx,x_array_scan,dy,y_array_scan)
#print(len(x))
syst.scan(dx,x_array_scan,dy,y_array_scan,num_avg=num_avg)
log.info('post SCAN')
elapsed_time =time.time() - initial_time
log.info('Time: {}, for num_avg: {}'.format(elapsed_time,num_avg))
#next(generator)
syst.disconnect()
#np.savetxt('long_de_onda.txt', long_de_onda, delimiter=',')
#np.savetxt('intensidad.txt', intensidad, delimiter=',')
#log.info('LENGHT intensidad: {}'.format(len(intensidad)))
#log.info('LENGHT longitud de onda: {}'.format(len(long_de_onda)))