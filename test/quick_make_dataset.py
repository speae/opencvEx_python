## Ex 5-1. QPushButton.
import os
import sys

from data_aug.data_aug import *
from data_aug.bbox_util import *
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap

import cv2


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.bboxes = []
        self.fileName = []
        self.name = ""
        self.img = []
        # C:/Users/BIT-R42/opencvEx/DataAugmentationForObjectDetection/img/background.jpg
        self.srcPath = "C:/Users/BIT-R42/opencvEx/DataAugmentationForObjectDetection/img/background.jpg"
        self.pixmap = self.srcPath
        self.HFlipImage = []
        self.hbox = QHBoxLayout()
        self.imgLabel = QLabel()

        self.initUI()

    def initUI(self):
        # inner = []
        self.fileName = os.path.join("C:/Users/BIT-R42/opencvEx/DataAugmentationForObjectDetection/img", "background"
                                                                                                         ".jpg")
        self.img = cv2.imread(self.fileName)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        img_width = self.img.shape[1]
        img_height = self.img.shape[0]

        white_color = (255, 255, 255)

        # jpg 확장자만 분리하여 txt파일 열기
        self.name, ext = os.path.splitext(self.fileName)

        # yolo v4포맷 파일 열기
        # f = open(self.name + ".txt", 'r')
        # if f is None:
        #     print('cannot open ' + self.fileName)
        #
        # while True:
        #     # 문자열 한줄을 읽어와서
        #     line = f.readline()
        #
        #     # 문자열이 비어있다면 종료
        #     if not line:
        #         break
        #
        #     # 문자열이 비어있지 않으면 문자열 나눠서 디코딩
        #     classNum, x, y, width_ratio, height_ratio = line.split(' ')
        #     # 박스의 센터 좌표값
        #     x_pos = round(img_width * float(x))
        #     y_pos = round(img_height * float(y))
        #     width_pixel = round(img_width * float(width_ratio))
        #     height_pixel = round(img_height * float(height_ratio))
        #     x1 = round(x_pos - width_pixel / 2)
        #     y1 = round(y_pos - height_pixel / 2)
        #     x2 = round(x_pos + width_pixel / 2)
        #     y2 = round(y_pos + height_pixel / 2)
        #
        #     # img = cv2.rectangle(img, (x1,y1), (x2,y2), white_color, 3)
        #     print(x1, y1, x2, y2)
        #
        #     inner.append([float(x1), float(y1), float(x2), float(y2), int(classNum)])
        #
        # f.close()
        # self.bboxes = np.array(inner)

        # Push Button을 객체 생성하면서 버튼 위에 표시되는 문자열 지정; 단축키와 함께 '&'는 단축키 지정
        # & + alphabet : 단축키 설정

        if self.pixmap == self.srcPath:
            # alt + b
            btn1 = QPushButton('Open', self)
            btn1.setIcon(QIcon("../DataAugmentationForObjectDetection/icons/open.png"))
            btn1.setIconSize(QSize(48, 48))

            # 버튼이 눌려있는 상태 시작 여부
            # btn1.setCheckable(True)
            # btn1.setCheckable(False)

            # 한번씩 눌릴때마다 상태 반전; True<->False
            # btn1.toggle()

            # alt + 2
            # btn2 = QPushButton('Button&2', self)
            # btn2 = QPushButton(self)
            # btn2.setText('Button&2')

            btn2 = QPushButton('Open Dir', self)
            btn2.setIcon(QIcon("../DataAugmentationForObjectDetection/icons/open.png"))
            btn2.clicked.connect(self.showDialog)

            # openDir = QAction(QIcon('open.png'), 'Open', self)
            # openDir.setShortcut('Ctrl+O')
            # openDir.setStatusTip('Open Dir')
            # openDir.triggered.connect(self.showDialog)

            # 버튼 비활성화 상태
            # btn3 = QPushButton('Button3', self)
            # btn3.setEnabled(False)

            btn3 = QPushButton('Change Save Dir', self)
            btn3.setIcon(QIcon("../DataAugmentationForObjectDetection/icons/open.png"))

            btn4 = QPushButton('HFLIP', self)
            btn4.setIcon(QIcon("../DataAugmentationForObjectDetection/img/exit.png"))
            btn4.clicked.connect(self.HFLIP)

            btn5 = QPushButton('ROTATE', self)
            btn5.setIcon(QIcon("../DataAugmentationForObjectDetection/img/left_arrow.png"))
            btn5.clicked.connect(self.HFLIP)

            self.pixmap = QPixmap(self.pixmap)

            # self를 앞에 븉여주어 MyApp 클래스의 어느 위치(함수)에서든 접근 가능
            # 클래스 안에서 사용할 수 있는 전역변수로 선언
            # self.imgLabel = QLabel('', self)
            # self.imgLabel.setAlignment(Qt.AlignVCenter)
            self.imgLabel.setPixmap(self.pixmap.scaled(640, 480))

            # self.imgInfoLabel = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
            # self.imgInfoLabel.setAlignment(Qt.AlignCenter)

            # Vertical Box Layout
            vbox = QVBoxLayout()
            vbox.addWidget(btn1)
            vbox.addWidget(btn2)
            vbox.addWidget(btn3)
            vbox.addWidget(btn4)
            vbox.addWidget(btn5)

            # Horizontal Box Layout
            self.hbox.addLayout(vbox)
            self.hbox.addWidget(self.imgLabel)

            self.setLayout(vbox)
            self.setLayout(self.hbox)
            self.setWindowTitle('QPushButton')
            self.setGeometry(300, 300, 300, 200)
            self.show()

        else:

            self.pixmap = QPixmap(self.pixmap)

            # self를 앞에 븉여주어 MyApp 클래스의 어느 위치(함수)에서든 접근 가능
            # 클래스 안에서 사용할 수 있는 전역변수로 선언
            # self.imgLabel = QLabel('', self)
            # self.imgLabel.setAlignment(Qt.AlignVCenter)
            self.imgLabel.setPixmap(self.pixmap.scaled(640, 480))

            # self.imgInfoLabel = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
            # self.imgInfoLabel.setAlignment(Qt.AlignCenter)

            # Vertical Box Layout
            vbox = QVBoxLayout()
            self.hbox.addLayout(vbox)
            self.hbox.addWidget(self.imgLabel)
            self.setLayout(self.hbox)
            self.setWindowTitle('QPushButton')
            self.setGeometry(300, 300, 300, 200)
            self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        print(fname[0])

        if fname[0]:
            # f = open(fname[0], 'r')
            self.imgLabel.setText(fname[0])

            # with f:
            #     data = f.read()
            #     self.imgLabel.setText(data)

    def label2Yolo(self, image_size):
        f = open(self.name + '_HFlip.txt', 'w')

        for value in self.bboxes:
            x1, y1, x2, y2, classNum = value
            img_width = x2 - x1
            img_height = y2 - y1
            width_ratio = img_width / image_size[0]
            height_ratio = img_height / image_size[1]
            yolo_x1 = (x1 + img_width / 2) / image_size[0]
            yolo_y1 = (y1 + img_height / 2) / image_size[1]
            f.write(str(int(classNum)) + ' ' + str(round(yolo_x1, 4)) + ' ' + str(round(yolo_y1, 4)) + ' ' + str(
                round(width_ratio, 4)) + ' ' + str(round(height_ratio, 4)) + '\n')

        f.close()

    # 좌우 반전
    def HFLIP(self):
        # img_, bboxes_ = RandomHorizontalFlip(1)(self.img.copy(), self.bboxes.copy())
        img_ = cv2.flip(self.img.copy(), 1)

        # 이미지 좌우 대칭을 실행
        # 함수의 결과는 좌우 대칭된 이미지와 박스 좌표값을 리턴한다.
        self.HFlipImage = cv2.cvtColor(img_, cv2.COLOR_RGB2BGR)

        # 좌우 대칭 이미지 저장
        Flip_file = self.name + '_HFlip.jpg'
        cv2.imwrite(Flip_file, self.HFlipImage)

        img_size = (img_.shape[1], img_.shape[0])
        # 좌우 대칭 레이블 텍스트로 저장
        # self.label2Yolo(img_size)

        cv2.imshow("HFlipImage", self.HFlipImage)
        self.pixmap = Flip_file
        # self.pixmap = self.HFlipImage

        self.initUI()

        # plotted_img = draw_rect(img_, bboxes_)
        # plt.imshow(plotted_img)
        # plt.show()

    # def ROTATE(self):
    #     # 인수 = 세타값(이동 각도)만큼 랜덤 이동
    #     img_, bboxes_ = RandomRotate(45)(img.copy(), bboxes.copy())
    #     plotted_img = draw_rect(img_, bboxes_)
    #     plt.imshow(plotted_img)
    #     plt.show()


if __name__ == '__main__':

    # int main(argc, argv : 문자열(배열))
    # 마우스 클릭, 키보드 등 사용자 인터페이스를 이벤트 루프에서 받아들여 QApplication() 메소드에서 처리하여
    # 어떤 callback 함수가 있는 슬롯에서 호출
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
