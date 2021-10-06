# Import packages
import cv2
import numpy as np

img = cv2.imread('road.jpg')
print(img.shape) # Print image shape
img_height = img.shape[0]
img_width = img.shape[1]

crop_pos_y = (img_height // 3) * 2

crop_pt_x = img_height
cv2.imshow("original", img)

# Cropping an image
# [height, width]
cropped_image = img[crop_pos_y:img_height-1, 200:img_width-100]

# Display cropped image
cv2.imshow("cropped", cropped_image)

# Save the cropped image
cv2.imwrite("Cropped Image.jpg", cropped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()