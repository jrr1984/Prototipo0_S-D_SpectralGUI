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



class Pico_recorder(multiprocessing.Process):
	ps = None
	alive = True
	def __init__(self,q,  n_captures=500,
					ChA_VRange=0.02,ChA_Offset=0.0,
					ChB_VRange=0.02,ChB_Offset=0.0,
					sampleInterval=2e-7, samplingDuration=15e-6,
					trigSrc='External', threshold_V=0.02, direction='Rising',
					timeout_ms=5,delay=0):

		super(Pico_recorder, self).__init__()

		self.q = q
		#self.ps = ps
		self.n_captures = n_captures
		self.ChA_VRange = ChA_VRange
		self.ChA_Offset = ChA_Offset
		self.ChB_VRange = ChB_VRange
		self.ChB_Offset = ChB_Offset
		self.sampleInterval = sampleInterval
		self.samplingDuration = samplingDuration
		self.trigSrc = trigSrc
		self.threshold_V = threshold_V
		self.direction = direction
		self.timeout_ms = timeout_ms
		self.delay = delay
		#self.ps.close()
	def close(self):
		self.alive=False
		self.ps.close()
	def config(self):
		self.ps = ps3000a.PS3000a(connect=False)
		self.ps.open()

		self.ps.setChannel("A", coupling="DC", VRange=self.ChA_VRange, VOffset=self.ChA_Offset)
		self.ps.setChannel("B", coupling="DC", VRange=self.ChB_VRange, VOffset=self.ChB_Offset)
		self.ps.setSamplingInterval(self.sampleInterval,self.samplingDuration)
		self.ps.setSimpleTrigger(trigSrc=self.trigSrc, threshold_V=self.threshold_V,
			direction=self.direction, timeout_ms=self.timeout_ms, enabled=True,delay=self.delay)
		max_samples_per_segment = self.ps.memorySegments(self.n_captures)
		self.samples_per_segment = int(self.samplingDuration / self.sampleInterval)
		self.ps.setNoOfCaptures(self.n_captures)

	def run(self):

		self.config()
		print('start')
		dataA = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		dataB = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		self.ps.runBlock()
		i = 0
		try:
			while self.alive:
				t0 = time.time()
				self.ps.waitReady()
				self.ps.getDataRawBulk(channel='A',data=dataA)
				self.ps.getDataRawBulk(channel='B',data=dataB)
				t1 = time.time()
				self.ps.runBlock()
				dataA1=dataA[:, 0:self.ps.noSamples]#.mean(axis=0)
				dataB1=dataB[:, 0:self.ps.noSamples]#.mean(axis=0)
				scanA=abs(dataA1.max(axis=1)-dataA1.min(axis=1))
				scanB=abs(dataB1.max(axis=1)-dataB1.min(axis=1))
				self.q.put([scanA,scanB,dataA1.mean(axis=0),dataB1.mean(axis=0),t1,t0])
				#time.sleep(1)
				print(time.time()-t0, t1-t0)
				#i+=1
				#if i == 10:
				#	self.close()
		except:
			traceback.print_exc()
		print('End')
		self.ps.close()

class Pico_view(QtGui.QMainWindow):
	timer = QtCore.QTimer()
	q = Queue()
	ps = ps3000a.PS3000a(connect=False)
	pico = Pico_recorder(q=q)
	liveA = []
	liveB = []
	liveT = []
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
		self.pico.start()
		#self.pico.join()
		#self.actionExit.toggled.connect(self.closeEvent)


	def update(self):
		#print(data)

			if not self.q.empty():
				data_q = []
				while not self.q.empty():
					data_q.append(self.q.get())
				#print(data)
				L = len(data_q)*self.pico.n_captures
				for data in data_q:
					self.liveA+= data[0].tolist()
					self.liveB+= data[1].tolist()
					self.liveT+= np.linspace(data[5],data[4],len(data[0])).tolist()
				dataA = data[2]
				dataB = data[3]
				if len(self.liveA)>500:

					self.liveA = self.liveA[L:]
					self.liveB = self.liveB[L:]
					self.liveT = self.liveT[L:]
				self.curveA.setData(dataA)
				self.curveB.setData(dataB)
				self.curveA1.setData(x=self.liveT,y=self.liveA)
				self.curveB1.setData(x=self.liveT,y=self.liveB)
				app.processEvents()


	def closeEvent(self, evnt=None):
		#self.pico.close()
		self.pico.alive=False
		ex.pico.terminate()
		data = np.array([self.liveT,self.liveA,self.liveB]).T
		np.savetxt('signal'+str(time.time())+'.txt',data)




## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	__spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

	app = QtGui.QApplication(sys.argv)
	ex = Pico_view()

	app.exec_()
