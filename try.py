from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys

class CoffeeKiosk(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('커피 키오스크')
        self.setGeometry(100, 100, 400, 80 + 6 * (120 + 20) + 200)

        # 이미지 높이와 간격
        self.image_height = 120
        self.image_gap = 20

        # 메뉴와 가격 정보
        self.menu_info = {
            '아메리카노': 2000,
            '카페모카': 3000,
            '카페라떼': 2500,
            '에스프레소': 1500,
            '카라멜마끼야또': 3500,
            '카푸치노': 2800
        }

        # 아메리카노 이미지
        self.americano_image = QLabel(self)
        pixmap = QPixmap('americano.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.americano_image.setPixmap(pixmap)
        self.americano_image.resize(pixmap.width(), pixmap.height())
        self.americano_image.move(200, 80)

        # 아메리카노 가격
        self.americano_price = QLabel(f'가격: {self.menu_info["아메리카노"]}원', self)
        self.americano_price.move(200, 80 + self.image_height)

        # 카페라떼 이미지
        self.latte_image = QLabel(self)
        pixmap = QPixmap('latte.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.latte_image.setPixmap(pixmap)
        self.latte_image.resize(pixmap.width(), pixmap.height())
        self.latte_image.move(200, 80 + self.image_height + self.image_gap)

        # 카페라떼 가격
        self.latte_price = QLabel(f'가격: {self.menu_info["카페라떼"]}원', self)
        self.latte_price.move(200, 80 + 2 * (self.image_height + self.image_gap))

        # 카푸치노 이미지
        self.cappuccino_image = QLabel(self)
        pixmap = QPixmap('cappuccion.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.cappuccino_image.setPixmap(pixmap)
        self.cappuccino_image.resize(pixmap.width(), pixmap.height())
        self.cappuccino_image.move(200, 80 + 2 * (self.image_height + self.image_gap))

        # 카푸치노 가격
        self.cappuccino_price = QLabel(f'가격: {self.menu_info["카푸치노"]}원', self)
        self.cappuccino_price.move(200, 80 + 3 * (self.image_height + self.image_gap))

        # 카페모카 이미지
        self.caffeEspresso_image = QLabel(self)
        pixmap = QPixmap('caffeEspresso.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.caffeEspresso_image.setPixmap(pixmap)
        self.caffeEspresso_image.resize(pixmap.width(), pixmap.height())
        self.caffeEspresso_image.move(200, 80 + 3 * (self.image_height + self.image_gap))

        # 카페모카 가격
        self.caffeEspresso_price = QLabel(f'가격: {self.menu_info["카페모카"]}원', self)
        self.caffeEspresso_price.move(200, 80 + 4 * (self.image_height + self.image_gap))

        # 에스프레소 이미지
        self.espresso_image = QLabel(self)
        pixmap = QPixmap('espresso.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.espresso_image.setPixmap(pixmap)
        self.espresso_image.resize(pixmap.width(), pixmap.height())
        self.espresso_image.move(200, 80 + 4 * (self.image_height + self.image_gap))

        # 에스프레소 가격
        self.espresso_price = QLabel(f'가격: {self.menu_info["에스프레소"]}원', self)
        self.espresso_price.move(200, 80 + 5 * (self.image_height + self.image_gap))

        # 카라멜마끼야또 이미지
        self.caramelMacchiato_image = QLabel(self)
        pixmap = QPixmap('caramelchiato.jpg')
        pixmap = pixmap.scaledToWidth(150)
        self.caramelMacchiato_image.setPixmap(pixmap)
        self.caramelMacchiato_image.resize(pixmap.width(), pixmap.height())
        self.caramelMacchiato_image.move(200, 80 + 5 * (self.image_height + self.image_gap))

        # 카라멜마끼야또 가격
        self.caramelMacchiato_price = QLabel(f'가격: {self.menu_info["카라멜마끼야또"]}원', self)
        self.caramelMacchiato_price.move(200, 80 + 6 * (self.image_height + self.image_gap))

        # 메뉴 라벨
        menu_label = QLabel('메뉴', self)
        menu_label.move(50, 50)

        # 메뉴 버튼
        self.americano_button = QPushButton('아메리카노', self)
        self.americano_button.move(50, 80)
        self.americano_button.clicked.connect(self.on_menu_button_clicked)

        self.latte_button = QPushButton('카페라떼', self)
        self.latte_button.move(50, 80 + self.image_height + self.image_gap)
        self.latte_button.clicked.connect(self.on_menu_button_clicked)

        self.cappuccino_button = QPushButton('카푸치노', self)
        self.cappuccino_button.move(50, 80 + 2 * (self.image_height + self.image_gap))
        self.cappuccino_button.clicked.connect(self.on_menu_button_clicked)

        self.caffeEspresso_button = QPushButton('카페모카', self)
        self.caffeEspresso_button.move(50, 80 + 3 * (self.image_height + self.image_gap))
        self.caffeEspresso_button.clicked.connect(self.on_menu_button_clicked)

        self.espresso_button = QPushButton('에스프레소', self)
        self.espresso_button.move(50, 80 + 4 * (self.image_height + self.image_gap))
        self.espresso_button.clicked.connect(self.on_menu_button_clicked)

        self.caramelMacchiato_button = QPushButton('카라멜마끼야또', self)
        self.caramelMacchiato_button.move(50, 80 + 5 * (self.image_height + self.image_gap))
        self.caramelMacchiato_button.clicked.connect(self.on_menu_button_clicked)


        # 수량 라벨
        quantity_label = QLabel('수량', self)
        quantity_label.move(200, 50)

        # 수량 입력창
        self.quantity_edit = QLineEdit(self)
        self.quantity_edit.move(200, 320)

        # 결제 버튼
        self.payment_button = QPushButton('결제', self)
        self.payment_button.move(200, 360 + 7 * (self.image_height + self.image_gap))
        self.payment_button.clicked.connect(self.on_payment_button_clicked)

        # 선택한 메뉴와 개수, 메뉴별로 개수에 따른 가격, 전체 가격을 보여주는 라벨
        self.selected_menu_label = QLabel('', self)
        self.selected_menu_label.move(50, 360 + 7 * (self.image_height + self.image_gap))
        self.quantity_label = QLabel('', self)
        self.quantity_label.move(50, 380 + 7 * (self.image_height + self.image_gap))
        self.price_label = QLabel('', self)
        self.price_label.move(50, 400 + 7 * (self.image_height + self.image_gap))
        self.total_price_label = QLabel('', self)
        self.total_price_label.move(50, 420 + 7 * (self.image_height + self.image_gap))

        # 창 위치 조정
        self.center()

        # 창 보이기
        self.show()



def center(self):
    # 창을 화면의 가운데로 이동
    qr = self.frameGeometry
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())

def on_menu_button_clicked(self):
    # 메뉴 버튼 클릭 시 동작하는 함수
    selected_menu = ''
    if self.sender() == self.americano_button:
        selected_menu = '아메리카노'
    elif self.sender() == self.latte_button:
        selected_menu = '카페라떼'
    elif self.sender() == self.cappuccino_button:
        selected_menu = '카푸치노'
    elif self.sender() == self.caffeEspresso_button:
        selected_menu = '카페모카'
    elif self.sender() == self.espresso_button:
        selected_menu = '에스프레소'
    elif self.sender() == self.caramelMacchiato_button:
        selected_menu = '카라멜마끼야또'

    # 선택한 메뉴와 가격을 출력
    self.selected_menu_label.setText(f'선택한 메뉴: {selected_menu}')
    self.selected_menu_label.adjustSize()
    self.price_label.setText(f'가격: {self.menu_info[selected_menu]}원')
    self.price_label.adjustSize()

def on_payment_button_clicked(self):
    # 결제 버튼 클릭 시 동작하는 함수
    quantity = self.quantity_edit.text()
    if not quantity.isdigit():
        QMessageBox.warning(self, '경고', '수량은 숫자로 입력해주세요.')
        return
    quantity = int(quantity)
    if quantity <= 0:
        QMessageBox.warning(self, '경고', '수량은 1 이상이어야 합니다.')
        return

    # 선택한 메뉴와 수량, 가격 정보를 출력
    selected_menu = self.selected_menu_label.text().split(': ')[1]
    price = self.menu_info[selected_menu]
    self.quantity_label.setText(f'수량: {quantity}')
    self.quantity_label.adjustSize()
    self.price_label.setText(f'가격: {price}원')
    self.price_label.adjustSize()

    # 메뉴별로 개수에 따른 가격을 계산하여 출력
    total_price = price * quantity
    self.total_price_label.setText(f'총 가격: {total_price}원')
    self.total_price_label.adjustSize()

    # 결제 완료 메시지 출력
    QMessageBox.information(self, '주문 완료', f'{selected_menu} {quantity}잔을 주문하셨습니다. 총 가격은 {total_price}원입니다. 감사합니다!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeKiosk()
    sys.exit(app.exec_())