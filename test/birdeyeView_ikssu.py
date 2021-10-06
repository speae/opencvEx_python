# Import packages
import sys
import cv2
import numpy as np

# 정지 이미지와 동영상을 모두 처리할 수 있는 형태
# 입력되는 이미지가 동영상인지, 정지 이미지인지 설정하는 플래그
project_video = "project_video.mp4"
img_filename = "road.jpg"

video = True
cap = cv2.VideoCapture(project_video)
if not cap.isOpened():
    print("Video isn't exist.")
    video = False

# 이전 좌표 초기값
pt_prev = 0

# 좌표 설정 후 차선만 보일 화면의 크기
w, h = 200, 350
dstQuad = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], np.float32)

# 마우스 클릭 여부
dragSrc = [False, False, False, False]


def draw_line(img, corners):
    copy_img = img.copy()

    c1 = (0, 0, 0)
    c2 = (0, 0, 0)

    for point in corners:
        # 이미지, 좌표, 곡률, 색깔, 두께, 선 종류
        cv2.circle(copy_img, tuple(point), 25, c1, -1, cv2.LINE_AA)

    #  이미지, 좌표1, 좌표2, 색깔, 두께
    cv2.line(copy_img, tuple(corners[0]), tuple(corners[1]), c2, 2, cv2.LINE_AA)
    cv2.line(copy_img, tuple(corners[1]), tuple(corners[2]), c2, 2, cv2.LINE_AA)
    cv2.line(copy_img, tuple(corners[2]), tuple(corners[3]), c2, 2, cv2.LINE_AA)
    cv2.line(copy_img, tuple(corners[3]), tuple(corners[0]), c2, 2, cv2.LINE_AA)

    click_point = cv2.addWeighted(img, 0.3, copy_img, 0.7, 0)

    return click_point


def on_mouse(event, x, y, flags, param):
    global srcQuad, dragSrc, pt_prev, src

    # 마우스 좌클릭 시
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):

            # 좌표를 계산하여 마우스로 클릭한 지점과 거리가 25 미만이 되는 위치의 원을 클릭할 수 있음. 
            # 0번 인덱스에서 거리가 25 이상이면 1번 인덱스로 넘어가 비교
            if cv2.norm(srcQuad[i] - (x, y)) < 25:
                print(cv2.norm(srcQuad[i] - (x, y)))

                # 클릭한 상태에서 i가 drag배열에 해당하는 인덱스로 되고, 해당 인덱스는 True가 됨
                dragSrc[i] = True

                # 처음 클릭했던 좌표값 저장 -> 처음 좌표값 기억
                pt_prev = (x, y)
                break

    # 마우스 좌클릭 후 손 뗄 경우
    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False

    # 클릭한 상태에서 마우스를 움직일 때
    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):

            # 첫번째 좌표 클릭 시 dragSrc[True, False, False, False]이 된 상태
            if dragSrc[i]:

                # 이동 거리에 따라 srcQuad의 좌표값 변화
                dx = x - pt_prev[0]
                dy = y - pt_prev[1]
                srcQuad[i] += (dx, dy)

                copy_img = draw_line(src, srcQuad)
                cv2.imshow('src', copy_img)

                # 현재 입력된 좌표값 할당
                pt_prev = (x, y)
                break
        print("srcQuad_update : %s" % srcQuad)


if video:

    # 비디오 파일 열기
    cap = cv2.VideoCapture(project_video)
    if not cap.isOpened():
        print("Video open failed!")
        sys.exit()

    # 비디오 프레임 크기, 전체 프레임수, FPS 등 출력
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = round(1000 / fps)

    ret, src = cap.read()

    if not ret:
        sys.exit()

    # persepective를 위한 4개 좌표값 초기화
    const_y, const_x = src.shape[:2]
    const_y, const_x = const_y >> 1, const_x >> 1
    print(const_x, const_y)
    pt1 = [const_x, const_y]
    pt2 = [const_x + 100, const_y]
    pt3 = [const_x + 100, const_y + 100]
    pt4 = [const_x, const_y + 100]

    # pt1 ~ pt4까지는 시계방향으로 좌표 지정(다른 방향으로도 설정 가능)
    # 선이 표시될 좌표; cv2.cirle() 메소드에는 정수형 인자만을 수용하므로 int type 설정
    srcQuad = np.array([pt1, pt2, pt3, pt4], np.int32)

    # 마우스의 이벤트가 감지되면 on_mouse메소드가 호출
    click_result = draw_line(src, srcQuad)

    # 처음 원본을 화면에 켜놓음
    cv2.imshow('src', click_result)
    cv2.setMouseCallback('src', on_mouse)

    # 마우스 좌표값이 모두 입력되면 아무 키나 눌러 아래 진행
    while True:
        key = cv2.waitKey()
        if key == 13:  # ENTER 키
            break
        elif key == 27:  # ESC 키
            cv2.destroyWindow('src')
            sys.exit()

    print("srcQuad : %s" % srcQuad)

    # pers는 변환행렬 (3 x 3 matrix); cv2.getPerspectiveTransform() 메소드는 실수형 타입만 수용하므로 float type 설정
    srcQuad = np.array(srcQuad, np.float32)
    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)

    while True:
        ret1, src = cap.read()
        if not ret1:
            sys.exit()
        ret2, click_result = cap.read()
        if not ret2:
            sys.exit()

        KeyValue = cv2.waitKey(delay)
        if KeyValue == 27:
            break

        # 프레임을 계속 읽어와 동영상처럼 움직임, dst에 변환한 행렬대로 화면이 출력하도록 설정하여 src 처럼 동영상으로 출력
        cv2.imshow('src', src)
        dst = cv2.warpPerspective(click_result, pers, (w, h))
        cv2.imshow('dst', dst)

    cap.release()

else:

    # 정지 이미지 읽기
    src = cv2.imread(img_filename)

    if src is None:
        print('Image load failed!')
        sys.exit()

    # persepective를 위한 4개 좌표값 초기화
    const_y, const_x = src.shape[:2]
    const_y, const_x = const_y >> 1, const_x >> 1
    print(const_x, const_y)
    pt1 = [const_x, const_y]
    pt2 = [const_x + 100, const_y]
    pt3 = [const_x + 100, const_y + 100]
    pt4 = [const_x, const_y + 100]

    srcQuad = np.array([pt1, pt2, pt3, pt4], np.int32)

    # 마우스의 이벤트가 감지되면 on_mouse메소드가 호출
    click_result = draw_line(src, srcQuad)

    # 마우스의 이벤트가 감지되면 on_mouse메소드가 호출
    cv2.imshow('src', click_result)
    cv2.setMouseCallback('src', on_mouse)

    cv2.waitKey()

    print("pt1:{}, pt2:{}, pt3:{}, pt4:{}".format(pt1, pt2, pt3, pt4))

    # pers는 변환행렬 (3x3 matrix)
    srcQuad = np.array(srcQuad, np.float32)
    pers = cv2.getPerspectiveTransform(srcQuad, dstQuad)
    dst = cv2.warpPerspective(src, pers, (w, h))

    cv2.imshow('dst', dst)

    cv2.waitKey()

cv2.destroyAllWindows()
