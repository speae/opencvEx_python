__author__ = "Seran"

# ./darknet detector demo cfg/coco.data cfg/yolo.cfg yolo.weights <video file> <-- 비디오 파일로 실행 시
import cv2

vidcap = cv2.VideoCapture("C:\\Users\\BIT-R42\\opencvEx\\z_airport_guide_automobile\\videos\\" \
                          "인천국제공항 제1여객터미널 - Walking around Incheon International Airport Terminal 1, " \
                          "Incheon, Korea.mp4")

count = 0

while vidcap.isOpened():

    ret, image = vidcap.read()

    if int(vidcap.get(1)) % 10 == 0:
        print('Saved frame number : ' + str(int(vidcap.get(1))))
        cv2.imwrite("C:\\Users\\BIT-R42\\opencvEx\\z_airport_guide_automobile\\videos_to_img\\iksu_cart%d.jpg"
                    % count, image)
        print('Saved frame%d.jpg' % count)
        count += 1

vidcap.release()
