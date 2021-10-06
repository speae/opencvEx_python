# -*- coding: utf-8 -*- # 한글 주석쓰려면 이거 해야함 <-- 파이썬 인터프리터에서 해석
import cv2  # opencv 사용
import numpy as np
import sys


image = cv2.imread('slope_test.jpg')  # 이미지 읽기
if image is None:
    print("Image File is not read!")
    sys.exit()

height, width = image.shape[:2]     # 이미지 높이, 너비

# 1. 이미지를 그레이이미지로 변경
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. 가우시안 블러(필터)
# kernel_size를 키울수록 blur는 심해진다.
kernel_size = 3     # 커널 사이즈를 키울수록 bluring이 커짐
blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

# 3. canny 영상처리
LOW_th, HIGH_th = 70, 210
canny = cv2.Canny(blur, LOW_th, HIGH_th)        # 커널 사이즈가 클수록 출력되는 선의 개수도 줄어듦

cv2.imshow('blur', blur)
cv2.imshow('gray', gray)
cv2.imshow('canny', canny)

cv2.waitKey()
cv2.destroyAllWindows()