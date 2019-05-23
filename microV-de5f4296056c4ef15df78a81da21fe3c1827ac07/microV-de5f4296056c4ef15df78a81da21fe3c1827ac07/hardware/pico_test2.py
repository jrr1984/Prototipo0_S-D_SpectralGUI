


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import time
import sys

from picoscope import ps3000a


ps = ps3000a.PS3000a(connect=False)
ps.open()
n_captures = 100
ps.setChannel("A", coupling="DC", VRange=0.1)
ps.setChannel("B", coupling="DC", VRange=0.1)
ps.setSamplingInterval(200e-9,93e-3)
ps.setSimpleTrigger(trigSrc="External", threshold_V=0.020, direction='Rising',
						 timeout_ms=5, enabled=True)
samples_per_segment = ps.memorySegments(n_captures)
ps.setNoOfCaptures(n_captures)


dataA = []
dataB = []
liveA = []
liveB = []

dataA = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
dataB = np.zeros((n_captures, samples_per_segment), dtype=np.int16)
t1 = time.time()
ps.runBlock()
ps.waitReady()
t2 = time.time()
print("Time to get sweep: " + str(t2 - t1))
ps.getDataRawBulk(channel='A',data=dataA)
ps.getDataRawBulk(channel='B',data=dataB)
t3 = time.time()
print("Time to read data: " + str(t3 - t2))
dataA=dataA[:, 0:ps.noSamples].mean(axis=0)
dataB=dataB[:, 0:ps.noSamples].mean(axis=0)


ps.close()
