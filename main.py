import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QDialog, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic


class Form(QDialog):
    def __init__(self, id):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.pushButton.clicked.connect(self.save)
        self.id = id

    def save(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if self.id == 0:
            sql = """
INSERT INTO 
    coffee (name_of_sort, degree_of_roasting, ground_in_grains, description_taste, price, volume_of_packaging) 
VALUES('"""
            sql += self.lineEdit_2.text() + "','"
            sql += self.lineEdit_3.text() + "','"
            sql += self.lineEdit_4.text() + "','"
            sql += self.lineEdit_5.text() + "','"
            sql += self.lineEdit_6.text() + "','"
            sql += self.lineEdit_7.text() + "' )"
        else:
            sql = """
UPDATE coffee SET
name_of_sort = '""" + self.lineEdit_2.text() + """',
degree_of_roasting = '""" + self.lineEdit_3.text() + """',
ground_in_grains = '""" + self.lineEdit_4.text() + """',
description_taste = '""" + self.lineEdit_5.text() + """',
price = '""" + self.lineEdit_6.text() + """',
volume_of_packaging = '""" + self.lineEdit_7.text() + """'
WHERE id = '""" + str(self.id) + """'"""
        cur.execute(sql)
        con.commit()
        self.close()

class Coffee(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('cappuccino')
        title = ['ID', 'Название сорта', 'Степень обжарки',
            'Молотый/в зернах', 'Описание', 'Цена', 'Обьём упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        self.pushButton.clicked.connect(self.change)
        self.pushButton_2.clicked.connect(self.add)
        self.fill_table()
        
    def fill_table(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()        
        try:
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            sql = """  
SELECT
    id,
    name_of_sort,
    degree_of_roasting,
    ground_in_grains,
    description_taste,
    price,
    volume_of_packaging
FROM coffee"""
            result = cur.execute(sql).fetchall()
            for i, row in enumerate(result):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, cell in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(cell)))
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(e)

    def change(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return
        dlg = Form(int(self.tableWidget.item(row, 0).text()))
        dlg.lineEdit_2.setText(self.tableWidget.item(row, 1).text())
        dlg.lineEdit_3.setText(self.tableWidget.item(row, 2).text())
        dlg.lineEdit_4.setText(self.tableWidget.item(row, 3).text())
        dlg.lineEdit_5.setText(self.tableWidget.item(row, 4).text())
        dlg.lineEdit_6.setText(self.tableWidget.item(row, 5).text())
        dlg.lineEdit_7.setText(self.tableWidget.item(row, 6).text())
        dlg.exec_()
        self.fill_table()
    
    def add(self):
        dlg = Form(0)
        dlg.exec_()
        self.fill_table()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
