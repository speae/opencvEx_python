import sys
import glob
import random

import cv2
import os
import matplotlib.pyplot as plt

img_files = glob.glob("C:\\Users\\BIT-R42\\opencvEx\\test\\dog_image\\*")
if not img_files:
    print("There are no exist img files")
    sys.exit()

cnt = len(img_files)

while True:
    idx = random.randint(0, len(img_files) - 1)
    img_org = cv2.imread(img_files[idx], cv2.IMREAD_COLOR)
    img_cvt = cv2.cvtColor(img_org, cv2.COLOR_BGR2RGB)
    if img_cvt is None:
        print('Image load failed')
        break

    stopKey = cv2.waitKey(2000)
    if stopKey == 27:
        break

    plt.axis("off")
    plt.imshow(img_cvt)
    plt.show()

cv2.destroyAllWindows()
