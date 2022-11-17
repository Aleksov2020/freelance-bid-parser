#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time

import bot

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFocusEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QTableWidget, QAbstractItemView, QLabel, \
    QTableWidgetItem, QSlider, QPlainTextEdit, QTextEdit

UPDATE_SEC = 2

data_weblancer = {
        "title": [],
        "link": [],
        "time_ago": [],
        "category": []
    }

cur_row_wl = 0
cur_col = 0

TEMPLATE_GENERATOR = "Здравствуйте!  \n \nГотов выполнить Ваш заказ. Имею большой опыт по разработке сайтов на " \
                     "WordPress и прочих движках. \n \nСвязаться со мной можно через мессенджеры: \nTelegram: " \
                     "https://t.me/aleksovd\nWhatsApp: +7 996 532-82-17 \nИли почтой: \nalexov.develope@gmail.com " \
                     "\n\nМои последние проекты:\n1. Разработка сайта для компании WordPress (дизайн, " \
                     "код). СЕО продвижение и настройка Яндекс.Директ https://promstal-kuban.ru/ \n2. Разработка " \
                     "лэндинга на WordPress (дизайн, код). https://grlpwrfranchise.ru/ \n3. Разработка сайта " \
                     "компании. Мультирегиональность с поддоменами. СЕО продвижение и настройка Яндекс.Директ " \
                     "https://narkocenter-24.ru/ \n\nРаботаю без предоплаты. Можем воспользоваться следующими " \
                     "схемами: \n1. Поэтапная оплата. Состоит в следующем: \nразбиваем заказ на несколько этапов -> я " \
                     "выполняю этап -> вы вносите правки -> я выполняю правки -> вы оплачиваете этап \n2. Безопасная " \
                     "Сделка. \n\nБуду рад сотрудничеству! "

def update_30_sec():
    global UPDATE_SEC
    UPDATE_SEC = 30


def update_1_min():
    global UPDATE_SEC
    UPDATE_SEC = 60


def update_5_min():
    global UPDATE_SEC
    UPDATE_SEC = 300


def update_30_min():
    global UPDATE_SEC
    UPDATE_SEC = 1800


class TableLoad(QObject):
    newInformationWl = QtCore.pyqtSignal(dict, object, dict, object)

    def load_weblancer_table(self):
        while True:
            self.newInformationWl.emit(
                bot.run_bot(), Ws.table1, bot.run_bot2(), Ws.table
            )
            time.sleep(UPDATE_SEC)


class WorkSpace(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = QtCore.QThread()
        self.wl = TableLoad()
        self.wl.moveToThread(self.thread)
        self.wl.newInformationWl.connect(self.setup_table)
        self.thread.started.connect(self.wl.load_weblancer_table)
        self.thread.start()

    def initUI(self):
        self.add_menu()
        self.add_table_weblancer()
        self.add_table_fl_ru()
        self.add_table_freelance_ru()
        self.add_table_freelance_com()
        self.setGeometry(0, 0, 1440, 850)
        self.setWindowTitle('WorkSpace')
        self.add_UI()
        self.show()

    def add_UI(self):
        self.default_text = QTextEdit(self)
        self.default_text.setGeometry(660, 470, 620, 300)
        self.default_text.setText(TEMPLATE_GENERATOR)

        self.default_price = QTextEdit(self)
        self.default_price.setGeometry(660, 780, 40, 25)
        self.default_price.setText('150')

        self.dollar = QLabel(self)
        self.dollar.setGeometry(705, 780, 40, 25)
        self.dollar.setText('$')

        self.default_days = QTextEdit(self)
        self.default_days.setGeometry(730, 780, 40, 25)
        self.default_days.setText('5')

        self.dollar = QLabel(self)
        self.dollar.setGeometry(775, 780, 40, 25)
        self.dollar.setText('Дней')


    def add_menu(self):
        add_from_generator = QAction('&Добавить по генератору', self)
        add_from_generator.setShortcut('Ctrl+G')
        add_from_generator.triggered.connect(self.add_request_from_generator)

        add_from_template = QAction('&Добавить из редактора', self)
        add_from_template.setShortcut('Ctrl+H')
        add_from_template.triggered.connect(self.add_request_from_edit)

        menu_update_30_sec = QAction('&Обновлять через 30 сек', self)
        menu_update_30_sec.triggered.connect(update_30_sec)

        menu_update_1_min = QAction('&Обновлять через 1 мин', self)
        menu_update_1_min.triggered.connect(update_1_min)

        menu_update_5_min = QAction('&Обновлять через 5 мин', self)
        menu_update_5_min.triggered.connect(update_5_min)

        menu_update_30_min = QAction('&Обновлять через 30 мин', self)
        menu_update_30_min.triggered.connect(update_30_min)

        self.order_go = QAction('&Открыть в браузере', self)
        self.order_go.setShortcut('Ctrl+O')
        self.order_go.setEnabled(False)
        self.order_go.triggered.connect(self.open_in_browser)

        self.statusBar()

        menubar = self.menuBar()

        addMenu = menubar.addMenu('&Добавить заявку')
        addMenu.addAction(add_from_generator)
        addMenu.addAction(add_from_template)

        updateMenu = menubar.addMenu('&Обновить')

        updateMenu.addAction(menu_update_30_sec)
        updateMenu.addAction(menu_update_1_min)
        updateMenu.addAction(menu_update_5_min)
        updateMenu.addAction(menu_update_30_min)

        orderMenu = menubar.addMenu('&Заказ')
        orderMenu.addAction(self.order_go)


    def add_table_weblancer(self):
        self.label = QLabel("WEBLANCER.NET", self)
        self.label.move(120, 30)
        self.label.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))

        self.table1 = QTableWidget(self)
        self.table1.setGeometry(20, 60, 300, 760)
        self.table1.setColumnCount(1)
        self.table1.setRowCount(0)
        self.table1.setColumnWidth(0, 255)
        self.table1.rowHeight(100)
        self.table1.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table1.setHorizontalHeaderLabels(["Заявка"])
        self.table1.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        self.table1.clicked.connect(self.on_click_weblancer)

    def add_table_fl_ru(self):
        self.label = QLabel("FL.RU", self)
        self.label.move(460, 30)
        self.label.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))

        self.table = QTableWidget(self)
        self.table.setGeometry(340, 60, 300, 760)
        self.table.setColumnCount(1)
        self.table.setRowCount(1)
        self.table.setColumnWidth(0, 282)
        self.table.setRowHeight(0, 100)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(["Заявка"])
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        #self.table.clicked.connect(self.on_click_freelance_ru)

    def add_table_freelance_ru(self):
        self.label = QLabel("FREELANCE.RU", self)
        self.label.move(760, 30)
        self.label.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))

        self.table = QTableWidget(self)
        self.table.setGeometry(660, 60, 300, 400)
        self.table.setColumnCount(1)
        self.table.setRowCount(1)
        self.table.setColumnWidth(0, 282)
        self.table.setRowHeight(0, 100)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(["Заявка"])
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        # self.table.clicked.connect(self.on_click)

    def add_table_freelance_com(self):
        self.label = QLabel("FREELANCE.COM", self)
        self.label.move(1080, 30)
        self.label.setFont(QtGui.QFont("Times", 9, QtGui.QFont.Bold))

        self.table = QTableWidget(self)
        self.table.setGeometry(980, 60, 300, 400)
        self.table.setColumnCount(1)
        self.table.setRowCount(1)
        self.table.setColumnWidth(0, 282)
        self.table.setRowHeight(0, 100)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setHorizontalHeaderLabels(["Заявка"])
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        # self.table.clicked.connect(self.on_click)

    def clearTable(self, table):
        if self.table1.rowCount() > 0:
            while self.table1.rowCount() > 0:
                self.table1.removeRow(0)

    def on_click_weblancer(self):
        global cur_row_wl
        self.order_go.setEnabled(True)
        for currentQTableWidgetItem in self.table1.selectedItems():
            cur_row_wl = currentQTableWidgetItem.row()

    def add_request_from_generator(self):
        global TEMPLATE_GENERATOR
        bot.send_request(data_weblancer["link"][cur_row_wl], TEMPLATE_GENERATOR)

    def open_in_browser(self):
        bot.open_order(data_weblancer["link"][cur_row_wl])

    def add_request_from_edit(self):
        bot.send_request(data_weblancer["link"][cur_row_wl], self.default_text, self.default_price, self.default_days)


    @QtCore.pyqtSlot(dict, object, dict, object)
    def setup_table(self, result, table, result2, table2):
        global data_weblancer, data_weblancer2
        data_weblancer = result
        self.clearTable(table)
        for i in range(0, len(result["title"])):
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            table.setItem(i, 0, QTableWidgetItem(
                result["title"][i] + "\n" + result["time_ago"][i] + "\n" +
                result["category"][i]))
            table.setRowHeight(i, 80)

        data_weblancer2 = result2
        self.clearTable(table2)
        for i in range(0, len(result2["title"])):
            rowPosition = table2.rowCount()
            table2.insertRow(rowPosition)
            table2.setItem(i, 0, QTableWidgetItem(
                result2["title"][i] + "\n" + result2["time_ago"][i] + "\n" +
                result2["category"][i]))
            table2.setRowHeight(i, 80)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ws = WorkSpace()
    sys.exit(app.exec_())
