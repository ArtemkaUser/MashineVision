import cv2
import numpy as np

img = cv2.imread('img4.JPG')
(width, height, channels) = np.shape(img)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gradX = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)

gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)
gradient = cv2.GaussianBlur(gray, (9, 9), 1)

edged = cv2.Canny(gradient, 20, 30)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (250, 250))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[1]

cv2.drawContours(img, cnts[len(cnts)-1], -2, (0, 255, 0), 1)

pixels = 0
for i in range(width):
    a = closed[i][int(height/2)]
    if (a == 255):
        pixels += 1
scale = 24.965
tolerance = scale/pixels
length = tolerance * pixels
print(length)
#    if (img.all[i, 3679] == (0, 255, 0)):
 #       answer.append(i)

#cv2.line(img, (0, int(height/2)), (width, int(height/2)), (0, 0, 255))
#cv2.imshow("image", img)
#cv2.waitKey(0)