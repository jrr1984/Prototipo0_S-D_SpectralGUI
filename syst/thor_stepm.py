import os
#import sys
from pprint import pprint

from msl.equipment import EquipmentRecord, ConnectionRecord, Backend

from msl.equipment.resources.thorlabs import MotionControl
# ensure that the Kinesis folder is available on PATH
os.environ['PATH'] += os.pathsep + 'C:/Program Files/Thorlabs/Kinesis'






#FUNCIONES DESEADAS POR EL USUARIO
#1) DECIME QUE STEP MOTORS/DRIVERS HAY CONECTADOS A LA COMPU Y DAME LOS SERIAL NUMBER'S
#2) CONECTATE A LOS MOTORES Y LLEVALOS AL HOME XQ ES OBLIGATORIO PARA PODER MOVERLOS
#3) WAIT QUE YA VENÌA..
#4) MOVELOS A UNA CIERTA POSICIÒN X,Y
#5) DESCONECTATE DE LOS MOTORES

class ThorlabsStageWithStepMotors:

    def whos_connected(self):
        print('Building the device list...')
        MotionControl.build_device_list()
        n_devices = MotionControl.get_device_list_size()
        if n_devices == 0:
            print('There are no devices in the device list')
            sys.exit(0)
        elif n_devices == 1:
            print('There is 1 device in the device list')
        else:
            print('There are {} devices in the device list'.format(n_devices))
        all_devices = MotionControl.get_device_list()
        print('The serial numbers of all the devices are: {}'.format(all_devices))
    
        
        
        
    def set_x_and_y_motor(self,serialx,serialy):        
        recordx = EquipmentRecord(
            manufacturer='Thorlabs',
            model='KST101',
            serial= str(serialx),  # update the serial number for your KST101
            connection=ConnectionRecord(
                backend=Backend.MSL,
                address='SDK::Thorlabs.MotionControl.KCube.StepperMotor.dll',
            ),
        )
        recordy = EquipmentRecord(
            manufacturer='Thorlabs',
            model='KST101',
            serial= str(serialy),  # update the serial number for your KST101
            connection=ConnectionRecord(
                backend=Backend.MSL,
                address='SDK::Thorlabs.MotionControl.KCube.StepperMotor.dll',
            ),
        )
        print('The motor in the x direction is the one with serial number # ' + str(serialx))
        print('The motor in the y direction is the one with serial number # ' + str(serialy))
        self.motorx = recordx.connect()
        self.motory = recordy.connect()
        print('Connected to {}'.format(self.motorx))
        print('Connected to {}'.format(self.motory))
        # load the configuration settings (so that we can use the get_real_value_from_device_unit() method)
        try:
            self.motory.load_settings()
            self.motorx.load_settings()
             # start polling at 200 ms
            self.motorx.start_polling(200)
            self.motory.start_polling(200)
            print('Homing both motors...')
            self.motorx.home()
            self.motory.home()
            #self.wait(0,self.motorx)
            #self.wait(0,self.motory)
            print('Homing done.')
        except:
            print("Can-t load settings")
             # start polling at 200 ms
            self.motorx.start_polling(200)
            self.motory.start_polling(200)
            print('Homing both motors...')
            self.motorx.home()
            self.motory.home()
            print('Homing done.')
        
        
    def wait(self,value,motor):
        motor.clear_message_queue()
        message_type, message_id, _ = motor.wait_for_message()
        while message_type != 2 or message_id != value:
            position = motor.get_position()
            real = motor.get_real_value_from_device_unit(position, 'DISTANCE')
            #print('  at position {} [device units] {} [real-world units]'.format(position, real))
            message_type, message_id, _ = motor.wait_for_message()
            
    def move_to_x_y(self,x,y):
        try:
            self.motorx.load_settings()
            self.motory.load_settings()
            self.motorx.move_to_position(self.motorx.get_device_unit_from_real_value(x,0))
            self.motory.move_to_position(self.motory.get_device_unit_from_real_value(y,0))
            
        except:
            self.motorx.move_to_position(self.from_mm_to_device_units(x))
            self.motory.move_to_position(self.from_mm_to_device_units(y))     
            
    def disconnect_stage(self):
        # stop polling and close the connection
        self.motorx.home()
        self.motory.home()
        print('Homing..')
        self.motorx.stop_polling()
        self.motory.stop_polling()
        self.motory.disconnect()
        self.motorx.disconnect()
        print('Stage disconnected')
        
    def get_vel_params(self):
        print(self.motorx.get_vel_params())
        print(self.motory.get_vel_params())
    
    
    def set_vel_params(self,max_vel_x, accel_x,max_vel_y,accel_y):
        self.motorx.set_vel_params(max_vel_x, accel_x)
        self.motory.set_vel_params(max_vel_y, accel_y)
        
      
    def from_device_units_to_mm(self,device_units):
        return float('%.7f'%(4.9785334303194085e-07*device_units - 3.6926158834568621e-12))
    def from_mm_to_device_units(self,mm):
        return int(2008623.651917194*mm + 7.4189049903691962e-06)
    
    def go_home(self):
        self.motorx.start_polling(200)
        self.motory.start_polling(200)
        print('Homing both motors...')
        self.motorx.home()
        self.motory.home()
        try:
            self.wait(0,self.motorx)
            self.wait(0,self.motory)
            print('Homing done.')
        except:
            print('Homing anyway')
    def set_stage(self):
        print('Building the device list...')
        MotionControl.build_device_list()
        n_devices = MotionControl.get_device_list_size()
        if n_devices == 0:
            print('There are no devices in the device list')
            sys.exit(0)
        elif n_devices == 1:
            print('There is 1 device in the device list')
        else:
            print('There are {} devices in the device list'.format(n_devices))
        all_devices = MotionControl.get_device_list()
        print('The serial numbers of all the devices are: {}'.format(all_devices))
        recordx = EquipmentRecord(
            manufacturer='Thorlabs',
            model='KST101',
            serial= str(26001683),  # update the serial number for your KST101
            connection=ConnectionRecord(
                backend=Backend.MSL,
                address='SDK::Thorlabs.MotionControl.KCube.StepperMotor.dll',
            ),
        )
        recordy = EquipmentRecord(
            manufacturer='Thorlabs',
            model='KST101',
            serial= str(26001718),  # update the serial number for your KST101
            connection=ConnectionRecord(
                backend=Backend.MSL,
                address='SDK::Thorlabs.MotionControl.KCube.StepperMotor.dll',
            ),
        )
        print('The motor in the x direction is the one with serial number # ' + str(26001683))
        print('The motor in the y direction is the one with serial number # ' + str(26001718))
        self.motorx = recordx.connect()
        self.motory = recordy.connect()
        print('Connected to {}'.format(self.motorx))
        print('Connected to {}'.format(self.motory))
        # load the configuration settings (so that we can use the get_real_value_from_device_unit() method)
        try:
            self.motory.load_settings()
            self.motorx.load_settings()
             # start polling at 200 ms
            self.motorx.start_polling(200)
            self.motory.start_polling(200)
            print('Homing both motors...')
            self.motorx.home()
            self.motory.home()
            #self.wait(0,self.motorx)
            #self.wait(0,self.motory)
            print('Homing done.')
        except:
            print("Can-t load settings")
             # start polling at 200 ms
            self.motorx.start_polling(200)
            self.motory.start_polling(200)
            print('Homing both motors...')
            self.motorx.home()
            self.motory.home()
            print('Homing done.')          

