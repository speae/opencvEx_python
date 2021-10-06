import sys
import matplotlib.pyplot as plt
import cv2
import glob
import os

# 컬러 영상 출력
# img_path = 'C:/Users/BIT-R42/opencvEx/ch01/cat.bmp'
# imageList = glob.glob('C:/Users/BIT-R42/opencvEx/ch01/*.bmp')
basePath = "C:/Users/BIT-R42/opencvEx/ch01/"
imageList = glob.glob('C:/Users/BIT-R42/opencvEx/ch01/*.bmp')
imgBGR = cv2.imread(imageList[0])
imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

plt.axis('off')
plt.imshow(imgRGB)
plt.show()

# 그레이스케일 영상 출력
imgGray = cv2.imread(os.path.join(basePath, "cat.bmp"), cv2.IMREAD_GRAYSCALE)
if imgGray is None:
    print("There are no jpg files in 'images' folder")
    sys.exit()

plt.axis('off')
plt.imshow(imgGray, cmap='gray')
plt.show()

# 두 개의 영상을 함께 출력
plt.subplot(121), plt.axis('off'), plt.imshow(imgRGB)
plt.subplot(122), plt.axis('off'), plt.imshow(imgGray, cmap='gray')
plt.show()
