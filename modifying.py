from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QMainWindow, QGridLayout, QHBoxLayout, QSpinBox)
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

        # 아메리카노 가격 추가
        am_price = QLabel('4500원', self)

        # 아메리카노 개수 선택
        am_spinbox = QSpinBox(self)
        am_spinbox.setMinimum(0)
        am_spinbox.setMaximum(20)

        # 아메리카노 버튼 추가
        btn1 = QPushButton('아메리카노', self)
        btn1.setStyleSheet("background-color: #A0522D; color: white;")
        btn1.clicked.connect(self.americano)

        # 카페라떼 이미지 추가
        latte_img = QLabel(self)
        latte_pixmap = QPixmap('latte.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        latte_img.setPixmap(latte_pixmap)

        # 카페라떼 가격 추가
        latte_price = QLabel('5000원', self)
        
        # 카페라떼 개수 선택
        latte_spinbox = QSpinBox(self)
        latte_spinbox.setMinimum(0)
        latte_spinbox.setMaximum(20)

        # 카페라떼 버튼 추가
        btn2 = QPushButton('카페라떼', self)
        btn2.setStyleSheet("background-color: #A0522D; color: white;")
        btn2.clicked.connect(self.latte)

        # 카푸치노 이미지 추가
        capp_img = QLabel(self)
        capp_pixmap = QPixmap('cappuccino.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        capp_img.setPixmap(capp_pixmap)

        # 카푸치노 가격 추가
        capp_price = QLabel('5000원', self)

        # 카푸치노 개수 선택
        capp_spinbox = QSpinBox(self)
        capp_spinbox.setMinimum(0)
        capp_spinbox.setMaximum(20)

        # 카푸치노 버튼 추가
        btn3 = QPushButton('카푸치노', self)
        btn3.setStyleSheet("background-color: #A0522D; color: white;")
        btn3.clicked.connect(self.cappuccino)

        # 구매 버튼 추가
        buy_btn = QPushButton('구매', self)
        buy_btn.setStyleSheet("background-color: #A0522D; color: white;")
        buy_btn.clicked.connect(self.buy)

        # 수직 박스 레이아웃에 위젯 추가
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(am_img)
        vbox.addWidget(am_price)
        vbox.addWidget(am_spinbox)
        vbox.addWidget(btn1)

        vbox.addWidget(latte_img)
        vbox.addWidget(latte_price)
        vbox.addWidget(latte_spinbox)
        vbox.addWidget(btn2)

        vbox.addWidget(capp_img)
        vbox.addWidget(capp_price)
        vbox.addWidget(capp_spinbox)
        vbox.addWidget(btn3)

        vbox.addWidget(buy_btn, alignment=Qt.AlignRight)

        self.setLayout(vbox)

        self.show()

    def americano(self):
        pass

    def latte(self):
        pass

    def cappuccino(self):
        pass

    def buy(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeKiosk()
    ex.show()
    sys.exit(app.exec_())