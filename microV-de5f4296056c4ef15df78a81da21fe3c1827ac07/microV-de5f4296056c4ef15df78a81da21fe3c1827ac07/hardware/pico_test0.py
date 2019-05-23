import matplotlib.pyplot as plt
import numpy as np
import time

from picoscope import ps3000a

ps = ps3000a.PS3000a()

# now = time.strftime("%Y%m%d_%H%M%S")
# filename = "sweep_" + now + ".swp"
# output_file = open(filename, "wb")

c = 3e8

# rapid block mode

ps.setChannel("A", coupling="DC", VRange=0.2)

n_captures = 10
ps.setSamplingInterval(200e-9,15e-6)
ps.setSimpleTrigger(trigSrc="External", threshold_V=0.020, direction='Rising',
						 timeout_ms=5, enabled=True)
samples_per_segment = ps.memorySegments(n_captures)
ps.setNoOfCaptures(n_captures)


for r in range(5):
	data = np.zeros((n_captures, samples_per_segment), dtype=np.int16)

	t1 = time.time()

	ps.runBlock()
	ps.waitReady()

	t2 = time.time()
	print("Time to get sweep: " + str(t2 - t1))

	ps.getDataRawBulk(data=data)

	t3 = time.time()
	print("Time to read data: " + str(t3 - t2))

	for d in data[:, 0:ps.noSamples]:
		plt.plot(d)

	plt.show(0)



ps.close()
