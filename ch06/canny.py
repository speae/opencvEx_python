import sys
import numpy as np
import cv2


src = cv2.imread('building.jpg', cv2.IMREAD_GRAYSCALE)

if src is None:
    print('Image load failed!')
    sys.exit()

# 50 미만이면 낮은 값, 150 이상이면 높은 값
# 하단 임계값을 낮출 수록 더 자세히 검출
# apertureSize -> edge에 대한 민감도 커짐
dst = cv2.Canny(src, 50, 150, apertureSize=5)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.waitKey()

cv2.destroyAllWindows()
