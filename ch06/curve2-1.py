# -*- coding: utf-8 -*-  # 한글 주석쓰려면 이거 해야함; utf-8 Encoding
import cv2 # opencv 사용
import numpy as np
import sys

image = cv2.imread('solidWhiteCurve.jpg') # 이미지 읽기
if image is None:
    print("Image File is not read!")
    sys.exit(-1)

mask = np.copy(image) # image 복사; mask를 뜸

#  BGR 컬러스페이스로 필터링하기 위한 Threshold (제한 값) 설정
blue_threshold = 190
green_threshold = 190
red_threshold = 190

# Threshold 값을 하나의 리스트로 설정
bgr_threshold = [blue_threshold, green_threshold, red_threshold]

# BGR 제한 값보다 작으면 검은색, 크면 흰색
# 스레쉬홀드 = 1 -> 검은색
# image.shape => (540, 960, 3)
# (이미지 세로폭, 가로폭, BGR 채널)
# image[:,:,0] => 이미지의 모든 행, 모든 열, 채널0[B]; 모든 세로, 모든 가로, 흑백
print(image.shape)

# 각 채널 픽셀값이 190보다 작으면 true
temp = (image[:,:,0] < bgr_threshold[0])
print(temp.shape)
print(temp)
np.savetxt("temp.csv", temp, fmt="%d", delimiter=',')

# b 채널 또는 g 채널 또는 r 채널
# BGR 채널 모두 Threshold 값보다 작은 픽셀 값은 True, 이상이면 False로 배열값 저장
thresholds = (image[:,:,0] < bgr_threshold[0]) \
            | (image[:,:,1] < bgr_threshold[1]) \
            | (image[:,:,2] < bgr_threshold[2])

# mask 배열중 thresholds 값이 True 부분은 픽셀값인 BGR 값을 0, 0, 0으로 설정
mask[thresholds] = [0,0,0]
np.savetxt("thresholds.csv", thresholds, fmt="%d", delimiter=',')

cv2.imshow('white',mask) # 흰색 추출 이미지 출력
cv2.imshow('result',image) # 이미지 출력
cv2.waitKey()
cv2.destroyAllWindows()