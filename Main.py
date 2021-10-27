import sqlite3
import sys
import datetime
import requests
from bs4 import BeautifulSoup

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
        a = self.lineEdit.text()
        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        res = cur.execute("""SELECT id FROM Names""").fetchall()
        res = [int(i[0]) for i in res]
        print(res)
        if len(res) > 0:
            b = res[-1] + 1
            cur.execute("""INSERT INTO Names (id, name) VALUES (?, ?)""", (res[-1] + 1, a))
            con.commit()
        else:
            b = 1
            cur.execute("""INSERT INTO Names (id, name) VALUES (?, ?)""", (1, a))
            con.commit()
            print(a)
        res = cur.execute("""SELECT id FROM Date""").fetchall()
        res = [int(i[0]) for i in res]
        if len(res) > 0:
            cur.execute("""INSERT INTO Date (id, name_id, date) VALUES (?, ?, ?)""", (res[-1] + 1, b, str(datetime.date.today())))
            con.commit()
        else:
            cur.execute("""INSERT INTO Date (id, name_id, date) VALUES (?, ?, ?)""", (1, b, str(datetime.date.today())))
            con.commit()
            print(str(datetime.date.today()))
        res = cur.execute("""SELECT id FROM Names""").fetchall()
        res = [int(i[0]) for i in res]
        con.commit()
        con.close()
        self.Parcing(a, res[-1], b)
        self.close()

    def cls(self):
        self.close()

    def Parcing(self, link, id_name, b):
        def search(link):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

            url = link
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            with open('Parc.html', 'w', encoding="utf-8") as output_file:
                output_file.write(str(soup))

        def parc(id_name):
            with open('Parc.html', 'r', encoding='utf-8') as input_file:
                contents = input_file.read()
                soup1 = BeautifulSoup(contents, 'lxml')
                quotes = soup1.find_all('h1')
                quotes1 = soup1.find_all('span')
                con = sqlite3.connect('Prods.db')
                cur = con.cursor()
                res = cur.execute("""SELECT id FROM Product""").fetchall()
                res = [int(i[0]) for i in res]
                id_name = [id_name]
                print(id_name)
                print(quotes)
                if len(res) > 0:
                    cur.execute("""INSERT INTO Product (id, name_id, prod) VALUES (?, ?, ?)""", (res[-1] + 1, int(id_name[0]), str(quotes[0].text)))
                    con.commit()
                else:
                    print(str(quotes[0].text))
                    cur.execute("""INSERT INTO Product (id, name_id, prod) VALUES (?, ?, ?)""", (1, int(id_name[0]), str(quotes[0].text)))
                    con.commit()
                flag = True
                for j in quotes1:
                    if j.text != '':
                        if j.text[len(j.text) - 1] == '₽' and flag:
                            j = str(j.text)
                            j = j[:len(j) - 2:] + j[len(j) - 1]
                            res1 = cur.execute("""SELECT id FROM Prices""").fetchall()
                            res1 = [int(i[0]) for i in res1]
                            if len(res1) > 0:
                                cur.execute("""INSERT INTO Prices (id, name_id, price) VALUES (?, ?, ?)""",
                                            (res1[-1] + 1, int(id_name[0]), j))
                                con.commit()
                            else:
                                cur.execute("""INSERT INTO Prices (id, name_id, price) VALUES (?, ?, ?)""",
                                            (1, int(id_name[0]), j))
                                con.commit()
                                print(j)
                            flag = False
                con.commit()
                con.close()
        search(link)
        parc(id_name)


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
        self.reboot.clicked.connect(self.parc)
        self.titles = None

        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        names = cur.execute("""SELECT prod FROM Product""").fetchall()
        names = [str(i[0]) for i in names]
        print(names)
        self.change_prod.addItems(names)
        self.now_name = self.change_prod.activated[str]

    def show_insert_form(self):
        # функция для открытия окна добавления элементов
        self.add_prod.show()

    def show_delete_form(self):
        # функция для открытия окна удаления элементов
        self.show_table.show()

    def parc(self):
        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        date = cur.execute("""SELECT date FROM Date
                    WHERE name_id = (SELECT id FROM Names WHERE name = ?)""", (self.now_name,)).fetchall()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
