import time
import sys

sys.path.insert(0, '../../../src')

from entities.vision.helpers.vision_helper import *


class Recognize(object):

    def __init__(self, helpers, color_range, saved_buildings=None, settings=None):
        self.color_range = color_range
        self.positions = []
        self.saved_buildings = saved_buildings
        self.helper = helpers.helper
        self.settings = settings

    def run(self):
        # Initialize camera
        cap = cv2.VideoCapture(0)

        while True:
            # Read frame from the camera
            ret, img = cap.read()

            # Apply gaussian blue to the image
            img = cv2.GaussianBlur(img, (9, 9), 0)

            # Calculate the masks
            mask, dead_memes = self.helper.calculate_mask(img, self.color_range)

            image_width = img.size
            img, center = self.helper.crop_to_contours(mask, img)

            # Calculate new cropped masks
            mask_cropped, valid_contours = self.helper.calculate_mask(img, self.color_range, set_contour=True)

            # Append the valid contours to the positions array
            for cnt in range(len(valid_contours)):
                self.positions = self.helper.append_to_positions(self.positions, valid_contours[cnt])

            # Recognize building
            if self.saved_buildings:
                self.recognize_building(self.positions, image_width, center)

            # Show the created image
            cv2.imshow('Spider Cam 3000', mask_cropped)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def recognize_building(self, positions, image_width, center):
        """
        Checks if the currents positions of the blocks matches any saved building
        :param positions: Current reading of POSITIONS
        :return: True if a building is recognized
        """
        result = []

        # If there are no blocks in view return false
        if not len(positions) > 0:
            return False

        # For each building in the saved building list
        for building in range(len(self.saved_buildings)):
            b = self.saved_buildings[building]
            # For each block on the front side of the saved building
            for block in range(len(b)):
                bl = b[block]
                result = [building, "front"]
                # If the current block color and position does not match a saved position,
                # break and check the next side.
                if not self.helper.is_duplicate(bl, positions, 20):
                    return False

        # Use audio to state the recognized building
        print("At time: " + time.ctime() + " Found: ", result[0], result[1])

        # If recent settings are handled
        if not self.settings.new:
            cx = center

            percentage_position = cx / image_width * 100

            # Add to settings
            self.settings.current_building = result[0]
            self.settings.current_side = result[1]
            self.settings.current_position = percentage_position

            self.settings.new = True

        # Return whether a building has been found
        return True

    def get_centre(self, b):
        total = 0

        for block in range(len(b)):
            total += b[block][0]

        return total / len(b)
