import numpy as np
import cv2

img = np.full((400, 400, 3), 255, np.uint8)

# 다각형의 좌표값을 list 로 줌
pts = np.array([[250, 200], [300, 200], [350, 300], [250, 300]])
cv2.polylines(img, [pts], True, (255, 0, 0), 2)

cv2.imshow("img", img)
cv2.waitKey()
cv2.destroyAllWindows()

