#from PyDAQmx import *
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
#from pylab import *
import ctypes
# Declaration of variable passed by reference
def read_ni():
	#taskHandle = TaskHandle()
	#read = int32()
	data = np.sin(np.arange(0,100,0.1)) #np.zeros((1000,), dtype=np.float64)
	data = (data>0)*2.5
	data1 = np.sin(np.arange(0,100,0.1))/100
	'''
	try:
		# DAQmx Configure Code
		DAQmxCreateTask("",ctypes.byref(taskHandle))
		DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai0","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
		DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)
		DAQmxCfgDigEdgeStartTrig(taskHandle, "PFI0", DAQmx_Val_Rising);
		# DAQmx Start Code
		DAQmxStartTask(taskHandle)

		# DAQmx Read Code
		DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data,1000,ctypes.byref(read),None)

		#print( "Acquired %d points"%read.value)
	except DAQError as err:
		print( "DAQmx Error: %s"%err)
	finally:
		if taskHandle:
			# DAQmx Stop Code
			DAQmxStopTask(taskHandle)
			DAQmxClearTask(taskHandle)

	taskHandle = TaskHandle()
	read = int32()
	data1 = np.zeros((1000,), dtype=np.float64)

	try:
		# DAQmx Configure Code
		DAQmxCreateTask("",ctypes.byref(taskHandle))
		DAQmxCreateAIVoltageChan(taskHandle,"Dev1/ai1","",DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None)
		DAQmxCfgDigEdgeStartTrig(taskHandle, "PFI0", DAQmx_Val_Rising);
		DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)

		# DAQmx Start Code
		DAQmxStartTask(taskHandle)

		# DAQmx Read Code
		DAQmxReadAnalogF64(taskHandle,1000,10.0,DAQmx_Val_GroupByChannel,data1,1000,ctypes.byref(read),None)

		#print( "Acquired %d points"%read.value)
	except DAQError as err:
		print( "DAQmx Error: %s"%err)
	finally:
		if taskHandle:
			# DAQmx Stop Code
			DAQmxStopTask(taskHandle)
			DAQmxClearTask(taskHandle)
	'''

	return data,data1

def find_shift(show_graph=False):

	res = read_ni()
	s=[]
	for i in range(1,100):
		s.append([i,abs(sum(res[0][:-i]/res[1][i:]))])
	s=np.array(s)
	if show_graph:
		plt.plot(s[:,0],s[:,1])
		plt.show(0)
	# for local minima
	m = argrelextrema(s[:,1], np.less)[0]
	print(">",s[m[1],0])
	return s[m[1],0]



def proc_data(DATA_SHIFT=7,show_graph=False):
	res = read_ni()
	d = res[1][DATA_SHIFT:]
	r = res[0][0:-DATA_SHIFT]
	w = r>r.mean()
	out = abs(d[w].mean()-d[~w].mean())
	if show_graph:
		plt.figure()
		plt.plot(d*100)
		plt.plot(r)
		plt.show()
	return abs(out*np.random.normal())

if __name__ == "__main__":

	find_shift()
	DATA_SHIFT = int(find_shift(show_graph=True))
	print(proc_data(DATA_SHIFT=DATA_SHIFT,show_graph=True))
