import minimalmodbus
import logging

class Driver:
    def __init__(self, port="COM4", debug_mode=False):
        self.port = port
        self.debug_mode = debug_mode

        # Set up detailed logging for Modbus frames
        if self.debug_mode:
            # Enable minimalmodbus internal debugging
            minimalmodbus._print_out = True
            
            # Configure logging to show detailed messages
            logging.basicConfig(level=logging.DEBUG)
            logging.getLogger('minimalmodbus').setLevel(logging.DEBUG)
            
            # Create a custom handler for printing raw bytes
            self._setup_custom_logging()


        self.driver = None
        self.connect()

        self.motor = None

        
    def _setup_custom_logging(self):
        """Set up custom logging to display raw Modbus frames"""
        original_write = minimalmodbus._serialports[self.port].write if self.port in minimalmodbus._serialports else None
        
        def _custom_write_wrapper(message):
            # Print message in the desired format
            hex_bytes = ' '.join(f"{b:02X}" for b in message)
            print(f"TX: {hex_bytes}")
            # Call the original function
            if original_write:
                return original_write(message)
            
        # We'll attach this custom writer after connection
        self._original_write = original_write

    def connect(self):
        # TO-DO: Refactor so that 'motor' and 'driver' objects can be passed during runtime after program is initialised
        self.driver = minimalmodbus.Instrument(self.port, 1, minimalmodbus.MODE_RTU)
        
        self.driver.close_port_after_each_call = True
        self.driver.serial.baudrate = 115200
        self.driver.serial.parity = 'N'
        self.driver.serial.bytesize = 8
        self.driver.serial.stopbits = 1
        self.driver.serial.timeout = 1
        self.driver.serial.debug = self.debug_mode
        self.driver.clear_buffers_before_each_transaction = True
        
        print("INFO: Successfully connected to the driver.")

        if self.debug_mode:
            print(self.driver)
            # Now that we're connected, patch the write method to show raw frames
            original_write = self.driver.serial.write
            
            def custom_write(message):
                # Format message as hex bytes with spaces
                hex_bytes = ' '.join(f"{b:02X}" for b in message)
                print(f"TX: {hex_bytes}")
                return original_write(message)
            
            # Replace with our custom writer
            self.driver.serial.write = custom_write
            
            # Also capture responses
            original_read = self.driver.serial.read
            
            def custom_read(size):
                result = original_read(size)
                if result:
                    hex_bytes = ' '.join(f"{b:02X}" for b in result)
                    print(f"RX: {hex_bytes}")
                return result
            
            self.driver.serial.read = custom_read

    def read_register(self, reg_address, decimals=0, is_32bit=False, signed=True):
        try:
            if is_32bit:
                # Read a 32-bit long value (2 registers)
                value = self.driver.read_long(reg_address, functioncode=3, signed=signed)
            else:
                # Read a normal 16-bit register
                value = self.driver.read_register(reg_address, decimals)

            if self.debug_mode:
                print(f"DEBUG: REG: {hex(reg_address)}, VALUE: {value}\n")

            return value
        except IOError as e:
            print(f"ERROR: Failed to read data from driver at register {hex(reg_address)}. Exception: {e}")
            return None

    def write_register(self, reg_address, value, decimals=0, functioncode=6, is_32bit=False, skip_validation=False):
        """
        Write a value to a register. Can handle both 16-bit and 32-bit values.
        
        Args:
            reg_address: Register address to write to
            value: Value to write (16-bit or 32-bit integer)
            decimals: Number of decimals for 16-bit registers
            functioncode: Function code to use for 16-bit writes
            is_32bit: Set to True to write a 32-bit value (uses two consecutive registers)
            skip_validation: Set to True for write-only registers (only applicable for 32-bit writes)
        """
        try:
            if is_32bit:
                # Split the 32-bit value into two 16-bit values
                low_word = value & 0xFFFF
                high_word = (value >> 16) & 0xFFFF
                
                # Write the values to two consecutive registers
                self.driver.write_registers(reg_address, [low_word, high_word])
                
                if self.debug_mode:
                    print(f"DEBUG: Wrote 32-bit value {value} (0x{value:08X}) to register {hex(reg_address)}")
                    print(f"DEBUG: Low word: 0x{low_word:04X}, High word: 0x{high_word:04X}")
                
                # Verify the write by reading back
                if not skip_validation:
                    try:
                        read_value = self.read_register(reg_address, decimals=0, is_32bit=True, signed=False)
                        
                        if read_value is not None and self.debug_mode:
                            print(f"DEBUG: Read back value: {read_value} (0x{read_value:08X})")
                            
                            # Verify if read value matches written value
                            if read_value == value:
                                print(f"DEBUG: Verification successful - values match")
                            else:
                                print(f"DEBUG: Verification failed - expected {value}, got {read_value}")
                        
                        return read_value
                    
                    except IOError as e:
                        if self.debug_mode:
                            print(f"DEBUG: Could not validate write (register may be write-only): {e}")
                        return None
                
                return True
            else:
                # Standard 16-bit register write
                self.driver.write_register(reg_address, value, decimals, functioncode)
                response = self.driver.read_register(reg_address, decimals)
                if self.debug_mode:
                    print(f"DEBUG: Wrote 16-bit value {value} to register {hex(reg_address)}, response: {response}")
                    print("DEBUG: Data written successfully.")
                return response
        
        except IOError as e:
            if self.debug_mode:
                print(f"DEBUG: IOError occurred: {e}")
            print(f'ERROR: Failed to write data to driver on register {hex(reg_address)}.')
            return False
