import logging
from logging.handlers import SocketHandler
from pymeasure.experiment import Results, Worker
from pymeasure.display import Plotter
from measure import XYmove
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)


procedure = XYmove()
procedure.num_avg = 5
procedure.initial_x = 0
procedure.final_x = 11
procedure.initial_y = 0
procedure.final_y = 11
procedure.dx = 1
procedure.dy = 1


data_filename = 'example.txt'
log.info("Constructing the Results with a data file: %s" % data_filename)
results = Results(procedure, data_filename)

'''log.info("Constructing the Plotter")
plotter = Plotter(results)
plotter.start()
log.info("Started the Plotter")'''

log.info("Constructing the Worker")
worker = Worker(results)
worker.start()
log.info("Started the Worker")

log.info("Joining with the worker in at most 1 hr")
worker.join(timeout=3600) # wait at most 1 hr (3600 sec)
log.info("Worker did his job, now pay him!")