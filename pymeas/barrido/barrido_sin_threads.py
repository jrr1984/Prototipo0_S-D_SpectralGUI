import logging
from logging.handlers import SocketHandler
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)
from StageAndSpec import StageAndSpec
syst = StageAndSpec()
syst.connect()
import numpy as np
dx = 1
dy=1
x_array_scan = np.arange(0.0,dx*(10+1),dx)
y_array_scan = np.arange(0.0,dy*(10+1),dy)

generator = syst.scan(dx,x_array_scan,dy,y_array_scan)
next(generator)
syst.disconnect()
#np.savetxt('long_de_onda.txt', long_de_onda, delimiter=',')
#np.savetxt('intensidad.txt', intensidad, delimiter=',')
#log.info('LENGHT intensidad: {}'.format(len(intensidad)))
#log.info('LENGHT longitud de onda: {}'.format(len(long_de_onda)))