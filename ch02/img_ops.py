import numpy as np
import cv2


# 새 영상 생성하기
# 행, 열

# grayscale image -> empty; 초기화하지 않은 배열 -> 쓰레기 값
# empty로 이미지 영역을 할당했을 때(초기화 x)
img1 = np.empty((240, 320), dtype=np.uint8)

# 검은색 이미지
img2 = np.zeros((240, 320, 3), dtype=np.uint8)    # color image

# 모든 픽셀에 (np.ones = 1)*255를 곱함 -> 흰색 이미지
img3 = np.ones((240, 320), dtype=np.uint8) * 255  # dark gray

# 노란색 이미지(모든 픽셀을 (0, 255, 255)로 채움)
img4 = np.full((240, 320, 3), (0, 255, 255), dtype=np.uint8)  # yellow

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)
cv2.imshow('img4', img4)
cv2.waitKey()
cv2.destroyAllWindows()

# 영상 복사
img1 = cv2.imread('HappyFish.jpg')

# 얕은 복사
img2 = img1

# 깊은 복사
img3 = img1.copy()

print(id(img2))
print(id(img3))

img1.fill(255)

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)
cv2.waitKey()
cv2.destroyAllWindows()

# 부분 영상 추출
img1 = cv2.imread('HappyFish.jpg')

img2 = img1[40:120, 30:150]  # numpy.ndarray의 슬라이싱
img3 = img1[40:120, 30:150].copy()

img2.fill(0)

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)
cv2.waitKey()
cv2.destroyAllWindows()
