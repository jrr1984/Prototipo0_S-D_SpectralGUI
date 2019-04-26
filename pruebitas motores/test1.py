"""
This example shows how to communicate with Thorlabs KST101, KCube Stepper Motor.
"""

# https://es.stackoverflow.com/questions/32165/qu%C3%A9-es-if-name-main
if __name__ == '__main__':
    import os
    from pprint import pprint

    from msl.equipment import EquipmentRecord, ConnectionRecord, Backend

    from msl.equipment.resources.thorlabs import MotionControl
    # ensure that the Kinesis folder is available on PATH
    os.environ['PATH'] += os.pathsep + 'C:/Program Files/Thorlabs/Kinesis'

    print('Building the device list...')
    MotionControl.build_device_list()
    # rather than reading the EquipmentRecord from a database we can create it manually
    record = EquipmentRecord(
        manufacturer='Thorlabs',
        model='KST101',
        serial='26001683',  # update the serial number for your KST101
        connection=ConnectionRecord(
            backend=Backend.MSL,
            address='SDK::Thorlabs.MotionControl.KCube.StepperMotor.dll',
        ),
    )

    def wait(value):
        motor.clear_message_queue()
        message_type, message_id, _ = motor.wait_for_message()
        while message_type != 2 or message_id != value:
            position = motor.get_position()
            real = motor.get_real_value_from_device_unit(position, 'DISTANCE')
            print('  at position {} [device units] {} [real-world units]'.format(position, real))
            message_type, message_id, _ = motor.wait_for_message()

    # connect to the KCube Stepper Motor
    motor = record.connect()
    print('Connected to {}'.format(motor))

    # load the configuration settings (so that we can use the get_real_value_from_device_unit() method)
    #motor.load_settings()

    # start polling at 200 ms
    #motor.start_polling(200)

    # home the device
    #print('Homing...')
    #motor.home()
    #wait(0)
    #print('Homing done. At position {} [device units]'.format(motor.get_position()))

    #motor.stop_polling()
    motor.disconnect()