import sys

from entities.threading.utils import SharedObject

sys.path.insert(0, '../../../src')

from entities.vision.helpers.json_handler import Json_Handler
from entities.vision.vision import Vision
from entities.vision.helpers.vision_helper import Color
from entities.vision.recognize_settings import Recognize_settings


def run(name):
    print("[RUN] " + str(name))
    shoe = [Color("red", [167, 116, 89], [180, 255, 255])]

    json_handler = Json_Handler(shoe, "shoe_ranges")
    color_range = json_handler.get_color_range()

    settings = Recognize_settings(grab_distance=183, recognize_distance_max=250, recognize_distance_min=130)

    vision = Vision(shared_object=SharedObject(), color_range=color_range, settings=settings, min_block_size=300, json=json_handler)

    vision.recognize.run()


run("shoe_detect")