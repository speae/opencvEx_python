import sys
import glob
import cv2
import os

# 이미지 파일을 모두 img_files 리스트에 추가
# . : 현재 디렉토리 아래 images 폴더 존재 -> 그 폴더 아래의 모든 jpg 파일; *로 모든 파일을 읽을 수 있음
img_files = glob.glob('C:/Users/BIT-R42/opencvEx/ch01/images/*.jpg')
img_files2 = os.listdir("C:/Users/BIT-R42/opencvEx/ch01/images")

if not img_files:
    print("There are no jpg files in 'images' folder")
    sys.exit()

# 전체 화면으로 'image' 창 생성
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# 무한 루프
cnt = len(img_files)
idx = 0

while True:
    img = cv2.imread(img_files[idx])

    if img is None:
        print('Image load failed!')
        break

    cv2.imshow('image', img)
    if cv2.waitKey(2000) >= 27:
        break

    idx += 1
    if idx >= cnt:
        idx = 0

cv2.destroyAllWindows()
