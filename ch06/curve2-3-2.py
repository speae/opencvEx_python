# -*- coding: utf-8 -*- #  UTF-8 encoding으로 변환

import cv2  # opencv
import numpy as np
import sys

def on_low_th(pos):
    global blur, HIGH_th, canny
    LOW_th = pos
    canny = cv2.Canny(blur, LOW_th, HIGH_th)
    cv2.imshow('canny', canny)

def on_high_th(pos):
    global blur, LOW_th, canny
    HIGH_th = pos
    canny = cv2.Canny(blur, LOW_th, HIGH_th)
    cv2.imshow('canny', canny)

# 0. trackbar를 추가하기 위해 canny window를 먼저 생성
cv2.namedWindow('canny', cv2.WINDOW_NORMAL)

cv2.createTrackbar('low_th', 'canny', 0, 99, on_low_th)
cv2.createTrackbar('high_th', 'canny', 80, 255, on_high_th)

cap = cv2.VideoCapture('solidWhiteRight.mp4')  # 동영상 불러오기

first_Frame = True

while (cap.isOpened()):
    ret, image = cap.read()

    if image is None:
        break

    height, width = image.shape[:2]  # 이미지 높이, 너비
    cv2.resizeWindow('canny', width, height)

    # 1. 그레이 이미지로 변경
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 가우시안 블러(필터)
    # kernel_size를 키울수록 blur는 심해진다.
    kernel_size = 3
    blur = cv2.GaussianBlur(gray, (kernel_size,kernel_size),0)

    # 3. canny 영상처리
    LOW_th, HIGH_th = 70, 210
    canny = cv2.Canny(blur, LOW_th, HIGH_th)

    cv2.imshow('gray', gray)
    cv2.imshow('blur', blur)
    cv2.imshow('canny',canny)
    if first_Frame==True:
        cv2.waitKey(0)
        first_Frame=False
    else:
        cv2.waitKey(25)

cv2.destroyAllWindows()