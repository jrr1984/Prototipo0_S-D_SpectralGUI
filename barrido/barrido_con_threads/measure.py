import logging
import sys
from logging.handlers import SocketHandler
import numpy as np
from StageAndSpecWithReturn import StageAndSpec
from pymeasure.experiment import Procedure
from pymeasure.experiment.parameters import ListParameter,IntegerParameter, FloatParameter
import time
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow

#log = logging.getLogger('Root logger')
#log.setLevel(1)  # to send all messages to cutelog
#socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
#log.addHandler(socket_handler)
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

class XYmove(Procedure, StageAndSpec):
    num_avg = IntegerParameter('Averages', default=1)
    initial_x = FloatParameter('Final x', units='micrometers', default=0)
    final_x = FloatParameter('Final x', units='micrometers', default=10)
    initial_y = FloatParameter('Final x', units='micrometers', default=0)
    final_y = FloatParameter('Final x', units='micrometers', default=10)
    dx = FloatParameter('Paso dx', units='micrometers', default=1)
    dy = FloatParameter('Paso dy', units='micrometers', default=1)
    #step = IntegerParameter('Step', default=1)
    #wavelength = ListParameter('Wavelength [nm]',units='nm')
    #intensity = ListParameter('Intensity [a.u.]', units='a.u.')

    DATA_COLUMNS = ['Wavelength [nm]','Intensity [a.u.]']

    def startup(self):
        log.info("CONNECTING to stage and spectrometer.")
        self.connect()

    def execute(self):
        x_array_scan = np.arange(self.initial_x, self.final_x, self.dx)
        y_array_scan = np.arange(self.initial_y, self.final_y, self.dy)
        x_positions,y_positions = self.generate_positions_list(self.dx,x_array_scan,self.dy,y_array_scan)
        for i,j in zip(x_positions,y_positions):
                self.stage.move_to_x_y(i, j)
                intensity, wavelength = self.ccs.take_data(integration_time=None, num_avg=self.num_avg, use_background=False)
                self.emit('results', {'Wavelength [nm]': wavelength,'Intensity [a.u.]': intensity})
                log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))
                if i == x_positions[-1] and j == y_positions[-1]:
                    log.info('FINISHED SCANNING.')
                time.sleep(0.01)
                if self.should_stop():
                    log.info("User aborted the procedure")
                    break

    def shutdown(self):
        self.disconnect()
