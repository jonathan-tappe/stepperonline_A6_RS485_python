from time import sleep

class Motor:
    def __init__(self, driver):
        self.driver = driver

    def example_multi_absolute_position(self):
        """
        01 06 00 00 00 00 CRC CRC	Set drive control mode to position mode C00.00=0
        01 06 03 00 00 01 CRC CRC	Enable multi-segment position command C03.00=1
        01 06 11 00 00 00 CRC CRC	Set single operation mode C11.00=0
        01 06 11 03 00 01 CRC CRC	Set position profile starting group to Group 1 C11.03=1
        01 06 11 04 00 02 CRC CRC	Set position profile ending group to Group 2 C11.04=2
        01 10 11 06 00 02 04 0B B8 00 00 CRC CRC	Set Group 1 displacement to 3000 pulses C11.06=3000
        01 06 11 08 00 05 CRC CRC	Set Group 1 running speed to 5 RPM C11.08=5
        01 10 11 0A 00 02 04 00 64 00 00 CRC CRC	Set Group 1 acceleration time to 100 ms C11.0A=100
        01 10 11 0C 00 02 04 00 64 00 00 CRC CRC	Set Group 1 deceleration time to 100 ms C11.0C=100
        01 10 11 0E 00 02 04 13 88 00 00 CRC CRC	Set post-operation delay to 5000 ms for Group 1 C11.0E=5000
        01 10 11 10 00 02 04 1F 40 00 00 CRC CRC	Set Group 2 displacement to 8000 pulses C11.10=8000
        01 06 11 12 00 01 CRC CRC	Set Group 2 running speed to 1 RPM C11.12=1
        01 10 11 14 00 02 04 00 64 00 00 CRC CRC	Set Group 2 acceleration time to 100 ms C11.14=100
        01 10 11 16 00 02 04 00 64 00 00 CRC CRC	Set Group 2 deceleration time to 100 ms C11.16=100
        01 10 11 18 00 02 04 13 88 00 00 CRC CRC	Set post-operation delay to 5000 ms for Group 2 C11.18=5000
        01 06 04 00 00 13 CRC CRC	Configure DI1 as position profile trigger C04.00=19 (0x13)
        01 06 04 11 00 01 CRC CRC	Enable motor and start operation C04.11=1
        01 06 04 01 00 01 CRC CRC	Trigger DI1 enable C04.01=1
        01 06 04 11 00 00 CRC CRC	Emergency stop command, disable motor C04.11=0
        01 06 04 01 00 00 CRC CRC	Disable DI1 C04.01=0
        """
        self.driver.write_register(0x0000, 0, 0, 6)  # Set control mode to position mode
        self.driver.write_register(0x0300, 1, 0, 6)  # Enable multi-segment position command
        self.driver.write_register(0x1100, 0, 0, 6)  # Set single operation mode
        self.driver.write_register(0x1103, 1, 0, 6)  # Set position profile starting group to Group 1
        self.driver.write_register(0x1104, 2, 0, 6)  # Set position profile ending group to Group 2
        self.driver.write_register(0x1106, 3000, 0, 6, is_32bit=True, skip_validation=False)  # Set Group 1 displacement to the target position
        self.driver.write_register(0x1108, 5, 0, 6)  # Set Group 1 running speed to 5 RPM
        self.driver.write_register(0x110A, 100, 0, 6, is_32bit=True, skip_validation=True)  # Set Group 1 acceleration time to 100 ms
        self.driver.write_register(0x110C, 100, 0, 6, is_32bit=True, skip_validation=True)  # Set Group 1 deceleration time to 100 ms
        self.driver.write_register(0x110E, 5000, 0, 6, is_32bit=True, skip_validation=True)  # Set post-operation delay to 5000 ms for Group 1
        self.driver.write_register(0x1110, 8000, 0, 6, is_32bit=True, skip_validation=True)  # Set Group 2 displacement to 8000 pulses
        self.driver.write_register(0x1112, 1, 0, 6)  # Set Group 2 running speed to 1 RPM
        self.driver.write_register(0x1114, 100, 0, 6, is_32bit=True, skip_validation=True)  # Set Group 2 acceleration time to 100 ms
        self.driver.write_register(0x1116, 100, 0, 6, is_32bit=True, skip_validation=True)  # Set Group 2 deceleration time to 100 ms
        self.driver.write_register(0x1118, 5000, 0, 6, is_32bit=True, skip_validation=True)  # Set post-operation delay to 5000 ms for Group 2
        self.driver.write_register(0x0400, 0x13, 0, 6)  # Configure DI1 as position profile trigger
        self.driver.write_register(0x0411, 1, 0, 6)  # Enable motor and start operation
        self.driver.write_register(0x0401, 1, 0, 6)  # Trigger DI1 enable
        sleep(3)
        self.driver.write_register(0x0411, 0, 0, 6)  # Emergency stop command, disable motor C04.11=0
        self.driver.write_register(0x0401, 0, 0, 6)  # Disable DI1

    def example_control_speed_mode(self):
        """
        01 06 00 00 00 01 CRC CRC	Set drive control mode to speed mode (C00.00=1)
        01 06 03 20 00 03 CRC CRC	Use internal speed command (C03.20=3)
        01 06 12 00 00 01 CRC CRC	Set speed profile mode to cyclic operation (C12.00=1)
        01 06 12 06 02 58 CRC CRC	Set running speed to 600rpm (C12.06=600)
        01 10 12 0A 00 02 04 00 64 00 00 CRC CRC	Set acceleration time to 100ms (C12.0A=100)
        01 10 12 0C 00 02 04 00 64 00 00 CRC CRC	Set deceleration time to 100ms (C12.0C=100)
        01 06 04 11 00 01 CRC CRC	Enable motor and start operation (C04.11=1)
        01 06 04 11 00 00 CRC CRC	Emergency stop command, disable motor (C04.11=0)
        """
        self.driver.write_register(0x0000, 1, 0, 6)  # Set control mode to speed mode
        self.driver.write_register(0x0320, 3, 0, 6)  # Use internal speed command
        self.driver.write_register(0x1200, 1, 0, 6)  # Set speed profile mode to cyclic operation
        self.driver.write_register(0x1206, 300, 0, 6)  # Set running speed to 600 RPM
        self.driver.write_register(0x120A, 100, 0, 6, is_32bit=True, skip_validation=True)  # Set acceleration time to 100 ms
        self.driver.write_register(0x120C, 100, 0, 6, is_32bit=True, skip_validation=True)  # Set deceleration time to 100 ms
        self.driver.write_register(0x0411, 1, 0, 6)  # Enable motor and start operation
        #self.driver.write_register(0x0411, 0, 0, 6)  # Emergency stop command, disable motor

    def example_control_position_mode(self, position):
        """
        01 06 00 00 00 00 CRC CRC
        01 06 11 01 00 00 CRC CRC
        01 06 03 00 00 02 CRC CRC
        01 06 03 0D 00 01 CRC CRC
        01 06 03 0C 13 88 CRC CRC
        01 06 04 00 00 22 CRC CRC
        01 06 04 11 00 01 CRC CRC
        01 06 04 01 00 01 CRC CRC 
        """

        self.driver.write_register(0x0000, 0, 0, 6)
        self.driver.write_register(0x1101, 0, 0, 6) # Absolute reference position
        self.driver.write_register(0x0300, 2, 0, 6) # reference selection -> steps
        self.driver.write_register(0x030D, 100, 0, 6) # speed
        self.driver.write_register(0x030C, position, 0, 6)
        self.driver.write_register(0x0400, 34, 0, 6)
        self.driver.write_register(0x0411, 1, 0, 6)
        self.driver.write_register(0x0401, 1, 0, 6)
        sleep(1)
        self.driver.write_register(0x0401, 0, 0, 6)
        self.driver.write_register(0x0411, 0, 0, 6)

    def e_stop(self):
        self.driver.write_register(0x0411, 0, 0, 6)  # Emergency stop command, disable motor

    def homing(self):
        pass

    def set_to_zero(self):
        pass

    def home(self):
        pass

    def get_status(self):
        """Read the current status of the motor."""
        try:
            status = self.driver.read_register(0X410A, 0)
            return status
        except IOError as e:
            print(f"ERROR: Failed to read motor status: {e}")
            return None

    def get_position(self):
        """Read the current position of the motor (32-bit value)."""
        try:
            position = self.driver.read_register(0x4016, is_32bit=True, signed=True)
            return position
        except IOError as e:
            print(f"ERROR: Failed to read position: {e}")
            return None
        
    def get_speed(self):
        """Read the current speed of the motor."""
        try:
            speed = self.driver.read_register(0x4001, 0)
            return speed
        except IOError as e:
            print(f"ERROR: Failed to read speed: {e}")
            return None
        
    def get_temperature(self):
        """Read the current temperature of the motor drive."""
        try:
            temperature = self.driver.read_register(0x4030, 0)
            return temperature
        except IOError as e:
            print(f"ERROR: Failed to read temperature: {e}")
            return None