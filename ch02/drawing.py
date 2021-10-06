import numpy as np
import cv2

img = np.full((400, 400, 3), 255, np.uint8)
# 도형이나 직선을 그릴 때는 점의 좌표, 선의 두께
# 점의 좌표 tuple로 표현한다.
# 시작점, 종점, 색깔
cv2.line(img, (50, 50), (200, 50), (0, 0, 255), 10)
cv2.line(img, (50, 60), (150, 160), (0, 0, 128), 5)

# 사각형을 그리는 2가지 방법

# 시작점의 좌표, width, height, 색상, 두께
cv2.rectangle(img, (50, 200, 150, 100), (0, 255, 0), 2)

# 시작점의 좌표, 종점의 좌표, 색상, 두께를 -1로 설정하면 사각형 안을 채워줌
cv2.rectangle(img, (70, 220), (180, 280), (0, 128, 0), -1)

# 중심점의 좌표, 반지름, 색상, 두께, 라인스타일
cv2.circle(img, (300, 100), 30, (255, 255, 0), -1, cv2.LINE_AA)
cv2.circle(img, (300, 100), 60, (255, 0, 0), 3, cv2.LINE_AA)

# 다각형의 좌표값을 list 로 줌
pts = np.array([[250, 200], [300, 200], [350, 300], [250, 300]])

# 다각형 좌표 안을 색깔로 채움
cv2.fillPoly(img, [pts], (255, 0, 255))

# 좌표를 모두 연결하여 폐루프 형성
# cv2.polylines(img, [pts], True, (255, 0, 255), 2)

# 캔버스에 문자열 추가
text = 'Hello? OpenCV ' + cv2.__version__
print(text)

# 문자열의 시작점 좌표, 폰트, 글자의 크기, 색상, 두꼐
cv2.putText(img, text, (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1,
            (0, 0, 255), 2, cv2.LINE_AA)

cv2.imshow("img", img)
cv2.waitKey()
cv2.destroyAllWindows()

