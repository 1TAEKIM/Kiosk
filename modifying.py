from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from google.cloud import dialogflow
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, QLabel,
                             QMainWindow, QGridLayout, QSpinBox, QMessageBox, QAction, QInputDialog)
import sys
import speech_recognition as sr
import uuid
import os

class CoffeeKiosk(QMainWindow):
    def __init__(self):
        super().__init__()

        self.project_id = 'CoffeeKiosk' 
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, str(uuid.uuid4()))

        self.initUI()
        # Dialogflow 인증 정보 설정
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_key.json'
        self.project_id = 'PROJECT_ID'
        self.session_id = 'SESSION_ID'
        self.language_code = 'ko-KR'

        # Dialogflow 세션 생성
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

    def initUI(self):
        self.setWindowTitle('커피 키오스크')

        # 메뉴바 추가
        menubar = self.menuBar()
        self.add_menu(menubar)

        # 음성 인식 객체 생성
        self.recognizer = sr.Recognizer()

        # 아메리카노 이미지 추가
        am_img = QLabel(self)
        am_pixmap = QPixmap('americano.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        am_img.setPixmap(am_pixmap)

        # 아메리카노 가격 추가
        self.am_price = 4500
        am_price_label = QLabel(f'{self.am_price}원', self)

        # 아메리카노 개수 선택
        self.am_spinbox = QSpinBox(self)
        self.am_spinbox.setMinimum(0)
        self.am_spinbox.setMaximum(20)
        self.am_spinbox.valueChanged.connect(self.update_total_price)

        # 아메리카노 버튼 추가
        btn1 = QPushButton('아메리카노', self)
        btn1.setStyleSheet("background-color: #A0522D; color: white;")
        btn1.clicked.connect(self.americano)

        # 카페라떼 이미지 추가
        latte_img = QLabel(self)
        latte_pixmap = QPixmap('latte.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        latte_img.setPixmap(latte_pixmap)

        # 카페라떼 가격 추가
        self.latte_price = 5000
        latte_price_label = QLabel(f'{self.latte_price}원', self)

        # 카페라떼 개수 선택
        self.latte_spinbox = QSpinBox(self)
        self.latte_spinbox.setMinimum(0)
        self.latte_spinbox.setMaximum(20)
        self.latte_spinbox.valueChanged.connect(self.update_total_price)

        # 카페라떼 버튼 추가
        btn2 = QPushButton('카페라떼', self)
        btn2.setStyleSheet("background-color: #A0522D; color: white;")
        btn2.clicked.connect(self.latte)

        # 카푸치노 이미지 추가
        capp_img = QLabel(self)
        capp_pixmap = QPixmap('cappuccino.jpg').scaled(300, 300, Qt.KeepAspectRatio)
        capp_img.setPixmap(capp_pixmap)

        # 카푸치노 가격 추가
        self.capp_price = 5000
        capp_price_label = QLabel(f'{self.capp_price}원', self)


        # 카푸치노 개수 선택
        self.capp_spinbox = QSpinBox(self)
        self.capp_spinbox.setMinimum(0)
        self.capp_spinbox.setMaximum(20)
        self.capp_spinbox.valueChanged.connect(self.update_total_price)

        # 카푸치노 버튼 추가
        btn3 = QPushButton('카푸치노', self)
        btn3.setStyleSheet("background-color: #A0522D; color: white;")
        btn3.clicked.connect(self.cappuccino)

        # 구매 버튼 추가
        buy_btn = QPushButton('구매', self)
        buy_btn.setStyleSheet("background-color: #A0522D; color: white;")
        buy_btn.clicked.connect(self.buy)

        # 총 가격 레이블 추가
        self.total_price_label = QLabel('총 가격: 0원', self)

        # 음성 인식 버튼 추가
        voice_btn = QPushButton('음성 인식', self)
        voice_btn.setStyleSheet("background-color: #A0522D; color: white;")
        voice_btn.clicked.connect(self.voice_recognition)


         # 레이아웃 설정
        grid = QGridLayout()
        grid.addWidget(am_img, 0, 0)
        grid.addWidget(latte_img, 0, 1)
        grid.addWidget(capp_img, 0, 2)
        grid.addWidget(QLabel('가격'), 1, 0)
        grid.addWidget(am_price_label, 2, 0)
        grid.addWidget(latte_price_label, 2, 1)
        grid.addWidget(capp_price_label, 2, 2)
        grid.addWidget(QLabel('개수'), 3, 0)
        grid.addWidget(self.am_spinbox, 4, 0)
        grid.addWidget(self.latte_spinbox, 4, 1)
        grid.addWidget(self.capp_spinbox, 4, 2)
        grid.addWidget(btn1, 5, 0)
        grid.addWidget(btn2, 5, 1)
        grid.addWidget(btn3, 5, 2)
        grid.addWidget(buy_btn, 6, 2)
        grid.addWidget(self.total_price_label, 7, 2)
        grid.addWidget(voice_btn, 8, 2)

        # 중앙 레이아웃 설정
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # 윈도우 크기 조절
        self.resize(900, 800)

    def add_menu(self, menubar):
        # 관리자 메뉴 추가
        admin_menu = menubar.addMenu('관리자')

        # 음료 관리 메뉴 추가
        drink_menu = admin_menu.addMenu('음료 관리')

        # 음료 추가 액션 추가
        add_action = QAction('음료 추가', self)
        add_action.triggered.connect(self.add_drink)
        drink_menu.addAction(add_action)

        # 음료 변경 액션 추가
        modify_action = QAction('음료 변경', self)
        modify_action.triggered.connect(self.modify_drink)
        drink_menu.addAction(modify_action)

        # 음료 삭제 액션 추가
        delete_action = QAction('음료 삭제', self)
        delete_action.triggered.connect(self.delete_drink)
        drink_menu.addAction(delete_action)

        # 가격 변경 액션 추가
        price_action = QAction('가격 변경', self)
        price_action.triggered.connect(self.change_price)
        admin_menu.addAction(price_action)

    def add_drink(self):
        pass

    def modify_drink(self):
        pass

    def delete_drink(self):
        pass

    def change_price(self):
        pass

    def americano(self):
        pass

    def latte(self):
        pass

    def cappuccino(self):
        pass

    def voice_recognition(self): 
        with sr.Microphone() as source: # 마이크 사용할 수 있도록 설정
            self.recognizer.adjust_for_ambient_noise(source) # 주변 소음 제거
            audio = self.recognizer.listen(source) # 음성 녹음

        try:
            text = self.recognizer.recognize_google(audio, language='ko-KR') # 음성 텍스트로 변환
            QMessageBox.information(self, '음성 인식 결과', f'음성 인식 결과: {text}')
            self.select_coffee(text)
        except sr.UnknownValueError:
            QMessageBox.warning(self, '음성 인식 실패', '음성을 인식할 수 없습니다.')
        except sr.RequestError as e:
            QMessageBox.warning(self, '음성 인식 실패', f'음성 인식 API에 접근할 수 없습니다. {e}')

    def select_coffee(self, coffee, quantity):
        if coffee == '아메리카노':
            self.am_spinbox.setValue(self.am_spinbox.value() + quantity)
        elif coffee == '카페라떼':
            self.latte_spinbox.setValue(self.latte_spinbox.value() + quantity)
        elif coffee == '카푸치노':
            self.capp_spinbox.setValue(self.capp_spinbox.value() + quantity)
        else:
            QMessageBox.warning(self, '음성 인식 실패', '음성 인식 결과에 해당하는 커피가 없습니다.')

    def update_total_price(self):
        am_count = self.am_spinbox.value()
        latte_count = self.latte_spinbox.value()
        capp_count = self.capp_spinbox.value()

        total_price = self.am_price * am_count + self.latte_price * latte_count + self.capp_price * capp_count
        self.total_price_label.setText(f'총 가격: {total_price}원')

    def buy(self):
        am_count = self.am_spinbox.value()
        latte_count = self.latte_spinbox.value()
        capp_count = self.capp_spinbox.value()

        total_price = self.am_price * am_count + self.latte_price * latte_count + self.capp_price * capp_count
        self.total_price_label.setText(f'총 가격: {total_price}원')

         # 선택한 커피와 개수 출력
        order = ''
        if am_count > 0:
            order += f'아메리카노 {am_count}잔\n'
        if latte_count > 0:
            order += f'카페라떼 {latte_count}잔\n'
        if capp_count > 0:
            order += f'카푸치노 {capp_count}잔\n'

        if order:
            QMessageBox.information(self, '주문 내역', order)
        else:
            QMessageBox.warning(self, '주문 실패', '커피를 선택해주세요.')

    def add_drink(self):
        drink, ok = QInputDialog.getText(self, '음료 추가', '추가할 음료 이름:')
        if ok and drink:
            price, ok = QInputDialog.getInt(self, '음료 추가', f'{drink} 가격:')
            if ok and price:
                if ok and price:
                    # Dialogflow 인텐트 생성
                    intent = dialogflow.types.Intent(
                        display_name=drink,
                        training_phrases=[
                            dialogflow.types.Intent.TrainingPhrase(parts=[dialogflow.types.Intent.TrainingPhrase.Part(text=drink)])
                    ],
                        messages=[
                            dialogflow.types.Intent.Message(text=dialogflow.types.Intent.Message.Text(text=f'{drink} 추가 완료'))
                    ]
                )

                 # Dialogflow 인텐트 생성 요청
                response = self.session_client.create_intent(
                     parent=self.session_client.project_agent_path(self.project_id),
                     intent=intent
                )
                
                QMessageBox.information(self, '음료 추가', f'{drink} 추가 완료')

    def modify_drink(self):
        drink, ok = QInputDialog.getText(self, '음료 변경', '변경할 음료 이름:')
        if ok and drink:
            price, ok = QInputDialog.getInt(self, '음료 변경', f'{drink} 가격:')
            if ok and price:
                # Dialogflow 인텐트 조회
                intent_path = self.session_client.intent_path(self.project_id, drink)
                intent = self.session_client.get_intent(intent_path)

                # Dialogflow 인텐트 업데이트
                intent.messages[0].text.text[0] = f'{drink} 변경 완료'
                intent.training_phrases[0].parts[0].text = drink
                intent.parameters[0].default_value.string_value = str(price)

                response = self.session_client.update_intent(intent)
                QMessageBox.information(self, '음료 변경', f'{drink} 변경 완료')

    def delete_drink(self):
        drink, ok = QInputDialog.getText(self, '음료 삭제', '삭제할 음료 이름:')
        if ok and drink:
            # Dialogflow 인텐트 삭제
            intent_path = self.session_client.intent_path(self.project_id, drink)
            response = self.session_client.delete_intent(intent_path)

            QMessageBox.information(self, '음료 삭제', f'{drink} 삭제 완료')

    def change_price(self):
        drink, ok = QInputDialog.getText(self, '가격 변경', '가격을 변경할 음료 이름:')
        if ok and drink:
            price, ok = QInputDialog.getInt(self, '가격 변경', f'{drink} 가격:')
            if ok and price:
                # Dialogflow 인텐트 조회
                intent_path = self.session_client.intent_path(self.project_id, drink)
                intent = self.session_client.get_intent(intent_path)

                # Dialogflow 인텐트 업데이트
                intent.parameters[0].default_value.string_value = str(price)

                response = self.session_client.update_intent(intent)
                
                QMessageBox.information(self, '가격 변경', f'{drink} 가격 변경 완료')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeKiosk()
    ex.show()
    sys.exit(app.exec_())