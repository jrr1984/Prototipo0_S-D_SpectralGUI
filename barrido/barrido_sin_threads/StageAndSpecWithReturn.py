import time
import logging
import numpy as np
from logging.handlers import SocketHandler
from thor_stepm import ThorlabsStageWithStepMotors
from instrumental import instrument, list_instruments
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)

class StageAndSpec():

    def __init__(self):
        self.intensity = []
        self.wavelength = []
        self.step = 0
        self.stop_program = False


    def connect(self):
        paramsets = list_instruments()
        self.ccs = instrument(paramsets[0])
        log.info('CCS200/M Spectrometer CONNECTED')
        time.sleep(0.1)
        self.stage = ThorlabsStageWithStepMotors()
        self.stage.set_stage()


    def disconnect(self):
        self.ccs.close()
        log.info('CCS200/M Spectrometer DISCONNECTED')
        self.stage.close()

    def meander_scan(self, x_array_scan, y_array_scan):

        for ndx, y in enumerate(y_array_scan):
            if ndx % 2:
                for x in reversed(x_array_scan):
                    yield x, y
            else:
                for x in x_array_scan:
                    yield x, y

    def scan(self,x_array_scan,y_array_scan,num_avg):
        for x,y in self.meander_scan(x_array_scan,y_array_scan):
            self.stage.move_to_x_y(x,y)
            self.intensity, self.wavelength = self.ccs.take_data(integration_time=None, num_avg=num_avg, use_background=False)
            log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))
            self.step += 1
            if self.stop_program:
                log.info('Stopping measurement - KeyboardInterrupt')
            break
        log.info('FINISHED SCANNING.')


    def one_direction_scan(self,x_array_scan, y_array_scan):

        for ndx, y in enumerate(y_array_scan):
            for x in x_array_scan:
                yield x, y

    def read(self,thread, q):
        while thread.is_alive():
            q.put([self.intensity, self.wavelength])
            time.sleep(0.01)
        log.info('Done SAVING the data.')





