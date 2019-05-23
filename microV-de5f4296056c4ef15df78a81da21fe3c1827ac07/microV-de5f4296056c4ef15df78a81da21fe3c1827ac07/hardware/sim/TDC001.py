# -*- coding: utf-8 -*-
"""
APT Motor Controller for Thorlabs
Adopted from
https://github.com/HaeffnerLab/Haeffner-Lab-LabRAD-Tools/blob/master/cdllservers/APTMotor/APTMotorServer.py
With thanks to SeanTanner@ThorLabs for providing APT.dll and APT.lib


V1.1
20141125 V1.0    First working version
20141201 V1.0a   Use short notation for moving (movRelative -> mRel)
20150417 V1.1    Implementation of simple QT GUI

Michael Leung
mcleung@stanford.edu
"""

from ctypes import c_long, c_buffer, c_float,  pointer#, windll

import os




class APTMotor():
	def __init__(self, SerialNum=None, HWTYPE=31, verbose=False, dllname= os.path.abspath(__file__).split('TDC001.py')[0]+'APT.dll'):
		'''
		HWTYPE_BSC001		11	// 1 Ch benchtop stepper driver
		HWTYPE_BSC101		12	// 1 Ch benchtop stepper driver
		HWTYPE_BSC002		13	// 2 Ch benchtop stepper driver
		HWTYPE_BDC101		14	// 1 Ch benchtop DC servo driver
		HWTYPE_SCC001		21	// 1 Ch stepper driver card (used within BSC102,103 units)
		HWTYPE_DCC001		22	// 1 Ch DC servo driver card (used within BDC102,103 units)
		HWTYPE_ODC001		24	// 1 Ch DC servo driver cube
		HWTYPE_OST001		25	// 1 Ch stepper driver cube
		HWTYPE_MST601		26	// 2 Ch modular stepper driver module
		HWTYPE_TST001		29	// 1 Ch Stepper driver T-Cube
		HWTYPE_TDC001		31	// 1 Ch DC servo driver T-Cube
		HWTYPE_LTSXXX		42	// LTS300/LTS150 Long Travel Integrated Driver/Stages
		HWTYPE_L490MZ		43	// L490MZ Integrated Driver/Labjack
		HWTYPE_BBD10X		44	// 1/2/3 Ch benchtop brushless DC servo driver
		'''
		pass
	def getPos(self):
		'''
		Obtain the current absolute position of the stage
		'''
		'''
		if self.verbose: print( 'getPos probing...')
		if not self.Connected:
			raise Exception('Please connect first! Use initializeHardwareDevice')

		position = c_float()
		self.aptdll.MOT_GetPosition(self.SerialNum, pointer(position))
		if self.verbose: print( 'getPos ', position.value)
		'''
		return 42

	def mRel(self, relDistance):
		'''
		Moves the motor a relative distance specified
		relDistance    float     Relative position desired
		'''
		if self.verbose: print( 'mRel ', relDistance, c_float(relDistance))
		if not self.Connected:
			print( 'Please connect first! Use initializeHardwareDevice')
			#raise Exception('Please connect first! Use initializeHardwareDevice')
		relativeDistance = c_float(relDistance)
		self.aptdll.MOT_MoveRelativeEx(self.SerialNum, relativeDistance, True)
		if self.verbose: print( 'mRel SUCESS')
		return True

	def mAbs(self, absPosition):
		'''
		Moves the motor to the Absolute position specified
		absPosition    float     Position desired
		'''
		'''
		if self.verbose: print( 'mAbs ', absPosition, c_float(absPosition))
		if not self.Connected:
			raise Exception('Please connect first! Use initializeHardwareDevice')
		absolutePosition = c_float(absPosition)
		self.aptdll.MOT_MoveAbsoluteEx(self.SerialNum, absolutePosition, True)
		if self.verbose: print( 'mAbs SUCESS')
		'''
		return True

	def mcRel(self, relDistance, moveVel=0.5):
		'''
		Moves the motor a relative distance specified at a controlled velocity
		relDistance    float     Relative position desired
		moveVel        float     Motor velocity, mm/sec
		'''
		'''
		if self.verbose: print( 'mcRel ', relDistance, c_float(relDistance), 'mVel', moveVel)
		if not self.Connected:
			raise Exception('Please connect first! Use initializeHardwareDevice')
		# Save velocities to reset after move
		maxVel = self.getVelocityParameterLimits()[1]
		# Set new desired max velocity
		self.setVel(moveVel)
		self.mRel(relDistance)
		self.setVel(maxVel)
		if self.verbose: print( 'mcRel SUCESS')
		'''
		return True

	def mcAbs(self, absPosition, moveVel=0.5):
		'''
		Moves the motor to the Absolute position specified at a controlled velocity
		absPosition    float     Position desired
		moveVel        float     Motor velocity, mm/sec
		'''
		'''
		if self.verbose: print( 'mcAbs ', absPosition, c_float(absPosition), 'mVel', moveVel)
		if not self.Connected:
			raise Exception('Please connect first! Use initializeHardwareDevice')
		# Save velocities to reset after move
		minVel, acc, maxVel = self.getVelocityParameters()
		# Set new desired max velocity
		self.setVel(moveVel)
		self.mAbs(absPosition)
		self.setVel(maxVel)
		if self.verbose: print( 'mcAbs SUCESS')
		'''
		return True

	def mbRel(self, relDistance):
		'''
		Moves the motor a relative distance specified
		relDistance    float     Relative position desired
		'''
		'''
		if self.verbose: print( 'mbRel ', relDistance, c_float(relDistance))
		if not self.Connected:
			print( 'Please connect first! Use initializeHardwareDevice')
			#raise Exception('Please connect first! Use initializeHardwareDevice')
		self.mRel(relDistance-self.blCorr)
		self.mRel(self.blCorr)
		if self.verbose: print( 'mbRel SUCESS')
		'''
		return True

	def mbAbs(self, absPosition):
		'''
		Moves the motor to the Absolute position specified
		absPosition    float     Position desired
		'''
		'''
		if self.verbose: print( 'mbAbs ', absPosition, c_float(absPosition))
		if not self.Connected:
			raise Exception('Please connect first! Use initializeHardwareDevice')
		if (absPosition < self.getPos()):
			if self.verbose: print( 'backlash mAbs', absPosition - self.blCorr)
			self.mAbs(absPosition-self.blCorr)
		self.mAbs(absPosition)
		if self.verbose: print( 'mbAbs SUCESS')
		'''
		return True


	def go_home(self):
		'''
		Move the stage to home position and reset position entry
		'''
		'''
		if self.verbose: print( 'Going home')
		if not self.Connected:
			raise Exception('Please connect first! Use initializeHardwareDevice')
		if self.verbose: print( 'go_home SUCESS')
		self.aptdll.MOT_MoveHome(self.SerialNum)
		'''
		return True


		''' Miscelaneous '''
	def identify(self):
		'''
		Causes the motor to blink the Active LED
		'''
		#self.aptdll.MOT_Identify(self.SerialNum)
		return True

	def cleanUpAPT(self):
		'''
		Releases the APT object
		Use when exiting the program
		'''
		'''
		self.aptdll.APTCleanUp()
		if self.verbose: print( 'APT cleaned up')
		self.Connected = False
		'''
		pass

if __name__ == '__main__':
	# -*- coding: utf-8 -*-

	import time
	Motor1 = APTMotor(83854487, HWTYPE=31) # The number should correspond to the serial number.
	# Use help APTMotor to obtain full list of hardware (HW) supported.

	# Note: You can control multiple motors by creating more APTMotor Objects


	# Obtain current position of motor
	print(Motor1.getPos())
	Motor1.go_home()
	print(Motor1.getPos())
	# You can control multiple motors by creating more APTMotor Objects
	# Serial numbers can be added later by using setSerialNumber and initializeHardwareDevice
	# This functionality is particularly useful in the GUI setup.


	# Move motor forward by 1mm, wait half a second, and return to original position.
	# mRel is move relative. mAbs is move absolute (go to position xxx)
	Motor1.mRel(10) # advance 1mm
	time.sleep(.5)
	print(Motor1.getPos())
	Motor1.mRel(-1) # retract 1mm
	print(Motor1.getPos())
	time.sleep(1)

	# Move motor forward by 1mm, wait half a second, and return to original position, at a velocity of 0.5mm/sec
	motVel = 0.5 #motor velocity, in mm/sec
	Motor1.mcRel(1, motVel) # advance 1mm
	print(Motor1.getPos())
	time.sleep(.5)
	Motor1.mcRel(-1, motVel) # retract 1mm
	print(Motor1.getPos())

	# Clean up APT object, free up memory
	Motor1.cleanUpAPT()
