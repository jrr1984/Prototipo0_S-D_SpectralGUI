import time
import logging
import numpy as np
from logging.handlers import SocketHandler
from barrido.thor_stepm import ThorlabsStageWithStepMotors
from instrumental import instrument,list_instruments
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)

class StageAndSpec():

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

    def scan(self,dx,x_array_scan,dy,y_array_scan):
        intensidad = []
        long_de_onda = []
        state = 'Init'
        success = False
        y = 0.0
        while success == False:
            log.info('ACTUAL y: {}'.format(y))
            log.info('STATE: {}'.format(state))
            if state == 'Init':
                log.info('INITIAL STATE y=0, FORWARD IN X')
                for i in x_array_scan:
                    self.stage.move_to_x_y(i, y)
                    intens,longi=self.ccs.take_data(integration_time=None, num_avg=1, use_background=False)
                    intensidad.append(intens)
                    long_de_onda.append(longi)
                    log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))

                self.stage.move_to_x_y(x_array_scan[-1], y)
                y += dy
                state = 'Reversed x'
            if state == 'Reversed x':
                log.info('STATE REVERSED X')
                for i in reversed(x_array_scan):
                    self.stage.move_to_x_y(i, y)
                    intens,longi  = self.ccs.take_data(integration_time=None, num_avg=1, use_background=False)
                    intensidad.append(intens)
                    long_de_onda.append(longi)
                    log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))
                self.stage.move_to_x_y(x_array_scan[-1], y)
                if y == y_array_scan[-1]:
                    success = True
                    log.info('FINISHED SCANNING.')
                    break
                y += dy
                state = 'Forward x'
            if state == 'Forward x':
                log.info('STATE FORWARD X')
                for i in x_array_scan:
                    self.stage.move_to_x_y(i, y)
                    intens, longi = self.ccs.take_data(integration_time=None, num_avg=1, use_background=False)
                    intensidad.append(intens)
                    long_de_onda.append(longi)
                    log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))
                self.stage.move_to_x_y(x_array_scan[-1], y)
                if y == y_array_scan[-1]:
                    success = True
                    log.info('FINISHED SCANNING.')
                y += dy
                state = 'Reversed x'
        return intensidad,long_de_onda