import threading

# GLOBAL VARIABLES
STOP_FLAG = threading.Event()

# REGISTER ADDRESSES
REG_MOTORDIRECTION  = 0x0007        # (Pr0.03)	default: 0		decimals: 0
REG_PEAKCURRENT     = 0x0191        # (Pr5.00)	default: 10		decimals: 1
REG_BAUDRATE        = 0x01BD        # (Pr5.22) 	default: 4		decimals: 0
REG_JOGVELOCITY     = 0x01E1        # (Pr6.00)	default: 60		decimals: 0
REG_PRCONTROL       = 0x6002        # (Pr8.02)	default: 256	decimals: 0
REG_CONTROLWORD     = 0x1801        # (------)	default: 0		decimals: 0

DIRECTION_CODES = {
    "CLOCKWISE": 0x4001,
    "CW": 0x4001,
    "COUNTERCLOCKWISE": 0x4002,
    "CCW": 0x4002
}


class Motor:
    def __init__(self, driver):
        self.driver = driver

        """# Set limit switches
        self.driver.write_register(0x0147, 0x25, 0) # Set DI2 to positive endstop
        self.driver.write_register(0x0149, 0x26, 0) # Set DI3 to negative endstop
        self.driver.write_register(0x014B, 0x27, 0) # Set DI4 to homing probe

        # Set homing method
                # Assuming `driver` is an instance of minimalmodbus.Instrument
        HOMING_REGISTER = 0x600A
        
        # Construct the value based on the manual's bit configuration
        homing_value = 0b0000000000000000  # Start with all bits cleared
        homing_value |= 0b0000000000000001  # Set bit for clockwise homing
        homing_value |= 0b0000000000000000  # Ensure "move to position after homing" is disabled
        homing_value |= 0b0000000000000100  # Set bit for using homing switch

        self.driver.write_register(0x600A, homing_value, 0)

        # Set homing speeds
        self.driver.write_register(0x600F, 200, 0)  # High speed (first approach)
        self.driver.write_register(0x6010, 50, 0)   # Low speed (final approach)"""
        
        """# Set acceleration and deceleration
        self.driver.write_register(0x6011, 2000, 0)  # Acceleration
        self.driver.write_register(0x6012, 2000, 0)  # Deceleration

        # Save parameters
        self.driver.write_register(0x1801, 0x2211, 0) """ 
    
    def enable_motor(self):

    def move_to_position(self, position):
        self.driver.write_register(0x6200, 0x01, 0)  # Set PR0 mode to absolute position mode
        self.driver.write_register(0x6201, position >> 16, 0)  # Set PR0 position high
        self.driver.write_register(0x6202, position & 0xFFFF, 0)  # Set PR0 position low
        self.driver.write_register(0x6203, 200, 0)  # Set PR0 speed value
        self.driver.write_register(0x6204, 2000, 0)  # Set PR0 acceleration
        self.driver.write_register(0x6205, 2000, 0)  # Set PR0 deceleration velocity
        self.driver.write_register(0x6002, 0x0010, 0)  # Trigger PR0 motion

    def e_stop(self):
        self.driver.write_register(0x6002, 0x0040, 0)

    def homing(self):
        self.driver.write_register(0x6002, 0x0020, 0)

    def set_to_zero(self):
        self.driver.write_register(0x6002, 0x0021, 0)

    def home(self):
        print(f"INFO: Starting homing.") 
        
        # Trigger homing operation
        print("INFO: Triggering homing operation...")
        self.driver.write_register(0x6002, 0x0020, 0)  # 0x0020 is the homing trigger command
        
        # Monitor status to confirm homing is complete
        print("INFO: Waiting for homing to complete...")
        while True:
            status = self.driver.read_register(0x1003, 0)  # Read motion state
            if status & 0x40:  # Check if the homing completed bit is set (bit 6)
                break
        
        print("INFO: Homing operation completed successfully.")

"""
01 06 62 00 00 00 01 57 B2      Set PR0 mode to absolute position mode
01 06 62 01 00 03 87 B3         Set PR0 position high
01 06 62 02 0D 40 32 D2         Set PR0 position low
01 06 62 03 02 58 66 E8         Set PR0 speed value
01 06 62 04 00 32 56 66         Set PR0 acceleration
01 06 62 05 00 32 07 A6         Set PR0 deceleration velocity
01 06 60 02 00 10 37 C6         Trigger PR0 motion
01 06 60 02 00 40 37 FA         Emergency stop
"""