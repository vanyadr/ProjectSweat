import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox


# Класс формы добавления, со всеми методами
class AddProd(QMainWindow):
    def __init__(self, parent=None):
        super(AddProd, self).__init__(parent)
        uic.loadUi("add_window.ui", self)
        self.go_back1.clicked.connect(self.cls)
        self.add_to.clicked.connect(self.save_item)

    def save_item(self):

        self.close()

    def cls(self):
        self.close()


# Класс формы удаления, со всеми методами
class ShowTable(QMainWindow):
    def __init__(self, parent=None):
        super(ShowTable, self).__init__(parent)
        uic.loadUi("table_window.ui", self)
        self.go_back2.clicked.connect(self.cls2)
        self.delete1.clicked.connect(self.delete)

    def delete(self):
        valid = QMessageBox.question(
            self, 'Вопросик', "Действительно удалить элемент с id: " + str(id),
            QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно,
        # переходим в функцию удаления элементов
        if valid == QMessageBox.Yes:
            self.parent().delete_item(id)
        self.close()

    def cls2(self):
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        # прикрепляем новое окно добавления
        self.add_prod = AddProd(self)

        # прикрепляем новое окно удаления
        self.show_table = ShowTable(self)

        self.to_add.clicked.connect(self.show_insert_form)
        self.to_table.clicked.connect(self.show_delete_form)
        self.titles = None

    def show_insert_form(self):
        # функция для открытия окна добавления элементов
        self.add_prod.show()

    def show_delete_form(self):
        # функция для открытия окна удаления элементов
        self.show_table.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
