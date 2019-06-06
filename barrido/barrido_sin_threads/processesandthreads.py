import logging,threading,time
from logging.handlers import SocketHandler
from StageAndSpecWithReturn import StageAndSpec

log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
import sched, time, threading

# This function is responsible for displaying the data
# it is run in its own process to liberate main process
def display(name,q):
    app2 = QtGui.QApplication([])

    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(1000,600)
    win2.setWindowTitle('pyqtgraph example: Plotting')
    p2 = win2.addPlot(title="Updating plot")
    curve = p2.plot(pen='y')

    x_np = []
    y_np = []

    def updateInProc(curve,q,x,y):
        item = q.get()
        x.append(item[0])
        y.append(item[1])
        curve.setData(x,y)

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curve,q,x_np,y_np))
    timer.start(50)

    QtGui.QApplication.instance().exec_()

# This is function is responsible for reading some data (IO, serial port, etc)
# and forwarding it to the display
# it is run in a thread

if __name__ == '__main__':
    q = Queue()
    syst = StageAndSpec()
    syst.connect()
    num_avg = 1
    x_array_scan = np.arange(0.0, 11.0, 1.0)
    y_array_scan = np.arange(0.0, 11.0, 1.0)
    BE_thread = threading.Thread(target=syst.scan, args=(x_array_scan, y_array_scan, num_avg))
    BE_thread.start()
    log.info('Thread started')
    while BE_thread.is_alive():
        print('im alive')
        #q.put([syst.intensity, syst.wavelength])
        time.sleep(0.01)

    # Run io function in a thread
    #t = threading.Thread(target=syst.read, args=(BE_thread,q))
    #t.start()

    # Start display process
    '''p = Process(target=display, args=('bob',q))
    p.start()
    print("Waiting for BACKEND thread to join...")'''
    BE_thread.join()
    #print("Waiting for scheduler thread to join...")
    #t.join()
    '''
    print("Waiting for graph window process to join...")
    p.join()
    print("Process joined successfully. C YA !")'''
    syst.disconnect()