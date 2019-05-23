# -*- coding: utf-8 -*-
import traceback
try:
	from .E727Wrapper import *
except:
	traceback.print_exc()
import time, re, os, sys
import traceback
from ctypes import create_string_buffer , c_char_p, c_double, c_bool, c_int
import numpy as np


def errorTranslator(f):
	def wrapper(*args,**kargs):
		out = f(*args,**kargs)
		if not args[0].err_out:
			iError = args[0].GetError()
			szErrorMesage = args[0].TranslateError(iError)
			print(f.__name__+"> ERROR ",iError, szErrorMesage)
			args[0].CloseConnection()
		return out
	return wrapper
'''
def errorTranslator(f):
	if not r:
		iError = self.GetError()
		szErrorMesage=self.TranslateError(iError)
		print("PI_qDRR_SYNC> ERROR ",iError, szErrorMesage)
		self.CloseConnection()
'''

class E727():


	szUsbController = create_string_buffer(1024)
	szAxes = create_string_buffer(512)
	bFlags = create_string_buffer(3);
	szErrorMesage = create_string_buffer(1024)
	ID = 0
	iError = None
	tmp='555'
	err_out = None
	def __init__(self):
		pass
	def EnumerateUSB(self):
		#print(self.libDLL)

		c=create_string_buffer(len(b"PI E-727"),b"PI E-727")
		r = PI_EnumerateUSB(self.szUsbController, 1024, c)
		print(c.value,r,self.szUsbController.value)
		usb_id = self.szUsbController.value.split(b'\n')
		pattern = re.compile(b".*PI E-727 Controller SN [0-9]+")
		for i in usb_id:
			if pattern.match(i):
				#print(i.decode())
				id_ = i+b"\n"
				self.szUsbController = c_char_p(id_)

		print("#",self.szUsbController.value)
		return self.szUsbController.value

	def ConnectUSB(self):
		#/////////////////////////////////////////
		#// connect to the controller over USB. //
		#/////////////////////////////////////////
		self.EnumerateUSB()

		self.ID = PI_ConnectUSB(self.szUsbController)
		print(self.ID)
		if self.ID<0:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("ConnectUSB: ERROR ",iError, szErrorMesage)
		return self.ID

	def ConnectUSBWithBaudRate(self,iBaudRate=115200):
		#/////////////////////////////////////////
		#// connect to the controller over USB. //
		#/////////////////////////////////////////
		self.EnumerateUSB()

		self.ID = PI_ConnectUSBWithBaudRate(self.szUsbController,iBaudRate)
		print(self.ID)
		if self.ID<0:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("ConnectUSBWithBaudRate: ERROR ",iError, szErrorMesage)
		return self.ID

	def CloseConnection(self):
		PI_CloseConnection(self.ID)
	def close(self):
		PI_CloseConnection(self.ID)
	def GetError(self):

		self.iError = PI_GetError(self.ID)
		return self.iError
	def TranslateError(self, iError):

		r = PI_TranslateError(iError, self.szErrorMesage, 1024)
		return self.szErrorMesage.value

	@errorTranslator
	def qSAI(self):
		#/////////////////////////////////////////
		#// Get the name of the connected axis. //
		#/////////////////////////////////////////

		self.err_out = PI_qSAI(self.ID, self.szAxes, 512)
		tmp = self.szAxes.value
		self.szAxes = tmp#.replace(b'\n',b'')
		return self.szAxes#.value


	def SVO(self,axis=b'1 2 3',flags=[True,True,True]):

		ax = axis.split(b' ')
		for i in range(len(flags)):
			r = PI_SVO(self.ID, ax[i], c_bool(flags[i]))
			if not r:
				iError = self.GetError()
				szErrorMesage=self.TranslateError(iError)
				print("SVO> ERROR ",iError, szErrorMesage)
				self.CloseConnection()
			else:
				pass
		return self.err_out

	def qSVO(self,axis=b'1 2 3'):
		val = (c_bool*3)()
		val[0] = c_bool(False)
		val[1] = c_bool(False)
		val[2] = c_bool(False)
		out = []
		ax = axis.split(b' ')
		for i in range(len(ax)):
			r = PI_qSVO(self.ID, ax[i], val)
			out.append(val[0])
			if not r:
				iError = self.GetError()
				szErrorMesage=self.TranslateError(iError)
				print("qSVO> ERROR ",iError, szErrorMesage)
				self.CloseConnection()
			else:
				pass
		return out

	def ATZ(self):
		pdLowVoltageArray = (c_double*3)()

		res = 0
		print('PI_ATZ')
		r = PI_ATZ(self.ID, b'', pdLowVoltageArray,c_bool(True))
		time.sleep(5)
		iError = self.GetError()
		k = 0
		while iError==61:
			print('ATZ',iError)
			iError = self.GetError()
			time.sleep(0.5)
			k+=1
			if k==1000:
				self.CloseConnection()
				break
		print('PI_ATZ:Done')
		return self.err_out

	@errorTranslator
	def MOV(self, dPos=[50.0,50.0,50.0],axis=b'1 2 3', waitUntilReady=False):
		if type(axis)==bytes:
			dPos_ = (c_double*len(dPos))()
			for i in range(len(dPos)):
				dPos_[i] = c_double(dPos[i])
		else:
			axis=str(axis).encode()
			dPos_ = c_double(dPos)

		self.err_out = PI_MOV(self.ID, axis, dPos_)


		if waitUntilReady:
			m = self.IsMoving()
			#print(m)
			N_max = 1000000
			n = 0
			while sum(m)!=0 or n>N_max:
				n=n+1
				m = self.IsMoving()
				#print(m)
				time.sleep(0.001)
		return self.err_out

	@errorTranslator
	def qPOS(self,axis=b"1 2 3"):
		val = (c_double*3)()
		self.err_out = PI_qPOS(self.ID, axis, val)

		return [v for v in val]

	@errorTranslator
	def IsMoving(self,axis=b""):
		val = (c_bool*3)()

		self.err_out = PI_IsMoving(self.ID, axis, val)

		return [v for v in val]

	@errorTranslator
	def VEL(self, dVel=[1000,1000,1000],axis=b'1 2 3'):
		if type(axis)==bytes:
			dVel_ = (c_double*len(dVel))()
			for i in range(len(dVel)):
				dVel_[i] = c_double(dVel[i])
		else:
			axis=str(axis).encode()
			dVel_ = c_double(dVel)

		self.err_out = PI_VEL(self.ID, axis, dVel_)


		return self.err_out

	@errorTranslator
	def qVEL(self,axis=b"1 2 3"):
		val = (c_double*3)()
		self.err_out = PI_qVEL(self.ID, axis, val)

		return [v for v in val]

	@errorTranslator
	def WAV_SIN_P(self,iWaveTableId, iOffsetOfFirstPointInWaveTable, iNumberOfPoints,
			iAppendWave, iCenterPointOfWave, dAmplitudeOfWave,
			dOffsetOfWave, iSegmentLength):
		'''
		BOOL PI_WAV_SIN_P (int ID, int iWaveTableId, int iOffsetOfFirstPointInWaveTable,
		 int iNumberOfPoints, int iAppendWave, int iCenterPointOfWave,
		 double dAmplitudeOfWave, double dOffsetOfWave, int iSegmentLength)
		'''


		self.err_out = PI_WAV_SIN_P(self.ID,iWaveTableId, iOffsetOfFirstPointInWaveTable, iNumberOfPoints,
				iAppendWave, iCenterPointOfWave, dAmplitudeOfWave,
				dOffsetOfWave, iSegmentLength)

		return self.err_out

	@errorTranslator
	def WAV_PNT(self,iWaveTableId, iOffsetOfFirstPointInWaveTable, iNumberOfPoints,
			iAppendWave, pdWavePoints):
		'''
		BOOL PI_WAV_PNT (int ID, int iWaveTableId, int iOffsetOfFirstPointInWaveTable,
		int iNumberOfWavePoints, int iAppendWave, const double* pdWavePoints )
		'''
		pdWavePoints_ = (c_double*len(pdWavePoints))()
		for i,val in enumerate(pdWavePoints):
			pdWavePoints_[i] = c_double(val)


		self.err_out = PI_WAV_PNT(self.ID,iWaveTableId, iOffsetOfFirstPointInWaveTable, iNumberOfPoints,
				iAppendWave, pdWavePoints_)

		return self.err_out

	@errorTranslator
	def DRC(self, iDataRecorderChannelIds, szDataRecorderChannelSources, iDataRecorderOptions):
		'''
		BOOL PI_DRC (int ID, const int* piRecordTableIdsArray, const char* szRecordSource, const int* piRecordOptionsArray)
		Set Data Recorder Configuration
		'''
		piRecordTableIdsArray = (c_int*len(iDataRecorderChannelIds))()
		for i,val in enumerate(iDataRecorderChannelIds):
			piRecordTableIdsArray[i] = c_int(val)

		piRecordOptionsArray = (c_int*len(iDataRecorderOptions))()
		for i,val in enumerate(iDataRecorderOptions):
			piRecordOptionsArray[i] = c_int(val)

		r = PI_DRC(self.ID, piRecordTableIdsArray, szDataRecorderChannelSources, piRecordOptionsArray)

		return self.err_out

	@errorTranslator
	def WSL(self, iWaveGenerator, iWaveTableIds, iArraySize):
		'''
		BOOL PI_WSL (int ID, const int* piWaveGeneratorIdsArray, const int* piWaveTableIdsArray, int iArraySize)
		Wave table selection: connects a wave table to a wave generator
		'''
		piWaveGeneratorIdsArray = (c_int*len(iWaveGenerator))()
		for i,val in enumerate(iWaveGenerator):
			piWaveGeneratorIdsArray[i] = c_int(val)

		piWaveTableIdsArray = (c_int*len(iWaveTableIds))()
		for i,val in enumerate(iWaveTableIds):
			piWaveTableIdsArray[i] = c_int(val)

		self.err_out = PI_WSL(self.ID, piWaveGeneratorIdsArray, piWaveTableIdsArray, iArraySize)

		return self.err_out

	@errorTranslator
	def WGO(self, iWaveGenerator, iStatMode, iArraySize):
		'''
		BOOL PI_WGO (int ID, const int* piWaveGeneratorIdsArray, condt int* piStartModArray, int iArraySize)
		Start and stop the specified wave generator
		'''
		piWaveGeneratorIdsArray = (c_int*len(iWaveGenerator))()
		for i,val in enumerate(iWaveGenerator):
			piWaveGeneratorIdsArray[i] = c_int(val)

		piStartModArray = (c_int*len(iStatMode))()
		for i,val in enumerate(iStatMode):
			piStartModArray[i] = c_int(val)

		self.err_out = PI_WGO(self.ID, piWaveGeneratorIdsArray, piStartModArray, iArraySize)

		return self.err_out

	@errorTranslator
	def qWGO(self,iWaveGenerator=[1,2,3]):
		'''
		BOOL PI_qWGO (int ID, const int piWaveGeneratorIdsArray, int* piValueArray, int iArraySize)
		Get the start/stop mode of the given wave generator
		'''
		piWaveGeneratorIdsArray = (c_int*len(iWaveGenerator))()
		for i,val in enumerate(iWaveGenerator):
			piWaveGeneratorIdsArray[i] = c_int(val)

		iArraySize = len(piWaveGeneratorIdsArray)

		piValueArray = (c_int*len(piWaveGeneratorIdsArray))()

		self.err_out = PI_qWGO(self.ID, piWaveGeneratorIdsArray, piValueArray, iArraySize)

		res = [val for val in piValueArray]
		return res

	@errorTranslator
	def qDRR(self, iDataRecorderChannelIds, iNReadChannels,
		iOffsetOfFirstPointInRecordTable, iNReadValues,
		dDataTable, szHeader, iGcsArrayHeaderMaxSize=300):
		'''
		BOOL PI_qDRR (int ID, const int* piRecTableIdsArray, int iNumberOfRecTables,
		int iOffsetOfFirstPointInRecordTable, int iNumberOfValues,
		double** pdValueArray, char* szGcsArrayHeader, int iGcsArrayHeaderMaxSize)
		Get Recorded Data Values
		'''
		self.dataTable_config = (iDataRecorderChannelIds, iNReadChannels,
			iOffsetOfFirstPointInRecordTable, iNReadValues,
			dDataTable, szHeader, iGcsArrayHeaderMaxSize)

		szHeader_ = create_string_buffer(iGcsArrayHeaderMaxSize+1)
		piRecTableIdsArray = (c_int*len(iDataRecorderChannelIds))()
		for i,val in enumerate(iDataRecorderChannelIds):
			piRecTableIdsArray[i] = c_int(val)

		piStartModArray = (c_int*len(iStatMode))()
		for i,val in enumerate(iStatMode):
			piStartModArray[i] = c_int(val)

		self.err_out = PI_qDRR(self.ID, piRecTableIdsArray, iNReadChannels,
			iOffsetOfFirstPointInRecordTable, iNReadValues,
			byref(dDataTable), szHeader_, iGcsArrayHeaderMaxSize)

		return self.err_out

	@errorTranslator
	def qDRR_SYNC(self, iRecordTableId, iOffsetOfFirstPointInRecordTable,
			iNumberOfValues):
			'''
			BOOL PI_qDRR_SYNC (int ID, int iRecordTableId, int iOffsetOfFirstPointInRecordTable, int iNumberOfValues, double* pdValueArray)
			'''
			pdValueArray = (c_double*iNumberOfValues)()

			self.err_out = PI_qDRR_SYNC(self.ID, iRecordTableId, iOffsetOfFirstPointInRecordTable,
				iNumberOfValues, pdValueArray)

			res = [val for val in pdValueArray]
			return res

	@errorTranslator
	def qDTL(self, piDdlTableIdsArray=[1,2,3]):
			'''
			BOOL PI_qDTL (int ID, const int* piDdlTableIdsArray, int* piValueArray, int iArraySize)
			Get DDL table length
			'''
			L = len(piDdlTableIdsArray)
			piValueArray = (c_int*L)()

			piDdlTableIdsArray_ = (c_int*len(piDdlTableIdsArray))()
			for i,val in enumerate(piDdlTableIdsArray):
				piDdlTableIdsArray_[i] = c_int(val)

			self.err_out = PI_qDTL(self.ID, piDdlTableIdsArray_, piValueArray, L)

			res = [val for val in piValueArray]
			return res

	@errorTranslator
	def WGC(self, piWaveGeneratorIdsArray=[1,2,3],piNumberOfCyclesArray=[0,0,0]):
			'''
			BOOL PI_WGC (int ID, const int* piWaveGeneratorIdsArray, const int* piNumberOfCyclesArray, int iArraySize)
			Set the number of cycles for the wave generator output
			'''
			piWaveGeneratorIdsArray_ = (c_int*len(piWaveGeneratorIdsArray))()
			for i,val in enumerate(piWaveGeneratorIdsArray):
				piWaveGeneratorIdsArray_[i] = c_int(val)

			piNumberOfCyclesArray_ = (c_int*len(piNumberOfCyclesArray))()
			for i,val in enumerate(piNumberOfCyclesArray):
				piNumberOfCyclesArray_[i] = c_int(val)
			iArraySize = len(piWaveGeneratorIdsArray_)
			self.err_out = PI_WGC(self.ID, piWaveGeneratorIdsArray_, piNumberOfCyclesArray_, iArraySize)

			return self.err_out

	def GetAsyncBufferIndex(self):
		index = PI_GetAsyncBufferIndex(self.ID)
		return index

	@errorTranslator
	def qTWG(self):
		'''
		BOOL PI_qTWG (int ID, int* iNumberOfWaveGenerators)
		Get the number of wave generators
		'''
		iNumberOfWaveGenerators = (c_int)()
		self.err_out = PI_qTWG(self.ID, iNumberOfWaveGenerators)
		return iNumberOfWaveGenerators.value

	def getDataTable(self):
		iDataRecorderChannelIds, iNReadChannels,iOffsetOfFirstPointInRecordTable, iNReadValues,	dDataTable, szHeader, iGcsArrayHeaderMaxSize = self.dataTable_config
		#/////////////////////////////////////////////////////////////
		# wait until the read pointer does not increase any more. //
		#///////////////////////////////////////////////////////////

		iIndex = self.GetAsyncBufferIndex()
		iOldIndex = -1
		#do// wait until the read pointer does not increase any more
		#{
		#x,y,t = [],[],[]
		while iOldIndex<iIndex:
			iOldIndex = iIndex
			time.sleep(0.0010)
			print(iOldIndex)
			iIndex = self.GetAsyncBufferIndex()
			#print(self.qPOS())
			p = piStage.qPOS()
			print(p)
			#x.append(p[0])
			#y.append(p[1])
			#t.append(time.time())
		#///////////////////////////////////
		# read the values from the array. //
		#///////////////////////////////////
		print("len:",self.qDTL())
		dataTable_out = []
		for iIndex in range(0, int(iOldIndex / iNReadChannels)):
		#{#// print read data
		#// the data columns
		#// c1_1 c2_1 c3_1 c4_1
		#// c1_2 c2_2 c3_2 c4_2
		#// ...
		#// c1_n c2_n c3_n c4_n
		#// are aligned as follows:
		#// dDataTable:
		#// {c1_1,c2_1,c3_1,c4_1,c1_2,c2_2,...,c4_n}

			#print("%03d"%iIndex);
			tmp = []
			for k in range(0,iNReadChannels):
				#print("\t%05.05f"%(dDataTable[(iIndex * iNReadChannels) + k]), end='')
				tmp.append(dDataTable[(iIndex * iNReadChannels) + k])
			dataTable_out.append(tmp)
			#print("\n");
		data = np.array(dataTable_out)
		return data#,x,y,t

if __name__ == "__main__":
	from E727Wrapper import *
	piStage = E727()
	print(piStage.ConnectUSBWithBaudRate())
	try:
		print(piStage.qSAI())
		print("SVO:",piStage.qSVO(b'1 2 3'))
		print(piStage.SVO(b'1 2 3',[True, True, True]))
		print("SVO:",piStage.qSVO(b'1 2 3'))

		print("qTWG:",piStage.qTWG())
		print("qWGO:",piStage.qWGO())

		#// select the desired wave generators to run (only wave generator 1 is used in this example).
		iWaveGenerator = [1,2,3]
		#// select the start mode for the corresponding wave generator.
		iStatMode= [0,0,0]
		piStage.WGO( iWaveGenerator, iStatMode, 3)

		#time.sleep(1)
		#print(piStage.ATZ())
		#print(piStage.MOV(dPos=[0,0,0],axis=b"1 2 3", waitUntilReady=True))
		#print(piStage.MOV(dPos=[50,50,50],axis=b"1 2 3", waitUntilReady=True))

		#print('X')
		#print(piStage.BRA(b'1 2 3',[True, True, True]))
		#print(piStage.CMO())
		#print(piStage.qCMO())
		print(piStage.VEL([1000,1000,1000],b'1 2 3'))
		print("qVEL:",piStage.qVEL())
		'''
		print(piStage.MOV(dPos=100,axis=1, waitUntilReady=True))
		print(piStage.qPOS())
		print(piStage.MOV(0,axis=1, waitUntilReady=True))
		print(piStage.qPOS())
		print('Y')
		print(piStage.MOV(100,axis=2, waitUntilReady=True))
		print(piStage.qPOS())
		print(piStage.MOV(0,axis=2, waitUntilReady=True))
		print(piStage.qPOS())
		print('Z')
		print(piStage.MOV(100,axis=3, waitUntilReady=True))
		print(piStage.qPOS())
		print(piStage.MOV(0,axis=3, waitUntilReady=True))
		print(piStage.qPOS())


		print(piStage.MOV(dPos=[50,50,50],axis=b"1 2 3", waitUntilReady=True))
		print(piStage.qPOS())
		'''
		print(piStage.qPOS())

		#///////////////////////////////////////////
		#// Write a sin wave to the wave table 1. //
		#///////////////////////////////////////////
		iWaveTableIds = [1,2,3]
		print(piStage.WAV_SIN_P(iWaveTableIds[0], 1, 1000, 0, 500, 30, 0, 1000))
		print(piStage.WAV_SIN_P(iWaveTableIds[1], 2, 1000, 0, 500, 15, 0, 1000))
		print(piStage.WAV_SIN_P(iWaveTableIds[2], 3, 1000, 0, 500, 5, 0, 1000))
		N = 20
		t = np.arange(0,2*np.pi,0.01)
		X = [0,100,0,100,0,100]#np.sin(t)*50+50
		Y = [50]*len(X)#np.sin(2*t)*50+50
		Z = [20]*len(X)#np.sin(4*t)*50+50
		#print(piStage.WAV_PNT(iWaveTableIds[0], 0, len(X), 0, X))
		#print(piStage.WAV_PNT(iWaveTableIds[1], 0, len(Y), 0, Y))
		#print(piStage.WAV_PNT(iWaveTableIds[2], 0, len(Z), 0, Z))


		#////////////////////////////////////////
		#// define the data recorder channels. //
		#////////////////////////////////////////

		#// select the desired record channels to change.
		iDataRecorderChannelIds = [1, 2, 3]

		#// select the corresponding record source id's.
		szDataRecorderChannelSources = b'1 2 3'

		#// select the corresponding record mode.
		iDataRecorderOptions = [0,0,0]

		print(piStage.DRC(iDataRecorderChannelIds, szDataRecorderChannelSources, iDataRecorderOptions))


		#////////////////////////////
		#// Select the wave table. //
		#////////////////////////////
		#// select the desired wave table.

		#iWaveTableIds = 1;

		#// select the desired wave generator.


		#// Call the wave selection command
		print(piStage.WSL( iWaveGenerator, iWaveTableIds, 3))

		#print(piStage.WGC(iWaveGenerator, [2,2,2]))

		#/////////////////////////////////
		#// start the wave generator 1. //
		#/////////////////////////////////

		#// select the desired wave generators to run (only wave generator 1 is used in this example).
		#iWaveGenerator[0] = 1;
		#// select the start mode for the corresponding wave generator.
		print('Start')
		iStatMode= [1,1,1]
		piStage.WGO( iWaveGenerator, iStatMode, 3)
		k=0
		m = sum(piStage.IsMoving())
		x = []
		y = []
		t = []
		while m and k<10000:
			k+=1
			p = piStage.qPOS()
			print(p,k)

			m = sum(piStage.IsMoving())
			print("qWGO:",piStage.qWGO())
			x.append(p[0])
			y.append(p[1])
			t.append(time.time())


		#time.sleep(5)
		#///////////////////////////////////
		#// start reading asynchronously. //
		#///////////////////////////////////

		#// select the desired record channels to change.
		iDataRecorderChannelIds[0] = 1;
		iDataRecorderChannelIds[1] = 2;
		iDataRecorderChannelIds[2] = 3;
		dDataTable = ctypes.POINTER(c_double)()
		szHeader = b''
		iNReadChannels = 3;

		iNReadValues = 1000

		print("qTWG:",piStage.qTWG())
		print("qWGO:",piStage.qWGO())
		#dDataTable = np.zeros((iNReadValues,iNReadValues),dtype=np.float64)

		print(piStage.qDRR(iDataRecorderChannelIds, iNReadChannels, 3, iNReadValues, dDataTable, szHeader, 300))
		#data = piStage.qDRR_SYNC(1, 1, iNReadValues)

		data = piStage.getDataTable()

		print(piStage.qPOS(),"<<<")

		#table = [i for i in dDataTable]
		#// select the desired wave generators to run (only wave generator 1 is used in this example).
		#iWaveGenerator = [1]
		#// select the start mode for the corresponding wave generator.
		iStatMode= [0,0,0]
		piStage.WGO( iWaveGenerator, iStatMode, 3)


		#piStage.SVO(b'1 2 3', flags=[False, False, False])
		print(piStage.close())

	except:
		traceback.print_exc()
		print(piStage.CloseConnection())
