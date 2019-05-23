from pylab import *
import numpy as np

import time
import sys
from scipy.signal import resample
from picoscope import ps3000a
from multiprocessing import Process, Queue





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
	n_captures = int(n_captures*k)
	print(n_captures, dt,k)
	max_samples_per_segment = ps.memorySegments(n_captures)

	samples_per_segment = ps.noSamples
	ps.setNoOfCaptures(n_captures)

	data_out = []
	start0 = time.time()
	for z in z_range:
		try:
			piStage.MOV(z,axis=3, waitUntilReady=True)
			print(z)
			t_list = []
			dataxyA = []
			dataxyB = []
			t_start = time.time()
			dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
			dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)

			for y in y_range:
				t1 = time.time()

				piStage.MOV(y,axis=2, waitUntilReady=True)
				t2 = time.time()
				ps.runBlock()
				t3 = time.time()
				if direction:
					piStage.MOV(x_range.max(),axis=1, waitUntilReady=0)
				else:
					piStage.MOV(x_range.min(),axis=1, waitUntilReady=0)

				t4 = time.time()
				dt1 = -1
				dt2 = -1
				for i in range(10000):
					isMoving = sum(piStage.IsMoving())
					isReading = ps.isReady()
					if isMoving == 0 and dt1==-1:
						dt1=time.time()-t4
					if isReading and dt2==-1:
						dt2=time.time()-t4
						if dt1==-1:
							for i in range(100):
								isMoving = sum(piStage.IsMoving())
								if isMoving == 0:
									dt1=time.time()-t4
									break
						break
					time.sleep(0.0001)
				#ps.waitReady()
				t5 = time.time()
				#k = (t4-t3)/(t5-t2)
				k = dt1/dt2
				#print("Time to get sweep: ",k, dt2, dt1)
				ps.getDataRawBulk(channel='A',data=dataA)
				ps.getDataRawBulk(channel='B',data=dataB)
				t6 = time.time()
				#tmp_data = dataA.copy()
				#print("Time to read data: " + str(t3 - t2))
				dataA1=dataA[:, 0:ps.noSamples]
				dataB1=dataB[:, 0:ps.noSamples]

				scanA = abs(dataA1.max(axis=1) - dataA1.min(axis=1))
				scanB = abs(dataB1.max(axis=1) - dataB1.min(axis=1))

				L = len(scanA)
				#if k<=1 and k>0:
				#	scanA=scanA[:int(L*k)]
				#	scanB=scanB[:int(L*k)]
				#elif k>1 and k<1.5:
				#	scanA = np.hstack((scanA,np.zeros((int(L*k)-L)//3)))
				#	scanB = np.hstack((scanB,np.zeros((int(L*k)-L)//3)))
				#else: pass
				scanA = resample(scanA,len(x_range))
				scanB = resample(scanB,len(x_range))
				if direction:
					dataxyA.append(scanA)
					dataxyB.append(scanB)
					direction = False
				else:
					dataxyA.append(scanA[::-1])
					dataxyB.append(scanB[::-1])
					direction = True
				#t_list.append(time.time()-t_start)
				t7 = time.time()
				print('\tZ: %.3f\tY: %.3f\tk: %.3f'%(z,y,k))#time.time()-t5,t5-t4,t4-t3,t3-t2,t2-t1)
			print("xyScan:", time.time()-t_start)
			t_start = time.time()
			data_out.append([np.array(dataxyA).T[::-1][::-1],np.array(dataxyB).T[::-1][::-1]])
			if not app is None:
				app.processEvents()
		except KeyboardInterrupt:
			break
			ps.close()
			piStage.CloseConnection()
	dataA_out=[]
	dataB_out=[]
	for d in data_out:
		dataA_out.append(d[0])
		dataB_out.append(d[1])
	a = np.array(dataA_out,dtype=np.int16)
	b = np.array(dataB_out,dtype=np.int16)
	#q.put((a,b))
	return a,b


if __name__=='__main__':
	get_ipython().run_line_magic('matplotlib', 'qt')
	from skimage.external.tifffile import imsave
	from E727 import *
	import traceback
	ps = ps3000a.PS3000a(connect=False)
	ps.open()

	ps.setChannel("A", coupling="DC", VRange=0.02)
	ps.setChannel("B", coupling="DC", VRange=0.02)
	capture_duration = 15e-6
	sample_interval = 200e-9
	ps.setSamplingInterval(sample_interval, capture_duration)
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
	try:
		a,b=fastScan(piStage,ps,n_captures=710,
			x_range=np.arange(0,100,1),
			y_range=np.arange(0,100,1),
			z_range=np.arange(48,50,2))

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
