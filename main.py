import cv2
import numpy as np
from helper_functions import increase_visibility, decrease_brightness_of_image, increase_contrast
from config import *

if __name__ == "__main__":

    cv2.namedWindow("Vorher -> Nachher")
    stream = cv2.VideoCapture(0)

    if stream.isOpened():  # try to get the first frame
        active, frame = stream.read()
    else:
        active = False

    while active:

        active, frame = stream.read()
        original_frame = decrease_brightness_of_image(frame, demo_effect)

        # TODO: smoothen the mask to achieve more even results in brightened image
        enhanced_frame = increase_visibility(frame)

        # TODO: smoothen the transition between the two images
        side_by_side = np.hstack((original_frame, enhanced_frame))
        cv2.imshow("Vorher -> Nachher", side_by_side)

        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    stream.release()
    cv2.destroyWindow("Vorher -> Nachher")
