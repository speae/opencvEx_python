import sys
import cv2


# 마스크 영상을 이용한 영상 합성
src = cv2.imread('airplane.bmp', cv2.IMREAD_COLOR)
mask = cv2.imread('mask_plane.bmp', cv2.IMREAD_GRAYSCALE)
dst = cv2.imread('field.bmp', cv2.IMREAD_COLOR)

if src is None or mask is None or dst is None:
    print('Image load failed!')
    sys.exit()

cv2.copyTo(src, mask, dst)
# dst[mask > 0] = src[mask > 0]

cv2.imshow('src', src)
cv2.imshow('dst', dst)
cv2.imshow('mask', mask)
cv2.waitKey()
cv2.destroyAllWindows()

# 알파 채널을 마스크 영상으로 이용
src = cv2.imread('cat.bmp', cv2.IMREAD_COLOR)
# logo = cv2.imread('opencv-logo-white.png', cv2.IMREAD_UNCHANGED)
logo = cv2.imread('dice.png', cv2.IMREAD_UNCHANGED)

if src is None or logo is None:
    print('Image load failed!')
    sys.exit()

print(logo.shape)

# png는 알파 채널이 있으므로 b ,g ,r + 알파채널, 즉 4가 됨 -> 검은색은 아무것도 없다는 표시
# 3 : 알파 채널
mask = logo[:, :, 3]    # mask는 알파 채널로 만든 마스크 영상
print(mask.shape)

# 0 ~ 2 : b, g, r
logo = logo[:, :, :-1]  # logo는 b, g, r 3채널로 구성된 컬러 영상
print(logo.shape)

h, w = mask.shape[:2]
print("mask height : {}, mask width : {}".format(h, w))
crop = src[10:10+h, 10:10+w]  # logo, mask와 같은 크기의 부분 영상 추출
print(src.shape)

cv2.copyTo(logo, mask, crop)
# crop[mask > 0] = logo[mask > 0]

cv2.imshow('src', src)
cv2.imshow('logo', logo)
cv2.imshow('mask', mask)
cv2.waitKey()
cv2.destroyAllWindows()
