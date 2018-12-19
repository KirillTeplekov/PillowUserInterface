import sys
from PIL import Image
from PIL import ImageDraw
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, \
                             QLineEdit, QMainWindow, QAction, QFileDialog,
                             QMessageBox, QScrollArea, QGridLayout,
                             QInputDialog, QColorDialog)
from PyQt5.QtGui import QPixmap
from random import randint


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface_PillowUI.ui', self)
        self.create_fileAction.triggered.connect(self.create_file)
        self.open_fileAction.triggered.connect(self.open_file)
        self.file_name = ''
        self.temp_name = ''
        self.load_image = Image
        self.pixmap = QPixmap()
        self.width = 0
        self.height = 0
        self.pixel = []

    # Открытие файла
    def open_file(self):
        try:
            while True:
                self.file_name = \
                    QFileDialog.getOpenFileName(self, 'Открыть файл', '.')[0]
                if self.file_name:
                    try:
                        self.load_image = Image.open(self.file_name)
                        self.width, self.height = self.load_image.size
                        self.pixel = self.load_image.load()
                        self.temp_image()
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
        except Exception as e:
            print(e)

    # Сохранение файла
    def save_file(self):
        self.load_image.save(self.file_name)

    # Создание файла
    def create_file(self):
        val, ok_btn_pressed = QInputDialog.getText(self, 'Создать',
                                                   'Введите название файла:')
        if ok_btn_pressed:
            # noinspection PyBroadException
            try:
                self.file_name = val
                self.load_image.new()
                self.load_image.save(self.file_name)
                self.temp_image()
            except Exception:
                QMessageBox.question(self, 'Предупреждение',
                                     'Упс... Что-то пошло не так, попробуйте снова',
                                     QMessageBox.Ok, QMessageBox.Ok)

    # Показ изображения в QScrollArea
    def show_image(self):
        self.pixmap = QPixmap(self.file_name)
        self.lbl.setPixmap(self.pixmap)
        self.lbl.resize(self.pixmap.width(), self.pixmap.height())
        self.lbl.resize(self.pixmap.width(), self.pixmap.height())
        self.scroll_image.setWidget(self.lbl)

    # Создание временного изображения, с которым будет вестись работа,
    # чтобы не испортить начальное изображение
    def temp_image(self):
        self.temp_name = 'temp_im.jpg'
        self.load_image.save(self.temp_name)
        self.pixel = self.load_image.load()
        self.width, self.height = self.load_image.size
        self.show_image()

    # Инициализация UI
    def init_ui(self):
        # Подключение сигналов для меню "Фильтры"
        # self.shade_of_gray_action.triggered.connect(self.shade_of_gray)
        # self.white_and_black_action.triggered.connect(self.white_and_black)
        # self.sepia_action.triggered.connect(self.sepia)
        # self.negative_action.triggered.connect(self.negative)
        # self.noise_action.triggered.connect(self.noise)
        # self.brightness_action.triggered.connect(self.brightness)

        # Подключение сигналов для кнопок
        self.merge_image_btn.clicked.connect(self.merge_image)
        self.thumbnail_image_btn.clicked.connect(self.thumbnail_image)
        self.set_transparency_btn.clicked.connect(self.set_transparency)
        self.image_resize_btn.clicked.connect(self.image_resize)
        self.cut_btn.clicked.connect(self.cut)
        self.cut_background_btn.clicked.connect(self.cut_background)
        self.palette_btn.clicked.connect(self.open_palette)
        self.grid_btn.clicked.connect(self.grid)
        self.random_color_btn.clicked.connect(self.random_color)
        self.rotation_btn.clicked.connect(self.rotation)
        self.flip_horizontally_btn.clicked.connect(self.flip_horizontally)
        self.flip_vertical_btn.clicked.connect(self.flip_vertical)

    # Слияние изображений
    def merge_image(self):
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
            # Установление прозрачности для файла,
            # с которым производится слияние
            val, ok_btn_pressed = QInputDialog.getInt(
                self, 'Прозрачность', 'Укажите процент прозрачности:',
                5, 0, 10, 1)
            val = val / 10
            if ok_btn_pressed:
                # Проверка размеров изображения, если они отличаются,
                # то второе изображения принимает размер первого
                width2, height2 = load_image2.size
                if self.width != width2 or self.height != height2:
                    load_image2 = load_image2.resize((self.width, self.height))
                pixels2 = load_image2.load()
                # Слияние пикселей изображений с учетом прозрачности
                for i in range(self.width):
                    for j in range(self.height):
                        r1, g1, b1 = self.pixel[i, j]
                        r2, g2, b2 = pixels2[i, j]
                        r1 = r1 * (1 - val) + r2 * val
                        g1 = g1 * (1 - val) + g2 * val
                        b1 = b1 * (1 - val) + b2 * val
                        self.pixel[i, j] = int(r1), int(g1), int(b1)
                self.temp_image()

    # Замена пикселей одного цвета на пиксели другого
    def thumbnail_image(self):
        # Получение значения из диалогового окна и проверка корректности
        while True:
            val, ok_btn_pressed = QInputDialog.getText(
                self, 'Масштабирование изоражения', 'Введите новый размер '
                                                    'изображения. размер '
                                                    'должен быть указан в '
                                                    'формате: "ширина";"высота"')

            if ok_btn_pressed:
                if ';' not in val:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Ширина и высота, указанные в '
                                         'диалоговом окне, должны быть '
                                         'разделены этим символом: ";"',
                                         QMessageBox.Ok, QMessageBox.Ok)
                elif len(val.split(';')) > 2:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Должно быть введено ТОЛЬКО два '
                                         'аргумента. Разве это так сложно?',
                                         QMessageBox.Ok, QMessageBox.Ok)
                else:
                    try:
                        val = [int(item) for item in val.split(';')]
                        # Масшатабирование изображения
                        self.load_image = self.load_image.thumbnail(val)
                        self.temp_image()
                        break
                    except ValueError:
                        QMessageBox.question(self, 'Предупреждение',
                                             'Введеные значения не соответствуют типу int',
                                             QMessageBox.Ok, QMessageBox.Ok)
            else:
                break

    # Изменение прозрачности
    def set_transparency(self):
        val, ok_btn_pressed = QInputDialog.getInt(
            self, 'Прозрачность', 'Укажите процент прозрачности:',
            5, 0, 10, 1)
        val = val / 10
        if ok_btn_pressed:
            # Установление прзрачности для пикселей
            for i in range(self.width):
                for j in range(self.height):
                    r1, g1, b1 = self.pixel[i, j]
                    r1 = r1 * val
                    g1 = g1 * val
                    b1 = b1 * val
                    self.pixel[i, j] = int(r1), int(g1), int(b1)
            self.temp_image()

    # Изменение размера
    def image_resize(self):
        # Создание диалогового окна и проверка корректности значений
        while True:
            val, ok_btn_pressed = QInputDialog.getText(
                self, 'Изменение размера изоражения', 'Введите новый размер '
                                                      'изображения. размер '
                                                      'должен быть указан в '
                                                      'формате: "ширина";"высота"')

            if ok_btn_pressed:
                if ';' not in val:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Ширина и высота, указанные в '
                                         'диалоговом окне, должны быть '
                                         'разделены этим символом: ";"',
                                         QMessageBox.Ok, QMessageBox.Ok)
                elif len(val.split(';')) > 2:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Должно быть введено ТОЛЬКО два '
                                         'аргумента. Разве это так сложно?',
                                         QMessageBox.Ok, QMessageBox.Ok)
                else:
                    try:
                        val = [int(item) for item in val.split(';')]
                        # Изменение размера
                        self.load_image = self.load_image.resize(val)
                        self.temp_image()
                        break
                    except ValueError:
                        QMessageBox.question(self, 'Предупреждение',
                                             'Введеные значения не соответствуют типу int',
                                             QMessageBox.Ok, QMessageBox.Ok)
            else:
                break

    # Обрезать изображение
    def cut(self):
        fl = False
        # Получение значения для левого верхнего угла
        while True:
            val, ok_btn_pressed = QInputDialog.getText(
                self, 'Обрезать', 'Введите координаты левого верхнего угла'
                                  ' в формате: x;y')
            if ok_btn_pressed:
                if ';' not in val:
                    QMessageBox.question(self, 'Предупреждение',
                                         'x и y, указанные в '
                                         'диалоговом окне, должны быть '
                                         'разделены этим символом: ";"',
                                         QMessageBox.Ok, QMessageBox.Ok)
                elif len(val.split(';')) > 2:
                    QMessageBox.question(self, 'Предупреждение',
                                         'Должно быть введено ТОЛЬКО два '
                                         'аргумента. Разве это так сложно?',
                                         QMessageBox.Ok, QMessageBox.Ok)
                else:
                    try:
                        val = [int(item) for item in val.split(';')]
                        x_min, y_min = val
                        fl = True
                        break
                    except Exception as e:
                        QMessageBox.question(self, 'Предупреждение',
                                             str(e),
                                             QMessageBox.Ok, QMessageBox.Ok)
            else:
                break

        # Получение значения для правого нижнего и последующая обрезка
        # изображения
        if fl:
            while True:
                val, ok_btn_pressed = QInputDialog.getText(
                    self, 'Обрезать',
                    'Введите координаты правого нижнего угла '
                    'в формате: x;y')
                if ok_btn_pressed:
                    if ';' not in val:
                        QMessageBox.question(self, 'Предупреждение',
                                             'x и y, указанные в '
                                             'диалоговом окне, должны быть '
                                             'разделены этим символом: ";"',
                                             QMessageBox.Ok,
                                             QMessageBox.Ok)
                    elif len(val.split(';')) > 2:
                        QMessageBox.question(self, 'Предупреждение',
                                             'Должно быть введено' ''
                                             'ТОЛЬКО два аргумента. '
                                             'Разве это так сложно?',
                                             QMessageBox.Ok,
                                             QMessageBox.Ok)
                    else:
                        try:
                            val = [int(item) for item in
                                   val.split(';')]
                            x_max, y_max = val
                            self.load_image = self.load_image.crop((x_min,
                                                                    y_min,
                                                                    x_max,
                                                                    y_max))
                            self.temp_image()
                            break
                        except Exception as e:
                            QMessageBox.question(self,
                                                 'Предупреждение',
                                                 str(e),
                                                 QMessageBox.Ok,
                                                 QMessageBox.Ok)
                else:
                    break

    # Обрезать однотонное изображение
    def cut_background(self):
        QMessageBox.question(self, 'Предупреждение',
                             'Данная функция корректно работает только, '
                             'если изображение окружено однотонным фоном со '
                             'всех сторон хотя бы на один пиксель.',
                             QMessageBox.Ok, QMessageBox.Ok)
        fl = False
        for i in range(self.width):
            for j in range(self.height):
                if self.pixel[i, j] != self.pixel[0, 0]:
                    x_min = i
                    fl = True
                    break
            if fl:
                break
        fl = False
        for i in range(self.height):
            for j in range(self.width):
                if self.pixel[i, j] != self.pixel[0, 0]:
                    y_min = i
                    fl = True
                    break
            if fl:
                break
        fl = False
        for i in range(self.width - 1, -1, -1):
            for j in range(self.height - 1, -1, -1):
                if self.pixel[i, j] != self.pixel[0, 0]:
                    x_max = i
                    fl = True
                    break
            if fl:
                break
        fl = False
        for i in range(self.height - 1, -1, -1):
            for j in range(self.width - 1, -1, -1):
                if self.pixel[j, i] != self.pixel[0, 0]:
                    y_max = i
                    fl = True
                    break
            if fl:
                break
        self.load_image.crop((x_min, y_min, x_max, y_max))
        self.temp_image()

    # Открыть палитру
    def open_palette(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color = color.name()
            QMessageBox.question(self, 'Выбранный цвет',
                                 color,
                                 QMessageBox.Ok, QMessageBox.Ok)
            QMessageBox.question(self, 'Сохранить?', 'Сохранить?',
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.Ok)
            if QMessageBox.Yes:
                # Запись значения цвета в файл
                while True:
                    val, ok_btn_pressed = QInputDialog.getText(
                        self, 'Сохранить!',
                        'Введите название файла')
                    if ok_btn_pressed:
                        try:
                            f = open(val, 'w')
                            f.write(color)
                            f.close()
                            break
                        except Exception as e:
                            QMessageBox.question(self, 'Ошибка', e,
                                                 QMessageBox.Ok,
                                                 QMessageBox.Ok)
                    else:
                        break

    # Добавить сетку
    def grid(self):
        # Создаем объект ImageDraw и передаем ему изображение
        draw = ImageDraw.Draw(self.load_image)

        # Рисуем вертикальные лини каждые 10 пикселей
        for i in range(0, self.width, 10):
            draw.line((i, 0, i + self.height, 0))

        # Рисуем горизонталные линии каждые 10 пикселей
        for j in range(0, self.height, 10):
            draw.line((0, i, 0, i + self.width))

        del draw
        self.temp_image()

    # Заполнить случайными цветами
    def random_color(self):
        for i in range(self.width):
            for j in range(self.height):
                r = randint(0, 255)
                g = randint(0, 255)
                b = randint(0, 255)
                self.pixel[i, j] = r, g, b

    # Поворот изображения
    def rotation(self):
        # Получение аргументов для поворота
        val, ok_btn_pressed = QInputDialog.getInt(
            self, 'Поворот', 'Укажите градус поворота:',
            45, 90, 270, 45)
        if ok_btn_pressed:
            direction, ok_btn_pressed = QInputDialog.getItem(
                self, 'Поворот', 'Выберите направление поворота:',
                ('Влево', 'Вправо'), 0, False)
            if ok_btn_pressed:
                # Поворот
                if direction == 'Влево':
                    self.load_image = self.load_image.rotate(val)
                else:
                    self.load_image = self.load_image.rotate(360 - val)
                self.temp_image()

    # Отражение по горизонтали
    def flip_horizontally(self):
        self.load_image = self.load_image.transpose(Image.FLIP_TOP_BOTTOM)
        self.temp_image()

    # Отражение по вертикали
    def flip_vertical(self):
        self.load_image = self.load_image.transpose(Image.FLIP_LEFT_RIGHT)
        self.temp_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
