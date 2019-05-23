


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
import sys

from picoscope import ps3000a

mode = 'live'
if len(sys.argv)>1:
	if sys.argv[1] == 'scope':
		mode = 'scope'

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('pyqtgraph example: PlotSpeedTest')

#p.setRange(QtCore.QRectF(0, -10, 5000, 20))
p.setLabel('bottom', 'Index', units='B')
curveA = p.plot(pen=(255,0,0))
curveB = p.plot(pen=(0,255,0))
curves=[]
n_captures = 100
for i in range(n_captures):
	curves.append(p.plot())

#curve.setFillBrush((0, 0, 100, 100))
#curve.setFillLevel(0)

#lr = pg.LinearRegionItem([100, 4900])
#p.addItem(lr)
ps = ps3000a.PS3000a(connect=False)
ps.open()
n_captures = 1000
ps.setChannel("A", coupling="DC", VRange=0.5)
ps.setChannel("B", coupling="DC", VRange=0.5)
ps.setSamplingInterval(200e-9,15e-6)
ps.setSimpleTrigger(trigSrc="External", threshold_V=0.030, direction='Rising',
						 timeout_ms=5, enabled=True)
samples_per_segment = ps.memorySegments(n_captures)
ps.setNoOfCaptures(n_captures)


dataA = []
dataB = []
liveA = []
liveB = []
tmp_data = []
def update():
	try:
		global dataA, liveA,dataB, liveB, tmp_data
		dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
		dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
		tmp_data = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
		t1 = time.time()
		ps.runBlock()
		#time.sleep(3)
		ps.waitReady()
		t2 = time.time()
		print("Time to get sweep: " + str(t2 - t1))
		ps.getDataRawBulk(channel='A',data=dataA)
		ps.getDataRawBulk(channel='B',data=dataB)
		t3 = time.time()
		tmp_data = dataA.copy()
		print("Time to read data: " + str(t3 - t2))
		dataA=dataA[:, 0:ps.noSamples].mean(axis=0)
		dataB=dataB[:, 0:ps.noSamples].mean(axis=0)
		#if dataA.min()>-100 :
		#	ps.setChannel("A", coupling="DC", VRange=2)
		#print (data.shape)
		if mode == 'scope':
			curveA.setData(dataA)
			curveB.setData(dataB)
		elif mode == "live":
			liveA.append(dataA.max()-dataA.min())
			curveA.setData(liveA)
			liveB.append(dataB.max()-dataB.min())
			curveB.setData(liveB)
		#for i in range(len(data)):
		#	curves[i].setData(data[i,:])
		app.processEvents()  ## force complete redraw for every plot
		#time.sleep(1)
	except:
		ps.close()
		timer.stop()
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0.1)



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	try:
		if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
			QtGui.QApplication.instance().exec_()
	except:
		ps.close()
	ps.close()
