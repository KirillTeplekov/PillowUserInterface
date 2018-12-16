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
        self.create_fileAction.triggered.connect(self.create_file)
        self.open_fileAction.triggered.connect(self.open_file)        
    
    def open_file(self):
        while True:
            self.file_name = \
                QFileDialog.getOpenFileName(self, 'Открыть файл', '.')[0]
            if self.file_name:
                try:
                    self.load_image = Image.open(self.file_name)
                    self.show_image()
                    self.init_ui()
                    break
                except OSError:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Файл должен иметь '
                                         'расширение графического файла, '
                                         'поддерживаемого библиотекой PIL',
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                break

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
        self.merge_image_btn.clicked.connect(self.merge_image)
        self.change_pixel_color_btn.clicked.connect(self.change_pixel_color)
        self.set_transparency_btn.clicked.connect(self.set_transparency)
        self.image_resize_btn.clicked.connect(self.image_resize)
        self.cut_btn.clicked.connect(self.cut)
        self.cut_background_btn.clicked.connect(self.cut_background)
        self.palette_btn.clicked.connect(self.open_palette)
        self.grid_btn.clicked.connect(self.grid)
        self.ruler_btn.clicked.connect(self.ruler)


    def merge_image(self):
        pass


    def change_pixel_color(self):
        pass


    def set_transparency(self):
        pass


    def image_resize(self):
        pass


    def cut(self):
        pass


    def cut_background(self):
        pass


    def open_palette(self):
        pass


    def grid(self):
        pass


    def ruler(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
