import cv2
import numpy as np
cv2.namedWindow("original")
cv2.namedWindow("new")
vc = cv2.VideoCapture(0)

# function to increase visibility in rgb image by adjusting the contrast and brightness


def increase_visibility(img):
    max_gain = 3.5
    # LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # L = LAB[:, :, 0]

    # # threshold L channel with triangle method
    # value, thresh = cv2.threshold(
    #     L, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)
    # print(value)

    # # threshold with adjusted value
    # value = value + 10
    # thresh = cv2.threshold(L, value, 255, cv2.THRESH_BINARY)[1]

    # # invert threshold and make 3 channels
    # #thresh = 255 - thresh
    # thresh = cv2.merge([thresh, thresh, thresh])

    # gain = 0.75
    # blue = cv2.multiply(img[:, :, 0], gain)
    # green = cv2.multiply(img[:, :, 1], gain)
    # red = cv2.multiply(img[:, :, 2], gain)
    # img_bright = cv2.merge([blue, green, red])

    # # blend original and brightened using thresh as mask
    # img = np.where(thresh == 255, img_bright, img)

    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    L = LAB[:, :, 0]

    # threshold L channel with triangle method
    value, thresh = cv2.threshold(
        L, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)
    print(value)

    for i in range(20):
        new_value = int(value*1/(i+1))

        if i == 0:
            thresh = cv2.threshold(L, new_value, 255, cv2.THRESH_BINARY)[1]
            thresh = 255 - thresh
            thresh = cv2.merge([thresh, thresh, thresh])

        gain = (max_gain * 1/(i+1)) + 1
        blue = cv2.multiply(img[:, :, 0], gain)
        green = cv2.multiply(img[:, :, 1], gain)
        red = cv2.multiply(img[:, :, 2], gain)
        img_bright = cv2.merge([blue, green, red])
        result = np.where(thresh == 255, img_bright, img)

    # invert threshold and make 3 channels

    # blend original and brightened using thresh as mask
    #result = np.where(thresh == 255, img_bright, img)
    return result


if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    frame_new = increase_visibility(frame)
    cv2.imshow("original", frame)
    cv2.imshow("new", frame_new)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")
cv2.destroyWindow("new")
