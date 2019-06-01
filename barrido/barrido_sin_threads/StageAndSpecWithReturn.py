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

    def generate_positions_list(self,dx,x_array_scan,dy,y_array_scan):
        log.info('ARRANCO EL SCAN')
        x_positions = []
        y_positions = []
        success = False
        state = 'Init'
        y = 0.0
        while success == False:
            if state == 'Init':
                for i in x_array_scan:
                    x_positions.append(i)
                    y_positions.append(y)
                y += dy
                state = 'Reversed x'
            if state == 'Reversed x':
                for i in reversed(x_array_scan):
                    x_positions.append(i)
                    y_positions.append(y)
                if y == y_array_scan[-1]:
                    success = True
                    break
                y += dy
                state = 'Forward x'
            if state == 'Forward x':
                for i in x_array_scan:
                    x_positions.append(i)
                    y_positions.append(y)
                if y == y_array_scan[-1]:
                    success = True
                y += dy
                state = 'Reversed x'
        return x_positions,y_positions

    def scan(self,dx,x_array_scan,dy,y_array_scan,num_avg):
        log.info('LISTA POR GENERAR')
        x_positions, y_positions = self.generate_positions_list(dx,x_array_scan,dy,y_array_scan)
        log.info('LISTA GENERADA')
        log.info('ANTES DEL FOR')
        intensidad = []
        long_de_onda = []
        for i, j in zip(x_positions, y_positions):
            self.stage.move_to_x_y(i,j)
            intensity,wavelength = self.ccs.take_data(integration_time=None, num_avg=num_avg, use_background=False)
            log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))
            if i == x_positions[-1]:
                log.info('FINISHED SCANNING.')
            intensidad.append(intensity)
            long_de_onda.append(wavelength)




