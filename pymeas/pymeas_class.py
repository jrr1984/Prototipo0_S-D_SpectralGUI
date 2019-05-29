import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
import numpy as np
from thor_stepm import ThorlabsStageWithStepMotors
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
from pymeasure.experiment import Procedure
from pymeasure.experiment import IntegerParameter, FloatParameter
import time


class XYmove(Procedure, ThorlabsStageWithStepMotors):
    #data_points = IntegerParameter('Data points', default=10)
    averages = IntegerParameter('Averages', default=10)
    step = FloatParameter('Step', units='mm',default=0.1)
    final_x = FloatParameter('Final x', units='mm', default=1.0)
    init_x = FloatParameter('Initial x', units='mm', default=0.0)

    DATA_COLUMNS = ['dx', 'Success']

    def startup(self):
        log.info("Connecting and configuring the stage of step motors")
        self.set_stage()

    def execute(self):
        x_move = np.arange(self.init_x,self.final_x,self.step)

        # Loop through each current point, measure and record the voltage
        for dx in x_move:
            log.info("Setting the position to %g mm" % dx)
            self.move_to_x_y(dx, 0.0)
            success = False
            while (self.get_x_y_position() <= (dx - 0.05, 0.0)):
                time.sleep(0.1)
            success = True
            self.emit('results', {'dx': dx,'Success': success})
            time.sleep(0.01)
            if self.should_stop():
                log.info("User aborted the procedure")
                break

    def shutdown(self):
        self.disconnect_stage()
        log.info("Finished measuring")


