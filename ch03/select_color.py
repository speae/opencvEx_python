import numpy as np
import cv2

DEBUG = True
img_path = 'trafficLight.jpg'

IMG_WIDTH = 640
IMG_HEIGHT = 480
Hmin = 0
Hmax = 179
Smin = 0
Smax = 255
Vmin = 0
Vmax = 255


def on_Hmin_change(pos):
    global Hmin
    global Hmax

    # Hmin값은 Hmax값보다 항상 작게 유지
    if Hmax < pos:
        Hmin = cv2.setTrackbarPos("Hmin", 'image', Hmax-1)
    else:
        Hmin = pos

    if DEBUG:
        print("pos:{}, Hmin:{}".format(pos, Hmax))

def on_Hmax_change(pos):
    global Hmin
    global Hmax

    if Hmin > pos:
        Hmax = cv2.setTrackbarPos("Hmax", 'image', Hmin+1)
    else:
        Hmax = pos

    if DEBUG:
        print("Hmax:{}".format(Hmax))

def on_Smin_change(pos):
    global Smin
    global Smax

    if Smax < pos:
        Smin = cv2.setTrackbarPos("Smin", 'image', Smax-1)
    else:
        Smin = pos

    if DEBUG:
        print("Smin:{}".format(Smin))

def on_Smax_change(pos):
    global Smin
    global Smax

    if Smin > pos:
        Smax = cv2.setTrackbarPos("Smax", 'image', Smin+1)
    else:
        Smax = pos
    if DEBUG:
        print("Smax:{}".format(Smax))

def on_Vmin_change(pos):
    global Vmin
    global Vmax

    if Vmax < pos:
        Vmin = cv2.setTrackbarPos("Vmin", 'image', Vmax-1)
    else:
        Vmin = pos

    if DEBUG:
        print("Vmin:{}".format(Vmin))

def on_Vmax_change(pos):
    global Vmin
    global Vmax

    if Vmin > pos:
        Vmax = cv2.setTrackbarPos("Vmax", 'image', Vmin+1)
    else:
        Vmax = pos
    if DEBUG:
        print("Vmax:{}".format(Vmax))


#비어있는 캔버스를 배열을 생성
#img = np.zeros((IMG_HEIGHT, IMG_WIDTH, 3), np.uint8)
img = cv2.imread(img_path)
HSVImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H, S, V = cv2.split(HSVImage)


# 창을 생성한다. 창의 이름을 지정해서,
#  trackbar를 추가하기 위해
# trackbar를 추가하고, 초기값도 설정
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', IMG_WIDTH, IMG_HEIGHT)

# trackbar를 추가
# createTrackbar는 trackbar를 추가하는 메소드
# trackbar이름, 추가할 창의 이름, 최소값, 최대값, trackbar를 움직였을때 호출되는 메소드
# H의 최소값 설정
cv2.createTrackbar('Hmin', 'image', 0, 179, on_Hmin_change)
cv2.createTrackbar('Hmax', 'image', 0, 179, on_Hmax_change)
cv2.createTrackbar('Smin', 'image', 0, 255, on_Smin_change)
cv2.createTrackbar('Smax', 'image', 0, 255, on_Smax_change)
cv2.createTrackbar('Vmin', 'image', 0, 255, on_Vmin_change)
cv2.createTrackbar('Vmax', 'image', 0, 255, on_Vmax_change)

# txt파일에 설정값을 저장하면 저장된 값을 읽어와서 셋팅해주는 기능을 추가

# trackbar의 위치를 특정값으로 설정
cv2.setTrackbarPos("Hmin", 'image', 0)
cv2.setTrackbarPos("Hmax", 'image', 179)
cv2.setTrackbarPos("Smin", 'image', 0)
cv2.setTrackbarPos("Smax", 'image', 255)
cv2.setTrackbarPos("Vmin", 'image', 0)
cv2.setTrackbarPos("Vmax", 'image', 255)

cv2.imshow('image', img)


while True:
    mask1 = cv2.inRange(HSVImage, (0, 135, 202), (12, 255, 255))
    mask2 = cv2.inRange(HSVImage, (160, 135, 202), (179, 255, 255))
    addmask = cv2.add(mask1, mask2)
    RANGEmask =  cv2.inRange(HSVImage, (Hmin,Smin,Vmin), (Hmax,Smax, Vmax))
    print(RANGEmask.shape)
    cv2.imshow('RANGEmask', RANGEmask)
    cv2.imshow('addmask', addmask)
    #result = cv2.cvtColor(HSVrange, cv2.COLOR_HSV2BGR)
    #cv2.imshow('result', result)

    if cv2.waitKey(200)==27:
        break

cv2.destroyAllWindows()