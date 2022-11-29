#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import sys

opcion = input("1. Segmentar foto\n2.Segmentar desde la webcam\n:")
color_rgb = np.uint8([[[180, 172, 159]]]) #Color verde 1

color_hsv = cv.cvtColor(color_rgb,cv.COLOR_BGR2HSV)
upperColor = np.array([250, 240, 160])
lowerColor = np.array([4, 150, 100])

print("Color verde hsv:{} ".format(color_hsv))
75,215,1375,215,13
# Segmentar una imagen predeterminada
if opcion == "1":
    img = cv.imread(cv.samples.findFile("verde.jpeg"))
    img = cv.resize(img, (1080, 920))
    colorDetected = cv.inRange(img, lowerColor,upperColor)
    cv.imshow("Display window", img)
    cv.imshow("COLOR", colorDetected)
    k = cv.waitKey(0)
else:
    # Segmentar de la webcam
    img = cv.VideoCapture(0)
    while (img.isOpened()):
        ret, frame = img.read()
        cv.imshow('webCam', frame)
        upperColor = np.array([40, 255, 255])
        lowerColor= np.array([0, 100, 0])
        colorDetected = cv.inRange(frame, lowerColor,upperColor)
        cv.imshow("COLOR", colorDetected)
        if (cv.waitKey(1) == ord('e')):
            break
    img.release()
    cv.destroyAllWindows()

