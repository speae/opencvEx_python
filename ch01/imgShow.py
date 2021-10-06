# pip3 install opencv-python
import sys
import cv2
import matplotlib.pyplot as plt

# opencv 채널 순서는 b, g, r 순으로 되어있음
img = cv2.imread('C:/Users/BIT-R42/opencvEx/ch01/cat.bmp')

# opencv의 imshow함수 -> jupyter notebook애서는 잘 안씀
cv2.imshow('win', img) 

print(img.shape)

# matplotlib은 채널의 순서를 r, g, b 순
# matplotlib으로 그림을 그리려면 bgr -> rgb로 바꿔야 함 : convert Color; cvtColor
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()