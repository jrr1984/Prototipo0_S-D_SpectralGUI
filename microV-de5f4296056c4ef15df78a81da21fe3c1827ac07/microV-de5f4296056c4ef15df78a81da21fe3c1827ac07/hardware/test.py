from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
import sys

import multiprocessing
from picoscope import ps3000a
import time
import traceback


class Pico_recorder(multiprocessing.Process):
	ps = None
	def __init__(self,q):

		super(Pico_recorder, self).__init__()
		self.q = q

	def run(self):
		ps = ps3000a.PS3000a(connect=False)
		ps.open()
		n_captures = 100
		N=16
		self.n_captures = n_captures
		ps.setChannel("A", coupling="DC", VRange=0.5)
		ps.setChannel("B", coupling="DC", VRange=0.5)
		capture_duration = 0.003
		sample_interval = 0.00001

		ps.setSamplingInterval(sample_interval,capture_duration)
		#ps.setSamplingFrequency(80e6,1000000,2)

		#ps.setEts(mode='slow', etsCycles=1,etsInterleave=1)

		ps.setSimpleTrigger(trigSrc="B", threshold_V=-0.350, direction='Falling',
								 timeout_ms=100, enabled=True,delay=120)
		max_samples_per_segment = ps.memorySegments(n_captures)
		samples_per_segment = int(capture_duration / sample_interval)
		self.samples_per_segment = samples_per_segment
		ps.setNoOfCaptures(n_captures)

		print('start')
		out = []
		dataA = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		dataB = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)

		for index in range(N):
			t0=time.time()
			print('>',index,' ',end='')

			ps.runBlock()
			while not ps.isReady():
				#pass
				time.sleep(0.00001)
			#tt=ps.getTriggerTimeOffset(index)
			print(time.time()-t0)

			k = index+n_captures-5
			k_ = index
			t0 = time.time()

			ps.getDataRawBulk(channel='A',data=dataA)
			ps.getDataRawBulk(channel='B',data=dataB)
			dataA1=dataA[:, 0:ps.noSamples]#.mean(axis=0)
			out.append(dataA1.copy())#.mean(axis=0))
			print('<',time.time()-t0)

		ps.stop()




		#print(" ",i,end='')
		#dataA1=dataA[:, 0:ps.noSamples]#.mean(axis=0)
		#out.append(dataA)

		#dataA=dataA[:, 0:ps.noSamples]#.mean(axis=0)
		#dataB=dataB[:, 0:ps.noSamples]#.mean(axis=0)
		q.put(out)
		print('done')
		print('End')
		ps.close()
		print('close')

if __name__ == "__main__":
	__spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"

	number = 7
	result = None

	#p1 = multiprocessing.Process(target=pico_proc, args=(ps,))
	q = multiprocessing.Queue()
	p1 = Pico_recorder(q)
	p1.start()
	#p1.join()
	print('exit')
