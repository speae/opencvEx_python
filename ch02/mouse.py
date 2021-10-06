# 마우스 RBUTTON 파란색 펜
# 마우스 MBUTTON 흰색 -> 지우개
import sys
import numpy as np
import cv2


oldx = oldy = -1

# 마우스 왼쪽, 오른쪽 클릭, 휠 등 등
def on_mouse(event, x, y, flags, param):
    global oldx, oldy

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN\
            or event == cv2.EVENT_MBUTTONDOWN:
        oldx, oldy = x, y
        print('EVENT_BUTTONDOWN: %d, %d' % (x, y))

    elif event == cv2.EVENT_LBUTTONUP or event == cv2.EVENT_RBUTTONUP\
            or event == cv2.EVENT_MBUTTONUP:
        print('EVENT_BUTTONUP: %d, %d' % (x, y))

    elif event == cv2.EVENT_MOUSEMOVE:
        
        # 마우스 왼쪽 버튼을 누른 상태에서 움직임 
        if flags & cv2.EVENT_FLAG_LBUTTON:

            # 라인을 그림
            cv2.line(img, (oldx, oldy), (x, y), (0, 0, 255), 4, cv2.LINE_AA)
            cv2.imshow('image', img)
            oldx, oldy = x, y

        elif flags & cv2.EVENT_FLAG_RBUTTON:
            # 라인을 그림
            cv2.line(img, (oldx, oldy), (x, y), (255, 0, 0), 4, cv2.LINE_AA)
            cv2.imshow('image', img)
            oldx, oldy = x, y

        elif flags & cv2.EVENT_FLAG_MBUTTON:
            # 라인을 그림
            cv2.line(img, (oldx, oldy), (x, y), (255, 255, 255), 4, cv2.LINE_AA)
            cv2.imshow('image', img)
            oldx, oldy = x, y

WIN_WIDTH = 1024
WIN_HEIGHT = 768
CHANNEL = 3

# 비어있는 캔버스 생성
img = np.ones((WIN_WIDTH, WIN_HEIGHT, CHANNEL), dtype=np.uint8) * 255

# 마우스 이벤트를 처리하는 사용자 함수 on_mouse를 Callback 함수로 등록
cv2.namedWindow('image')
cv2.setMouseCallback('image', on_mouse, img)

cv2.imshow('image', img)
cv2.waitKey()

cv2.destroyAllWindows()
