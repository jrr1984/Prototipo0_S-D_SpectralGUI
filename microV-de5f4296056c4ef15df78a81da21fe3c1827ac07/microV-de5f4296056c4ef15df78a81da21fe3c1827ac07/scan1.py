
import numpy as np

import time
import sys
mode = ''
if len(sys.argv)>1:
	mode = sys.argv[1]

from hardware.picoscope import ps3000a
import multiprocessing
from multiprocessing import Queue
import time
import traceback
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

if mode == 'sim':
	from hardware.sim.E727 import E727
else:
	#pass
	from hardware.E727 import E727

t_start = time.time()


class Pico_recorder(multiprocessing.Process):
	kill_counter_N = 500
	def __init__(self,input_q, output_q, n_captures=200,
					ChA_VRange=0.05,ChA_Offset=0.0,
					ChB_VRange=0.05,ChB_Offset=0.0,
					sampleInterval=2e-7, samplingDuration=15e-6,
					trigSrc='External', threshold_V=0.02, direction='Rising',
					timeout_ms=5,delay=0):

		super(Pico_recorder, self).__init__()

		self.output_q = output_q
		self.input_q = input_q
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


	def config(self):
		self.ps = ps3000a.PS3000a(connect=False)
		self.ps.open()

		self.ps.setChannel("A", coupling="DC", VRange=self.ChA_VRange, VOffset=self.ChA_Offset)
		self.ps.setChannel("B", coupling="DC", VRange=self.ChB_VRange, VOffset=self.ChB_Offset)
		self.ps.setSamplingInterval(self.sampleInterval,self.samplingDuration,oversample=0)
		self.ps.setSimpleTrigger(trigSrc=self.trigSrc, threshold_V=self.threshold_V,
			direction=self.direction, timeout_ms=self.timeout_ms, enabled=True,delay=self.delay)
		max_samples_per_segment = self.ps.memorySegments(self.n_captures)
		self.samples_per_segment = int(self.samplingDuration / self.sampleInterval)
		self.ps.setNoOfCaptures(self.n_captures)

	def update(self):
		self.input_q.put('alive')

	def pause(self):
		self.input_q.put('pause')

	def stop(self):
		self.input_q.put('kill')

	def isReady(self):
		out = False
		while self.input_q.qsize()>0:
			status = self.input_q.get()
			if status == 'ready':
				out = True
		if out:
			self.go()
			while self.output_q.empty():
				pass
		return out

	def go(self):
		self.input_q.put('alive')

	def getData(self):
		scanA = np.array([])
		scanB = np.array([])
		scanT = np.array([])
		dataA = []
		dataB = []
		while output_q.qsize()>0:
			d = output_q.get()
			scanT = np.hstack((scanT,d[0]))
			scanA = np.hstack((scanA,d[1]))
			scanB = np.hstack((scanB,d[2]))
			dataA.append(d[3])
			dataB.append(d[4])
		w = scanT.argsort()
		return scanT[w],scanA[w],scanB[w],dataA,dataB

	def run(self):

		self.config()
		status = 'ready'
		self.input_q.put(status)

		while status != 'alive':
			if self.input_q.qsize()>0:
				status = self.input_q.get()
		print('start')
		dataA = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		dataB = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)

		self.ps.runBlock()

		t0 = time.time()
		i = 0
		t0_ = 0
		kill_counter = self.kill_counter_N

		try:
			while status != 'kill' and kill_counter>0:
				#self.ps.runBlock()
				while not self.ps.isReady():
					time.sleep(0.001)
				#self.ps.waitReady()
				t1 = time.time()
				self.ps.getDataRawBulk(channel='A',data=dataA,downSampleRatio=1)
				self.ps.getDataRawBulk(channel='B',data=dataB,downSampleRatio=1)
				t0_ = t0

				self.ps.runBlock()
				t0 = time.time()
				dataA1=dataA[:, 0:self.ps.noSamples].copy()#.mean(axis=0)
				dataB1=dataB[:, 0:self.ps.noSamples].copy()#.mean(axis=0)
				scanA=abs(dataA1.max(axis=1)-dataA1.min(axis=1))
				scanB=abs(dataB1.max(axis=1)-dataB1.min(axis=1))
				scanT = np.linspace(t0_,t1,len(scanA))
				self.output_q.put([scanT,scanA,scanB,dataA1.mean(axis=0),dataB1.mean(axis=0)])
				#self.output_q.put([np.array([scanT[-1]]),np.array([0]),np.array([0]),0,0])
				#time.sleep(1)
				print("<<",time.time(),kill_counter,'>>>>>>>>>',t0-t0_)#, t1-t0_)
				#i+=1
				#if i == 10:
				#	self.close()
				if self.input_q.qsize()>0:
					kill_counter = self.kill_counter_N
					status = self.input_q.get()
					print(status)

				if status == 'pause':
					while status == 'pause' and kill_counter>0:

						time.sleep(0.1)
						print(status)
						if self.input_q.qsize()>0:
							kill_counter = 100
							status = self.input_q.get()
						kill_counter -=1

				kill_counter -= 1

		except:
			traceback.print_exc()
		if kill_counter == 0:
			print('watchdog...')
		print('pico: KILL')
		self.ps.close()

def tableXYZ(X,Y,Z):
	for z in Z:
		for x,y in zip(X,Y):
			 yield [x,y,z]



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	import sys
	__spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

	from scipy.interpolate import interp1d
	from scipy.interpolate import griddata
	#app = QtGui.QApplication(sys.argv)
	#ex = Pico_view()

	#app.exec_()
	#out = ex.out
	input_q = Queue()
	output_q = Queue()

	pico = Pico_recorder(input_q, output_q, n_captures=50,
					ChA_VRange=0.02,ChA_Offset=0.0,
					ChB_VRange=0.02,ChB_Offset=0.0,
					#sampleInterval=0.000001, samplingDuration=0.003,
					#trigSrc="B", threshold_V=-0.350, direction='Falling',
					#						 timeout_ms=10, delay=120)
					)
	'''
	pico = Pico_recorder(input_q, output_q, n_captures=100,
					ChA_VRange=0.5,ChA_Offset=0.0,
					ChB_VRange=0.5,ChB_Offset=0.0,
					sampleInterval=0.000001, samplingDuration=0.003,
					trigSrc="B", threshold_V=-0.350, direction='Falling',
											 timeout_ms=10, delay=150)
	'''

	piStage = E727()
	print(piStage.ConnectUSBWithBaudRate())
	print(piStage.qSAI())
	piStage.qSVO(b'1 2 3')
	piStage.VEL([1000,1000,1000],b'1 2 3')
	pico.start()

	while not pico.isReady():
		pass
	#pico.go()
	N = 25
	X = [0,100,100,0]*N
	Y = np.repeat(np.linspace(0,100,N*2),2)
	Z = [50]

	posTable = tableXYZ(X,Y,Z)
	x = []
	y = []
	t = []

	while True:
		try:
			target = next(posTable)
		except StopIteration:
			break
		real_position = piStage.qPOS()
		x.append(real_position[0])
		y.append(real_position[1])
		t.append(time.time())
		piStage.MOV(target,b'1 2 3',waitUntilReady=0)
		while sum(piStage.IsMoving()):
			real_position = piStage.qPOS()
			x.append(real_position[0])
			y.append(real_position[1])
			t.append(time.time())

		print(output_q.qsize(),x[-1],y[-1])
		#time.sleep(1)
		#pico.update()

	pico.pause()

	piStage.CloseConnection()
	time.sleep(2)

	scanT,scanA,scanB,dataA,dataB = pico.getData()
	sm_step_x = interp1d(t,x)
	sm_step_y = interp1d(t,y)
	t1 = np.linspace(min(t),max(t),len(t)*2)
	x1 = sm_step_x(t1)
	y1 = sm_step_y(t1)

	interp_T = interp1d(scanT,scanA,bounds_error=False,fill_value=0)
	p=interp_T(t1)

	xi=np.linspace(min(x),max(x),len(x))
	yi = np.linspace(min(y),max(y),len(x))
	xi,yi = np.meshgrid(xi,yi)
	data = griddata((x1,y1),p,(xi,yi))
	pico.stop()
	pico.join()
	import matplotlib.pyplot as plt
	plt.figure()
	plt.plot(t1,x1*10,'r')
	plt.plot(t1,y1*10,'g')
	plt.plot(scanT,scanA,'m')
	plt.show(0)
	plt.figure()

	plt.contourf(xi,yi,data,20)
	plt.plot(X,Y,'r')
	plt.show()
