# -*- coding: utf-8 -*-
# 2-5
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import random
import os, sys

# %matplotlib inline

import pafy
import cv2

# 좌표 설정 후 차선만 보일 화면의 크기
# pt1, pt2, pt3, pt4 = [593, 406], [794, 407], [1158, 664], [267, 672]

prev_left_x, prev_left_y, prev_right_x, prev_right_y = [], [], [], []

def video_info(video_arg):
    print("video title : {}".format(video_arg.title))  # 제목
    print("video rating : {}".format(video_arg.rating))  # 평점
    print("video viewcount : {}".format(video_arg.viewcount))  # 조회수
    print("video author : {}".format(video_arg.author))  # 저작권자
    print("video length : {}".format(video_arg.length))  # 길이
    print("video duration : {}".format(video_arg.duration))  # 길이
    print("video likes : {}".format(video_arg.likes))  # 좋아요
    print("video dislikes : {}".format(video_arg.dislikes))  # 싫어요


def wrapping(image):
    (h, w) = image.shape[:2]
    # print("width : {}, height : {}".format(w, h))
    srcQuad = np.array([[w // 2 - 30, h * 0.53], [w // 2 + 60, h * 0.53], [w * 0.3, h], [w, h]], np.float32)
    dstQuad = np.array([[0, 0], [w-350, 0], [400, h], [w-150, h]], np.float32)

    transform_perspective = cv2.getPerspectiveTransform(srcQuad, dstQuad)
    reverse_perspective = cv2.getPerspectiveTransform(dstQuad, srcQuad)
    warp_image = cv2.warpPerspective(image, transform_perspective, (w, h))

    return warp_image, reverse_perspective


def color_filter(image):
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    # b, g, r
    lower = np.array([20, 150, 20])
    upper = np.array([255, 255, 255])

    y_lower = np.array([0, 85, 81])
    y_upper = np.array([190, 255, 255])

    y_mask = cv2.inRange(hls, y_lower, y_upper)
    w_mask = cv2.inRange(hls, lower, upper)
    mask = cv2.bitwise_or(y_mask, w_mask)
    masked = cv2.bitwise_and(image, image, mask=mask)

    return masked


# 히스토그램의 결과를 이용하여 window를 나눔
def plot_gram(threshold):
    hist = np.sum(threshold[threshold.shape[0] // 2:, :], axis=0)
    # hist = cv2.calcHist([threshold], [0], None, [256], [0, 256])
    mid = np.int32(hist.shape[0] / 2)
    left = np.argmax(hist[:mid])
    right = np.argmax(hist[mid:]) + mid + round(mid//10)

    # plt.imshow(threshold)
    # plt.show()

    return left, right


# Define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use the lower case
# out = cv2.VideoWriter('output.mp4', fourcc, 20.0, ( 960, 540 ))


def region_of_interest(img):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    y, x = img.shape[:2]
    # print("roi_width : {}, roi_height : {}".format(x, y))

    # 왼쪽과 오른쪽 roi를 동시 설정; 영역의 범위에 따라 보이는 영역이 바뀜
    left1 = [int(0.1*x), int(y)]
    left2 = [int(0.1*x), int(0.1*y)]
    left3 = [int(0.4*x), int(0.1*y)]
    left4 = [int(0.4*x), int(y)]

    right1 = [int(0.7*x), int(y)]
    right2 = [int(0.7*x), int(0.1*y)]
    right3 = [int(0.9*x), int(0.1*y)]
    right4 = [int(0.9*x), int(y)]

    middle = [int(0.2*x), int(y)]

    shaper = np.array([left1, left2, left3, left4, right1, right2, right3, right4, middle])

    mask = np.zeros_like(img)

    # 흑백, 컬러 구분 없이 흑백으로 채움
    if len(img.shape) > 2:
        ignore_mask_color = (255, 255, 255)
    else:
        ignore_mask_color = 255

    # 식별된 구간 제외 전부 검은색칠
    cv2.fillPoly(mask, np.int32([shaper]), ignore_mask_color)

    # bitwise_and 연산
    masked_image = cv2.bitwise_and(img, mask)
    # cv2.imshow('ROI', masked_image)
    # cv2.waitKey()

    return masked_image


def slide_window_search(binary_warped, left_current, right_current):
    global prev_left_x, prev_left_y, prev_right_x, prev_right_y

    out_img = np.dstack((binary_warped, binary_warped, binary_warped))

    nwindows = 4
    margin = 100
    minpix = 50
    window_height = np.int32(binary_warped.shape[0] / nwindows)
    nonzero = binary_warped.nonzero()  # 선이 있는 부분의 인덱스만 저장
    nonzero_y = np.array(nonzero[0])  # 선이 있는 부분 y의 인덱스 값
    nonzero_x = np.array(nonzero[1])  # 선이 있는 부분 x의 인덱스 값
    left_lane = []
    right_lane = []
    color = [0, 255, 0]
    thickness = 2
    # print("nonzero_x : {}".format(nonzero_x))

    for w in range(nwindows):
        win_y_low = binary_warped.shape[0] - (w + 1) * window_height  # window 윗부분
        win_y_high = binary_warped.shape[0] - w * window_height  # window 아랫 부분
        win_x_left_low = left_current - margin  # 왼쪽 window 왼쪽 위
        win_x_left_high = left_current + margin  # 왼쪽 window 오른쪽 아래
        win_x_right_low = right_current - margin  # 오른쪽 window 왼쪽 위
        win_x_right_high = right_current + margin  # 오른쪽 window 오른쪽 아래

        cv2.rectangle(out_img, (win_x_left_low, win_y_low), (win_x_left_high, win_y_high), color, thickness)
        cv2.rectangle(out_img, (win_x_right_low, win_y_low), (win_x_right_high, win_y_high), color, thickness)
        good_left = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_left_low) & (
                nonzero_x < win_x_left_high)).nonzero()[0]
        good_right = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_right_low) & (
                         nonzero_x < win_x_right_high)).nonzero()[0]

        # if nonzero_x[0] >= win_x_right_low:
        #     good_right = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x >= win_x_right_low) & (
        #             nonzero_x < win_x_right_high)).nonzero()[0]
        # else:
        #     good_right = ((nonzero_y >= win_y_low) & (nonzero_y < win_y_high) & (nonzero_x < win_x_right_low) & (
        #             nonzero_x < win_x_right_high)).nonzero()[0]
        # print("good_right : {}".format(good_right))

        left_lane.append(good_left)
        right_lane.append(good_right)
        cv2.imshow("oo", out_img)

        if len(good_left) > minpix:
            left_current = np.int32(np.mean(nonzero_x[good_left]))
        if len(good_right) > minpix:
            right_current = np.int32(np.mean(nonzero_x[good_right]))

    left_lane = np.concatenate(left_lane)  # np.concatenate() -> array를 1차원으로 합침
    right_lane = np.concatenate(right_lane)

    leftx = nonzero_x[left_lane]
    lefty = nonzero_y[left_lane]
    rightx = nonzero_x[right_lane]
    righty = nonzero_y[right_lane]

    if len(leftx) >= 1000 and len(lefty) >= 1000:
        prev_left_x = leftx
        prev_left_y = lefty

    elif len(leftx) < 1000 or len(leftx) < 1000:
        leftx = prev_left_x
        lefty = prev_left_y

    if len(rightx) >= 1000 and len(righty) >= 1000:
        prev_right_x = rightx
        prev_right_y = righty
    elif len(rightx) < 1000 or len(righty) < 1000:
        rightx = prev_right_x
        righty = prev_right_y


    if rightx.shape == (0,) or righty.shape == (0,):
        rightx = prev_right_x
        righty = prev_right_y


    print("rightx : {}".format(len(rightx)))
    print("righty : {}".format(len(righty)))

    # 0인 행렬이 없어야 함
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)

    ploty = np.linspace(0, binary_warped.shape[0] - 1, binary_warped.shape[0])
    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[2]

    ltx = np.trunc(left_fitx)  # np.trunc() -> 소수점 부분을 버림
    rtx = np.trunc(right_fitx)

    out_img[nonzero_y[left_lane], nonzero_x[left_lane]] = [255, 0, 0]
    out_img[nonzero_y[right_lane], nonzero_x[right_lane]] = [0, 0, 255]

    # 창이 생성됐는지 확인
    # plt.imshow(out_img)
    # plt.plot(left_fitx, ploty, color = 'yellow')
    # plt.plot(right_fitx, ploty, color = 'yellow')
    # plt.xlim(0, 1280)
    # plt.ylim(720, 0)
    # plt.show()

    # 생성된 창들에서 threshold로 이진화한 인덱스들 저장
    ret = {'left_fitx': ltx, 'right_fitx': rtx, 'ploty': ploty}

    return ret


def draw_lane_lines(original_image, warped_image, reverse_warped_image, draw_info):
    left_fitx = draw_info['left_fitx']
    right_fitx = draw_info['right_fitx']
    ploty = draw_info['ploty']

    # 투시 변환한 이미지 크기만한 영역을 만듦
    warp_zero = np.zeros_like(warped_image).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    # vstack -> 두 개의 행렬을 위아래로 합침 -> 열은 같고 행은 늘어남 -> 1차원 증가
    # hstack -> 두 개의 행렬을 좌운로 합침 -> 행은 같고 열은 늘어남 -> 같은 차원에서 요소 증가
    # 도로(면) 그리기
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))

    # 선 그리기
    pts_left_lane_l = np.array([np.transpose(np.vstack([left_fitx - 100 / 5, ploty]))])
    pts_left_lane_r = np.array([np.flipud(np.transpose(np.vstack([left_fitx + 100 / 5, ploty])))])
    pts_left_lane = np.hstack((pts_left_lane_l, pts_left_lane_r))

    pts_right_lane_l = np.array([np.transpose(np.vstack([right_fitx - 100 / 5, ploty]))])
    pts_right_lane_r = np.array([np.flipud(np.transpose(np.vstack([right_fitx + 100 / 5, ploty])))])
    pts_right_lane = np.hstack((pts_right_lane_l, pts_right_lane_r))

    mean_x = np.mean((left_fitx, right_fitx), axis=0)
    pts_mean = np.array([np.flipud(np.transpose(np.vstack([mean_x, ploty])))])

    cv2.fillPoly(color_warp, np.int_([pts]), (216, 168, 74))
    cv2.fillPoly(color_warp, np.int_([pts_mean]), (216, 168, 74))

    cv2.fillPoly(color_warp, np.int_([pts_left_lane]), (0, 0, 255))
    cv2.fillPoly(color_warp, np.int_([pts_right_lane]), (0, 0, 255))

    newwarp = cv2.warpPerspective(color_warp, reverse_warped_image, (original_image.shape[1], original_image.shape[0]))

    result = cv2.addWeighted(original_image, 1, newwarp, 0.4, 0)

    return pts_mean, result


url = "https://www.youtube.com/watch?v=ipyzW38sHg0"

video = pafy.new(url)

video_info(video)

# 원본의 해상도를 불러옴
best = video.getbest(preftype="mp4")
print("best resolution : {}".format(best.resolution))

cap = cv2.VideoCapture(best.url)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = int(cap.get(cv2.CAP_PROP_FPS))
cw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
ch = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (cw, ch)

# test_image = cv2.imread("road.jpg")
# mask_filter = color_filter(test_image)
# cv2.imshow('masked', mask_filter)

out = cv2.VideoWriter("record.avi", fourcc, fps, size)

while cap.isOpened():
    ret1, frame = cap.read()
    if frame is None:
        break

    wrap_img, reverse_img = wrapping(frame)
    wrap_color_filtered_img = color_filter(wrap_img)
    wrap_roi_img = region_of_interest(wrap_color_filtered_img)

    # 이진화를 하여 임계값을 통해 최대한 선만 선명하게 나오도록 설정 
    _gray = cv2.cvtColor(wrap_roi_img, cv2.COLOR_BGR2GRAY)

    # 회색화면으로 전환한 이미지를 픽셀값이 160의 임계값을 넘으면 255, 넘지 않으면 0 처리하여 이진화
    ret2, thresh = cv2.threshold(_gray, 160, 255, cv2.THRESH_BINARY)

    left_threshold, right_threshold = plot_gram(thresh)

    # if frame.shape[0] != 540:  # resizing for challenge video
    #     frame = cv2.resize(frame, None, fx=3 / 4, fy=3 / 4, interpolation=cv2.INTER_AREA)
    # result = detect_lanes_img(frame)

    # cv2.imshow('wrap_img', wrap_img)
    # cv2.imshow('wrap_color_filtered_img', wrap_color_filtered_img)
    # cv2.imshow('wrap_roi_img', wrap_roi_img)
    # cv2.imshow('wrap_reverse_roi_img', wrap_reverse_roi_img)
    # cv2.imshow('threshold', thresh)

    draw_info = slide_window_search(thresh, left_threshold, right_threshold)
    meanPts, result = draw_lane_lines(frame, thresh, reverse_img, draw_info)
    out.write(result)
    cv2.imshow('result', result)

    keyValue = cv2.waitKey(1)
    if keyValue == ord('q'):
        break
    elif keyValue == ord('a'):
        cv2.waitKey(0)

cap.release()

# cv2.waitKey()
cv2.destroyAllWindows()
