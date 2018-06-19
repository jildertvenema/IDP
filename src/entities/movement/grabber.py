import datetime
import time
import sys
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.movement.limb.joints.servo import Servo
from entities.movement.sequences.sequences import *


class Grabber(object):
    """
    Base class for grabber which directly implements servo
    """

    def __init__(self, servos, initial_positions):
        """
        Constructor for grabber class
        :param servos: Array of grabber servo id`s
        :param initial_positions: Array of servo positions
        """
        self.previous = datetime.datetime.now()  # The time used for delta timing

        self.servo_0 = Servo(servos[0], initial_positions[0], 5)
        self.servo_1 = Servo(servos[1], initial_positions[1], 5)
        self.servo_2 = Servo(servos[2], initial_positions[2], 5)

        self.servos = [self.servo_0, self.servo_1, self.servo_2]

        self.reposition = False
        self.grabbed = False

        self.move_grabber(initial_positions, 100)

        self.type = 'grabber'
        print("Grabber setup")

    def grab(self, speed):
        """
        Function that contains commands to close grabber
        :param speed: Speed to move with
        :return: None
        """
        positions = [215, 425, 83]  # The servo positions for grabbing
        self.move_grabber(positions, speed)
        self.grabbed = True

    def loosen(self, speed):
        """
        Function that contains commands top open grabber
        :param speed: Speed to move with
        :return: None
        """
        positions = [455, 185, 83]  # The servo positions for loosening
        self.move_grabber(positions, speed)
        self.grabbed = False

    def get_delta(self):
        """
        Calculate the delta time, which can be used so movement always happens at same speed
        :return: Delta time
        """
        next_time = datetime.datetime.now()
        elapsed_time = next_time - self.previous
        self.previous = next_time
        return elapsed_time.total_seconds()

    def move_grabber(self, positions, speed):
        """
        Move the grabber servo`s
        :param positions: Array of servo positions
        :param speed: Speed to move with
        :return: None
        """
        for i in range(len(self.servos)):
            self.servos[i].move(positions[i], speed)
        self.update()  # Update the servos

    def update(self):
        """
        Update all the unready servos
        :return: None
        """
        self.get_delta()
        while len([elem for elem in self.servos if not elem.is_ready()]) != 0:
            print("Unready servos: " + str(len([elem for elem in self.servos if not elem.is_ready()])))
            delta = self.get_delta()
            for i in range(len(self.servos)):
                if not self.servos[i].is_ready():
                    print("Servo " + str(self.servos[i].servo_id + " Load: " + str(self.servos[i].read_load())))
                    if self.servos[i].read_load() > 10000:
                        print("Load to high, loosening: " + str(self.servos[i].read_load()))
                        # self.loosen(100)
                        # self.reposition = True
                        # break
                    self.servos[i].update(delta)


