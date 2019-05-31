import logging
from logging.handlers import SocketHandler
import numpy as np
from StageAndSpecWithReturn import StageAndSpec
from pymeasure.experiment import Procedure, Results, Worker
from pymeasure.experiment import IntegerParameter, FloatParameter
import time

log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)


class XYmove(Procedure, StageAndSpec):
    num_avg = IntegerParameter('Averages', default=1)
    initial_x = FloatParameter('Final x', units='micrometers', default=0)
    final_x = FloatParameter('Final x', units='micrometers', default=10)
    initial_y = FloatParameter('Final x', units='micrometers', default=0)
    final_y = FloatParameter('Final x', units='micrometers', default=10)
    dx = FloatParameter('Paso dx', units='micrometers', default=1)
    dy = FloatParameter('Paso dy', units='micrometers', default=1)

    DATA_COLUMNS = ['Intensidad', 'longitud de onda']

    def startup(self):
        log.info("CONNECTING to stage and spectrometer.")
        self.connect()

    def execute(self):
        x_array_scan = np.arange(self.initial_x, self.final_x, self.dx)
        y_array_scan = np.arange(self.initial_y, self.final_y, self.dy)
        x_positions,y_positions = self.generate_positions_list(self.dx,x_array_scan,self.dy,y_array_scan)

        # Loop through each current point, measure and record the voltage
        for i,j in zip(x_positions,y_positions):
                self.stage.move_to_x_y(i, j)
                intensity, wavelength = self.ccs.take_data(integration_time=None, num_avg=self.num_avg, use_background=False)
                log.info('Spectra measured in {}'.format(self.stage.get_x_y_position()))
                if i == x_positions[-1] and j == y_positions[-1]:
                    log.info('FINISHED SCANNING.')

                self.emit('results', {'Intensidad': intensity,'longitud de onda': wavelength})
                time.sleep(0.01)
                if self.should_stop():
                    log.info("User aborted the procedure")
                    break

    def shutdown(self):
        self.disconnect()


procedure = XYmove()
procedure.num_avg = 5
procedure.initial_x = 0
procedure.final_x = 11
procedure.initial_y = 0
procedure.final_y = 11
procedure.dx = 1
procedure.dy = 1

data_filename = 'example.csv'
log.info("Constructing the Results with a data file: %s" % data_filename)
results = Results(procedure, data_filename)

log.info("Constructing the Worker")
worker = Worker(results)
worker.start()
log.info("Started the Worker")

log.info("Joining with the worker in at most 1 hr")
worker.join(timeout=3600) # wait at most 1 hr (3600 sec)
log.info("Worker did his job, now pay him!")