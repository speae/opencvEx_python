import cv2  # opencv 사용
import numpy as np

img = cv2.imread("Driving_fog.jpg")
height, width = img.shape[:2]
print(width, height)


def roi(image, vertices, color=255):
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, vertices, color)
    cv2.imshow('mask', mask)

    ROI_IMG = cv2.bitwise_and(image, mask)

    return ROI_IMG


vertices = np.array(
    [[(370, height), (width / 2 + 45, height / 2 + 145), (width / 2 + 160, height / 2 + 145),
      (width - 150, height)]],
    dtype=np.int32)
roi_img = roi(img, vertices)
mark = np.copy(roi_img)

cv2.imshow("roi", mark)
cv2.waitKey()
cv2.destroyAllWindows()
