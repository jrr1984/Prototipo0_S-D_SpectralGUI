# coding= latin-1

import numpy
from scipy.signal import argrelextrema
from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
import time

class MultiChannelAnalogInput():
	"""Class to create a multi-channel analog input

	Usage: AI = MultiChannelInput(physicalChannel)
		physicalChannel: a string or a list of strings
	optional parameter: limit: tuple or list of tuples, the AI limit values
						reset: Boolean
	Methods:
		read(name), return the value of the input name
		readAll(), return a dictionary name:value
	"""
	def __init__(self,physicalChannel, limit = None, reset = False):
		if type(physicalChannel) == type(""):
			self.physicalChannel = [physicalChannel]
		else:
			self.physicalChannel  =physicalChannel
		self.numberOfChannel = physicalChannel.__len__()
		if limit is None:
			self.limit = dict([(name, (-10.0,10.0)) for name in self.physicalChannel])
		elif type(limit) == tuple:
			self.limit = dict([(name, limit) for name in self.physicalChannel])
		else:
			self.limit = dict([(name, limit[i]) for  i,name in enumerate(self.physicalChannel)])
		if reset:
			DAQmxResetDevice(physicalChannel[0].split('/')[0] )
	def configure(self):
		# Create one task handle per Channel
		taskHandles = dict([(name,TaskHandle(0)) for name in self.physicalChannel])
		for name in self.physicalChannel:
			DAQmxCreateTask("",byref(taskHandles[name]))
			DAQmxCreateAIVoltageChan(taskHandles[name],name,"",DAQmx_Val_Cfg_Default,
									 self.limit[name][0],self.limit[name][1],
									 DAQmx_Val_Volts,None)
			DAQmxCfgDigEdgeStartTrig(taskHandles[name], "PFI0", DAQmx_Val_Rising);
			DAQmxCfgSampClkTiming(taskHandles[name],"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)
		self.taskHandles = taskHandles
	def readAll(self):
		return self.read(self.physicalChannel[0])#dict([(name,self.read(name)) for name in self.physicalChannel])
	def read(self,name = None):
		if name is None:
			name = self.physicalChannel[0]
		taskHandle = self.taskHandles[name]
		DAQmxStartTask(taskHandle)
		data = numpy.zeros((400,), dtype=numpy.float64)
#        data = AI_data_type()
		read = int32()

		DAQmxReadAnalogF64(taskHandle,200,10.0,DAQmx_Val_GroupByChannel,data,400,byref(read),None)
		DAQmxStopTask(taskHandle)
		return data

	def getData(self,DATA_SHIFT=6):
		#self.configure()
		start=time.time()
		data=self.readAll()
		print("|",time.time()-start)

		data_ = [data[:(len(data)//2)], data[(len(data)//2):]]
		#print(data['Dev1/ai0,Dev1/ai2'].shape)
		d = data_[1][DATA_SHIFT:]
		r = data_[0][0:-DATA_SHIFT]
		w = r>r.mean()
		out = abs(d[w].mean()-d[~w].mean())

		print("|",time.time()-start,out)
		return out

def find_shift(data1,data2):

	s=[]
	for i in range(1,100):
		s.append([i,abs(sum(data1[:-i]/data2[i:]))])
	s=np.array(s)
	figure()
	plot(s[:,0],s[:,1])
	show(0)
	# for local minima
	m = argrelextrema(s[:,1], np.less)[0]
	print(">",s[m[0],0],m[0])
	return s[m[0],0]

if __name__ == '__main__':
	import time
	multipleAI = MultiChannelAnalogInput(["Dev1/ai0,Dev1/ai2"])
	multipleAI.configure()
	start=time.time()
	print("dt:",multipleAI.getData())
	print(time.time()-start)
	data=multipleAI.readAll()
	from pylab import *

	data_ = [data[:(len(data)//2)], data[(len(data)//2):]]
	plot(data_[0][:-6],'-b')
	plot(data_[1][6:],'-r')
	find_shift(data_[0],data_[1])
	show()
	print(data)
