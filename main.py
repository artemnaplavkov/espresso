import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QDialog, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic


class Coffee(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('coffee')
        title = ['ID', 'Название сорта', 'Степень обжарки',
            'Молотый/в зернах', 'Описание', 'Цена', 'Обьём упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
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

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())
