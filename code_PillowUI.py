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
        flag_opening = True
        while flag_opening:
            self.file_name = \
                QFileDialog.getOpenFileName(self, 'Открыть файл', '.')[0]
            if self.file_name:
                try:
                    self.load_image = Image.open(self.file_name)
                    flag_opening = False
                except OSError:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Файл должен иметь '
                                         'расширение графического файла, '
                                         'поддерживаемого библиотекой PIL',
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                break
        else:
            self.show_image()
            self.init_ui()

    def save_file(self):
        pass

    def create_file(self):
        pass

    def show_image(self):
        self.pixmap = QPixmap(self.file_name)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.resize(self.pixmap.width(), self.pixmap.height())
        self.lbl.resize(self.pixmap.width(), self.pixmap.height())
        self.scroll_image.setWidget(self.lbl)

    def init_ui(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
