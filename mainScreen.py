import sys
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit,
QGridLayout, QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox,
QMainWindow, QAction, QMenu, qApp)
from PyQt5.QtCore import QCoreApplication

class Kiosk(QWidget):
    def __init__(sekf):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        coffee1_btn = QPushButton('아메리카노', self)
        coffee1_btn.resize(coffee1_btn.sizeHint())
        coffee1_btn.setToolTip("Americano")
        