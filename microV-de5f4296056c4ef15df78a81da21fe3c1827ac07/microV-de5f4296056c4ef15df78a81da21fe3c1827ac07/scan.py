from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
import sys
if len(sys.argv[1])>0:
	mode = sys.argv[1]

from picoscope import ps3000a
import multiprocessing
from multiprocessing import Queue
import time
import traceback
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

if mode == 'sim':
	from hardware.sim.E727 import E727
else:
	from hardware.E727 import E727

t_start = time.time()


class Pico_recorder(multiprocessing.Process):
	ps = None
	alive = True
	isReady = False
	def __init__(self,q,  n_captures=10000,
					ChA_VRange=0.05,ChA_Offset=0.0,
					ChB_VRange=0.05,ChB_Offset=0.0,
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
		self.isReady = True
		print('start')
		dataA = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		dataB = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		self.ps.runBlock()

		t0 = time.time()
		i = 0
		t0_ = 0
		try:
			while self.alive:
				#self.ps.runBlock()
				self.ps.waitReady()
				t1 = time.time()
				self.ps.getDataRawBulk(channel='A',data=dataA)
				self.ps.getDataRawBulk(channel='B',data=dataB)
				t0_ = t0
				self.ps.runBlock()
				t0 = time.time()
				dataA1=dataA[:, 0:self.ps.noSamples]#.mean(axis=0)
				dataB1=dataB[:, 0:self.ps.noSamples]#.mean(axis=0)
				scanA=abs(dataA1.max(axis=1)-dataA1.min(axis=1))
				scanB=abs(dataB1.max(axis=1)-dataB1.min(axis=1))
				self.q.put([scanA,scanB,dataA1.mean(axis=0),dataB1.mean(axis=0),t0_-t_start,t1-t_start])
				#time.sleep(1)
				print("<<",time.time())#, t1-t0_)
				#i+=1
				#if i == 10:
				#	self.close()
		except:
			traceback.print_exc()
		print('End')
		self.ps.close()

def tableXYZ(X,Y,Z):
	for z in Z:
		for x,y in zip(X,Y):
			 yield [x,y,z]


class Pico_view(QtGui.QMainWindow):
	timer = QtCore.QTimer()
	q = Queue()
	#ps = ps3000a.PS3000a(connect=False)
	#pico = Pico_recorder(q=q)
	pico = Pico_recorder(q=q,n_captures=1000,
					ChA_VRange=0.5,ChA_Offset=0.0,
					ChB_VRange=0.5,ChB_Offset=0.0,
					sampleInterval=0.00001, samplingDuration=0.003,
					trigSrc="B", threshold_V=-0.350, direction='Falling',
											 timeout_ms=10, delay=120)
	liveA = []
	liveB = []
	liveT = []
	data_stack = []
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



		self.img = pg.ImageView()  ## giving the plots names allows us to link their axes together
		data = np.zeros((100,100))
		l.addWidget(self.img)
		self.img.setMinimumHeight(500)
		self.img.setImage(data)
		colors = [(0, 0, 0),(255, 214, 112)]
		cmap = pg.ColorMap(pos=[0.,1.], color=colors)
		self.img.setColorMap(cmap)
		g = pg.GridItem()
		self.img.addItem(g)
		self.show()

		pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
		l.addWidget(pw)
		pw1 = pg.PlotWidget(name='Plot2')  ## giving the plots names allows us to link their axes together
		l.addWidget(pw1)

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

		self.curveX1 = pw1.plot()
		self.curveX1.setPen((100,105,0))

		self.piStage = E727()
		print(self.piStage.ConnectUSBWithBaudRate())
		print(self.piStage.qSAI())
		self.piStage.qSVO(b'1 2 3')
		print(self.piStage.VEL([1000,1000,1000],b'1 2 3'))
		print(self.piStage.qVEL())



		self.pico.start()
		time.sleep(3)
		self.timer.start(0.5)
		#while self.q.empty():
		#	time.sleep(0.5)
		#
		self.timer.timeout.connect(self.update)
		#self.pico.join()
		#self.actionExit.toggled.connect(self.closeEvent)



	def update(self):
		#print(data)
			self.timer.stop()
			self.liveA = []
			self.liveT = []
			dataA = []
			dataB = []
			print('update')
			try:
				N = 5
				X = [0,100,100,0]*N
				Y = np.repeat(np.linspace(0,100,N*2),2)
				Z = [50]

				self.posTable = tableXYZ(X,Y,Z)
				t = [time.time()-t_start]
				x = [0]
				y = [0]
				for zz in range(len(X)*len(Y)):
					try:
						target = next(self.posTable)
						#print(target)
						self.piStage.MOV(dPos=target,axis=b"1 2 3", waitUntilReady=True)
						t.append(time.time()-t_start)
						real_position = self.piStage.qPOS()
						x.append(real_position[0])
						y.append(real_position[1])
						print(">>",time.time(),self.q.qsize())
						data_q = []
						while self.q.qsize()>3:
							data_q.append(self.q.get())
							#print(self.q.qsize())
						if len(data_q)>0:
							for data in data_q:
								self.liveA+= data[0].tolist()
								self.liveB+= data[1].tolist()
								self.liveT+= np.linspace(data[4],data[5],len(data[0])).tolist()
					except StopIteration:
						break
				app.processEvents()
				#time.sleep(5)
				x_ = x
				t_ = t
				#while self.q.empty():
				#	time.sleep(0.5)
				#self.pico.terminate()
				#if not self.q.empty():
				data_q = []
				#self.q.join()

				while self.q.qsize()>0:
					data_q.append(self.q.get_nowait())
					print(self.q.qsize())
				if len(data_q)>0:
					for data in data_q:
						self.liveA+= data[0].tolist()
						self.liveB+= data[1].tolist()
						self.liveT+= np.linspace(data[4],data[5],len(data[0])).tolist()
					dataA = data[2]
					dataB = data[3]
				T_interp = interp1d(self.liveT,self.liveA,bounds_error=False,fill_value=0)
				pmt = T_interp(t)
				xi = np.linspace(min(x),max(x),N*2)
				yi = np.linspace(min(y),max(y),N*2)

				xi, yi = np.meshgrid(xi,yi)
				self.PMT = griddata((x,y),pmt,(xi,yi))
				self.x = x
				self.out=[x,y,t,pmt,T_interp]
				print(min(x),max(x),xi.min(),xi.max())
				print(min(y),max(y),yi.min(),yi.max())

				print(self.PMT,xi.shape,yi.shape)
				#self.image = np.array(pmt[1:]).reshape((N,N))
				self.img.setImage(self.PMT)
				#if len(self.liveA)>500:

					#self.liveA = self.liveA[L:]
					#self.liveB = self.liveB[L:]
					#self.liveT = self.liveT[L:]
				self.curveA.setData(pmt)
				#self.curveB.setData(dataB)
				self.curveA1.setData(x=self.liveT,y=self.liveA)
				self.curveB1.setData(x=self.liveT,y=self.liveB)
				self.curveX1.setData(x=t_,y=x_)
				app.processEvents()
				#self.timer.start(0.5)
			except:
				traceback.print_exc()
				pass

	def closeEvent(self, evnt=None):
		#self.pico.close()
		self.pico.alive=False
		self.pico.terminate()
		data = np.array([self.liveT,self.liveA,self.liveB]).T
		np.savetxt('signal'+str(time.time())+'.txt',data)
		self.piStage.CloseConnection()




## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	__spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

	app = QtGui.QApplication(sys.argv)
	ex = Pico_view()

	app.exec_()
	out = ex.out
