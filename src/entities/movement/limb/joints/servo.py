#!/bin/python
from __future__ import division
import math

import time

import numpy as np
from libs.ax12 import Ax12


class Servo(object):
    """
    Base class for servo
    """

    def __init__(self, servo_id, initial_position):
        """
        Constructor for servo class
        :param servo_id: ID of the servo
        :param initial_position: The position you want to set the servo at on initialising
        """

        # Create an instance of the Ax12 servo class from the Ax12 library.
        self.ax12 = Ax12()

        print("Setting servo " + str(servo_id) + " to " + str(initial_position))
        # Set the servo variables and move servo to initial position.
        self.servo_id = servo_id
        self.last_position = initial_position
        self.ax12.move_speed(servo_id, initial_position, 300)
        self.sensitivity = 5
        print(str(self.ax12.read_rw_status(self.servo_id)))
        time.sleep(0.1)

    def move_speed(self, degrees, delay, max_speed):
        """
        Function that moves the servo using the ax12 library move function
        :param degrees: Position to move to
        :param delay: Time to wait after executing
        :param speed: The speed at which the servo moves
        :return: None
        """

        # If degrees are out of range print an error
        if degrees < 0 or degrees > 998:
            print("In servo " + str(self.servo_id) + ", degrees: " + str(degrees) + ", must be between 0 and 998")

        # While the servo has not completed it last command wait a bit and check again.
        while not self.is_ready():
            time.sleep(0.1)

        max_speed = max_speed * 1
        # Could be changed or set as parameter
        total_steps = 1

        # Calculating de difference that has to be moved
        start_position = self.last_position
        difference = degrees - start_position
        step = difference / total_steps

        current_position = start_position

        for i in range(total_steps):
            current_position += step
            speed = math.sin((i + 0.5) / total_steps * math.pi) * max_speed
            print("Servo " + str(self.servo_id) + ", step: " + str(i) + ", speed: " + str(round(speed)) + ", degrees: " + str(round(current_position)))
            # Move the servo using the ax12 library with the servo id and degrees.
            self.ax12.move_speed(self.servo_id, round(current_position), round(speed))
            self.last_position = current_position
            while not self.is_ready:
                time.sleep(0.05)
        # Set the last position to the degrees.
        self.last_position = degrees

        time.sleep(delay)

    def is_ready(self):
        """
        Function that checks if a servo completed it`s last move
        :return: Whether or not the servo has completed it`s last move
        """
        return abs(self.ax12.read_position(self.servo_id) - self.last_position) <= self.sensitivity

    def read_position(self):
        """
        Read the position of the servo
        :return: Current position of this servo
        """
        return self.ax12.read_position(self.servo_id)

    def read_speed(self):
        """
        Read the speed of the servo
        :return: The servo speed
        """
        return self.ax12.read_speed(self.servo_id)

def main():
    servo = Servo(13, 0)
    servo.move(500, 0)


if __name__ == "__main__":
    main()
