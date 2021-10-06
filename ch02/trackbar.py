import numpy as np
import cv2


def on_level_change(pos):
    color_value = pos * 16
    if color_value >= 255:
        color_value = 255

    # 캔버스의 색깔을 바꿈
    img[:] = color_value
    cv2.imshow('image', img)
    print("pos={}".format(pos))


#  검은색 캔버스
img = np.zeros((480, 640), np.uint8)

# 'image' 창을 생성
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 640, 480)

# 'image'창 안에 Trackbar 추가(trackbar 의 이름은 'level')
# trackbar 가 움직이면 on_level_change 함수가 호출
cv2.createTrackbar('level', 'image', 0, 16, on_level_change)

cv2.imshow('image', img)

# 어떤 키든 상호작용
cv2.waitKey()
cv2.destroyAllWindows()
