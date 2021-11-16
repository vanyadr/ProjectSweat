import sqlite3
import sys
import datetime
import requests
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as dts

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QHeaderView, QComboBox
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
        res1 = cur.execute("""SELECT name FROM Names""").fetchall()
        res1 = [i[0] for i in res1]
        res = [int(i[0]) for i in res]
        print(res)
        if a not in res1:
            if len(res) > 0:
                b = res[-1] + 1
                cur.execute("""INSERT INTO Names (id, name) VALUES (?, ?)""", (res[-1] + 1, a))
                con.commit()
            else:
                b = 1
                cur.execute("""INSERT INTO Names (id, name) VALUES (?, ?)""", (1, a))
                con.commit()
                print(a)

        res = cur.execute("""SELECT id FROM Names""").fetchall()
        res = [int(i[0]) for i in res]
        con.commit()
        con.close()
        self.Parcing(a, res[-1])
        self.close()

    def cls(self):
        self.close()

    def Parcing(self, link, id_name):
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
                print(res)
                print(quotes1)

                if len(quotes) == 0:
                    QMessageBox.question(self, 'Connection Error!',
                                         "We can't connect to the service right now. Try again in 30 minutes!",
                                         QMessageBox.No, QMessageBox.Yes)

                else:
                    if len(res) > 0:
                        cur.execute("""INSERT INTO Product (id, name_id, prod) VALUES (?, ?, ?)""",
                                    (res[-1] + 1, int(id_name[0]), str(quotes[0].text)))
                        con.commit()
                    else:
                        print(str(quotes[0].text))
                        cur.execute("""INSERT INTO Product (id, name_id, prod) VALUES (?, ?, ?)""",
                                    (1, int(id_name[0]), str(quotes[0].text)))
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


class ShowTable(QMainWindow):
    def __init__(self, parent=None):
        super(ShowTable, self).__init__(parent)
        uic.loadUi("table_window.ui", self)
        self.go_back2.clicked.connect(self.cls2)
        self.delete1.clicked.connect(self.delete)
        self.load()

    def load(self):
        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        names = cur.execute("""SELECT prod FROM Product""").fetchall()
        ids = cur.execute(("""SELECT id FROM Product""")).fetchall()

        print(ids)
        print(names)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Number", 'Name', 'Minimal Price'])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.setRowCount(0)
        count = 0

        for i in range(len(names)):
            prices = cur.execute(
                """SELECT price FROM Prices WHERE name_id = (SELECT name_id FROM Product WHERE prod = ?)""",
                (names[i][0],)).fetchall()
            print(prices)
            prices = min(prices)
            count += 1
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(ids[i][0])))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(names[i][0]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(prices[0]))

        self.tableWidget.resizeColumnsToContents()

    def delete(self):
        strs = [i.row() for i in self.tableWidget.selectedItems()]
        ids = [self.tableWidget.item(i, 0).text() for i in strs]
        ids = set(ids)
        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        print(ids)

        valid = QMessageBox.question(
            self, 'Attention!', "Are you sure you want delete this element?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            for i in ids:
                cur.execute("""DELETE FROM Product WHERE id = ?""", (i,))
                cur.execute("""DELETE FROM Prices WHERE id = ?""", (i,))
                cur.execute("""DELETE FROM Date WHERE id = ?""", (i,))
                cur.execute("""DELETE FROM Names WHERE id = ?""", (i,))
                con.commit()
        self.load()

    def cls2(self):
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main_window.ui", self)

        self.add_prod = AddProd(self)
        self.show_table = ShowTable(self)

        self.to_add.clicked.connect(self.show_insert_form)
        self.to_table.clicked.connect(self.show_delete_form)
        self.reboot.clicked.connect(self.parc)
        self.titles = None

        self.orig = Image.open('2.png')
        self.temp = ImageQt(self.orig)
        self.pixmap = QPixmap.fromImage(self.temp)
        self.grafik.setPixmap(self.pixmap.scaled(self.grafik.size()))

        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        names = cur.execute("""SELECT prod FROM Product""").fetchall()
        names = [str(i[0]) for i in names]
        print(names)
        self.change_prod.addItems(names)
        self.now_name = self.change_prod.currentText()
        print(str(self.now_name))

    def show_insert_form(self):
        self.add_prod.show()

    def show_delete_form(self):
        self.show_table.show()

    def parc(self):
        self.now_name = self.change_prod.currentText()
        con = sqlite3.connect('Prods.db')
        cur = con.cursor()
        link = cur.execute("""SELECT name FROM Names WHERE id = (SELECT id FROM Product WHERE prod = ?)""",
                           (self.now_name,)).fetchall()
        print(link)
        id = cur.execute("""SELECT id FROM Product WHERE prod = ?""", (self.now_name,)).fetchall()
        print(id)

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
                quotes1 = soup1.find_all('span')
                con = sqlite3.connect('Prods.db')
                cur = con.cursor()
                res = cur.execute("""SELECT id FROM Product""").fetchall()
                res = [int(i[0]) for i in res]
                id_name = [id_name]
                print(id_name)
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

        search(link[0][0])
        parc(id[0][0])

        prices = cur.execute(
            """SELECT price FROM Prices WHERE name_id = (SELECT name_id FROM Product WHERE prod = ?)""",
            (self.now_name,)).fetchall()
        print(prices)
        pr = [i[0] for i in prices]
        pr = [i[:len(i) - 1:] for i in pr]
        print(pr)
        plt.title(self.now_name, fontsize=10, fontname='Times New Roman')
        plt.plot([i for i in range(len(pr))], pr)
        plt.savefig('1.png')
        self.orig = Image.open('1.png')
        self.temp = ImageQt(self.orig)
        self.pixmap = QPixmap.fromImage(self.temp)
        self.grafik.setPixmap(self.pixmap.scaled(self.grafik.size()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
