import numpy as np
import time

class PS3000a():
	noSamples=-1
	ChA_VRange = 1
	ChB_VRange = 1
	def __init__(self):
		pass
	def open(self):
		pass
	def close(self):
		pass
	def setChannel(self, channel='B',coupling='DC',VRange=1,VOffset=0):
		if channel == "B":
			self.ChB_VRange = VRange
		else:
			self.ChA_VRange = VRange
		#print('chrange:',channel,self.ChA_VRange,self.ChB_VRange)
	def setSamplingInterval(self,a,b):
		pass
	def setSimpleTrigger(self, trigSrc="External", threshold_V=0.020, direction='Rising',
							 timeout_ms=5, enabled=True):
		pass
	def memorySegments(self,n_captures):
		return 100
	def setNoOfCaptures(self,n_captures):
		pass
	def runBlock(self):
		pass
	def waitReady(self):
		time.sleep(0.03)
	def getDataRawBulk(self,channel='B',data=np.zeros(100)):
		data[:]=np.random.normal(1,10,100)
	def rawToV(self, channel="B", dataRaw=np.zeros(100)):
		k = 1
		dataRaw = dataRaw.astype(np.float)

		if channel == "B":
			k = self.ChB_VRange
		else:
			k = self.ChA_VRange
		#print('chrange:',channel,self.ChA_VRange,self.ChB_VRange)
		return dataRaw*k


class ps3000a():
	def __init__(self):
		pass
	def PS3000a(connect=False):
		return PS3000a()
