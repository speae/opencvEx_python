# -*- coding: utf-8 -*-

import cv2
import numpy as np


def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅

    # img라는 배열을 참조해서 img.shape -> height, width, channel을 읽어와 그와 동일한 배열 mask 생성
    # zeros_like -> height, width, channel 배열 크기로 0으로 채워진 배열 생성
    # ones_like -> height, width, channel 배열 크기로 1로 채워진 배열 생성
    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 그레이 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)
    cv2.imshow('mask', mask)

    # 이미지와 color로 채워진 ROI를 합침; 픽셀값이 1인 것들은 1이 되고 한 쪽이 0인 것들은 모두 0이 됨
    ROI_image = cv2.bitwise_and(img, mask)
    cv2.imshow('ROI_image', ROI_image)
    # cv2.waitKey()
    return ROI_image


image = cv2.imread("slope_test.jpg")
height, width = image.shape[:2]

# 1. 이미지를 그레이이미지로 변경
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 2. 가우시안 블러(필터)
# kernel_size를 키울수록 blur는 심해진다.
kernel_size = 3  # 커널 사이즈를 키울수록 bluring이 커짐
blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

# 3. canny 영상처리
LOW_th, HIGH_th = 50, 255
canny = cv2.Canny(blur, LOW_th, HIGH_th)  # 커널 사이즈가 클수록 출력되는 선의 개수도 줄어듦

# 4. ROI 영역을 위한 포인트 설정(사다리꼴 포인트 4개 지정)
vertices = np.array(
    [[(80, height), (width / 2 - 25, height / 2 + 60), (width / 2 + 75, height / 2 + 60), (width - 50, height)]],
    dtype=np.int32)

# cv2.polylines(image, [vertices], True, (255, 0, 0), 2)
# cv2.imshow('image', image)
# cv2.waitKey()

# 5. ROI 영역
ROI_img = region_of_interest(canny, vertices)
# cv2.imshow("ROI_img", ROI_img)
# cv2.waitKey()

# 6. hough_lines을 통해 직선 성분 찾기
# line_arr = hough_lines(ROI_img, 1, 1 * np.pi / 180, 30, 10, 20)
rho = 1
theta = 1 * np.pi / 180
threshold = 30
min_line_len = 10
max_line_gap = 20

# 결과값 lines는 리스트
lines = cv2.HoughLinesP(ROI_img, rho, theta, threshold, np.array([]), min_line_len, max_line_gap)
print(len(lines))


def draw_lines(img, lines, color=[0, 0, 255], thickness=2):  # 선 그리기
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

    cv2.imshow("line_img", img)
    cv2.waitKey()


# HoughLinesP의 결과를 확인하기 위한 디버깅 코드
# line_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
# draw_lines(line_img, lines)

# 허프라인을 통해 받는 리턴값
# print(lines)
# print("=================================")
# line 정보에서 2차원 리스트 -> np.squeeze로 1차원 리스트
line_arr = np.squeeze(lines, axis=1)
# print(line_arr)

# fx : line_arr[:, 1] - line_arr[:, 3]
# fy : line_arr[:, 0] - line_arr[:, 2]
# 앞에서 그려진 직선 성분들을 Angle(각도)로 변환하여 slope_degree 리스트 생성ㅂ
slope_degree = (np.arctan2(line_arr[:, 1] - line_arr[:, 3], line_arr[:, 0] - line_arr[:, 2]) * 180) / np.pi

print(slope_degree)
print("before:{}".format(len(line_arr)))

# 직선성분 중에 160도보다 작은 각도들만 저장
line_arr = line_arr[np.abs(slope_degree) < 160]

# 라인 뿐만 아니라 slope_degree 리스트도 160 미만 삭제
slope_degree = slope_degree[np.abs(slope_degree) < 160]
print("after:{}".format(len(line_arr)))

line_arr = line_arr[np.abs(slope_degree) > 95]
slope_degree = slope_degree[np.abs(slope_degree) > 95]
print("after2:{}".format(len(line_arr)))

# Left와 Right 구분 없이 저장
line_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
line_arr_exp = np.expand_dims(line_arr, axis=1)
draw_lines(line_img, line_arr_exp)

# Left, Right Lane을 분리
L_lines, R_lines = line_arr[(slope_degree > 0), :], line_arr[(slope_degree < 0), :]

line_arr_left = np.expand_dims(L_lines, axis=1)
line_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
draw_lines(line_img, line_arr_left)

line_arr_right = np.expand_dims(R_lines, axis=1)
# line_img = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
draw_lines(line_img, line_arr_right)

# 원본 이미지에 차선을 추가로 그리기
alpha = 1
beta = 1
lambd = 0
result = cv2.addWeighted(image, alpha, line_img, beta, lambd)

cv2.imshow('result', result)
cv2.waitKey()

cv2.destroyAllWindows()
