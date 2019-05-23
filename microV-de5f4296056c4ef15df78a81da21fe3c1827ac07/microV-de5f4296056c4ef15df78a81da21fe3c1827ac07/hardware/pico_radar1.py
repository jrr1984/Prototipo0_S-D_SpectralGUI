from pylab import *
import numpy as np

import time
import sys
from scipy.signal import resample
from picoscope import ps3000a
from multiprocessing import Process, Queue
from scipy.signal import medfilt





def fastScan(piStage,ps,n_captures=643,x_range=np.arange(0,100,1),y_range=np.arange(0,100,1),z_range=np.arange(0,100,1),q=Queue(),app=None):
	direction = True
	piStage.MOV(x_range.min(),axis=1, waitUntilReady=True)
	piStage.MOV(y_range.min(),axis=2, waitUntilReady=True)
	piStage.MOV(z_range.min(),axis=3, waitUntilReady=True)
	n_calibr = 3
	t0=time.time()
	dt = 0
	for i in range(n_calibr):
		t1=time.time()
		piStage.MOV(x_range.max(),axis=1, waitUntilReady=True)
		piStage.MOV(x_range.min(),axis=1, waitUntilReady=True)
		dt += (time.time() - t1)/2
	dt = dt/n_calibr
	k = dt/0.09000015258789062
	#n_captures = int(n_captures*k)
	print(n_captures, dt,k)


	data_out_A = []
	data_out_B = []
	start0 = time.time()

	for z in z_range:
		try:
			piStage.MOV(z,axis=3, waitUntilReady=True)
			print(z)
			t_list = []
			dataxyA = []
			dataxyB = []
			t_start = time.time()
			data_tmp = []
			t_read0 = time.time()
			t_read1 = 0
			samples_per_segment = ps.memorySegments(n_captures)
			ps.setNoOfCaptures(n_captures)
			ps.runBlock()
			dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
			dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
			for y in y_range:
				print(y)

				piStage.MOV(y,axis=2, waitUntilReady=True)
				if direction:
					piStage.MOV(x_range.max(),axis=1, waitUntilReady=True)
					direction = False
				else:
					piStage.MOV(x_range.min(),axis=1, waitUntilReady=True)
					direction = True
				if ps.isReady():
					t_read1 = time.time()
					ps.getDataRawBulk(channel='A',data=dataA)
					ps.getDataRawBulk(channel='B',data=dataB)
					dataA1=dataA[:, 0:ps.noSamples]
					dataB1=dataB[:, 0:ps.noSamples]

					dataxyA.append(dataA1)
					dataxyB.append(dataB1)

					ps.runBlock()
					samples_per_segment = ps.memorySegments(n_captures)
					ps.setNoOfCaptures(n_captures)


			dt_move = time.time() - t_read0
			dt_read = t_read1 - t_read0

			dataxyA=np.vstack(dataxyA)
			dataxyB=np.vstack(dataxyB)

			scanA=abs(dataxyA.max(axis=1)-dataxyA.min(axis=1))
			scanB=abs(dataxyB.max(axis=1)-dataxyB.min(axis=1))
			k=dt_read/dt_move
			print("total blocks:",len(dataxyA), k,scanA.shape, dataxyA.shape)

			L=len(scanA)-int(len(scanA)*k)
			#scanA = np.hstack((scanA,np.zeros(L)))
			#scanB = np.hstack((scanB,np.zeros(L)))
			print(scanA.shape, len(x_range)*len(y_range))
			scanA = resample(scanA,len(x_range)*len(y_range))
			scanB = resample(scanB,len(x_range)*len(y_range))

			scanA = scanA.reshape((len(y_range),len(x_range)))
			scanB = scanB.reshape((len(y_range),len(x_range)))
			#scanA[::2,:] = scanA[::2,::-1]
			#scanB[::2,:] = scanB[::2,::-1]
			data_out_A.append(scanA)
			data_out_B.append(scanB)

			print("xyScan:", time.time()-t_start,dt_read,dt_move)
			t_start = time.time()
			#data_out.append([np.array(dataxyA).T[::-1][::-1],np.array(dataxyB).T[::-1][::-1]])
			if not app is None:
				app.processEvents()
		except KeyboardInterrupt:
			break
			ps.close()
			piStage.CloseConnection()
	dataA = np.array(data_out_A,dtype=np.int16)
	dataB = np.array(data_out_B,dtype=np.int16)
	return dataA, dataB


if __name__=='__main__':
	get_ipython().run_line_magic('matplotlib', 'qt')
	from skimage.external.tifffile import imsave
	from E727 import *
	import traceback
	ps = ps3000a.PS3000a(connect=False)
	ps.open()

	ps.setChannel("A", coupling="DC", VRange=0.02)
	ps.setChannel("B", coupling="DC", VRange=0.02)
	ps.setSamplingInterval(200e-9,15e-6)
	ps.setSimpleTrigger(trigSrc="External", threshold_V=0.020, direction='Rising',
							 timeout_ms=5, enabled=True)


	#dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
	#dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
	#t1 = time.time()
	#ps.runBlock()
	#ps.waitReady()
	#t4 = time.time()
	#ps.getDataRawBulk(channel='A',data=dataA)
	#ps.getDataRawBulk(channel='B',data=dataB)

	#print('pico_time',t4-t1)

	piStage = E727()
	print(piStage.ConnectUSBWithBaudRate())
	print(piStage.qSAI())
	print(piStage.SVO())

	start0=time.time()
	a=[]
	b=[]
	x_range=np.arange(0,100,1)
	y_range=np.arange(0,100,1)
	z_range=np.arange(40,43,3)
	try:
		a,b =fastScan(piStage,ps,n_captures=3000,
			x_range=x_range,
			y_range=y_range,
			z_range=z_range)

		print('TotalTime:',time.time()-start0)

		print(piStage.CloseConnection())
		ps.close()

		imsave('dataA.tif',a)
		imsave('dataB.tif',a)
		from pylab import *
		matshow(a[0])
		show(0)
	except:
		traceback.print_exc()
		print(piStage.CloseConnection())
		ps.close()

#plot(dataA)
#plot(dataB)
#show(0)
