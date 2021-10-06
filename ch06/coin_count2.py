import sys
import numpy as np
import cv2

# 입력 이미지 불러오기
src = cv2.imread('coin_custom.jpg')

if src is None:
    print('Image open failed!')
    sys.exit()

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 이미지에서 고주파 노이즈가 흐려지게 됨
# 이미지에 고주파 노이즈가 있다고 판단하고 제거하려고 할 때 사용
# gray를 cv2.imshow()한 것과 blr를 cv2.imshow()한 것 비교
blr = cv2.GaussianBlur(gray, (0, 0), 1)

# 허프 변환 원 검출
# 1st : 이미지
# 2nd : 검출방법, 현재는 HOUGH_GRADIENT와  HOUGH_GRADIENT_ALT(OPENCV 4.2 이후 추가)가 있음
# method 는 cv2.HOUGH_GRADIENT_ALT 가 기존 방법보다 더 정확한 원을 검출. 단, HOUGH_GRADIENT_ALT의 경우 입력 인자가 달라지므로 주의.
# 3rd : 입력 영상과 축적 배열의 크기 비율, 1이면 동일 크기
# 4th : 검출된 원 중심점들의 최소 거리
# 5th : 검출기의 높은 임계값
# 6th : 원 검출을 위한 임계값
# 7th : 검출할 원의 최소 반지름
# 8th : 검출할 원의 최대 반지름
circles = cv2.HoughCircles(blr, cv2.HOUGH_GRADIENT, 1, 50,
                           param1=150, param2=40, minRadius=20, maxRadius=80)

print(circles)

# 원 검출 결과 및 동전 금액 출력
sum_of_money = 0
# deep copy
dst = src.copy()

if circles is not None:
    for i in range(circles.shape[1]):
        cx, cy, radius = circles[0][i]
        cv2.circle(dst, (int(cx), int(cy)), int(radius), (0, 0, 255), 2, cv2.LINE_AA)

        # 동전 영역 부분 영상 추출
        x1 = int(cx - radius)
        y1 = int(cy - radius)
        x2 = int(cx + radius)
        y2 = int(cy + radius)
        radius = int(radius)

        crop = dst[y1:y2, x1:x2, :]
        ch, cw = crop.shape[:2]

        # 동전 영역에 대한 ROI 마스크 영상 생성
        # ch, cw 만큼 0으로 채움 -> 검은색 마스크 생성
        # 그 영역 내에서 원을 그림
        mask = np.zeros((ch, cw), np.uint8)
        cv2.circle(mask, (int(cw // 2), int(ch // 2)), radius, 255, -1)
        cv2.imshow('test', mask)

        # 동전 영역 Hue 색 성분을 +40 시프트하고, Hue 평균을 계산
        # 색상
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        hue, _, _ = cv2.split(hsv)
        hue_shift = (hue + 40) % 180
        mean_of_hue = cv2.mean(hue_shift, mask)[0]
        cv2.imshow('test2', hue_shift)

        cv2.waitKey()

        # Hue 평균이 90보다 작으면 10원, 90보다 크면 100원으로 간주
        won = 500
        if mean_of_hue < 45:
            won = 100
        elif mean_of_hue < 50:
            won = 50
        elif mean_of_hue <= 55.5:
            won = 10

        print(mean_of_hue)

        sum_of_money += won

        cv2.putText(crop, "{}th {}won".format(i, won), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (255, 0, 0), 2, cv2.LINE_AA)

cv2.putText(dst, str(sum_of_money) + ' won', (40, 80),
            cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2, cv2.LINE_AA)

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.imshow('gray', gray)
cv2.imshow('blr', blr)
cv2.waitKey()

cv2.destroyAllWindows()
