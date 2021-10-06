import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2


# 그레이스케일 영상의 히스토그램
src = cv2.imread('lenna.bmp', cv2.IMREAD_GRAYSCALE)

if src is None:
    print('Image load failed!')
    sys.exit()

# 입력영상 리스트, 채널, 마스크, 히스토그램 사이즈(bin), ranges(0~255)
hist = cv2.calcHist([src], [0], None, [256], [0, 256])

cv2.imshow('src', src)

plt.plot(hist)
plt.show()

cv2.waitKey()

# 컬러 영상의 히스토그램
# img_name = "lenna.bmp"
img_name = "road.jpg"
src = cv2.imread(img_name)

if src is None:
    print('Image load failed!')
    sys.exit()

colors = ['b', 'g', 'r']
bgr_planes = cv2.split(src)

for (p, c) in zip(bgr_planes, colors):
    hist = cv2.calcHist([p], [0], None, [256], [0, 256])
    plt.plot(hist, color=c)

cv2.imshow('src', src)

plt.show()

cv2.waitKey()

cv2.destroyAllWindows()
