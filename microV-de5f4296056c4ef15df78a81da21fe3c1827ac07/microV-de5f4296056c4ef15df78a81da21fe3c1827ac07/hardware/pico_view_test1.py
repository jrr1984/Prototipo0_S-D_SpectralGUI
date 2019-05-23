


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
import sys
import traceback
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
n_captures = 50
ps.setChannel("A", coupling="DC", VRange=0.5)
ps.setChannel("B", coupling="DC", VRange=0.5)
ps.setSamplingInterval(0.000001,0.0035)
ps.setSimpleTrigger(trigSrc="B", threshold_V=-0.350, direction='Falling',
						 timeout_ms=10, enabled=True,delay=120)
samples_per_segment = ps.memorySegments(n_captures)
ps.setNoOfCaptures(n_captures)


dataA = []
dataB = []
liveA = np.array([0])
liveB = np.array([0])
tmp_data = []
dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
def update():
	try:
		global dataA, liveA,dataB, liveB, tmp_data

		#tmp_data = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
		t1 = time.time()
		while not ps.isReady():
			time.sleep(0.01)
		#time.sleep(3)
		#ps.waitReady()
		t2 = time.time()
		print("Time to get sweep: " + str(t2 - t1))
		ps.getDataRawBulk(channel='A',data=dataA)
		ps.getDataRawBulk(channel='B',data=dataB)
		ps.runBlock()
		t3 = time.time()

		print("Time to read data: " + str(t3 - t2))
		dataA1=dataA[:, 0:ps.noSamples].copy()#.mean(axis=0)
		dataB1=dataB[:, 0:ps.noSamples].copy()#.mean(axis=0)
		#if dataA.min()>-100 :
		#	ps.setChannel("A", coupling="DC", VRange=2)
		#print (data.shape)
		scanA=abs(dataA1.max(axis=1)-dataA1.min(axis=1))
		scanB=abs(dataB1.max(axis=1)-dataB1.min(axis=1))

		if mode == 'scope':
			curveA.setData(dataA1.mean(axis=0))
			curveB.setData(dataB1.mean(axis=0))
		elif mode == "live":
			liveA = np.hstack((liveA,scanA))
			curveA.setData(liveA)
			#liveB+=scanB.tolist()
			liveB = np.hstack((liveB,scanB))
			curveB.setData(liveB)
		#for i in range(len(data)):
		#	curves[i].setData(data[i,:])
		print("Time to plot data: " + str(time.time()-t3))
		print("Time of cycle: " + str(time.time()-t1))
		app.processEvents()  ## force complete redraw for every plot
		#time.sleep(1)
	except:
		traceback.print_exc()
		ps.close()
		timer.stop()
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)
ps.runBlock()



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	try:
		if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
			QtGui.QApplication.instance().exec_()
	except:
		ps.close()
	ps.close()
