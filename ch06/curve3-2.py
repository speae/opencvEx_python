import cv2  # opencv 사용
import numpy as np


# color3, color1 인수가 넘어오지 않을 경우 기본값 설정
def region_of_interest(img, vertices, color3=(255, 255, 255), color1=255):  # ROI 셋팅

    mask = np.zeros_like(img)  # mask = img와 같은 크기의 빈 이미지

    if len(img.shape) > 2:  # Color 이미지(3채널)라면 :
        color = color3
    else:  # 흑백 이미지(1채널)라면 :
        color = color1

    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움
    cv2.fillPoly(mask, vertices, color)
    cv2.imshow('test', mask)

    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    cv2.imshow('test2', ROI_image)
    cv2.waitKey()
    return ROI_image


def mark_img(img, blue_threshold=155, green_threshold=155, red_threshold=155):  # 흰색 차선 찾기

    #  BGR 제한 값
    bgr_threshold = [blue_threshold, green_threshold, red_threshold]

    # BGR 제한 값보다 작으면 검은색으로
    thresholds = (image[:, :, 0] < bgr_threshold[0]) \
                 | (image[:, :, 1] < bgr_threshold[1]) \
                 | (image[:, :, 2] < bgr_threshold[2])
    
    # 영역을 제외한 나머지 부분은 검은색으로 칠함
    mark[thresholds] = [0, 0, 0]
    return mark


image = cv2.imread('Driving_fog.jpg')  # 이미지 읽기
height, width = image.shape[:2]  # 이미지 높이, 너비

# 사다리꼴 모형의 Points
vertices = np.array(
    [[(370, height), (width / 2 + 45, height / 2 + 145), (width / 2 + 160, height / 2 + 145), (width - 150, height)]],
    dtype=np.int32)
# cv2.polylines(image, [vertices], True, (255, 255, 255), 2)
cv2.imshow('test1', image)

# 3번째 인자값은 결과값으로 나오는 차선의 색상값 지정
roi_img = region_of_interest(image, vertices, (0, 0, 255))  # vertices에 정한 점들 기준으로 ROI 이미지 생성

cv2.imshow('test2', image)
cv2.waitKey()

#  roi_img 와 동일한 사이즈의 메모리 할당
mark = np.copy(roi_img)  # roi_img 복사

# 2-1.py의 코드를 mark_img 라는 함수로 만듦
mark = mark_img(mark)  # 흰색 차선 찾기

# 흰색 차선 검출한 부분을 원본 image에 overlap 하기
color_thresholds = (mark[:,:,0] == 0) & (mark[:,:,1] == 0) & (mark[:,:,2] > 155)
image[color_thresholds] = [0,0,255]

cv2.imshow('roi_white', mark)  # 흰색 차선 추출 결과 출력
cv2.imshow('result', image)  # 이미지 출력
cv2.waitKey()
cv2.destroyAllWindows()
