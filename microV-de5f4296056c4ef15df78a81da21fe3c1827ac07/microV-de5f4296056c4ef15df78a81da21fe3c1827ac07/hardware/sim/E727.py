# -*- coding: utf-8 -*-
import ctypes# give location of dll
from ctypes import c_int, c_bool, c_void_p, c_float, c_double, c_char, c_char_p, c_ulong, byref, create_string_buffer
import time, re, os, sys
import numpy as np
"""  Открыть Com-порт
function SMD_OpenComPort(AComNmbr: integer): boolean; stdcall;
Функция открывает COM-порт, и устанавливает заданный номер порта.
Вход:  AComNmbr - номер COM-порта. Целое число > 0.
Выход:  TRUE – если операция выполнена, FALSE – еслиимеются ошибки.
"""

class E727():

	libDLL = 1#ctypes.windll.LoadLibrary( os.path.abspath(__file__).split('E727.py')[0]+'PI_GCS2_DLL_x64.dll')
	szUsbController = create_string_buffer(1024)
	szAxes = create_string_buffer(17)
	bFlags = create_string_buffer(3);
	szErrorMesage = create_string_buffer(1024)
	ID = 0
	iError = None
	pos = np.array([0,0,0])

	def __init__(self):
		pass
	def EnumerateUSB(self):
		#print(self.libDLL)
		#PI_EnumerateUSB = self.libDLL['PI_EnumerateUSB']
		#PI_EnumerateUSB.argtypes = (c_char_p,c_int,c_char_p)
		c=create_string_buffer(len(b"PI E-727"),b"PI E-727")
		r = 1#PI_EnumerateUSB(self.szUsbController, 1024, c)
		print(c.value,r,self.szUsbController.value)
		#usb_id = self.szUsbController.value.split(b'\n')
		#pattern = re.compile(b".*PI E-727 Controller SN [0-9]+")
		#for i in usb_id:
		#	if pattern.match(i):
		#		#print(i.decode())
		#		id_ = i+b"\n"
		#		self.szUsbController = c_char_p(id_)

		#print("#",self.szUsbController.value)
		return 1#self.szUsbController.value

	def ConnectUSB(self):
		#/////////////////////////////////////////
		#// connect to the controller over USB. //
		#/////////////////////////////////////////
		self.EnumerateUSB()
		#PI_ConnectUSB = self.libDLL['PI_ConnectUSB']
		#PI_ConnectUSB.argtypes = (c_char_p,)
		#PI_ConnectUSB.restype = c_int
		#self.ID = PI_ConnectUSB(self.szUsbController)
		#print(self.ID)
		#if self.ID<0:
		#	iError = self.GetError()
		#	szErrorMesage=self.TranslateError(iError)
		#	print("ConnectUSB: ERROR ",iError, szErrorMesage)
		return self.ID

	def ConnectUSBWithBaudRate(self,iBaudRate=115200):
		#/////////////////////////////////////////
		#// connect to the controller over USB. //
		#/////////////////////////////////////////
		'''
		self.EnumerateUSB()
		PI_ConnectUSBWithBaudRate = self.libDLL['PI_ConnectUSBWithBaudRate']
		PI_ConnectUSBWithBaudRate.argtypes = (c_char_p, c_int)
		PI_ConnectUSBWithBaudRate.restype = c_int
		self.ID = PI_ConnectUSBWithBaudRate(self.szUsbController,iBaudRate)
		print(self.ID)
		if self.ID<0:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("ConnectUSBWithBaudRate: ERROR ",iError, szErrorMesage)
		'''
		return self.ID

	def CloseConnection(self):
		'''
		PI_CloseConnection = self.libDLL['PI_CloseConnection']
		PI_CloseConnection.argtypes = (c_int,)
		PI_CloseConnection.restype = c_void_p
		PI_CloseConnection(self.ID)
		'''
		pass
	def GetError(self):
		'''
		PI_GetError = self.libDLL['PI_GetError']
		PI_GetError.argtypes = (c_int,)
		PI_GetError.restype = c_int
		self.iError = PI_GetError(self.ID)
		'''
		return self.iError
	def TranslateError(self, iError):
		'''
		PI_TranslateError = self.libDLL['PI_TranslateError']
		PI_TranslateError.argtypes = (c_int,c_char_p,c_int)
		PI_TranslateError.restype = c_bool
		r = PI_TranslateError(iError, self.szErrorMesage, 1024)
		'''
		return self.szErrorMesage.value

	def qSAI(self):
		#/////////////////////////////////////////
		#// Get the name of the connected axis. //
		#/////////////////////////////////////////
		'''
		PI_qSAI = self.libDLL['PI_qSAI']
		PI_qSAI.argtypes = (c_int,c_char_p, c_int)
		PI_qSAI.restype = c_bool
		r = PI_qSAI(self.ID, self.szAxes, 16)
		tmp = self.szAxes.value
		self.szAxes = tmp.replace(b'\n',b'')
		if not r:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("qSAI> ERROR ",iError, szErrorMesage)
			self.CloseConnection()
		else:
			pass
		'''
		return self.szAxes#.value

	def SVO(self,a,b):
		'''
		for axis in range(1,4):
			bFlags = (c_bool*3)()
			bFlags[0] = c_bool(True)
			bFlags[1] = c_bool(True)
			bFlags[2] = c_bool(True)
			PI_SVO = self.libDLL['PI_SVO']
			PI_SVO.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
			PI_SVO.restype = c_bool
			r = PI_SVO(self.ID, str(axis).encode(), bFlags)
			if not r:
				iError = self.GetError()
				szErrorMesage=self.TranslateError(iError)
				print("SVO> ERROR ",iError, szErrorMesage)
				self.CloseConnection()
			else:
				pass
		'''
		return 1
	def qSVO(self,ax=b''):
		return 1
	def VEL(self,vel=[],ax=b''):
		self.vel = vel
		return 1
	def qVEL(self):
		return self.vel

	def MOV(self, dPos,axis=1, waitUntilReady=False):
		self.prev_pos = self.pos
		self.pos=np.array(dPos)
		'''
		PI_MOV = self.libDLL['PI_MOV']
		PI_MOV.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
		PI_MOV.restype = c_bool
		dPos_ = c_double(dPos)

		r = PI_MOV(self.ID, str(axis).encode(), dPos_)
		if not r:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("MOV> ERROR ",iError, szErrorMesage)
			self.CloseConnection()
		else:
			pass
		'''
		if waitUntilReady:
			m = self.IsMoving()
			#print(m)
			N_max = 1000
			n = 0
			while sum(m)!=0 or n>N_max:
				n=n+1
				m = self.IsMoving()
				#print(m)
				#time.sleep(0.001)


		return 1


	def qPOS(self,axis=b""):
		val = (c_double*3)()
		'''
		PI_qPOS = self.libDLL['PI_qPOS']
		PI_qPOS.argtypes = (c_int,c_char_p, ctypes.POINTER(c_double))
		PI_qPOS.restype = c_bool
		r = PI_qPOS(self.ID, axis, val)
		if not r:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("qPOS> ERROR ",iError, szErrorMesage)
			self.CloseConnection()
		'''
		return self.pos
	def IsMoving(self,axis=b""):

		val = (c_bool*3)()
		'''
		PI_IsMoving = self.libDLL['PI_IsMoving']
		PI_IsMoving.argtypes = (c_int,c_char_p, ctypes.POINTER(c_bool))
		PI_IsMoving.restype = c_bool
		r = PI_IsMoving(self.ID, axis, val)
		if not r:
			iError = self.GetError()
			szErrorMesage=self.TranslateError(iError)
			print("IsMoving> ERROR ",iError, szErrorMesage)
			#self.CloseConnection()
		'''
		dr = np.sqrt(sum((self.prev_pos-self.pos)**2))
		t = dr/100/self.vel[0]
		#print(">>>>>",t,dr)
		time.sleep(t)

		return [0,0,0]

if __name__ == "__main__":
	e = E727()
	print(e.ConnectUSBWithBaudRate())
	print(e.qSAI())
	print(e.SVO())
	time.sleep(5)
	print('X')
	print(e.MOV(100,axis=1, waitUntilReady=True))
	print(e.qPOS())
	print(e.MOV(0,axis=1, waitUntilReady=True))
	print(e.qPOS())
	print('Y')
	print(e.MOV(100,axis=2, waitUntilReady=True))
	print(e.qPOS())
	print(e.MOV(0,axis=2, waitUntilReady=True))
	print(e.qPOS())
	print('Z')
	print(e.MOV(100,axis=3, waitUntilReady=True))
	print(e.qPOS())
	print(e.MOV(0,axis=3, waitUntilReady=True))
	print(e.qPOS())

	print(e.CloseConnection())
