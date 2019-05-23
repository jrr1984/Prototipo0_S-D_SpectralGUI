from ni import *
from CCS200 import *
from E727 import *
from pylab import *
get_ipython().run_line_magic('matplotlib', 'qt')
import time
import threading
data = zeros((100,100))

e = E727()	
print(e.ConnectUSB())
print(e.qSAI())
print(e.SVO())
print(e.MOV(0,axis=1,waitUntilReady=True))
time.sleep(0.2)
print(e.MOV(0,axis=2,waitUntilReady=True))
time.sleep(0.2)
print(e.MOV(0,axis=3,waitUntilReady=True))
time.sleep(1)
print('start')
fig, ax = plt.subplots()
step = 2
im = ax.matshow(data[::step,::step])
show(0)

spectrometer = CCS200()
print(spectrometer.init())
print(spectrometer.setIntegrationTime(0.01))

def plot_data():

	ax.matshow(data[::step,::step])
	#draw()
	#pause(0.1)


forward = True
try:
	for i in range(0,100,step):

		if forward:
			Range = range(0,100,step)
			forward = False
		else:
			Range = range(100-step,-step,-step)
			forward = True
		for j in Range:

			r = e.MOV(j,axis=1,waitUntilReady=True)
			if not r: break
			#time.sleep(1)
			
			spectrometer.startScanExtTrg()
			spectrometer.getDeviceStatus()
			d = spectrometer.getScanData()

			data[i,j] = d[1550:1570].sum()
			print(i,j,d[1550:1570].sum())

		r = e.MOV(i,axis=2,waitUntilReady=True)
		if not r: break
		#t = threading.Thread(target=plot_data)
		#t.start()
		ax.matshow(data[::step,::step])
		pause(0.01)
except KeyboardInterrupt:
	e.CloseConnection()
	print(spectrometer.close())

print(spectrometer.close())
print(e.CloseConnection())
ax.matshow(data[::step,::step])
savefig(str(round(time.time()))+".png")




