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
        if input_position == "h":
            motor.homing()
        elif input_position == "z":
            motor.set_to_zero()
        elif input_position == "s":
            current_status = motor.get_status()
            current_position = motor.get_position()
            current_speed = motor.get_speed()
            current_temperature = motor.get_temperature()
            print(f"Current Status: {current_status}")
            print(f"Current Position: {current_position} mm")
            print(f"Current Speed: {current_speed} mm/s")
            print(f"Current Temperature: {current_temperature} °C")
        elif input_position == "es":
            motor.example_control_speed_mode()
        elif input_position == "em":
            motor.example_multi_absolute_position()
        elif input_position == "q":
            print("Exiting program.")
            break
        else:
            try:
                position_mm = int(input_position)
                motor.example_control_position_mode(position_mm)
            except ValueError:
                print("Invalid input. Please enter a valid number or command.")


if __name__ == "__main__":
    main()
