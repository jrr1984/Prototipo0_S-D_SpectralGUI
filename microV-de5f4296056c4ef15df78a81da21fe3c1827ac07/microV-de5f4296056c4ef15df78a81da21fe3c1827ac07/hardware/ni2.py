import pprint
import nidaqmx
import time
from nidaqmx.constants import AcquisitionType, TaskMode

pp = pprint.PrettyPrinter(indent=4)

for j in range(10):

	with nidaqmx.Task() as master_task:
		#master_task = nidaqmx.Task()
		master_task.ai_channels.add_ai_voltage_chan("Dev1/ai0,Dev1/ai2,Dev1/ai3")

		master_task.timing.cfg_samp_clk_timing(
			100000, sample_mode=AcquisitionType.FINITE)

		#master_task.control(TaskMode.TASK_COMMIT)

		master_task.triggers.start_trigger.cfg_anlg_edge_start_trig("Dev1/ai0",trigger_level=1.5)


		master_task.start()
		start = time.time()
		#for i in range(100):
		master_data = master_task.read(number_of_samples_per_channel=300)

		r,d,d1 = master_data
		#pp.pprint(master_data)
		print(time.time()-start,master_task.is_task_done())
		#master_task.close()
		#from pylab import *
		#plot(r[:-6],'-b')
		#plot(d[6:],'-r')
		#how(0)
