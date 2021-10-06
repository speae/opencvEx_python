import sys
import numpy as np
import cv2

pt1 = [0, 0]
pt2 = [0, 0]
pt3 = [0, 0]
pt4 = [0, 0]

counter = 0
def on_mouse(event, x, y, flags, param):
    global counter, pt1, pt2, pt3, pt4
    if flags & cv2.EVENT_FLAG_LBUTTON:
        if counter == 0:
            pt1 = [x, y]
            print("pt1, x:{}, y:{}".format(x, y))

        elif counter == 1:
            pt2 = [x, y]
            print("pt2, x:{}, y:{}".format(x, y))

        elif counter == 2:
            pt3 = [x, y]
            print("ptr3, x:{}, y:{}".format(x, y))

        elif counter == 3:
            pt4 = [x, y]
            print("ptr4, x:{}, y:{}".format(x, y))

        counter += 1
        print("x:{}, y:{}".format(x, y))

    elif flags & cv2.EVENT_FLAG_RBUTTON:
        counter -= 1

    if event == cv2.EVENT_MOUSEMOVE:
        print("x:{}, y:{}".format(x, y))


src = cv2.imread('namecard.jpg')

if src is None:
    print('Image load failed!')
    sys.exit()

# 마우스의 이벤트가 감지되면 on_mouse 메소드가 호출
cv2.imshow('src', src)
cv2.setMouseCallback('src', on_mouse, src)

# 마우스 좌표값이 입력되면 아무 키를 눌러 아래를 진행
cv2.waitKey()

w, h = 720, 400
# srcQuad = np.array([[325, 307], [760, 369], [718, 611], [231, 515]], np.float32)
# pt1 ~ pt4 까지는 시계방향으로 마우스를 통해 좌표 지정
srcQuad = np.array([pt1, pt2, pt3, pt4], np.float32)
dstQuad = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], np.float32)

# pers는 변환행렬 (3x3 matrix)
pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
dst = cv2.warpPerspective(src, pers, (w, h))

cv2.imshow('dst', dst)
cv2.waitKey()
cv2.destroyAllWindows()
