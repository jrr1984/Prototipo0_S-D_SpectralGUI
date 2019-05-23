# -*- coding: utf-8 -*-
import time, os
import numpy as np
import serial
from serial.tools import list_ports
import threading
import time



class AG_UC2():
	STEPS_DEG = 500  #  steps per 1 deg
	ser = None
	connected = False
	currentAngle = 0
	outStr = b''
	def __init__(self):
		pass
	def connect(self):
		ports = list_ports.comports()
		s = 'Newport AG-UC2-UC8 USB Serial Port'
		test_ports = []
		for i in ports:
			if s in i[1]:
				test_ports.append(i[0])
				print(i)
		for p in test_ports:
			try:
				self.ser = serial.Serial(p,baudrate=921600,timeout=1)
				self.connected = True
				print('connected',p)
				break
			except:
				pass
	def close(self):
		if self.isConnected():
			self.ser.close()

	def isConnected(self):
		r = False
		try:
			self.ser.inWaiting()
			r = True
		except:
			r = False
		return r
	def setRemote(self):
		if self.isConnected():
			self.ser.write(b'MR\r\n')
	def setLocal(self):
		if self.isConnected():
			self.ser.write(b'ML\r\n')
	def stop(self):
		if self.isConnected():
			self.ser.write(b'1ST\r\n')
			self.ser.write(b'2ST\r\n')
	def readOut(self):
		s = b''
		self.outStr = b''
		while self.isConnected():
			try:
				s+=self.ser.read(1)
				if len(s)>1:
					if s[-1]==10 and s[-2]==13:
						print(">",s)
						self.outStr = s
						s = b''
						time.sleep(0.2)
			except:
				print('stop')
				break

	def isMoving(self):
		if self.isConnected():
			#thread = threading.Thread(target=self.readOut)
			#thread.start()
			self.ser.write(b'1TS\r\n')
			r = self.ser.readline()
			#for i in range(100):
			#	r = self.outStr
			#	if len(r)>3:
			#		break
			#		time.sleep(0.5)
			r = r.decode().replace('\r','')
			print("r=",r)
			if r == '1TS0\n':
				return 0
			if r == '1TS-3\n':
				return -1
			else:
				return 1
	def move(self,step_angle=0,waitUntilReady=False):
		if self.isConnected():
			self.setRemote()
			if step_angle>=0:
				self.ser.write(b'1SU50\r\n')
			if step_angle<0:
				self.ser.write(b'1SU-50\r\n')
			steps = round(step_angle*self.STEPS_DEG)
			self.ser.write(b'1PR'+str(steps).encode()+b'\r\n')
			if waitUntilReady:
				while self.isMoving()>0:
					time.sleep(0.1)
			self.currentAngle += step_angle
			self.setLocal()

	def resetAngle(self):
		if self.isConnected():
			self.ser.write(b'1ZP\r\n')
			self.currentAngle = 0
	def getAngle(self):
		if self.isConnected():
			#self.ser.write(b'1ST\r\n')
			#r = self.ser.readline()
			#steps = r.decode().replace('\r\n','')
			#steps = int(steps[3:])
			#ang = steps/self.STEPS_DEG
			return	self.currentAngle#, ang





if __name__ == "__main__":
	ag = AG_UC2()
	ag.connect()
	ag.move(20,waitUntilReady=True)
	print(ag.getAngle())
	ag.move(-20,waitUntilReady=True)
	print(ag.getAngle())
	ag.close()
