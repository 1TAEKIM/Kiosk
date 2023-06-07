import sqlite3
from datetime import datetime
import sys
import os
from google.cloud import dialogflow
import speech_recognition as sr
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class AdminLoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        id_label = QLabel('아이디')
        self.id_edit = QLineEdit()
        vbox.addWidget(id_label)
        vbox.addWidget(self.id_edit)

        pw_label = QLabel('비밀번호')
        self.pw_edit = QLineEdit()
        self.pw_edit.setEchoMode(QLineEdit.Password)
        vbox.addWidget(pw_label)
        vbox.addWidget(self.pw_edit)

        hbox = QHBoxLayout()
        login_btn = QPushButton('로그인')
        login_btn.clicked.connect(self.accept)
        hbox.addWidget(login_btn)

        cancel_btn = QPushButton('취소')
        cancel_btn.clicked.connect(self.reject)
        hbox.addWidget(cancel_btn)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def get_id_pw(self):
        return self.id_edit.text(), self.pw_edit.text()


class CoffeeKiosk(QMainWindow):
    def __init__(self):
        super().__init__()

        self.order_items = []
        self.total_price = 0
        self.initUI()

        # Dialogflow 인증 정보 설정
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'capstone-kiosk-eff1d91cef43.json'
        self.project_id = 'PROJECT_ID'
        self.session_id = 'SESSION_ID'
        self.language_code = 'ko-KR'

        # Dialogflow 세션 생성
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(self.project_id, self.session_id)

        # 주문한 메뉴와 수량을 저장할 리스트
        self.order_list = []

    def initUI(self):

        menubar = self.menuBar()
        admin_menu = menubar.addMenu('관리자')

        admin_login_action = QAction('로그인', self)
        admin_login_action.triggered.connect(self.show_admin_login)
        admin_menu.addAction(admin_login_action)

        self.setWindowTitle('커피 키오스크')

        # 음성 인식 객체 생성
        self.recognizer = sr.Recognizer()


        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a grid layout
        layout = QGridLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # Connect to the SQLite database
        conn = sqlite3.connect('coffee.db')
        cursor = conn.cursor()

        # Fetch the menu items from the database
        cursor.execute("SELECT * FROM coffee")
        menu_items = cursor.fetchall()

        # Create the menu items dynamically using a loop
        for index, item in enumerate(menu_items):
            name = item[1]
            image_path = item[2]
            price = item[3]

            # Create QLabel for the image
            image_label = QLabel(self)
            pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)

            # Create QLabel for the price
            price_label = QLabel(f'{price}원', self)

            # # Create QSpinBox for quantity selection
            # spinbox = QSpinBox(self)
            # spinbox.setMinimum(0)
            # spinbox.setMaximum(20)
            # spinbox.valueChanged.connect(self.update_total_price)

            # Create QPushButton for menu item
            btn = QPushButton(name, self)
            btn.setStyleSheet("background-color: #A0522D; color: white;")
            btn.clicked.connect(lambda _, name=name: self.menu_item_clicked(name))

            # Connect the click event of the image_label to menu_item_clicked
            image_label.mousePressEvent = lambda _, name=name: self.menu_item_clicked(name)

            # Add the widgets to the layout
            layout.addWidget(image_label, index // 4 * 4, index % 4)
            layout.addWidget(price_label, index // 4 * 4 + 1, index % 4)
            # layout.addWidget(spinbox, index // 4 * 4 + 2, index % 4)
            layout.addWidget(btn, index // 4 * 4 + 2, index % 4)

            # Limit the number of menu items to 12 (3 rows x 4 columns)
            if index >= 11:
                break

        # Set column and row stretch
        layout.setColumnStretch(0, 1)
        layout.setRowStretch(index // 4 + 3, 1)

        # Close the database connection
        # conn.close()

        # Create a table for order items
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(["메뉴", "수량", "가격", "취소"])
        self.order_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.order_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Create a layout for the order section
        order_layout = QVBoxLayout()

        # Create QLabel for total price
        self.total_price_label = QLabel()

        # Create QPushButton for purchase
        purchase_button = QPushButton("구매")
        purchase_button.setStyleSheet("background-color: #008000; color: white;")
        # purchase_button.clicked.connect(self.purchase_items)
        purchase_button.clicked.connect(self.show_purchase_confirmation)
        order_layout.addWidget(purchase_button)

        # Create QPushButton for cancel
        cancel_button = QPushButton('취소', self)
        cancel_button.setStyleSheet("background-color: #FF0000; color: white;")
        cancel_button.clicked.connect(self.cancel_clicked)
        order_layout.addWidget(cancel_button)

        # Add the order_layout to the main layout
        layout.addLayout(order_layout, (index // 4) * 4 + 4, 0, 1, 4)

        # Create a layout for the order table
        order_table_layout = QVBoxLayout()
        order_table_layout.addWidget(self.order_table)

        # Add the order_table_layout to the main layout
        layout.addLayout(order_table_layout, (index // 4) * 4 + 5, 0, 1, 4)

        # Create a QLabel for total price
        self.total_price_label = QLabel()
        layout.addWidget(self.total_price_label, (index // 4) * 4 + 5, 3, 1, 4)


        # Close the database connection
        self.show()
        conn.close()

    def menu_item_clicked(self, name):
        # Handle the menu item clicked event
        # print(f"Menu item clicked: {name}")
        
         # Connect to the SQLite database
        conn = sqlite3.connect('coffee.db')
        cursor = conn.cursor()

        # Check if the menu item already exists in the order table
        for row in range(self.order_table.rowCount()):
            item_name = self.order_table.item(row, 0).text()
            if item_name == name:
                return  # Skip adding the menu item if it already exists

        # Fetch the price from the database based on the menu item name
        cursor.execute("SELECT price FROM coffee WHERE name=?", (name,))
        result = cursor.fetchone()
        if result:
            price = result[0]

            # Add the clicked menu item to the order table
            row = self.order_table.rowCount()
            self.order_table.insertRow(row)
            self.order_table.setItem(row, 0, QTableWidgetItem(name))

            # Create QSpinBox for quantity selection
            spinbox = QSpinBox(self)
            spinbox.setMinimum(0)
            spinbox.setMaximum(20)
            spinbox.setValue(1)
            spinbox.valueChanged.connect(lambda value, row=row, price=price: self.update_item_price(row, price, value))
            self.order_table.setCellWidget(row, 1, spinbox)

            # Calculate the total price for the initial quantity
            total_price = price * spinbox.value()
            self.order_table.setItem(row, 2, QTableWidgetItem(str(total_price)))

            # Create QPushButton for cancel
            cancel_button = QPushButton('취소', self)
            cancel_button.setStyleSheet("background-color: #FF0000; color: white;")
            cancel_button.clicked.connect(self.cancel_item_clicked)
            self.order_table.setCellWidget(row, 3, cancel_button)

            self.update_total_price()

        # Close the database connection
        conn.close()

    def update_item_price(self, row, price, quantity):
        total_price = price * quantity
        self.order_table.setItem(row, 2, QTableWidgetItem(str(total_price)))
        self.update_total_price()

    def cancel_item_clicked(self):
        # Handle the cancel item clicked event
        button = self.sender()
        if button:
            row = self.order_table.indexAt(button.pos()).row()
            self.order_table.removeRow(row)
            self.update_total_price()

    def update_total_price(self):
        total_price = sum(int(self.order_table.item(row, 2).text()) for row in range(self.order_table.rowCount()))
        self.total_price_label.setText(f'총 가격: {total_price}원')



    def purchase_clicked(self):
        # Handle the purchase button clicked event
        total_price = 0
        for row in range(self.order_table.rowCount()):
            price_item = self.order_table.item(row, 2)
            if price_item:
                price = int(price_item.text())
                total_price += price
        print(f"Total Price: {total_price}")

    def cancel_clicked(self):
        # Handle the cancel button clicked event
        self.order_table.clearContents()
        self.order_table.setRowCount(0)

    def purchase_items(self):
        # Perform the purchase logic here
        print("Purchase items")

        # Clear the order table and update the total price
        self.order_table.clearContents()
        self.update_total_price()
    
    def show_purchase_confirmation(self):

        conn = sqlite3.connect('purchaseLog.db')
        cursor = conn.cursor()

        # Create a new window for purchase confirmation
        self.purchase_dialog = QDialog(self)
        self.purchase_dialog.setWindowTitle("구매 확인")

        # Get the coffee names and quantities from the order_table
        purchase_info = []
        for row in range(self.order_table.rowCount()):
            coffee_name = self.order_table.item(row, 0).text()
            quantity = self.order_table.cellWidget(row, 1).value()
            purchase_info.append(coffee_name + " (수량: " + str(quantity) + ")")

        # Create QLabel for purchase information
        purchase_info_label = QLabel()
        purchase_info_label.setText("구매 정보: " + "\n".join(purchase_info))
        purchase_info_label.setStyleSheet("font-size: 14pt")  # Adjust the font size as desired

        # Update the total price
        self.update_total_price()

        # Create QLabel for total price
        total_price_label = QLabel()
        total_price_label.setText(self.total_price_label.text())
        total_price_label.setStyleSheet("font-size: 14pt")  # Adjust the font size as desired

        # Create QPushButton for purchase confirmation
        confirm_button = QPushButton("구매 확정")
        confirm_button.clicked.connect(self.confirm_purchase)

        # Create QVBoxLayout for the purchase confirmation window
        layout = QVBoxLayout()
        layout.addWidget(purchase_info_label)
        layout.addWidget(total_price_label)
        layout.addWidget(confirm_button)

        # Set the layout for the purchase dialog
        self.purchase_dialog.setLayout(layout)

        # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Iterate over the rows in the order table
        for row in range(self.order_table.rowCount()):
            # Get the coffee name, quantity, and price from the table
            coffee_name = self.order_table.item(row, 0).text()
            quantity = self.order_table.cellWidget(row, 1).value()
            price = self.order_table.item(row, 2).text()

            # Calculate the total price
            total_price = int(price)

            # Insert the purchase information into the purchaseLog table
            cursor.execute("INSERT INTO purchaseLog (purchase_date, coffee_name, quantity, total_price) VALUES (?, ?, ?, ?)",
                        (current_time, coffee_name, quantity, total_price))

        # Commit the changes to the database
        conn.commit()
        # Close the database connection
        conn.close()

        # Show the purchase confirmation dialog
        self.purchase_dialog.exec_()
    
    def confirm_purchase(self):
        # Close the purchase dialog
        self.purchase_dialog.close()

        # Clear the order table
        self.order_table.clearContents()
        self.order_table.setRowCount(0)

        # Reset the total price label
        self.total_price_label.setText("총 가격: 0 원")

        # Show the main window again
        self.show()

    def close_purchase_window(self):
        if hasattr(self, 'purchase_window'):
            self.purchase_window.close()

    def show_admin_login(self):
        dialog = AdminLoginDialog()
        dialog.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.ImhNoAutoUppercase)
        if dialog.exec_() == QDialog.Accepted:
            id, pw = dialog.get_id_pw()
            if id == 'admin' and pw == '1111':
                self.show_new_window()
                #QMessageBox.information(self, '로그인 성공', '로그인에 성공했습니다.')
            else:
                QMessageBox.warning(self, '로그인 실패', '아이디 또는 비밀번호가 올바르지 않습니다.')

    def show_new_window(self):
        self.new_window = QMainWindow()
        self.new_window.setWindowTitle('관리자 창')


        label = QLabel("새로운 창")
        layout = QVBoxLayout()
        layout.addWidget(label)
        widget = QWidget()
        widget.setLayout(layout)
        self.new_window.setCentralWidget(widget)
        self.new_window.show()

    def closeEvent(self, event):
        if self.new_window is not None:
            self.new_window.close()
        event.accept()

# 메인 애플리케이션 실행
app = QApplication([])
window = CoffeeKiosk()
# window.show_admin_login()
app.exec_()
