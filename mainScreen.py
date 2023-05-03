from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from google.cloud import dialogflow
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
                             QMainWindow, QGridLayout, QSpinBox, QMessageBox)
import sys
import speech_recognition as sr
import os


class CoffeeKiosk(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # # Dialogflow 인증 정보 설정
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'dialogflow_key.json'
        # self.project_id = 'PROJECT_ID'
        # self.session_id = 'SESSION_ID'
        # self.language_code = 'ko-KR'

        # # Dialogflow 세션 생성
        # self.session_client = dialogflow.SessionsClient()
        # self.session = self.session_client.session_path(self.project_id, self.session_id)

    def initUI(self):
        self.setWindowTitle('커피 키오스크')

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

        # 수직 박스 레이아웃에 위젯 추가
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        vbox.addWidget(am_img)
        vbox.addWidget(am_price_label)
        vbox.addWidget(self.am_spinbox)
        vbox.addWidget(btn1)

        vbox.addWidget(latte_img)
        vbox.addWidget(latte_price_label)
        vbox.addWidget(self.latte_spinbox)
        vbox.addWidget(btn2)

        vbox.addWidget(capp_img)
        vbox.addWidget(capp_price_label)
        vbox.addWidget(self.capp_spinbox)
        vbox.addWidget(btn3)

        vbox.addWidget(self.total_price_label, alignment=Qt.AlignRight)
        vbox.addWidget(buy_btn, alignment=Qt.AlignRight)
        vbox.addWidget(voice_btn, alignment=Qt.AlignRight)

        self.setLayout(vbox)

        self.show()

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

    # def process_text(self, text):
    #     # Dialogflow에 대화 요청
    #     text_input = dialogflow.types.TextInput(text=text, language_code=self.language_code)
    #     query_input = dialogflow.types.QueryInput(text=text_input)
    #     response = self.session_client.detect_intent(session=self.session, query_input=query_input)

    #     # 대화 결과 처리
    #     if response.query_result.intent.display_name == 'order':
    #         coffee = response.query_result.parameters.fields['coffee'].string_value
    #         quantity = response.query_result.parameters.fields['quantity'].number_value
    #         self.select_coffee(coffee, quantity)
    #     else:
    #         QMessageBox.warning(self, '대화 처리 실패', '대화 처리 결과가 없습니다.')

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeKiosk()
    ex.show()
    sys.exit(app.exec_())