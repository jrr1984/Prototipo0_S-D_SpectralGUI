import time
import logging
from logging.handlers import SocketHandler
from barrido.thor_stepm import ThorlabsStageWithStepMotors
from instrumental import instrument,list_instruments

log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)
paramsets = list_instruments()
ccs = instrument(paramsets[0])
log.info('CCS200/M Spectrometer CONNECTED')
time.sleep(1)
stage = ThorlabsStageWithStepMotors()
stage.set_stage()


def disconnect():
    ccs.close()
    stage.close()

disconnect()