import glob
import os
import cv2
import sys
import matplotlib.pyplot as plt
import win32api

base_path = "C:\\Users\\Administrator\\PycharmProjects\\opencvEx_python"
img_path = os.path.join(base_path, "dog_image\\*.jpg")
img_files = glob.glob(img_path)
print(len(img_files))

# 1.5sec
interval = 3000

# 리스트에 있는 파일들이 존재하지 않을 경우 예외처리
if not img_files:
    print("img_files : No jpg files")
    sys.exit()

# 이미지를 출력할 창을 생성
# cv2.WINDOW_NORMAL는 불러오는 이미지 사이즈에 맞게 창을 생성
cv2.namedWindow('win1', cv2.WINDOW_NORMAL)
cv2.namedWindow('win2', cv2.WINDOW_NORMAL)
cv2.namedWindow('win3', cv2.WINDOW_NORMAL)
cv2.namedWindow('win4', cv2.WINDOW_NORMAL)

# 이미지를 출력할 창의 크기를 화면 최대로 설정
# cv2.setWindowProperty('win1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('win2', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('win3', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
# cv2.setWindowProperty('win4', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

# 모니터의 가로 픽셀 - 윈도우에서 사용
print("Width = ", win32api.GetSystemMetrics(0))

# 모니터의 세로 픽셀 - 윈도우에서 사용
print("Width = ", win32api.GetSystemMetrics(1))

idx = 0
while True:
    if idx >= len(img_files) - 4:
        idx = 0

    img1 = cv2.imread(img_files[idx])
    img2 = cv2.imread(img_files[idx+1])
    img3 = cv2.imread(img_files[idx+2])
    img4 = cv2.imread(img_files[idx+3])

    if img1 is None or img2 is None or img3 is None or img4 is None:
        print('Image load failed')
        break

    idx += 4

    cv2.imshow('win1', img1)
    cv2.imshow('win2', img2)
    cv2.imshow('win3', img4)
    cv2.imshow('win4', img3)

    # 창의 좌표
    cv2.moveWindow('win1', 0, 0)
    cv2.moveWindow('win3', 0, win32api.GetSystemMetrics(1)//2)
    cv2.moveWindow('win2', win32api.GetSystemMetrics(0)//2, 0)
    cv2.moveWindow('win4', win32api.GetSystemMetrics(0)//2, win32api.GetSystemMetrics(1)//2)

    # 창의  크기 제어
    cv2.resizeWindow('win1', win32api.GetSystemMetrics(0)//2, win32api.GetSystemMetrics(1)//2)
    cv2.resizeWindow('win3', win32api.GetSystemMetrics(0)//2, win32api.GetSystemMetrics(1)//2)
    cv2.resizeWindow('win2', win32api.GetSystemMetrics(0)//2, win32api.GetSystemMetrics(1)//2)
    cv2.resizeWindow('win4', win32api.GetSystemMetrics(0)//2, win32api.GetSystemMetrics(1)//2)

    # ESC입력이 들어올 때까지 1.5초 간격으로 슬라이드 쇼 진행
    if cv2.waitKey(interval) == 27:
        sys.exit()

    # 특정한 창 닫기
    # cv2.destroyWindow('image')

    # 열려있는 모든 창 닫기
    cv2.destroyAllWindows()