import cv2
import numpy as np
cv2.namedWindow("Vorher -> Nachher")
vc = cv2.VideoCapture(0)


def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    # Stacking the original image with the enhanced image
    return enhanced_img


def increase_visibility(img):
    img_hc = increase_contrast(img)
    max_gain = 3  # TODO needs to be adjusted
    LAB = cv2.cvtColor(img_hc, cv2.COLOR_BGR2LAB)

    L = LAB[:, :, 0]

    for i in range(1):  # TODO needs adjustment
        value, thresh = cv2.threshold(
            L, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)
        new_value = value + 10

        thresh = cv2.threshold(L, new_value, 255, cv2.THRESH_BINARY)[1]
        thresh = 255 - thresh
        thresh = cv2.merge([thresh, thresh, thresh])

        gain = max_gain * 1+(1/(i+1))
        blue = cv2.multiply(img_hc[:, :, 0], gain)
        green = cv2.multiply(img_hc[:, :, 1], gain)
        red = cv2.multiply(img_hc[:, :, 2], gain)
        img_bright = cv2.merge([blue, green, red])
        result = np.where(thresh == 255, img_bright, img_hc)

    result = np.hstack((img, result))
    return result


if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:

    frame_new = increase_visibility(frame)
    cv2.imshow("Vorher -> Nachher", frame_new)

    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

vc.release()
cv2.destroyWindow("Vorher -> Nachher")
