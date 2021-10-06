import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt

src_img1 = cv2.imread("trafficLight.jpg")
src_img2 = cv2.imread("trafficLight2.jpg")

src_hsv1 = cv2.cvtColor(src_img1, cv2.COLOR_BGR2HSV)
src_hsv2 = cv2.cvtColor(src_img2, cv2.COLOR_BGR2HSV)

h_max = 179
s_max = v_max = 255


def onchange(pos):
    h1 = cv2.getTrackbarPos('H1', 'dst1')
    s1 = cv2.getTrackbarPos('S1', 'dst1')
    v1 = cv2.getTrackbarPos('V1', 'dst1')

    h2 = cv2.getTrackbarPos('H2', 'dst2')
    s2 = cv2.getTrackbarPos('S2', 'dst2')
    v2 = cv2.getTrackbarPos('V2', 'dst2')

    dst1 = cv2.inRange(src_hsv1, (h1, s1, v1), (h_max, s_max, v_max))
    dst2 = cv2.inRange(src_hsv2, (h2, s2, v2), (h_max, s_max, v_max))

    cv2.imshow('dst1', dst1)
    cv2.imshow('dst2', dst2)


cv2.imshow('src_img1', src_img1)
cv2.imshow('src_img2', src_img2)
cv2.namedWindow('dst1')
cv2.namedWindow('dst2')

cv2.createTrackbar('H1', 'dst1', 0, h_max, onchange)
cv2.createTrackbar('S1', 'dst1', 0, s_max, onchange)
cv2.createTrackbar('V1', 'dst1', 0, v_max, onchange)

cv2.createTrackbar('H2', 'dst2', 0, h_max, onchange)
cv2.createTrackbar('S2', 'dst2', 0, s_max, onchange)
cv2.createTrackbar('V2', 'dst2', 0, v_max, onchange)

cv2.waitKey()

cv2.destroyAllWindows()
