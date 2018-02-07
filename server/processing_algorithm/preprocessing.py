import numpy as np
import cv2


def threshold_img(img):
    rotated_matrix = cv2.getRotationMatrix2D((320, 240), 180, 1.0)
    rotated = cv2.warpAffine(img, rotated_matrix, (640, 480))
    threshold_image = cv2.threshold(rotated, 70, 255, cv2.THRESH_BINARY)[1]
    threshold_image = cv2.bitwise_not(threshold_image)
    return threshold_image


def prepare_img(raw_frame):
    frame = np.fromstring(raw_frame, dtype=np.uint8)
    raw_img = frame.reshape(480, 640)
    prepared_image = threshold_img(raw_img)
    return prepared_image


def find_contours(img):
    contours = cv2.findContours(img.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[0]
    return contours
