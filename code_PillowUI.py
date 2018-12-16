import sys
from PIL import Image
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, \
                             QLineEdit, QMainWindow, QAction, QFileDialog,
                             QMessageBox, QScrollArea, QGridLayout, QInputDialog)
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

    def temp_image(self):
        self.file_name = 'temp_im.jpg'
        self.load_image.save(self.file_name)

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
        self.rotation_btn.clicked.connect(self.rotation)
        self.flip_horizontally_btn.clicked.connect(self.flip_horizontally)
        self.flip_vertical_btn.clicked.connect(self.flip_vertical)

    def merge_image(self):
        pixels1 = self.load_image.load()
        while True:
            file_name2 = \
                QFileDialog.getOpenFileName(self, 'Совместить файл', '.')[0]
            if file_name2:
                try:
                    load_image2 = Image.open(file_name2)
                    break
                except OSError:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Файл должен иметь '
                                         'расширение графического файла, '
                                         'поддерживаемого библиотекой PIL',
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                break
        if load_image2:
            val, ok_btn_pressed = QInputDialog.getInt(
                self, 'Прозрачность', 'Укажите процент прозрачности:',
                10, 50, 100, 10)
            val = val / 100
            if ok_btn_pressed:
                width1, height2 = self.load_image.size
                width2, height1 = load_image2.size
                if width1 != width2 or height1 != height2:
                    load_image2 = load_image2.resize((width1, height2))
                pixels2 = load_image2.load()
                x, y = self.load_image.size
                for i in range(x):
                    for j in range(y):
                        r1, g1, b1 = pixels1[i, j]
                        r2, g2, b2 = pixels2[i, j]
                        r1 = r1 * val + r2 * val
                        g1 = g1 * val + g2 * val
                        b1 = b1 * val + b2 * val
                        pixels1[i, j] = int(r1), int(g1), int(b1)
                self.temp_image()
                self.show_image()


    def change_pixel_color(self):
        pass


    def set_transparency(self):
        pixels1 = self.load_image.load()
        val, ok_btn_pressed = QInputDialog.getInt(
            self, 'Прозрачность', 'Укажите процент прозрачности:',
            10, 50, 100, 10)
        val = val / 100
        if ok_btn_pressed:
            x, y = self.load_image.size
            for i in range(x):
                for j in range(y):
                    r1, g1, b1 = pixels1[i, j]
                    r1 = r1 * val
                    g1 = g1 * val
                    b1 = b1 * val
                    pixels1[i, j] = int(r1), int(g1), int(b1)
            self.temp_image()
            self.show_image()


    def image_resize(self):
        while True:
            i, ok_btn_pressed = QInputDialog.getText(
                self, 'Изменение размера изоражения', 'Введите новый размер '
                                                      'изображения. размер '
                                                      'должен быть указан в '
                                                      'формате: "ширина";"высота"')

            if ok_btn_pressed:
                if ';' not in i:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Ширина и высота, указанные в '
                                         'диалоговом окне, должны быть '
                                         'разделены этим символом: ";"',
                                         QMessageBox.Ok, QMessageBox.Ok)
                try:
                    i = [int(item) for item in i.split(';')]
                    self.load_image = self.load_image.resize(i)
                    self.temp_image()
                    self.show_image()
                    break
                except TypeError:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Введеные значения не соответствуют типу int',
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                break


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

    def rotation(self):
        pass

    def flip_horizontally(self):
        pass

    def flip_vertical(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
