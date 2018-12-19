from PyQt5.QtWidgets import QInputDialog
from  random import randint

# Фильтры для изображения
class Filtres:
    def __init__(self, app):
        self.app = app
        self.image_obj = app.load_image
        self.width, self.height = self.image_obj.size
        self.pixel = self.image_obj.load()

    def shade_of_gray(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pixel[i, j]
                new_color = (r * 30 + g * 59 + b * 11) / 100
                self.pixel[i, j] = (new_color, new_color, new_color)
        self.app.temp_image()
        self.app.show_image()

    # Черно-белое изображение
    def black_and_white(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pixel[i, j]
                new_color = r + g + b
                if new_color > 531:
                    new_color = 255, 255, 255
                else:
                    new_color = 0, 0, 0
                self.pixel[i, j] = (new_color, new_color, new_color)
        self.app.temp_image()
        self.app.show_image()

    # Негатив
    def negative(self):
        for i in range(self.width):
            for j in range(self.height):
                r, g, b = self.pixel[i, j]
                r, g, b = self.pixel[i, j]
                self.pixel[i, j] = ((255 - r), (255 - g), (255 - b))
        self.app.temp_image()
        self.app.show_image()

    # Сепия
    def sepia(self):
        depth, ok_btn_pressed = QInputDialog.getInt(
            self.app, 'Шум', 'Укажите глубину:',
            5, 0, 10, 1)
        depth *= 10
        if ok_btn_pressed:
            for i in range(self.width):
                for j in range(self.height):
                    r, g, b = self.pixel[i, j]
                    new_color = (r + g + b) // 3
                    r = new_color + depth * 2
                    g = new_color + depth
                    b = new_color
                    self.pixel[i, j] = r, g, b
            self.app.temp_image()
            self.app.show_image()

    # Добавление шума
    def noise(self):
        factor, ok_btn_pressed = QInputDialog.getInt(
            self.app, 'Шум', 'Укажите уровень шума:',
            5, 0, 10, 1)
        factor *= 10
        if ok_btn_pressed:
            for i in range(self.width):
                for j in range(self.height):
                    r, g, b = self.pixel[i, j]
                    rand = randint(-factor, factor)
                    r += rand
                    g += rand
                    b += rand
                    if r < 0:
                        r = 0
                    if g < 0:
                        g = 0
                    if b < 0:
                        b = 0
                    if r > 255:
                        r = 255
                    if g > 255:
                        g = 255
                    if b > 255:
                        b = 255
                    self.pixel[i, j] = r, g, b
            self.app.temp_image()
            self.app.show_image()

    # Яркость
    def brightness(self):
        factor, ok_btn_pressed = QInputDialog.getInt(
            self.app, 'Шум', 'Укажите уровень яркости:',
            5, -10, 10, 1)
        factor *= 10
        if ok_btn_pressed:
            for i in range(self.width):
                for j in range(self.height):
                    r, g, b = self.pixel[i, j]
                    if r < 0:
                        r = 0
                    if g < 0:
                        g = 0
                    if b < 0:
                        b = 0
                    if r > 255:
                        r = 255
                    if g > 255:
                        g = 255
                    if b > 255:
                        b = 255
                    self.pixel[i, j] = r, g, b
            self.app.temp_image()
            self.app.show_image()
