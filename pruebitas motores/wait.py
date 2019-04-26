def wait(value):
        motor.clear_message_queue()
        message_type, message_id, _ = motor.wait_for_message()
        while message_type != 2 or message_id != value:
            position = motor.get_position()
            real = motor.get_real_value_from_device_unit(position, 'DISTANCE')
            print('  at position {} [device units] {} [real-world units]'.format(position, real))
            message_type, message_id, _ = motor.wait_for_message()