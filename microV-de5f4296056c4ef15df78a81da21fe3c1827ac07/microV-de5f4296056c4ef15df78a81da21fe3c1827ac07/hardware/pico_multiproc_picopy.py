from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
import sys

from picoscope import ps3000a
import multiprocessing
from multiprocessing import Queue
import time
import traceback
import picopy

def reader(q):
	pico = picopy.Pico3k()
	n_captures = 100
	pico.setChannel("A", coupling="DC", VRange='500mV')
	pico.setChannel("B", coupling="DC", VRange='500mV')
	(sampleInterval, noSamples, maxSamples) = pico.setSamplingInterval(0.00001,0.0035)

	#trigger = picopy.EdgeTrigger(channel='B', threshold=-0.35, direction='FALLING')
	#pico.set_trigger(trigger)
	pico.setSimpleTrigger(trigSrc="B", threshold_V=-0.350, direction='FALLING',
							 timeout_ms=10, enabled=True,delay=0)

	for i in range(50):

		r = pico.capture_prep_block( number_of_frames=n_captures, downsample=1, downsample_mode='NONE',
			return_scaled_array=1)
		q.put(r)
	pico.close()
	q.put('done')

class Pico_view(QtGui.QMainWindow):
	timer = QtCore.QTimer()
	q = Queue()
	liveA = np.array([])
	liveB = np.array([])
	liveT = np.array([])
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		#QtGui.QApplication.setGraphicsSystem('raster')
		#app = QtGui.QApplication([])
		self.setWindowTitle('pyqtgraph example: PlotWidget')
		self.resize(800,800)
		cw = QtGui.QWidget()
		self.setCentralWidget(cw)
		l = QtGui.QVBoxLayout()
		cw.setLayout(l)

		pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
		l.addWidget(pw)
		pw1 = pg.PlotWidget(name='Plot2')  ## giving the plots names allows us to link their axes together
		l.addWidget(pw1)

		self.show()

		## Create an empty plot curve to be filled later, set its pen
		self.curveA = pw.plot()
		self.curveA.setPen((255,0,0))

		self.curveB = pw.plot()
		self.curveB.setPen((0,255,0))

		## Create an empty plot curve to be filled later, set its pen
		self.curveA1 = pw1.plot()
		self.curveA1.setPen((255,0,0))

		self.curveB1 = pw1.plot()
		self.curveB1.setPen((0,255,0))


		self.timer.timeout.connect(self.update)
		self.timer.start(0.5)
		self.ps = multiprocessing.Process(target=reader,args=[self.q,])
		self.ps.start()
		#self.pico.join()
		#self.actionExit.toggled.connect(self.closeEvent)


	def update(self):
		#print(data)

			if not self.q.empty():
				data_q = []
				while not self.q.empty():
					out = self.q.get()
					if out == 'done':
						self.timer.stop()
						self.ps.join()
						return
					data_q.append(out)
				#print(data)
				#L = len(data_q)*self.pico.n_captures
				for data in data_q:
					self.liveA = np.hstack((self.liveA,
						abs(data[0]['A'].max(axis=1)-data[0]['A'].min(axis=1))))
					self.liveB = np.hstack((self.liveB,
						abs(data[0]['B'].max(axis=1)-data[0]['B'].min(axis=1))))
					self.liveT = np.hstack((self.liveT,data[1]))
				dataA = data[0]['A'].mean(axis=0)
				dataB = data[0]['B'].mean(axis=0)
				L = len(data[1])
				if len(self.liveA)>500:

					self.liveA = self.liveA[L:]
					self.liveB = self.liveB[L:]
					self.liveT = self.liveT[L:]
				print(dataA.shape)
				self.curveA.setData(dataA)
				self.curveB.setData(dataB)
				self.curveA1.setData(x=self.liveT,y=self.liveA)
				self.curveB1.setData(x=self.liveT,y=self.liveB)
				app.processEvents()


	def closeEvent(self, evnt=None):
		print('closeEvent')
		#self.pico.close()
		#self.pico.alive=False
		#ex.pico.terminate()
		#data = np.array([self.liveT,self.liveA,self.liveB]).T
		#np.savetxt('signal'+str(time.time())+'.txt',data)




## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	__spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

	app = QtGui.QApplication(sys.argv)
	ex = Pico_view()

	app.exec_()
