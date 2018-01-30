import cv2
import numpy as np


class Draw2Circuits:
    def __init__(self, first, second, file_name):
        width_first, height_first = first.shape[:2]
        width_second, height_second = second.shape[:2]
        img = np.zeros((max(width_first, width_second), max(height_second, height_second), 3), dtype=np.uint8)
        img[::] = (0, 0, 0)
        a = cv2.findContours(cv2.cvtColor(first, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]
        b = cv2.findContours(cv2.cvtColor(second, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

        #b = cv2.findNonZero(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY))
        cv2.drawContours(img, a, -1, (0, 255, 0), 5)
        cv2.drawContours(img, b, -1, (255, 0, 0), 5)
        cv2.imwrite(file_name, img)
