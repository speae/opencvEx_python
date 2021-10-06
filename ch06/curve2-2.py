# 2-2는 2-1보다 ROI 설정 부분이 추가
import cv2  # opencv 사용
import numpy as np
import sys

ROI_DISP = False


# color3, color1 인수가 넘어오지 않을 경우 기본값 설정
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
    # cv2.imshow('ROI_image', ROI_image)
    # cv2.waitKey()
    return ROI_image


def mask_img(img, blue_threshold=200, green_threshold=200, red_threshold=200):  # 흰색 차선 찾기
    global mask
    
    #  BGR 제한 값
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]

    # BGR 제한 값보다 작으면 검은색으로
    thresholds = (image[:, :, 0] < bgr_threshold[0]) \
                 | (image[:, :, 1] < bgr_threshold[1]) \
                 | (image[:, :, 2] < bgr_threshold[2])

    # 영역을 제외한 나머지 부분은 검은색으로 칠함
    mask[thresholds] = [0, 0, 0]
    return mask


image = cv2.imread('solidWhiteCurve.jpg')  # 이미지 읽기
if image is None:
    print("Image File is not read!")
    sys.exit(-1)

height, width = image.shape[:2]  # 이미지 높이, 너비

# 사다리꼴 모형의 Points; 좌표값
vertices = np.array(
    [[(140, height), (width / 2 - 45, height / 2 + 60), (width / 2 + 65, height / 2 + 60), (width - 30, height)]],
    dtype=np.int32)

# ROI 마스크를 확인하기 위한 디버깅 부분
if ROI_DISP:
    cv2.polylines(image, [vertices], True, (255, 0, 0), 2)
    cv2.imshow("image", image)

# 3번째 인자값은 결과값으로 나오는 차선의 색상값 지정
# ROI 영역의 색상을 Red로 설정(0, 0, 255)
roi_img = region_of_interest(image, vertices, (0, 0, 255))  # vertices에 정한 점들 기준으로 ROI 이미지 생성

#  roi_img 와 동일한 사이즈의 메모리 할당
mask = np.copy(roi_img)  # roi_img 복사

# 2-1.py의 코드를 mask_img 라는 함수로 만듦
mask = mask_img(mask)  # 흰색 차선 찾기

# 흰색 차선 검출한 부분을 원본 image에 overlap 하기
color_thresholds = (mask[:,:,0] == 0) & (mask[:,:,1] == 0) & (mask[:,:,2] > 200)
image[color_thresholds] = [0,0,255]

cv2.imshow('roi_white', mask)  # 흰색 차선 추출 결과 출력
cv2.imshow('result', image)  # 이미지 출력
cv2.waitKey()
cv2.destroyAllWindows()
