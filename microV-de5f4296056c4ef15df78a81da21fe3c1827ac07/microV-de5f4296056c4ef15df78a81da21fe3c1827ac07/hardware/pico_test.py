# -*- coding: utf-8
# Example by Colin O'Flynn
#
import time
import numpy as np
from picoscope import ps3000a

from matplotlib.mlab import find


class freqMeasure():
	def __init__(self):
		self.ps = ps3000a.PS3000a(connect=False)

	def openScope(self):
		self.ps.open()

		self.ps.setChannel("A")
		self.ps.setChannel("B")
		res = self.ps.setSamplingInterval(0.00001,0.005)

		self.sampleRate = res[0]

		# Use external trigger to mark when we sample
		#self.ps.setSimpleTrigger(trigSrc="A", threshold_V=0.10,
		#						 timeout_ms=500)

	def closeScope(self):
		self.ps.close()

	def armMeasure(self):
		self.ps.runBlock()

	def freq_from_crossings(self, sig):
		"""Estimate frequency by counting zero crossings"""
		# From https://gist.github.com/endolith/255291:

		fs = self.sampleRate

		# Find all indices right before a rising-edge zero crossing
		indices = find((sig[1:] >= 0) & (sig[:-1] < 0))
		# More accurate, using linear interpolation to find intersample
		# zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
		crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]
		# Some other interpolation based on neighboring points might be better.
		# Spline, cubic, whatever
		return fs / np.mean(np.diff(crossings))

	def measure(self):
		#print("Waiting for trigger")
		while(self.ps.isReady() is False):
			time.sleep(0.0001)
		#print("Sampling Done")
		data = self.ps.getDataV("A")
		data1 = self.ps.getDataV("B")
		w = data>data.mean()
		a = data[w].mean()-data[~w].mean()
		b = data1[w].mean()-data1[~w].mean()
		#data = data - np.mean(data)
		#freq = self.freq_from_crossings(data)

		return a,b


if __name__ == "__main__":
	fm = freqMeasure()
	fm.openScope()

	try:
		while 1:
			start = time.time()
			fm.armMeasure()
			r=fm.measure()
			print(time.time()-start,r)
	except KeyboardInterrupt:
		pass

	fm.closeScope()
