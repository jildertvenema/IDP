import sys
import time
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from threading import Thread

sys.path.insert(0, '../../../src')


class Emotion(object):

    def __init__(self, audio):
        self.audio = audio

        self.pixel_count = 14  # Configure the count of pixels:
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.spi_port = 0
        self.spi_device = 0
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.pixel_count, spi=SPI.SpiDev(self.spi_port, self.spi_device),
                                                   gpio=GPIO)
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!
        self.busy = True
        self.blinking = False
        self.mad = False
        self.happy = False
        self.cycle = False
        self.confused = False
        self.searching = False

    def set_emotion(self, emotion):
        """
        Set the correct emotion based on the input.
        This includes lights and sounds
        :param emotion: string with the kind of emotion you want
        :return:
        """
        self.busy = True
        self.blinking = False
        self.mad = False
        self.happy = False
        self.cycle = False
        self.confused = False
        self.searching = False
        time.sleep(0.1)
        Thread(target=self.set_emotion_thread(emotion)).start()
        #if not self.busy:
            #Thread(target=self.set_emotion_thread, args=(emotion,)).start()

    def set_emotion_thread(self, emotion):
        if emotion == "neutral":
            self.set_color(205, 0, 0)
        elif emotion == "anthem":
            self.blinking = True
            self.busy = False
            while self.blinking:
                self.blink_color(205, 0, 0, 1, 0.3)
            self.set_emotion("neutral")
        elif emotion == "mad":
            self.mad = True
            self.busy = False
            self.audio.play('cyka.mp3')
            while self.mad:
                self.blink_color(205, 0, 0, 1, 0.3)
        elif emotion == "success":
            self.set_color(0, 205, 0)
            self.audio.play('success.mp3')
        elif emotion == "happy":
            self.happy = True
            self.busy = False
            self.audio.play('success.mp3')
            while self.happy:
                self.rainbow_colors()
        elif emotion == "sad":
            self.audio.play('sad.mp3')
            self.set_color(0, 0, 255)
        elif emotion == "pain":
            self.set_color(205, 0, 0)
            self.audio.play('OOF.mp3')
            time.sleep(2)
            self.set_brightness(-255)
        elif emotion == "cycle":
            self.cycle = True
            self.busy = False
            while self.cycle:
                self.rainbow_cycle()
        elif emotion == "appear":
            self.appear_from_back()
        elif emotion == "confused":
            self.confused = True
            self.busy = False
            while self.confused:
                self.blink_color(255, 105, 180, 1, 0.2)
        elif emotion == "confirmed":  # Used for building detection
            self.set_color(0, 205, 0)
        elif emotion == "searching":  # Used for building detection
            self.searching = True
            self.busy = False
            while self.searching:
                self.rotate_color(255, 165, 0, 1)
        elif emotion == "shutdown":
            self.audio.play("powerdown.mp3")
            for i in range(20):
                self.set_brightness(-15)
                time.sleep(0.2)
        self.busy = False

    def set_color(self, r, b, g):
        """
        Function to set the color of the leds
        :param r: red color value
        :param g: green color value
        :param b: blue color value
        :return: void
        """
        for i in range(self.pixels.count()):
            self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
        self.pixels.show()

    def blink_color(self, r, b, g, blink_times, blinkdelay):
        for i in range(blink_times):
            # blink x times, then wait
            self.pixels.clear()
            for k in range(self.pixels.count()):
                self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(r, g, b))
            self.pixels.show()
            time.sleep(blinkdelay)
            self.pixels.clear()
            self.pixels.show()
            time.sleep(blinkdelay)

    @staticmethod
    def wheel(pos):
        """
        Wheel method to generate all the RGB colors for rainbow effects
        """
        if pos < 85:
            return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)

    def set_brightness(self, brightnessoffset):
        for i in range(self.pixels.count()):
            r, g, b = self.pixels.get_pixel_rgb(i)
            r = int(max(0, r + brightnessoffset))
            g = int(max(0, g + brightnessoffset))
            b = int(max(0, b + brightnessoffset))
            self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
        self.pixels.show()

    def rainbow_cycle(self, wait=0.005):
        """
        Function to make the leds display a rainbow cycling animation
        :param wait: Time to wait after a color change, lower is faster animation.
        :return: void
        """
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(self.pixels.count()):
                self.pixels.set_pixel(i, self.wheel(((i * 256 // self.pixels.count()) + j) % 256))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)

    def rainbow_colors(self, wait=0.1):
        """
        Function to make the entire strip cycle rainbow colors at once
        :param wait:
        :return:
        """
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(self.pixels.count()):
                self.pixels.set_pixel(i, self.wheel((256 // self.pixels.count() + j) % 256))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)

    def appear_from_back(self, color=(0, 0, 255)):
        pos = 0
        for i in range(self.pixels.count()):

            for j in reversed(range(i, self.pixels.count())):
                self.pixels.clear()
                # first set all pixels at the begin
                for k in range(i):
                    self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
                # set then the pixel at position j
                self.pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
                self.pixels.show()
                time.sleep(0.01)

    def rotate_color(self, r, g, b, rotate_times):
        for j in range(rotate_times):
            self.pixels.clear()
            for i in range(self.pixels.count()):
                if i > 1:
                    self.pixels.set_pixel(i - 2, Adafruit_WS2801.RGB_to_color(0, 0, 0))
                self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, b, g))
                time.sleep(0.05)
                self.pixels.show()


