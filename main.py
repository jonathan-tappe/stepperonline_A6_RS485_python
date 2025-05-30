import sys
import signal
import atexit

from driver import Driver
from motor import Motor

PORT = "/dev/tty.usbmodem58B60081891"
DEBUG_MODE = True


def main():
    driver = Driver(PORT, DEBUG_MODE)
    motor = Motor(driver)
   
    atexit.register(lambda : motor.e_stop())
    atexit.register(lambda : print("INFO: Program terminated."))
    while True:
        input_position = input("Enter the position to move to: ")
        if input_position == "home":
            motor.homing()
        elif input_position == "zero":
            motor.set_to_zero()
        else:
            motor.move_to_position(int(input_position) * 10000)


if __name__ == "__main__":
    main()
