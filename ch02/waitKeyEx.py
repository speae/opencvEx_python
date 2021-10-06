import sys
import numpy as np
import cv2


img = cv2.imread('cat.bmp', cv2.IMREAD_GRAYSCALE)

if img is None:
    print('Image load failed!')
    sys.exit()

cv2.namedWindow('image')
cv2.imshow('image', img)

while True:
    # waitKeyEx : 특수문자
    keycode = cv2.waitKeyEx()

    # ord를 통해 ASCII코드 값을 바꿈
    if keycode == 0x250000 or keycode == 0x270000:
        img = ~img
        cv2.imshow('image', img)
    elif keycode == 27:
        break

cv2.destroyAllWindows()
