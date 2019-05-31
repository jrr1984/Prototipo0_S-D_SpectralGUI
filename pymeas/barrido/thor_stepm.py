import os
import logging
from logging.handlers import SocketHandler
import sys,time
from msl.equipment import EquipmentRecord, ConnectionRecord, Backend
from msl.equipment.resources.thorlabs import MotionControl
os.environ['PATH'] += os.pathsep + 'C:/Program Files/Thorlabs/Kinesis'
log = logging.getLogger('Root logger')
log.setLevel(1)  # to send all messages to cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
log.addHandler(socket_handler)

class ThorlabsStageWithStepMotors:

    def wait(self,value,motor):
        motor.clear_message_queue()
        message_type, message_id, _ = motor.wait_for_message()
        while message_type != 2 or message_id != value:
            message_type, message_id, _ = motor.wait_for_message()
            
    def move_to_x_y(self,x,y): #INPUT EN microm
        x=x/1000 #CONVERSION a mm
        y=y/1000
        try:
            log.info('Moving to position ({},{})'.format(x,y))
            self.motorx.load_settings()
            self.motory.load_settings()
            self.motorx.move_to_position(self.motorx.get_device_unit_from_real_value(x,0))
            self.motory.move_to_position(self.motory.get_device_unit_from_real_value(y,0))
            while self.get_x_y_position() != (x,y):
                time.sleep(0.1)
                log.info('{}'.format(self.get_x_y_position()))
            log.info('Stage in position ({},{})'.format(x, y))
        except:
            log.error('Could not load settings, moving anyway to {},{}'.format(x,y))
            log.info('Moving to position ({},{})'.format(x, y))
            self.motorx.move_to_position(self.from_mm_to_device_units(x))
            self.motory.move_to_position(self.from_mm_to_device_units(y))
            while self.get_x_y_position() != (x ,y):
                time.sleep(0.1)
            log.info('Stage in position ({},{})'.format(x, y))
    def close(self):
        self.motorx.home()
        self.motory.home()
        self.motorx.stop_polling()
        self.motory.stop_polling()
        self.motory.disconnect()
        self.motorx.disconnect()
        log.info('Stage of stepper motors DISCONNECTED')
        
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

    def get_x_y_position(self):
        pos_x = self.motorx.get_position()
        x = float('%.4f' % (self.motorx.get_real_value_from_device_unit(pos_x, 'DISTANCE')))
        pos_y = self.motory.get_position()
        y = float('%.4f' % (self.motory.get_real_value_from_device_unit(pos_y, 'DISTANCE')))
        return x, y

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
        MotionControl.build_device_list()
        all_devices = MotionControl.get_device_list()
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
        self.motorx = recordx.connect()
        self.motory = recordy.connect()
        # load the configuration settings (so that we can use the get_real_value_from_device_unit() method)
        try:
            self.motory.load_settings()
            self.motorx.load_settings()
             # start polling at 200 ms
            self.motorx.start_polling(200)
            self.motory.start_polling(200)
            self.motorx.home()
            self.motory.home()
            time.sleep(1)
            while self.get_x_y_position() != (0.0000, 0.0000):
                time.sleep(0.1)
            log.info('Stage of stepper motors CONNECTED')
        except:
            log.error('Can-t load settings')
            self.motorx.start_polling(200)
            self.motory.start_polling(200)
            self.motorx.home()
            self.motory.home()
            time.sleep(1)
            while self.get_x_y_position() != (0.0000,0.0000):
                time.sleep(0.1)
            log.info('Stage of stepper motors CONNECTED')