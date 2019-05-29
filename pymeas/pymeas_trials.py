import logging
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
#import matplotlib.pyplot as plt
#import time
from time import sleep
#import numpy as np
#from thor_stepm import ThorlabsStageWithStepMotors
from pymeasure.log import console_log
from pymeasure.experiment import Results, Worker
#from pymeasure.experiment import IntegerParameter,FloatParameter
#from instrumental import instrument,list_instruments,u, Q_
#from instrumental.drivers.spectrometers.thorlabs_ccs import CCS
from pymeas_class import XYmove
#paramsets = list_instruments()
#print(paramsets)
#ccs = instrument(paramsets[0])
#print(ccs)
#stage = ThorlabsStageWithStepMotors()
#stage.set_stage()

if __name__ == "__main__":
    console_log(log)
    log.info("Constructing an x scan")
    procedure = XYmove()
    log.info("Starting up the stage")
    procedure.startup()
    averages = 5
    step = 0.1
    final_x = 1.0
    initial_x = 0.0
    sleep(0.1)

    data_filename = 'example.csv'
    log.info("Constructing the Results with a data file: %s" % data_filename)
    results = Results(procedure, data_filename)

    log.info("Constructing the Worker")
    worker = Worker(results)
    worker.start()
    log.info("Started the Worker")

    log.info("Joining with the worker in at most 1 hr")
    worker.join(timeout=3600)  # wait at most 1 hr (3600 sec)
    log.info("Finished the measurement")
