import cv2
import numpy as np
cv2.namedWindow("original")
cv2.namedWindow("new")
vc = cv2.VideoCapture(0)

# adjust brightness in rgb image to make object more visible


def adjust_image(frame):
    # convert to hsv
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # get brightness
    h, s, v = cv2.split(hsv)
    # increase brightness
    lim = 255 - 50
    v[v > lim] = 255
    v[v <= lim] += 50
    # merge hsv
    final_hsv = cv2.merge((h, s, v))
    # convert to rgb
    frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return frame


if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    frame_new = adjust_image(frame)
    cv2.imshow("original", frame)
    cv2.imshow("new", frame_new)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
cv2.destroyWindow("new")
