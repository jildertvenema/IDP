#!/bin/python

import time

from libs.ax12 import Ax12

class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id, initial_position):
        self.ax12 = Ax12()
        self.servo_id = servo_id
        self.last_position = initial_position
        self.ax12.move(servo_id, initial_position)
        self.sensitivity = 2

    def is_ready(self):
        return abs(self.ax12.read_position(self.servo_id) - self.last_position) <= self.sensitivity

    # Degrees are 0 - 998
    def move(self, degrees, delay):
        if degrees < 0 or degrees > 998:
            print("In servo " + str(self.servo_id) + ", degrees: " + str(degrees) + ", must be between 0 and 998")

        while not self.is_ready():
            time.sleep(0.2)

        self.last_position = degrees
        self.ax12.move(self.servo_id, degrees)
        time.sleep(delay)

    def read_position(self):
        return self.ax12.read_position(self.servo_id)


def main():
    servoprivod = Servo(13, 0)
    servoprivod.move(500, 0)


if __name__ == "__main__":
    main()