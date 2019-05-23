import sys,time,os
os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'
import qdarkstyle
from pyqtgraph.Qt import QtGui, QtCore, uic
import pyqtgraph as pg
import numpy as np
from scipy.signal import medfilt
from scipy.signal import argrelextrema
import scipy.misc
import matplotlib
from skimage.external.tifffile import imsave

if len(sys.argv)>1:
	if sys.argv[1] == 'sim':
		from hardware.sim.CCS200 import *
		from hardware.sim.ni import *
		from hardware.sim.E727 import *
		from hardware.sim.TDC001 import *
		from hardware.sim.picoscope import ps3000a
		from hardware.sim.AG_UC2 import AG_UC2
		import picopy
		#from hardware.sim.PM100 import visa
else:
	from hardware.ni1 import *
	from hardware.CCS200 import *
	from hardware.E727 import *
	from hardware.TDC001 import *
	from nidaqmx.constants import AcquisitionType, TaskMode
	import nidaqmx
	from picoscope import ps3000a
	from hardware.AG_UC2 import AG_UC2
	import visa
	from ThorlabsPM100 import ThorlabsPM100
	import picopy

from hardware.pico_radar import fastScan

#get_ipython().run_line_magic('matplotlib', 'qt')

import traceback
from multiprocessing import Process, Queue


class microV(QtGui.QMainWindow):
	data = []
	alive = True
	piStage = E727()
	spectrometer = CCS200()
	HWP = APTMotor(83854487, HWTYPE=31)
	rotPiezoStage = AG_UC2()
	#ps = ps3000a.PS3000a(connect=False)
	ps = None
	n_captures = None
	#inst = visa.instrument('USB0::0x0000::0x0000::DG5Axxxxxxxxx::INSTR', term_chars='\n', timeout=1)
	power_meter = None#ThorlabsPM100(inst=inst)
	#DAQmx = nidaqmx.Task()
	#DAQmx = MultiChannelAnalogInput(["Dev1/ai0,Dev1/ai2"])
	live_pmt = []
	live_pmt1 = []
	live_x = []
	live_y = []
	live_integr_spectra = []
	pico_VRange_dict = {"Auto":20.0,'20mV':0.02,'50mV':0.05,'100mV':0.1,
			'200mV':0.2,'500mV':0.5,'1V': 1.0, '2V': 2.0,
			'5V': 5.0, '10V': 10.0, '20V': 20.0,}

	processOut = Queue()
	def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)
		#from mainwindow import Ui_mw
		self.ui = uic.loadUi("microV.ui")#Ui_mw()
		self.ui.closeEvent = self.closeEvent
		self.ui.show()
		self._want_to_close = False
		self.initPiStage()
		#self.initSpectrometer()
		self.initHWP()
		#self.initPico()
		#self.initDAQmx()

		self.calibrTimer = QtCore.QTimer()
		self.initUI()

		#self.scan_image()
	############################################################################
	###############################   DAQmx	#################################
	def connect_DAQmx(self,state):
		if state:
			self.initDAQmx()
		else:
			try:
				self.DAQmx.close()
			except:
				traceback.print_exc()

	def initDAQmx(self):
		self.DAQmx.ai_channels.add_ai_voltage_chan("Dev1/ai0,Dev1/ai2,Dev1/ai3", max_val=10, min_val=-10)
		self.DAQmx.timing.cfg_samp_clk_timing(10000, sample_mode=AcquisitionType.CONTINUOUS)
		self.DAQmx.control(TaskMode.TASK_COMMIT)
		self.DAQmx.triggers.start_trigger.cfg_anlg_edge_start_trig("Dev1/ai0",trigger_level=1.5)

		#self.DAQmx.configure()

	def readDAQmx(self,preview=False,print_dt=False):
		start = time.time()
		with nidaqmx.Task() as master_task:
			#master_task = nidaqmx.Task()
			master_task.ai_channels.add_ai_voltage_chan("Dev1/ai0,Dev1/ai2,Dev1/ai3", max_val=10, min_val=-10)
			master_task.timing.cfg_samp_clk_timing(
				100000, sample_mode=AcquisitionType.FINITE)
			master_task.control(TaskMode.TASK_COMMIT)
			master_task.triggers.start_trigger.cfg_dig_edge_start_trig("PFI0")
			master_task.start()
			#start = time.time()
			for i in range(100):
				master_data = master_task.read(number_of_samples_per_channel=1000)
				if master_task.is_task_done():
					break
			r,d,d1 = master_data
			#pp.pprint(master_data)
			#print(time.time()-start,master_task.is_task_done())
		r,d,d1 = master_data
		r = np.array(r)
		d = np.array(d)
		d1 = np.array(d1)

		d = d[int(self.ui.DAQmx_shift.value()):]
		d1 = d1[int(self.ui.DAQmx_shift.value()):]
		r = r[0:int(-self.ui.DAQmx_shift.value())]
		if self.ui.DAQmx_preview.isChecked():
			self.line_DAQmx_sig.setData(d)
			self.line_DAQmx_sig1.setData(d1)
			self.line_DAQmx_ref.setData(r)

		#pp.pprint(master_data)
		if print_dt:
			print("readDAQmx(tdiff):\n", time.time()-start)

		w = r>r.mean()
		out = abs(d[w].mean()-d[~w].mean())
		out1 = abs(d1[w].mean()-d1[~w].mean())
		print(time.time()-start,i)

		return out, out1

	def optimizeDAQmx(self):
		start = time.time()
		with nidaqmx.Task() as master_task:
			#master_task = nidaqmx.Task()
			master_task.ai_channels.add_ai_voltage_chan("Dev1/ai0,Dev1/ai2,Dev1/ai3", max_val=10, min_val=-10)

			master_task.timing.cfg_samp_clk_timing(
				100000, sample_mode=AcquisitionType.FINITE)

			master_task.control(TaskMode.TASK_COMMIT)

			master_task.triggers.start_trigger.cfg_dig_edge_start_trig("PFI0")


			master_task.start()
			#start = time.time()
			for i in range(100):
				master_data = master_task.read(number_of_samples_per_channel=1000)
				if master_task.is_task_done():
					break
			r,d,d1 = master_data
			#pp.pprint(master_data)
			#print(time.time()-start,master_task.is_task_done())
		r = np.array(r)
		d = np.array(d)
		data_shift = 0
		shift_array = []
		for data_shift in range(len(r)//2):
			d_ = d[int(data_shift):]
			r_ = r[0:int(-data_shift)]
			w = r_>r_.mean()
			out = abs(d_[w].mean()-d_[~w].mean())
			shift_array.append(out)


		shift_array = np.array(shift_array)
		self.line_DAQmx_ref.setData(shift_array)
		m = argrelextrema(shift_array, np.greater)[0]
		#pp.pprint(master_data)
		print("optimizeDAQmx(tdiff):\n", time.time()-start,m)
		self.ui.DAQmx_shift.setValue(m[1])

		return m

	############################################################################
	###############################   Picoscope	#############################

	def connect_pico(self,state):
		if state:
			self.initPico()
		else:
			try:
				self.ps.close()
			except:
				traceback.print_exc()

	def pico_set(self):
		self.n_captures = self.ui.pico_n_captures.value()

		ChA_VRange = self.ui.pico_ChA_VRange.currentText()
		#ChA_VRange = self.pico_VRange_dict[ChA_VRange]

		ChA_Offset = self.ui.pico_ChA_offset.value()

		ChB_VRange = self.ui.pico_ChB_VRange.currentText()
		#ChB_VRange = self.pico_VRange_dict[ChB_VRange]
		ChB_Offset = self.ui.pico_ChB_offset.value()

		self.ps.setChannel("A", coupling="DC", VRange=ChA_VRange, VOffset=ChA_Offset)
		self.ps.setChannel("B", coupling="DC", VRange=ChB_VRange, VOffset=ChB_Offset)

		sampleInterval = float(self.ui.pico_sampleInterval.text())
		samplingDuration = float(self.ui.pico_samplingDuration.text())
		self.ps.setSamplingInterval(sampleInterval,samplingDuration)

		trigSrc = self.ui.pico_TrigSource.currentText()
		if trigSrc == 'External':
			trigSrc = 'ext'
		threshold_V = self.ui.pico_TrigThreshold.value()
		direction = self.ui.pico_Trig_mode.currentText().upper()
		self.pico_pretrig = float(self.ui.pico_pretrig.text())
		self.ps.setSimpleTrigger(trigSrc=trigSrc, threshold_V=threshold_V, direction=direction,
								 timeout_ms=5, enabled=True)
		#self.samples_per_segment = self.ps.memorySegments(self.n_captures)
		#self.ps.setNoOfCaptures(self.n_captures)
		#print(self.n_captures)

	def initPico(self):

		#self.ps.open()
		self.ps = picopy.Pico3k()
		self.pico_set()

	def readPico(self):
		#dataA = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		#dataB = np.zeros((self.n_captures, self.samples_per_segment), dtype=np.int16)
		#t1 = time.time()
		#self.ps.runBlock()
		r = self.ps.capture_prep_block( pre_trigger=self.pico_pretrig, number_of_frames=self.n_captures, downsample=2, downsample_mode='NONE',
			return_scaled_array=1)
		dataA = r[0]['A']
		dataB = r[0]['B']
		scanT = r[1]


		if self.ui.raw_data_preview.isChecked():
			self.line_pico_ChA.setData(dataA.mean(axis=0))
			self.line_pico_ChB.setData(dataB.mean(axis=0))

		if self.ui.pico_AutoRange.isChecked():

			indexChA = self.ui.pico_ChA_VRange.currentIndex()
			ChA_VRange = pico_VRange_dict[self.ui.pico_ChA_VRange.currentText()]
			if abs(dataA.min())> ChA_VRange*0.9 and indexChA<8:
				indexChA += 1

			self.ui.pico_ChA_VRange.setCurrentIndex(indexChA)
			ChA_VRange = self.ui.pico_ChA_VRange.currentText()
			#print('AutoA',ChA_VRange)
			ChA_Offset = self.ui.pico_ChA_offset.value()
			self.ps.setChannel(channel="A", coupling="DC", VRange=ChA_VRange, VOffset=ChA_Offset)



			indexChB = self.ui.pico_ChB_VRange.currentIndex()
			ChB_VRange = pico_VRange_dict[self.ui.pico_ChB_VRange.currentText()]
			if abs(dataB.min())> ChB_VRange*0.9 and indexChB<8:
				indexChB += 1

			self.ui.pico_ChB_VRange.setCurrentIndex(indexChB)

			ChB_VRange = self.ui.pico_ChB_VRange.currentText()
			#ChB_VRange = self.pico_VRange_dict[ChB_VRange]
			ChB_Offset = self.ui.pico_ChB_offset.value()
			self.ps.setChannel(channel="B", coupling="DC", VRange=ChB_VRange, VOffset=ChB_Offset)

		#dataA = self.ps.rawToV(channel="A", dataRaw=dataA)
		#dataB = self.ps.rawToV(channel="B", dataRaw=dataB)

		dataA_p2p = abs(dataA.max() - dataA.min())
		dataB_p2p = abs(dataB.max() - dataB.min())

		self.ui.pico_ChA_value.setText(str(round(dataA_p2p,8)))
		self.ui.pico_ChB_value.setText(str(round(dataB_p2p,8)))

		return dataA_p2p, dataB_p2p

	############################################################################
	###############################   Powermeter     ###########################
	###############################   Thorlabs PM100 ###########################

	def connect_powermeter(self,state):
		if state:
			self.initPowermeter()
		else:
			try:
				self.ps.close()
			except:
				traceback.print_exc()

	def powermeter_set(self):
		pass

	def initPowermeter(self):
		pass
		#self.pico_set()

	def readPower(self):
		pass

	############################################################################
	###############################   HWP	###################################

	def initHWP(self):
		pos = self.HWP.getPos()
		self.ui.HWP_angle.setText(str(round(pos,6)))

	def HWP_go(self):
		to_angle = self.ui.HWP_move_to_angle.value()
		self.HWP.mAbs(to_angle)
		pos = self.HWP.getPos()
		self.ui.HWP_angle.setText(str(round(pos,6)))

	def HWP_go_home(self):
		self.HWP.go_home()
		pos = self.HWP.getPos()
		self.ui.HWP_angle.setText(str(round(pos,6)))

	def HWP_negative_step(self):
		to_angle = -self.ui.HWP_rel_step.value()
		self.HWP.mRel(to_angle)
		pos = self.HWP.getPos()
		self.ui.HWP_angle.setText(str(round(pos,6)))
	def HWP_positive_step(self):
		to_angle = self.ui.HWP_rel_step.value()
		self.HWP.mRel(to_angle)
		pos = self.HWP.getPos()
		self.ui.HWP_angle.setText(str(round(pos,6)))

	############################################################################
	###############################   PiNanoCube	############################

	def initPiStage(self):
		print(self.piStage.ConnectUSB())
		print(self.piStage.qSAI())
		print(self.piStage.SVO(b'1 2 3', [True, True, True]))

		#print(self.piStage.MOV(self.ui.Pi_X_move_to.value(),axis=1,waitUntilReady=True))
		time.sleep(0.2)
		#print(self.piStage.MOV(self.ui.Pi_X_move_to.value(),axis=2,waitUntilReady=True))
		#time.sleep(0.2)
		#print(self.piStage.MOV(self.ui.Pi_X_move_to.value(),axis=3,waitUntilReady=True))
		pos = self.piStage.qPOS()
		self.setUiPiPos(pos=pos)
		time.sleep(1)

	def setUiPiPos(self,pos):
		self.ui.Pi_XPos.setText(str(pos[0]))
		self.ui.Pi_YPos.setText(str(pos[1]))
		self.ui.Pi_ZPos.setText(str(pos[2]))

	def Pi_X_go(self):
		pos = self.ui.Pi_X_move_to.value()
		print(self.piStage.MOV(pos,axis=1,waitUntilReady=True))
		pos = self.piStage.qPOS()
		self.setUiPiPos(pos=pos)

	def Pi_Y_go(self):
		pos = self.ui.Pi_Y_move_to.value()
		print(self.piStage.MOV(pos,axis=2,waitUntilReady=True))
		pos = self.piStage.qPOS()
		self.setUiPiPos(pos=pos)

	def Pi_Z_go(self):
		pos = self.ui.Pi_Z_move_to.value()
		print(self.piStage.MOV(pos,axis=3,waitUntilReady=True))
		pos = self.piStage.qPOS()
		self.setUiPiPos(pos=pos)

	def Pi_XYZ_50mkm(self):
		print(self.piStage.MOV(50,axis=1,waitUntilReady=True))
		time.sleep(0.2)
		print(self.piStage.MOV(50,axis=2,waitUntilReady=True))
		time.sleep(0.2)
		print(self.piStage.MOV(50,axis=3,waitUntilReady=True))
		pos = self.piStage.qPOS()
		self.setUiPiPos(pos=pos)
		time.sleep(1)
	def Pi_autoZero(self):
		print(self.piStage.ATZ())
		pos = self.piStage.qPOS()
		self.setUiPiPos(pos=pos)

	def Pi_Set(self):
		vel = self.ui.Pi_Velocity.value()
		self.piStage.VEL([vel]*3,b'1 2 3')
		print('VEL:',self.piStage.qVEL())
	############################################################################
	###############################   rotPiezoStage	#########################

	def connect_rotPiezoStage(self,state):
		if state:
			self.rotPiezoStage.connect()
		else:
			self.rotPiezoStage.close()
	def rotPiezoStage_Go(self):
		toAngle = self.ui.rotPiezoStage_Step.value()
		wait = self.ui.rotPiezoStage_wait.isChecked()
		self.rotPiezoStage.move(toAngle,waitUntilReady=wait)
		self.ui.rotPiezoStage_Angle.setText(str(self.rotPiezoStage.getAngle()))

	############################################################################
	###############################   Spectrometer	##########################

	def initSpectrometer(self):
		print(self.spectrometer.init())
		print(self.spectrometer.setIntegrationTime(self.ui.usbSpectr_integr_time.value()))
	def usbSpectr_set_integr_time(self):
		print(self.spectrometer.setIntegrationTime(self.ui.usbSpectr_integr_time.value()))

	def getSpectra(self):
		self.spectrometer.startScanExtTrg()
		#self.spectrometer.getDeviceStatus()
		data = self.spectrometer.getScanData()
		return data

	############################################################################
	###############################   scan3D	################################

	def scan3D_path_dialog(self):
		fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', self.ui.scan3D_path.text())
		if type(fname)==tuple:
			fname = fname[0]
		try:
			self.ui.scan3D_path.setText(fname)
		except:
			traceback.print_exc()
	def startCalibr(self,state):
		if state:
			self.calibrTimer.start(self.ui.usbSpectr_integr_time.value()*2000)
			self.live_pmt = []
			self.live_pmt1 = []
			self.live_x = []
			self.live_y = []

			self.live_integr_spectra = []
		else:
			self.calibrTimer.stop()

	def onCalibrTimer(self):
		self.calibrTimer.stop()
		spectra = np.zeros(3648)#self.getSpectra()
		pmt_val,pmt_val1 = self.readPico()#self.readDAQmx(print_dt=True)
		self.live_pmt.append(pmt_val)
		self.live_pmt1.append(pmt_val1)
		if len(self.live_pmt)>800:
			self.live_pmt.pop(0)
		if len(self.live_pmt1)>800:
			self.live_pmt1.pop(0)
		s_from = self.ui.usbSpectr_from.value()
		s_to = self.ui.usbSpectr_to.value()
		self.live_integr_spectra.append(np.sum(spectra[s_from:s_to])/1000)
		#setLine(spectra)
		self.line_pmt.setData(self.live_pmt)
		self.line_pmt1.setData(self.live_pmt1)
		#self.line_spectra.setData(self.live_integr_spectra)

		self.calibrTimer.start(self.ui.usbSpectr_integr_time.value()*2000)
		app.processEvents()
	def test(self,q):
		for i in range(100):
			real_position = [round(p,4) for p in self.piStage.qPOS()]
			q.put(real_position)
			print()
			time.sleep(0.1)
		print('done')

	def start3DScan(self, state):
		print(state)
		if state:
			try:
				self.live_pmt = []
				self.live_pmt1 = []
				self.live_x = []
				self.live_y = []

				self.scan3DisAlive = True
				self.scan3D()

			except:
				traceback.print_exc()
		else:
			self.live_pmt = []
			self.live_pmt1 = []
			self.live_x = []
			self.live_y = []

			self.scan3DisAlive = False

	def scan3D(self):
		wait = self.ui.Pi_wait.isChecked()
		path = self.ui.scan3D_path.text()
		if "_" in path:
			path = "".join(path.split("_")[:-1])#+"_"+str(round(time.time()))
		else:
			path = path #+ "_"+str(round(time.time()))

		self.ui.scan3D_path.setText(path)
		spectra_range = [self.ui.usbSpectr_save_from.value(),self.ui.usbSpectr_save_to.value()]
		try:
			z_start = float(self.ui.scan3D_config.item(0,1).text())
			z_end = float(self.ui.scan3D_config.item(0,2).text())
			z_step = float(self.ui.scan3D_config.item(0,3).text())
			if z_step == 0:
				Range_z = np.array([z_start]*1000)
			else:
				Range_z = np.arange(z_start,z_end,z_step)
			Range_zi = np.arange(len(Range_z))
			y_start = float(self.ui.scan3D_config.item(1,1).text())
			y_end = float(self.ui.scan3D_config.item(1,2).text())
			y_step = float(self.ui.scan3D_config.item(1,3).text())

			Range_y = np.arange(y_start,y_end,y_step)
			Range_yi = np.arange(len(Range_y))


			x_start = float(self.ui.scan3D_config.item(2,1).text())
			x_end = float(self.ui.scan3D_config.item(2,2).text())
			x_step = float(self.ui.scan3D_config.item(2,3).text())

			Range_x = np.arange(x_start,x_end,x_step)
			Range_xi = np.arange(len(Range_x))
			data_pmt = np.zeros((len(Range_z),len(Range_xi),len(Range_yi)))
			data_pmt1 = np.zeros((len(Range_z),len(Range_xi),len(Range_yi)))
			layerIndex = 0
			for z,zi in zip(Range_z,Range_zi):
				if not self.scan3DisAlive: break
				print(self.piStage.MOV(z,axis=3,waitUntilReady=True))
				#time.sleep(0.1)

				fname = path+"Z"+str(z)+"_"+str(round(time.time()))+'.txt'
				with open(fname,'a') as f:
					f.write("#X\tY\tZ\tpmt_signal\tpmt1_signal\tspectra_px[" +
						str(spectra_range[0]) + ":"+
						str(spectra_range[1]) +"]\n")



				data_spectra = np.zeros((len(Range_yi),len(Range_xi)))


				forward = True
				for y,yi in zip(Range_y,Range_yi):
					if not self.scan3DisAlive: break
					Range_x_tmp = Range_x
					if forward:
						Range_x_tmp = Range_x[::-1]
						Range_xi_tmp = Range_xi[::-1]
						forward = False
					else:
						Range_x_tmp = Range_x
						Range_xi_tmp = Range_xi
						forward = True
					r = self.piStage.MOV(y,axis=2,waitUntilReady=True)
					if not r: break
					self.live_pmt = []
					self.live_pmt1 = []
					self.live_x = []
					self.live_y = []

					self.live_integr_spectra = []
					for x,xi in zip(Range_x_tmp, Range_xi_tmp):

						start=time.time()
						#print('Start',start)
						if not self.scan3DisAlive: break
						r = self.piStage.MOV([x],axis=b'1',waitUntilReady=wait)
						if not r: break

						real_position0 = [round(p,6) for p in self.piStage.qPOS()]
						pmt_val, pmt_val1 = self.readPico()
						real_position = [round(p,6) for p in self.piStage.qPOS()]
						self.live_pmt.append(pmt_val)
						self.live_pmt1.append(pmt_val1)
						self.live_x.append(np.mean([real_position0[0],real_position[0]]))
						self.live_y.append(np.mean([real_position0[1],real_position[1]]))

						spectra = np.zeros(3648)
						dataSet = real_position +[pmt_val,pmt_val1]# + spectra[spectra_range[0]:spectra_range[1]]
						#print(dataSet[-1])
						with open(fname,'a') as f:
							f.write("\t".join([str(i) for i in dataSet])+"\n")
						#print(time.time()-start)
						s_from = self.ui.usbSpectr_from.value()
						s_to = self.ui.usbSpectr_to.value()
						#print(data_spectra.shape,yi,xi)
						if wait:
							xi_ = xi
							yi_ = yi
						else:
							xi_ = int(round((self.live_x[-1]-Range_x[0])*len(Range_xi_tmp)/(Range_x_tmp.max()-Range_x_tmp.min())))
							yi_ = int(round((self.live_y[-1]-Range_y[0])*len(Range_yi)/(Range_y.max()-Range_y.min())))
							#data_spectra[yi_,xi_] = np.sum(spectra[s_from:s_to])
							if xi_>= len(Range_xi_tmp):
								xi_ = len(Range_xi_tmp)-1
							if yi_>= len(Range_yi):
								yi_ = len(Range_yi)-1
						data_pmt[zi,xi_,yi_] = pmt_val
						data_pmt1[zi,xi_,yi_] = pmt_val1
						print(self.live_x[-1], x, xi_,xi, yi_, yi)

						#self.live_integr_spectra.append(np.sum(spectra[s_from:s_to]))

						self.line_pmt.setData(x=self.live_x,y=self.live_pmt)
						self.line_pmt1.setData(x=self.live_x,y=self.live_pmt1)

						#self.line_spectra.setData(self.live_integr_spectra)

						#self.setLine(spectra)
						#print(time.time()-start)
						self.setUiPiPos(real_position)
						print("[\t%.5f\t%.5f\t%.5f\t]\t%.5f"%tuple(real_position+[time.time()-start]))
						app.processEvents()
						#time.sleep(0.01)
						wait = self.ui.Pi_wait.isChecked()
						#print(time.time()-start)
					#self.setImage(data_spectra)

					self.img.setImage(data_pmt,pos=(Range_x.min(),Range_y.min()),
					scale=(x_step,y_step),xvals=Range_z)
					self.img1.setImage(data_pmt1,pos=(Range_x.min(),Range_y.min()),
					scale=(x_step,y_step),xvals=Range_z)
					self.img.setCurrentIndex(layerIndex)
					self.img1.setCurrentIndex(layerIndex)

					#print(sum(data_pmt),sum(data_pmt1))

				#imsave(fname+"_pmt.tif",data_pmt1.astype(np.int16))
				#imsave(fname+"_pmt1.tif",data_pmt1.astype(np.int16))
				layerIndex+=1

		except KeyboardInterrupt:
			data_pmt_16 = data_pmt/data_pmt.max()*32768
			data_pmt1_16 = data_pmt1/data_pmt1.max()*32768
			imsave(fname+"_pmt.tif",data_pmt_16.astype(np.int16))
			imsave(fname+"_pmt1.tif",data_pmt1_16.astype(np.int16))
			print(self.spectrometer.close())
			print(self.piStage.CloseConnection())
			return

		data_pmt_16 = data_pmt/data_pmt.max()*32768
		data_pmt1_16 = data_pmt1/data_pmt1.max()*32768
		imsave(fname+"_pmt.tif",data_pmt_16.astype(np.int16))
		imsave(fname+"_pmt1.tif",data_pmt1_16.astype(np.int16))
		self.ui.start3DScan.setChecked(False)
		#print(self.spectrometer.close())
		#print(self.piStage.CloseConnection())
	def start_fast3DScan(self,state):
		if state:
			self.fast3DScan()
			self.ui.fast3DScan.setChecked(False)
		else:
			pass


	def fast3DScan(self):
		z_start = float(self.ui.scan3D_config.item(0,1).text())
		z_end = float(self.ui.scan3D_config.item(0,2).text())
		z_step = float(self.ui.scan3D_config.item(0,3).text())
		Range_z = np.arange(z_start,z_end,z_step)

		y_start = float(self.ui.scan3D_config.item(1,1).text())
		y_end = float(self.ui.scan3D_config.item(1,2).text())
		y_step = float(self.ui.scan3D_config.item(1,3).text())

		Range_y = np.arange(y_start,y_end,y_step)

		x_start = float(self.ui.scan3D_config.item(2,1).text())
		x_end = float(self.ui.scan3D_config.item(2,2).text())
		x_step = float(self.ui.scan3D_config.item(2,3).text())

		Range_x = np.arange(x_start,x_end,x_step)

		start0=time.time()
		#
		#q = Queue()
		n_captures = self.ui.fastScan_n_captures.value()
		data_pmt,data_pmt1 = fastScan(self.piStage,self.ps,n_captures=n_captures, x_range=Range_x,y_range=Range_y,z_range=Range_z,app=app)
		#p = Process(target=fastScan,args=(self.piStage,self.ps,Range_x,Range_y,Range_z,q,))
		#p.start()
		#while q.empty():
		#	app.processEvents()
		#	time.sleep(0.1)
		#data_pmt, data_pmt1 = q.get()
		print('TotalTime:',time.time()-start0)
		self.img.setImage(data_pmt,pos=(Range_x.min(),Range_y.min()),
		scale=(x_step,y_step),xvals=Range_z)
		self.img1.setImage(data_pmt1,pos=(Range_x.min(),Range_y.min()),
		scale=(x_step,y_step),xvals=Range_z)
		path = self.ui.scan3D_path.text()
		if "_" in path:
			path = "".join(path.split("_")[:-1])#+"_"+str(round(time.time()))
		else:
			path = path #+ "_"+str(round(time.time()))
		t = round(time.time())
		print(data_pmt.shape,type(data_pmt))
		imsave(path+"_fastScan_"+str(t)+'.tif',data_pmt)
		imsave(path+"_fastScan1_"+str(t)+'.tif',data_pmt1)
		self.ps.close()
		self.initPico()


	############################################################################
	###############################   scan3D	################################

	def scan1D_filePath_find(self):
		fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', self.ui.scan1D_filePath.text())
		if type(fname)==tuple:
			fname = fname[0]
		try:
			self.ui.scan1D_filePath.setText(fname)
		except:
			traceback.print_exc()

	def polarScan(self):
		fname = self.ui.scan1D_filePath.text()+"_"+str(round(time.time()))+".txt"
		with open(fname,'a') as f:
			f.write("#X\tY\tZ\tHWP\tpmt_signal\tpmt1_signal\ttime\n")
		self.rotPiezoStage.move(self.ui.scanPolar_angle.value())
		isMoving = self.rotPiezoStage.isMoving()
		n = 0
		while isMoving and self.alive:
			print(n)
			n = n+1
			if n>10:
				isMoving = self.rotPiezoStage.isMoving()
				n = 0
			pmt_val,pmt_val1 = self.readPico()#self.readDAQmx(print_dt=True)
			self.live_pmt.append(pmt_val)
			self.live_pmt1.append(pmt_val1)
			self.line_pmt.setData(self.live_pmt)
			self.line_pmt1.setData(self.live_pmt1)
			app.processEvents()
			real_position = [round(p,4) for p in self.piStage.qPOS()]
			HWP_angle = float(self.ui.HWP_angle.text())

			dataSet = real_position +[HWP_angle, pmt_val, pmt_val1, time.time()]# + spectra[spectra_range[0]:spectra_range[1]]
			#print(dataSet[-1])
			with open(fname,'a') as f:
				f.write("\t".join([str(round(i,6)) for i in dataSet])+"\n")
			print(n)
		self.ui.scanPolar.setChecked(False)

	def scanPolar(self,state):
		if state:
			print(state)
			self.live_pmt = []
			self.live_pmt1 = []
			self.alive = True
			self.polarScan()

		else:
			self.live_pmt = []
			self.live_pmt1 = []
			self.alive = False
			self.rotPiezoStage.stop()

	def scan1D(self):
		fname = self.ui.scan1D_filePath.text()+"_"+str(round(time.time()))+".txt"
		with open(fname,'a') as f:
			f.write("#X\tY\tZ\tHWP\tpmt_signal\tpmt1_signal\ttime\n")
		axis = self.ui.scan1D_axis.currentText()
		move_function = None
		if axis == "X":
			move_function = lambda pos: self.piStage.MOV(pos,axis=1,waitUntilReady=True)
		elif axis == "Y":
			move_function = lambda pos: self.piStage.MOV(pos,axis=2,waitUntilReady=True)
		elif axis == "Z":
			move_function = lambda pos: self.piStage.MOV(pos,axis=3,waitUntilReady=True)
		elif axis == 'HWP':
			def move_function(pos):
				self.HWP.mAbs(pos)
				pos = self.HWP.getPos()
				self.ui.HWP_angle.setText(str(round(pos,6)))

		steps_range = np.arange(self.ui.scan1D_start.value(),
								self.ui.scan1D_end.value(),
								self.ui.scan1D_step.value())
		for new_pos in steps_range:
			if not self.alive: break
			pmt_val,pmt_val1 = self.readPico()#self.readDAQmx(print_dt=True)

			real_position = [round(p,4) for p in self.piStage.qPOS()]
			HWP_angle = float(self.ui.HWP_angle.text())
			if axis == 'X':
				x = real_position[0]
			if axis == 'Y':
				x = real_position[1]
			if axis == 'Z':
				x = real_position[2]
			if axis == 'HWP':
				x = HWP_angle

			self.live_pmt.append([x,pmt_val])
			self.live_pmt1.append([x,pmt_val1])
			X,Y = np.array(self.live_pmt).T
			self.line_pmt.setData(x=X,y=Y)
			X,Y = np.array(self.live_pmt1).T
			self.line_pmt1.setData(x=X,y=Y)
			app.processEvents()
			dataSet = real_position +[HWP_angle, pmt_val, pmt_val1, time.time()]# + spectra[spectra_range[0]:spectra_range[1]]
			#print(dataSet[-1])
			with open(fname,'a') as f:
				f.write("\t".join([str(round(i,6)) for i in dataSet])+"\n")
			move_function(new_pos)
		self.ui.scan1D_Scan.setChecked(False)

	def scan1D_Scan(self,state):
		if state:
			self.live_pmt = []
			self.live_pmt1 = []
			self.alive = True
			self.scan1D()

		else:
			self.live_pmt = []
			self.live_pmt1 = []
			self.alive = False
			#self.rotPiezoStage.stop()

	############################################################################
	##########################   Ui   ##########################################
	def initUI(self):
		self.ui.actionExit.toggled.connect(self.closeEvent)

		self.ui.scan1D_filePath_find.clicked.connect(self.scan1D_filePath_find)



		self.ui.scan3D_path_dialog.clicked.connect(self.scan3D_path_dialog)

		self.ui.usbSpectr_set_integr_time.clicked.connect(self.usbSpectr_set_integr_time)

		self.ui.connect_DAQmx.toggled[bool].connect(self.connect_DAQmx)
		self.ui.DAQmx_find_shift.clicked.connect(self.optimizeDAQmx)

		self.ui.HWP_go.clicked.connect(self.HWP_go)
		self.ui.HWP_go_home.clicked.connect(self.HWP_go_home)
		self.ui.HWP_negative_step.clicked.connect(self.HWP_negative_step)
		self.ui.HWP_positive_step.clicked.connect(self.HWP_positive_step)

		self.ui.Pi_X_go.clicked.connect(self.Pi_X_go)
		self.ui.Pi_Y_go.clicked.connect(self.Pi_Y_go)
		self.ui.Pi_Z_go.clicked.connect(self.Pi_Z_go)
		self.ui.Pi_XYZ_50mkm.clicked.connect(self.Pi_XYZ_50mkm)
		self.ui.Pi_autoZero.clicked.connect(self.Pi_autoZero)

		self.ui.connect_rotPiezoStage.toggled[bool].connect(self.connect_rotPiezoStage)
		self.ui.rotPiezoStage_Go.clicked.connect(self.rotPiezoStage_Go)

		self.ui.scanPolar.toggled[bool].connect(self.scanPolar)

		self.ui.scan1D_Scan.toggled[bool].connect(self.scan1D_Scan)

		self.ui.start3DScan.toggled[bool].connect(self.start3DScan)

		self.ui.fast3DScan.toggled[bool].connect(self.start_fast3DScan)

		self.ui.startCalibr.toggled[bool].connect(self.startCalibr)
		self.calibrTimer.timeout.connect(self.onCalibrTimer)

		self.ui.connect_pico.toggled[bool].connect(self.connect_pico)
		self.ui.pico_set.clicked.connect(self.pico_set)

		self.ui.Pi_Set.clicked.connect(self.Pi_Set)

		########################################################################
		########################################################################
		########################################################################

		self.tabColors = {
			0: 'green',
			1: 'red',
			2: 'wine',
			3: 'orange',
			4: 'blue',
		}
		self.ui.configTabWidget.tabBar().currentChanged.connect(self.styleTabs)

		self.pw = pg.PlotWidget(name='PlotMain')  ## giving the plots names allows us to link their axes together
		#self.ui.plotArea.addWidget(self.pw)
		self.line0 = self.pw.plot()
		self.line1 = self.pw.plot(pen=(255,0,0))
		self.line3 = self.pw.plot(pen=(255,0,255))

		self.pw_preview = pg.PlotWidget(name='preview')  ## giving the plots names allows us to link their axes together
		self.ui.previewArea.addWidget(self.pw_preview)

		self.line_DAQmx_sig = self.pw_preview.plot(pen=(255,0,0))
		self.line_DAQmx_sig1 = self.pw_preview.plot(pen=(255,255,0))
		self.line_DAQmx_ref = self.pw_preview.plot(pen=(255,0,255))

		self.line_pico_ChA = self.pw_preview.plot(pen=(255,215,0))
		self.line_pico_ChB = self.pw_preview.plot(pen=(0,255,255))

		self.pw1 = pg.PlotWidget(name='Graph1')  ## giving the plots names allows us to link their axes together
		self.ui.plotArea.addWidget(self.pw1)

		self.line_pmt = self.pw1.plot(pen=(255,215,0))
		self.line_pmt1 = self.pw1.plot(pen=(0,255,255))
		self.line_spectra = self.pw1.plot(pen=(0,255,0))

		self.img = pg.ImageView()  ## giving the plots names allows us to link their axes together
		data = np.zeros((100,100))
		self.ui.imageArea.addWidget(self.img)
		self.img.setImage(data)
		colors = [(0, 0, 0),(255, 214, 112)]
		cmap = pg.ColorMap(pos=[0.,1.], color=colors)
		self.img.setColorMap(cmap)
		g = pg.GridItem()
		self.img.addItem(g)

		self.img1 = pg.ImageView()  ## giving the plots names allows us to link their axes together
		data = np.zeros((100,100))
		self.ui.imageArea.addWidget(self.img1)
		self.img1.setImage(data)
		colors = [(0, 0, 0),(204, 255, 255)]
		cmap = pg.ColorMap(pos=[0.,1.], color=colors)
		self.img1.setColorMap(cmap)
		g1 = pg.GridItem()
		self.img1.addItem(g1)
		#self.ui.configTabWidget.setStyleSheet('QTabBar::tab[objectName="Readout"] {background-color=red;}')

	def styleTabs(self, index):
		self.ui.configTabWidget.setStyleSheet('''
			QTabBar::tab {{}}
			QTabBar::tab:selected {{background-color: {color};}}
			'''.format(color=self.tabColors[index]))

	def closeEvent(self, evnt):
		print('closeEvent')
		try:
			self.piStage.CloseConnection()
		except:
			traceback.print_exc()
		try:
			self.spectrometer.close()
		except:
			traceback.print_exc()
		try:
			self.HWP.cleanUpAPT()
		except:
			traceback.print_exc()
		try:
			self.DAQmx.close()
		except:
			traceback.print_exc()
		try:
			self.ps.close()
		except:
			traceback.print_exc()
		try:
			self.rotPiezoStage.close()
		except:
			traceback.print_exc()


	def setImage(self,data):
		self.img.setImage(data.T,levels=(data.min(), data.max()))
		#app.processEvents()

	def setImage1(self,data):
		self.img1.setImage(data.T,levels=(data.min(), data.max()))
		#app.processEvents()


		#app.processEvents()



if __name__ == '__main__':


	app = QtGui.QApplication(sys.argv)
	try:
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
	except RuntimeError:
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
	ex = microV()
	app.exec_()
