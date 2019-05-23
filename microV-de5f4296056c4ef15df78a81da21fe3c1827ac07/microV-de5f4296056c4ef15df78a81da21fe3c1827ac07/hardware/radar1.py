import numpy as np
import time

# collect 20% more samples than nominally necessary
SAMPLE_SAFETY_MARGIN = 1.25
LIGHTSPEED = 2.99e8
#lr = pg.LinearRegionItem([100, 4900])
#p.addItem(lr)

if __name__ == '__main__':
	# picoscope = reload(picoscope)
	from picoscope import ps3000a
	# ps3000a = reload(ps3000a)
	ps = ps3000a.PS3000a(connect=False)
	ps.open()
	n_captures = 50
	ps.setChannel("A", coupling="DC", VRange=0.5)
	ps.setChannel("B", coupling="DC", VRange=0.5)
	capture_duration = 0.003
	sample_interval = 0.00001
	ps.setSamplingInterval(sample_interval,capture_duration)
	ps.setSimpleTrigger(trigSrc="B", threshold_V=-0.320, direction='Falling',
							 timeout_ms=10, enabled=True,delay=120)
	max_samples_per_segment = ps.memorySegments(n_captures)
	samples_per_segment = int(capture_duration / sample_interval)
	ps.setNoOfCaptures(n_captures)


	start_t = time.time()
	blocks = []
	ps.runBlock()
	dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
	dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
	try:
		while True:
			if ps.isReady():
				t0 = time.time()
				ps.stop()
				ps.getDataRawBulk(channel='A',data=dataA)
				ps.getDataRawBulk(channel='B',data=dataB)
				t1 = time.time()
				dataA1=dataA[:, 0:ps.noSamples]
				dataB1=dataB[:, 0:ps.noSamples]
				blocks.append([dataA1,dataB1,t0,t1])

				ps.runBlock()
				print(t0-start_t)

	except KeyboardInterrupt:
		pass

	ps.close()
