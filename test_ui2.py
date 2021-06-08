# -*- coding: utf-8 -*-
# python 3.9 | PyQt5
import sys
import requests
import socket

from functools import partial
from hashlib import md5
from datetime import date

from PyQt5.QtCore import QSize, QRect, Qt, QMetaObject
from PyQt5.QtGui import QFont, QPixmap, QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QSizePolicy, QWidget, QListWidget, QListWidgetItem, QScrollArea, QLabel, \
    QVBoxLayout, QPushButton, QLineEdit, QComboBox, QMessageBox, QMainWindow, QApplication, QAction, qApp, \
    QInputDialog, QDialog, QGridLayout, QCalendarWidget, QDesktopWidget

THEMES = {'Простейший поток': 0,
          'Суммирование и разъединение простейших потоков': 1,
          'Показательный закон распределения времени обслуживания': 2,
          'Нестационарный Пуассоновский поток': 3,
          'Теорема Литтла': 4,
          'Задачи для самостоятельного решения 1': 5,
          'Одноканальная система массового обслуживания с отказами': 6,
          'Система массового обслуживания с ожиданием и без ограничения очереди': 7,
          'Система массового обслуживания с ожиданием и ограничением длины очереди': 8,
          'Многоканальная система массового обслуживания с отказами М/М/N/0': 9,
          'Многоканальная система массового обслуживания с неограниченным ожиданием': 10,
          'Многоканальная система массового обслуживания с ожиданием и ограниченной длиной очереди': 11,
          'Задачи для самостоятельного решения 2': 12,
          'Контрольная работа': 13,
          }


class ProgramAuth:
    def __init__(self):
        self.activated = False
        self.admin_pass = '22cdd7a0eac9348c762dd4f5f4ccd889'
        self.lecturer_pass = ''
        self.date = ''  # TODO: установить дату на текущую лицензию
        self.connection = True

    def password_verification(self, password):
        hash_pass = md5(str(password).encode()).hexdigest()
        if hash_pass == self.admin_pass or hash_pass == self.lecturer_pass:
            return True
        else:
            return False

    def set_lecturer_pass(self, password, previous_password):
        password = password.text()
        previous_password = previous_password.text()
        hash_password = md5(str(previous_password).encode()).hexdigest()
        if hash_password == self.lecturer_pass or (previous_password == '' and self.lecturer_pass == ''):
            self.lecturer_pass = md5(str(password).encode()).hexdigest()
            modal_message = QMessageBox(QMessageBox.NoIcon, 'Успешно', 'Пароль изменён')
            modal_message.exec_()
        else:
            modal_message = QMessageBox(QMessageBox.Warning, 'Ошибка', 'Пароли не совпадают')
            modal_message.exec_()

    def set_date(self, calendar_date):
        self.date = calendar_date.selectedDate().toString("yyyy-MM-dd")

    def get_licence(self):
        pass

    def update_licence(self, calendar_date):
        pass

    def check_date(self):
        current_date = str(date.today())
        if self.connection:
            online_date = requests.get('http://worldclockapi.com/api/json/est/now').json()['currentDateTime'][:10]
            if current_date != online_date:
                return False
            else:
                return True
        return True

    def check_internet_connection(self):
        try:
            socket.create_connection(("1.1.1.1", 53))
            self.connection = True
            return
        except OSError:
            pass
        self.connection = False


class Testing:
    def __init__(self):
        self.answers = {}
        self.current_questions_pack = 1  # от 1 до 7, по 3 вопроса в группе | 21 / 3 = 7
        self.MIN_QUESTION = 1
        self.MAX_QUESTION = 21


class MainWindowUI(object):
    def __init__(self):
        self.tester = Testing()
        self.auth = ProgramAuth()

    def setupUi(self, main_window):
        main_window.resize(1280, 720)
        main_window.setMinimumSize(QSize(1280, 720))
        main_window.setMaximumSize(QSize(1280, 720))
        font = QFont()
        font.setFamily("Times New Roman")
        font.setKerning(True)
        font.setPointSize(15)
        font.setWeight(50)
        main_window.setFont(font)

        frame_geometry = main_window.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_geometry.moveCenter(center_point)
        main_window.move(frame_geometry.topLeft())

        self.main_window = main_window
        self.centralwidget = QWidget(main_window)

        main_window.statusBar().hide()

        exitAct = QAction('&Exit', main_window)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        tool_bar = main_window.addToolBar('Выход')
        tool_bar.setMovable(False)
        tool_bar.addAction('Администрирование').triggered.connect(self.admin_app)
        tool_bar.addAction('Выход').triggered.connect(self.exit_app)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QRect(0, 0, 391, 711))
        self.listWidget.setMinimumSize(QSize(0, 0))
        self.listWidget.setMaximumSize(QSize(16777215, 16777215))
        self.listWidget.setFont(font)
        self.listWidget.setStyleSheet("QListWidget { border-style: outset; border-width: 1px }\n"
                                      "QListWidget::item { border-bottom: 2px solid black }\n"
                                      "QListWidget::item:selected { background-color: rgb(77, 148, 255) }\n"
                                      "QListWidget::item:hover { background-color: rgb(153, 194, 255) }")
        self.listWidget.setLineWidth(5)
        self.listWidget.setWordWrap(True)

        for i in range(len(THEMES)):
            self.listWidget.addItem(QListWidgetItem())

        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QRect(389, -1, 891, 711))
        self.scrollArea.setStyleSheet("border-style: outset; border-width: 1px")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 875, 709))

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QRect(0, 0, 891, 711))
        self.label.setText("")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.label.setWordWrap(False)

        self.scrollArea.setWidget(self.label)
        main_window.setCentralWidget(self.centralwidget)

        self.ui_add_content(main_window)
        self.tester_ui(main_window)

        QMetaObject.connectSlotsByName(main_window)

        self.auth.check_internet_connection()


    def tester_ui(self, main_window):
        self.tsArea = QScrollArea(main_window)
        self.tsArea.setGeometry(QRect(389, -1, 891, 711))
        self.tsArea.setStyleSheet("border-style: outset; border-width: 1px")
        self.tsArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tsArea.setWidgetResizable(True)

        self.tWidget = QWidget(main_window)
        self.tWidget.setGeometry(QRect(0, 0, 875, 709))

        self.layout = QVBoxLayout(main_window)

        self.btn_next = QPushButton('Далее', main_window)
        self.btn_next.setGeometry(0, 0, 100, 50)
        self.btn_next.setEnabled(True)
        self.btn_next.clicked.connect(self.next_question)
        self.btn_next.setStyleSheet("QPushButton { border-style: outset; border-width: 2px; border-radius: 10px;"
                                    "border-color: black; min-width: 10em; padding: 6px; "
                                    "background: rgb(140, 140, 140) }"
                                    "QPushButton:hover { background: rgb(179, 179, 179) }"
                                    "QPushButton:pressed { font: bold }")

        self.btn_back = QPushButton('Назад', main_window)
        self.btn_back.setGeometry(QRect(0, 0, 100, 50))
        self.btn_back.setEnabled(True)
        self.btn_back.clicked.connect(self.previous_question)
        self.btn_back.setStyleSheet("QPushButton { border-style: outset; border-width: 2px; border-radius: 10px;"
                                    "border-color: black; min-width: 10em; padding: 6px; "
                                    "background: rgb(140, 140, 140) }"
                                    "QPushButton:hover { background: rgb(179, 179, 179) }"
                                    "QPushButton:pressed { font: bold }")

        self.btn_end = QPushButton('Закончить', main_window)
        self.btn_end.setGeometry(0, 0, 100, 50)
        self.btn_end.setEnabled(True)
        self.btn_end.clicked.connect(self.end_test)
        self.btn_end.setStyleSheet("QPushButton { border-style: outset; border-width: 2px; border-radius: 10px;"
                                   "border-color: black; min-width: 10em; padding: 6px; "
                                   "background: rgb(140, 140, 140) }"
                                   "QPushButton:hover { background: rgb(179, 179, 179) }"
                                   "QPushButton:pressed { font: bold }")

        self.options = QLabel(self.tWidget)
        self.options.setGeometry(QRect(0, 0, 891, 711))

        self.options.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.options.setPixmap(QPixmap('img/options.png'))
        self.options.resize(self.options.pixmap().height(), self.options.pixmap().height())

        variant_validator = QIntValidator()
        variant_validator.setRange(0, 9)

        self.variant = QComboBox(self.tWidget)
        self.variant.setGeometry(0, 0, 50, 50)
        self.variant.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.variant.activated.connect(self.confirm_variant)

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        validator.setRange(0, 1000.0, 2)

        self.question_p1 = QLabel(self.tWidget)
        self.question_p1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.answer_p1 = QLineEdit(self.tWidget)
        self.answer_p1.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.answer_p1.setPlaceholderText('Введите ответ:')
        self.answer_p1.setValidator(validator)

        self.question_p2 = QLabel(self.tWidget)
        self.question_p2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.answer_p2 = QLineEdit(self.tWidget)
        self.answer_p2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.answer_p2.setPlaceholderText('Введите ответ:')
        self.answer_p2.setValidator(validator)

        self.question_p3 = QLabel(self.tWidget)
        self.question_p3.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.answer_p3 = QLineEdit(self.tWidget)
        self.answer_p3.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.answer_p3.setPlaceholderText('Введите ответ:')
        self.answer_p3.setValidator(validator)

        self.answer_p1.setEnabled(False)
        self.answer_p2.setEnabled(False)
        self.answer_p3.setEnabled(False)

        self.layout.addWidget(self.options)
        self.layout.addWidget(self.variant)
        self.layout.addWidget(self.question_p1)
        self.layout.addWidget(self.answer_p1)
        self.layout.addWidget(self.question_p2)
        self.layout.addWidget(self.answer_p2)
        self.layout.addWidget(self.question_p3)
        self.layout.addWidget(self.answer_p3)
        self.layout.addWidget(self.btn_next)
        self.layout.addWidget(self.btn_back)
        self.layout.addWidget(self.btn_end)

        self.tWidget.setLayout(self.layout)

        self.tsArea.setWidget(self.tWidget)

        self.tsArea.hide()

        self.update_question()

    def admin_app(self):
        text, ok = QInputDialog.getText(self.tWidget, 'Войти', 'Введите пароль:', QLineEdit.Password)
        if self.auth.password_verification(text):
            admin_modal = QDialog(self.centralwidget)
            admin_modal.setGeometry(QRect(0, 0, 800, 600))

            grid = QGridLayout()

            empty = QWidget()
            empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

            old_pass = QLabel()
            old_pass.setText('Введите старый пароль:')

            old_pass_line = QLineEdit()
            old_pass_line.setEchoMode(QLineEdit.Password)

            new_pass = QLabel()
            new_pass.setText('Введите новый пароль:')

            new_pass_line = QLineEdit()
            new_pass_line.setEchoMode(QLineEdit.Password)

            btn_accept = QPushButton('Изменить пароль')
            btn_accept.clicked.connect(partial(self.auth.set_lecturer_pass, new_pass_line, old_pass_line))

            expired_date = QLabel()
            expired_date.setText('Дата действия программы:')

            date_widget = QCalendarWidget()

            btn_licence = QPushButton('Применить')
            btn_licence.clicked.connect(partial(self.auth.set_date, date_widget))

            grid.addWidget(old_pass, 1, 0)
            grid.addWidget(old_pass_line, 1, 1)
            grid.addWidget(new_pass, 2, 0)
            grid.addWidget(new_pass_line, 2, 1)
            grid.addWidget(btn_accept, 3, 0)
            grid.addWidget(expired_date, 4, 0)
            grid.addWidget(date_widget, 5, 0)
            grid.addWidget(btn_licence, 6, 0)
            grid.addWidget(empty, 10, 0)

            admin_modal.setLayout(grid)
            admin_modal.exec_()
            # a6CR~QMaracuja1;

    def exit_app(self):
        cv_modal = QMessageBox(QMessageBox.NoIcon, 'Выйти', 'Вы уверены?',
                               QMessageBox.No | QMessageBox.Yes)
        cv_modal.exec_()
        if cv_modal.result() == QMessageBox.Yes:
            self.main_window.close()

    def confirm_variant(self, variant):
        cv_modal = QMessageBox(QMessageBox.NoIcon, 'Подтверждение', f'Выбрать вариант {variant}',
                               QMessageBox.No | QMessageBox.Yes)
        cv_modal.exec_()
        if cv_modal.result() == QMessageBox.Yes:
            self.variant.setEnabled(False)
            self.answer_p1.setEnabled(True)
            self.answer_p2.setEnabled(True)
            self.answer_p3.setEnabled(True)

    def end_test(self):
        self.update_answers()

    def next_question(self):
        if self.tester.current_questions_pack < 7:
            self.update_answers()
            self.tester.current_questions_pack += 1
            self.update_question()
        else:
            self.tester.current_questions_pack = 7

    def previous_question(self):
        if self.tester.current_questions_pack > 1:
            self.update_answers()
            self.tester.current_questions_pack -= 1
            self.update_question()
        else:
            self.tester.current_questions_pack = 1

    def update_answers(self):
        self.answer_p1.setFocus()
        curr_qp = self.tester.current_questions_pack
        q1, q2, q3 = curr_qp * 3 - 2, curr_qp * 3 - 1, curr_qp * 3

        a_keys = self.tester.answers.keys()
        input_answers = [self.answer_p1, self.answer_p2, self.answer_p3]
        q_index = [q1, q2, q3]

        for index in range(3):
            if input_answers[index].text().isdigit():
                if q_index[index] not in a_keys:
                    self.tester.answers[q_index[index]] = input_answers[index].text()
                if q_index[index] != self.tester.answers[q_index[index]]:
                    self.tester.answers[q_index[index]] = input_answers[index].text()
                input_answers[index].setText('')

    def update_question(self):
        curr_qp = self.tester.current_questions_pack
        q1, q2, q3 = curr_qp * 3 - 2, curr_qp * 3 - 1, curr_qp * 3

        self.question_p1.setPixmap(QPixmap(f'img/q{q1}.png'))
        self.question_p1.resize(self.question_p1.pixmap().height(), self.question_p1.pixmap().height())
        self.question_p2.setPixmap(QPixmap(f'img/q{q2}.png'))
        self.question_p2.resize(self.question_p2.pixmap().height(), self.question_p2.pixmap().height())
        self.question_p3.setPixmap(QPixmap(f'img/q{q3}.png'))
        self.question_p3.resize(self.question_p3.pixmap().height(), self.question_p3.pixmap().height())

        self.answer_p1.setText(self.tester.answers.get(q1))
        self.answer_p2.setText(self.tester.answers.get(q2))
        self.answer_p3.setText(self.tester.answers.get(q3))

    def ui_add_content(self, main_window):
        main_window.setWindowTitle("Теория телетрафика мультисервисных сетей")

        self.listWidget.setSortingEnabled(False)

        for i in THEMES:
            self.listWidget.item(THEMES[i]).setText(i)

        self.listWidget.itemClicked.connect(self.menu_action)

    def menu_action(self, item):
        item_value = int(THEMES[item.text()])
        if item_value < 13:
            self.tsArea.hide()
            self.scrollArea.show()

            self.scrollArea.setWidget(self.label)
            self.label.setPixmap(QPixmap(f'img/{item_value}.png'))
            self.label.resize(self.label.pixmap().height(), self.label.pixmap().height())

            if len(self.tester.answers) > 0:
                self.tester.answers = {}
                self.tester.current_questions_pack = 1
                self.answer_p1.setText('')
                self.answer_p2.setText('')
                self.answer_p3.setText('')
                self.update_answers()
                self.set_default_question()
        elif item_value == 13:
            self.scrollArea.hide()
            self.tsArea.show()
            self.variant.setFocus()

    def set_default_question(self):
        self.question_p1.setPixmap(QPixmap(f'img/q1.png'))
        self.question_p1.resize(self.question_p1.pixmap().height(), self.question_p1.pixmap().height())
        self.question_p2.setPixmap(QPixmap(f'img/q2.png'))
        self.question_p2.resize(self.question_p2.pixmap().height(), self.question_p2.pixmap().height())
        self.question_p3.setPixmap(QPixmap(f'img/q3.png'))
        self.question_p3.resize(self.question_p3.pixmap().height(), self.question_p3.pixmap().height())

    def check_date_wrapper(self):
        if not self.auth.check_date():
            modal_message = QMessageBox(QMessageBox.Warning, 'Ошибка', 'Дата на компьютере не совпадает с реальной')
            modal_message.exec_()
            exit(2)

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = MainWindowUI()
        self.ui.setupUi(self)


app = QApplication([])
application = MyWindow()
application.show()
application.ui.check_date_wrapper()

sys.exit(app.exec())
