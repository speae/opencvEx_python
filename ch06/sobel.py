import sys
import numpy as np
import cv2


src = cv2.imread('lenna.bmp', cv2.IMREAD_GRAYSCALE)

if src is None:
    print('Image load failed!')
    sys.exit()

# x 방향으로만 선이 두꺼워짐
dx = cv2.Sobel(src, -1, 1, 0, delta=128)

# y 방향으로만 선이 두꺼워짐
dy = cv2.Sobel(src, -1, 0, 1, delta=128)

dxdy = cv2.Sobel(src, -1, 1, 1, delta=128)

cv2.imshow('src', src)
cv2.imshow('dx', dx)
cv2.imshow('dy', dy)
cv2.imshow('dxdy', dxdy)
cv2.waitKey()

cv2.destroyAllWindows()
