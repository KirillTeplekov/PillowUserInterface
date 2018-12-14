import sys
from PIL import Image
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, \
                             QLineEdit, QMainWindow, QAction, QFileDialog,
                             QMessageBox, QScrollArea, QGridLayout)
from PyQt5.QtGui import QPixmap


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface_PillowUI.ui', self)

    def open_file(self):
        pass

    def save_file(self):
        pass

    def create_file(self):
        pass

    def show_image(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
