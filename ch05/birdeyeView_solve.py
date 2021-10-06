import sys
import numpy as np
import cv2

# 정지 이미지와 동영상을 모두 처리 할수 있는 형태
# 입력되는 이미지가 동영상인지, 정지 이미지인지 설정하는 플래그
video = True



def drawROI(img, corners):
    cpy = img.copy()

    # c1 = (192, 192, 255)
    # c2 = (128, 128, 255)
    # 원의 색상
    c1 = (240, 240, 255)
    # 라인의 색상
    c2 = (200, 0, 255)

    for pt in corners:
        cv2.circle(cpy, tuple(pt), 25, c1, -1, cv2.LINE_AA)

    cv2.line(cpy, tuple(corners[0]), tuple(corners[1]), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[1]), tuple(corners[2]), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[2]), tuple(corners[3]), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, tuple(corners[3]), tuple(corners[0]), c2, 2, cv2.LINE_AA)

    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0)

    return disp

def on_mouse(event, x,y, flags, param):
    global srcQuad, dragSrc, ptOld, src

    if event == cv2.EVENT_FLAG_LBUTTON:
        for i in range(4):
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                dragSrc[i] = True
                ptOld = (x, y)
                break
    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False

    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if dragSrc[i]:
                dx = x - ptOld[0]
                dy = y - ptOld[1]

                srcQuad[i] += (dx, dy)

                cpy = drawROI(src, srcQuad)
                cv2.imshow('src', cpy)
                ptOld = (x, y)
                break

img_filename = 'road.jpg'
video_filename = 'project_video.mp4'
dw, dh = 200, 350

if video==True:
    # 비디오 파일 열기
    cap = cv2.VideoCapture(video_filename)

    if not cap.isOpened():
        print("Video open failed!")
        sys.exit()

    # 비디오 프레임 크기, 전체 프레임수, FPS 등 출력
    w  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_fps    = cap.get(cv2.CAP_PROP_FPS)
    delay = round(1000 / video_fps)
    print('video_width:{}'.format(w))
    print('video_height:{}'.format(h))
    print('video_fps:{}'.format(video_fps))

    # 비디오 첫 프레임 읽어오기
    ret, src = cap.read()

    if not ret:
        sys.exit()

    # 정지 이미지로 저장
    # cv2.imwrite(img_filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # 모서리 점들의 좌표, 드래그 상태 여부
    srcQuad = np.array([[30, 30], [30, h - 30], [w - 30, h - 30], [w - 30, 30]], np.float32)
    dstQuad = np.array([[0, 0], [0, dh - 1], [dw - 1, dh - 1], [dw - 1, 0]], np.float32)
    dragSrc = [False, False, False, False]

    # 마우스의 이벤트가 감지되면 on_mouse메소드가 호출
    cv2.namedWindow('src')
    cv2.setMouseCallback('src', on_mouse, src)

    # 모서리점, 사각형 그리기
    disp = drawROI(src, srcQuad)
    cv2.imshow('src', disp)
    cv2.waitKey()

    #pers는 변환행렬 (3x3 matrix)
    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)

    # 마우스 좌표값이 모두 입력되면 아무키나 눌러서 아래를 진행한다.


    while True:
        # 비디오 첫 프레임 읽어오기
        ret, src = cap.read()

        if not ret:
            break

        dst = cv2.warpPerspective(src, pers, (dw, dh))
        cv2.imshow('src', src)
        cv2.imshow('dst', dst)

        keyValue = cv2.waitKey(delay)
        if keyValue==27:
            break

    cap.release()


else:
    # 정지 이미지 읽기
    src = cv2.imread(img_filename)
    if src is None:
        print('Image load failed!')
        sys.exit()

    h, w = src.shape[:2]

    # 모서리 점들의 좌표, 드래그 상태 여부
    srcQuad = np.array([[30, 30], [30, h - 30], [w - 30, h - 30], [w - 30, 30]], np.float32)
    dstQuad = np.array([[0, 0], [0, dh - 1], [dw - 1, dh - 1], [dw - 1, 0]], np.float32)
    dragSrc = [False, False, False, False]

    # 마우스의 이벤트가 감지되면 on_mouse메소드가 호출
    cv2.namedWindow('src')
    cv2.setMouseCallback('src', on_mouse, src)

    # 모서리점, 사각형 그리기
    disp = drawROI(src, srcQuad)

    cv2.imshow('src', disp)

    # 마우스 좌표값이 모두 입력되면 아무키나 눌러서 아래를 진행한다.
    cv2.waitKey()

    #pers는 변환행렬 (3x3 matrix)
    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
    dst = cv2.warpPerspective(src, pers, (dw, dh))

    cv2.imshow('src', src)
    cv2.imshow('dst', dst)

    keyValue = cv2.waitKey()

cv2.destroyAllWindows()