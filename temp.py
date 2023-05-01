from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QMainWindow, QGridLayout)
import sys


class CoffeeKiosk(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('커피 키오스크')

        # 아메리카노 이미지 추가
        am_img = QLabel(self)
        am_pixmap = QPixmap('americano.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        am_img.setPixmap(am_pixmap)

        # 아메리카노 버튼 추가
        btn1 = QPushButton('아메리카노', self)
        btn1.setStyleSheet("background-color: #A0522D; color: white;")
        btn1.clicked.connect(self.americano)

        # 카페라떼 이미지 추가
        latte_img = QLabel(self)
        latte_pixmap = QPixmap('latte.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        latte_img.setPixmap(latte_pixmap)

        # 카페라떼 버튼 추가
        btn2 = QPushButton('카페라떼', self)
        btn2.setStyleSheet("background-color: #A0522D; color: white;")
        btn2.clicked.connect(self.latte)

        # 카푸치노 이미지 추가
        capp_img = QLabel(self)
        capp_pixmap = QPixmap('cappuccino.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        capp_img.setPixmap(capp_pixmap)

        # 카푸치노 버튼 추가
        btn3 = QPushButton('카푸치노', self)
        btn3.setStyleSheet("background-color: #A0522D; color: white;")
        btn3.clicked.connect(self.cappuccino)

        vbox = QVBoxLayout()
        vbox.addWidget(am_img, 0, alignment=Qt.AlignCenter)
        vbox.addWidget(btn1, 0, alignment=Qt.AlignCenter)
        vbox.addWidget(latte_img, 0, alignment=Qt.AlignCenter)
        vbox.addWidget(btn2, 0, alignment=Qt.AlignCenter)
        vbox.addWidget(capp_img, 0, alignment=Qt.AlignCenter)
        vbox.addWidget(btn3, 0, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

    def americano(self):
        print("아메리카노")

    def latte(self):
        print("카페라떼")

    def cappuccino(self):
        print("카푸치노")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeKiosk()
    ex.show()
    sys.exit(app.exec_())