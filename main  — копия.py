#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PySide2.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide2.QtWidgets import (
    QTableView,
    QApplication,
    QHBoxLayout,
    QGridLayout,
    QPushButton,
    QWidget,
    QLineEdit,
    QFrame,
    QLabel,
    QHeaderView,
    QDateEdit,
    QTabWidget
)
from PySide2.QtCore import (
    QAbstractTableModel,
    Signal,
    Slot,
)
from PySide2.QtCore import QSortFilterProxyModel, Qt, QRect
import sys


class DateBase:
    def __init__(self, db_file) -> None:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_file)
        if not db.open():
            return False
        self.q = QSqlQuery()
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Car (
            "Код билета" text PRIMARY KEY,
            "Пункт отправления" text,
            "Пункт прибытия" text,
            "Тип транспорта" text);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Owner (
            "Id пассажира" text PRIMARY KEY,
            "ФИО" text,
            "Дата рождения" date,
            "Номер и серия паспорта" text);"""
        )
        self.q.exec_(
            """
        CREATE TABLE IF NOT EXISTS Docs (
            "Id водителя" text PRIMARY KEY,
            "Имя водителя" text,
            "Дата отправления" date,
            "Тип транспорта" text);"""
        )
        self.q.exec_(
            """INSERT INTO Car VALUES("8d2cbab4e5ec03c99215bb6cbf619348", "Москва", "Самара", "Поезд")"""
        )
        self.q.exec_(
            """INSERT INTO Car VALUES("d7f1748981fe83e7e33d177e7ecd8e70", "Самара", "Вашингтон", "Самолёт")"""
        )
        self.q.exec_(
            """INSERT INTO Car VALUES("adbbc672f485dc806ca03d9e7287d192", "Тольятти", "Уфа", "Автобус")"""
        )
        self.q.exec_(
            """INSERT INTO Owner VALUES("3130675567", "Абрамов Андрей", "09.09.2000", "0719568675")"""
        )
        self.q.exec_(
            """INSERT INTO Owner VALUES("2130175567", "Орлов Иван", "08.08.2001", "0399568675")"""
        )
        self.q.exec_(
            """INSERT INTO Owner VALUES("6430175567", "Горностай Яна", "07.07.2002", "1999568675")"""
        )
        self.q.exec_(
            """INSERT INTO Docs VALUES("3130675567", "Ахмед", "29.12.2022", "Поезд")"""
        )
        self.q.exec_(
            """INSERT INTO Docs VALUES("2130175567", "Абдул-Хамид", "30.12.2022", "Самолёт")"""
        )
        self.q.exec_(
            """INSERT INTO Docs VALUES("6430175567", "Шамсудин", "1.12.2023", "Автобус")"""
        )


class TableView:
    tabBarClicked = Signal(int)

    def __init__(self, parent):
        self.parent = parent
        self.SetupUI()
        self.current_tab = "Car"
        self.tab_id = "VIN-номер"

    def SetupUI(self):
        self.parent.setGeometry(400, 500, 1000, 650)
        self.parent.setWindowTitle("Транспортная служба Ставропольского Края")
        self.main_conteiner = QGridLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        self.frame2.setVisible(False)
        self.main_conteiner.addWidget(self.frame1, 0, 0)
        self.main_conteiner.addWidget(self.frame2, 0, 0)
        self.frame1.setStyleSheet(
            """
            font: bold;
            font-size: 15px;
            """
        )
        self.frame2.setStyleSheet(
            """
            font: bold;
            font-size: 15px;
            """
        )
        self.table_view = QTableView()
        self.table_view.setModel(self.tableCar())
        self.table_view2 = QTableView()
        self.table_view2.setModel(self.tableOwner())
        self.table_view3 = QTableView()
        self.table_view3.setModel(self.tableDocs())
        self.table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view3.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table_view2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.layout_main = QGridLayout(self.frame1)
        self.layh = QHBoxLayout()
        self.btn_add = QPushButton("Добавить")
        self.btn_del = QPushButton("Удалить")
        self.layh.addWidget(self.btn_add)
        self.layh.addWidget(self.btn_del)
        self.tab_conteiner = QTabWidget()
        self.tab_conteiner.setTabShape(QTabWidget.Triangular)
        self.tab_conteiner.addTab(self.table_view, "Билеты")
        self.tab_conteiner.addTab(self.table_view2, "Пассажиры")
        self.tab_conteiner.addTab(self.table_view3, "Водители")
        self.layout_main.addWidget(self.tab_conteiner, 0, 0)
        self.layout_main.addLayout(self.layh, 1, 0)
        self.parent.setLayout(self.main_conteiner)
        self.btn_del.clicked.connect(self.delete)
        self.btn_add.clicked.connect(self.add)
        self.layout_grid = QGridLayout(self.frame2)
        self.btn_add2 = QPushButton("Добавить данные")
        self.btn_add2.setFixedWidth(300)
        self.btn_otmena = QPushButton("Отмена")
        self.line_name = QLineEdit()
        self.name = QLabel("ФИО: ")
        self.doc_num_line = QLineEdit()
        self.doc_num = QLabel("Номер удостоверения: ")
        self.color_line = QLineEdit()
        self.color = QLabel("Цвет: ")
        self.dateb_line = QDateEdit()
        self.dateb_line.setCalendarPopup(True)
        self.dateb_line.setTimeSpec(Qt.LocalTime)
        self.dateb_line.setGeometry(QRect(220, 31, 133, 20))
        self.dateb = QLabel("Дата рождения: ")
        self.line_pasport = QLineEdit()
        self.pasport = QLabel("Номер и серия паспорта: ")
        self.vin_line = QLineEdit()
        self.vin = QLabel("VIN-номер: ")
        self.marka_line = QLineEdit()
        self.marka = QLabel("Марка авто: ")
        self.model_line = QLineEdit()
        self.models = QLabel("Модель: ")
        self.docs_reg = QLabel("Дата выдачи документа: ")
        self.docs_reg_line = QDateEdit()
        self.docs_reg_line.setCalendarPopup(True)
        self.docs_reg_line.setTimeSpec(Qt.LocalTime)
        self.docs_reg_line.setGeometry(QRect(220, 31, 133, 20))
        self.cate_line = QLineEdit()
        self.cate = QLabel("Категория прав: ")
        self.layout_grid.addWidget(self.line_name, 0, 1)
        self.layout_grid.addWidget(self.name, 0, 0)
        self.layout_grid.addWidget(self.doc_num, 1, 0)
        self.layout_grid.addWidget(self.doc_num_line, 1, 1)
        self.layout_grid.addWidget(self.dateb, 2, 0)
        self.layout_grid.addWidget(self.dateb_line, 2, 1)
        self.layout_grid.addWidget(self.marka_line, 3, 1)
        self.layout_grid.addWidget(self.marka, 3, 0)
        self.layout_grid.addWidget(self.model_line, 4, 1)
        self.layout_grid.addWidget(self.models, 4, 0)
        self.layout_grid.addWidget(self.line_pasport, 5, 1)
        self.layout_grid.addWidget(self.pasport, 5, 0)
        self.layout_grid.addWidget(self.vin_line, 6, 1)
        self.layout_grid.addWidget(self.vin, 6, 0)
        self.layout_grid.addWidget(self.color_line, 7, 1)
        self.layout_grid.addWidget(self.color, 7, 0)
        self.layout_grid.addWidget(self.docs_reg_line, 8, 1)
        self.layout_grid.addWidget(self.docs_reg, 8, 0)
        self.layout_grid.addWidget(self.cate, 9, 0)
        self.layout_grid.addWidget(self.cate_line, 9, 1)
        self.layout_grid.addWidget(self.btn_add2, 10, 1)
        self.layout_grid.addWidget(self.btn_otmena, 10, 0)
        self.btn_otmena.clicked.connect(self.back)
        self.btn_add2.clicked.connect(self.add_data)
        self.tab_conteiner.tabBarClicked.connect(self.handle_tabbar_clicked)

    def tableCar(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Car"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Car"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableOwner(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Owner"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Owner"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def tableDocs(self):
        self.raw_model = QSqlTableModel()
        self.sqlquery = QSqlQuery()
        self.query = """SELECT * FROM Docs"""
        self.sqlquery.exec_(self.query)
        self.raw_model.setQuery(self.sqlquery)
        self.current_tab = "Docs"
        self.tab_id = "Номер удостоверения"
        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.raw_model)
        return self.model

    def add(self):
        self.frame1.setVisible(False)
        self.frame2.setVisible(True)

    def back(self):
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def update(self):
        self.table_view.setModel(self.tableCar())
        self.table_view2.setModel(self.tableOwner())
        self.table_view3.setModel(self.tableDocs())


    def add_data(self):
        self.sqlquery = QSqlQuery()
        self.query = "INSERT INTO Car VALUES('{}', '{}', '{}', '{}')".format(self.marka_line.text(), self.vin_line.text(), self.marka_line.text(), self.color_line.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Owner VALUES('{}', '{}', '{}', '{}')".format(self.doc_num_line.text(), self.line_name.text(), self.dateb_line.text(), self.line_pasport.text())
        self.sqlquery.exec_(self.query)
        self.query = "INSERT INTO Docs VALUES('{}', '{}', '{}', '{}')".format(self.doc_num_line.text(), self.vin_line.text(), self.docs_reg_line.text(), self.cate_line.text())
        self.sqlquery.exec_(self.query)
        self.update()
        self.frame1.setVisible(True)
        self.frame2.setVisible(False)

    def cell_click(self):
        if self.current_tab == "Car":
            return self.table_view.model().data(self.table_view.currentIndex())
        if self.current_tab == "Docs":
            return self.table_view3.model().data(self.table_view3.currentIndex())
        if self.current_tab == "Owner":
            return self.table_view2.model().data(self.table_view2.currentIndex())

    def delete(self):
        self.sqlquery = QSqlQuery()
        self.query = f"""DELETE FROM {self.current_tab} WHERE ("{self.tab_id}" = "{self.cell_click()}")"""
        print(self.query)
        self.sqlquery.exec_(self.query)
        self.update()

    def handle_tabbar_clicked(self, index):
        if(index==0):
            self.current_tab = "Car"
            self.tab_id = "VIN-номер"
        elif(index==1):
            self.current_tab = "Owner"
            self.tab_id = "Номер удостоверения"
        else:
            self.tab_id = "Номер удостоверения"
            self.current_tab = "Docs"

class MainWindow(QWidget):
    def __init__(self) -> None:
        QWidget.__init__(self)
        self.my_datebase = DateBase("datebase.db")
        if not self.my_datebase:
            sys.exit(-1)
        self.main_view = TableView(self)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
