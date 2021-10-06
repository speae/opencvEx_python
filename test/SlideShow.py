import glob
import os
import cv2
import sys

base_path = "C:\\Users\\Administrator\\PycharmProjects\\opencvEx_python"
img_path = os.path.join(base_path, "ch01\\images\\*.jpg")
img_files = glob.glob(img_path)

# 1.5sec
interval = 1500

# 리스트에 있는 파일들이 존재하지 않을 경우 예외처리
if not img_files:
    print("img_files : No jpg files")
    sys.exit()

# 이미지를 출력할 창을 생성
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

# 이미지를 출력할 창의 크기를 화면 최대로 설정
cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

idx = 0

while True:
    img = cv2.imread(img_files[idx])

    if img is None:
        print('Image load failed')
        break

    cv2.imshow('image', img)

    # ESC입력이 들어올 때까지 1.5초 간격으로 슬라이드 쇼 진행
    if cv2.waitKey(interval) == 27:
        break

    idx += 1
    if idx >= len(img_files):
        idx = 0

    # 특정한 창 닫기
    cv2.destroyWindow('image')
    
    # 열려있는 모든 창 닫기
    # cv2.destroyAllWindows()