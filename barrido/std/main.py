import logging,threading,time
from logging.handlers import SocketHandler
from StageAndSpec import StageAndSpec
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
        print(item[0])
        x.append(item[0])
        y.append(item[1])
        curve.setData(x,y)

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curve,q,x_np,y_np))
    timer.start(50)

    QtGui.QApplication.instance().exec_()



if __name__ == '__main__':
    q = Queue()
    syst = StageAndSpec()
    syst.connect()
    initial_time = time.time()
    num_avg=1
    dx = 1
    dy=1
    x_array_scan = np.arange(0.0,dx*(5+1),dx)
    y_array_scan = np.arange(0.0,dy*(5+1),dy)
    BE_thread = threading.Thread(target=syst.scan, args= (dx,x_array_scan,dy,y_array_scan,num_avg))
    BE_thread.start()

    while BE_thread.is_alive():
        q.put([syst.intensity, syst.wavelength])
        time.sleep(0.01)
    log.info('Done SAVING the data.')
    #run = threading.Event()
    #run.set()
    #storage = threading.Thread(target=read, args=(BE_thread,q))
    #storage.start()
    # Start display process
    GUI = Process(target=display, args=('bob', q))
    GUI.start()
    #input("See ? Main process immediately free ! Type any key to quit.")
    #run.clear()
    BE_thread.join()
    log.info("Waiting for scheduler thread to join...")
    #storage.join()
    log.info("Waiting for graph window process to join...")
    GUI.join()
    log.info("Process joined successfully. C YA !")
    syst.disconnect()
