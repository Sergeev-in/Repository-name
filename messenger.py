from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui


# наследование - процедура при котороый все содержимое дочернего класса копируется в класс наследника
class MessengerWindow(QtWidgets.QMainWindow, clientui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.pressed.connect(self.sendMessage)
        self.last_message_time = 0
        self.timer = QtCore.QTimer()  # создает событие которые вызывается не пользователем, а по таймаут функцию
        self.timer.timeout.connect(self.getUpdates)
        self.timer.start(1000)  # т.е. раз в секунду будет вызываться getUpdates

    def sendMessage(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()
        if not username:
            self.Wrtext('User is empty :(')
            self.Wrtext('')
            return
        if not password:
            self.Wrtext('password is empty :(')
            self.Wrtext('')
            return
        if not text:
            self.Wrtext('text is empty :(')
            self.Wrtext('')
            return
        response = requests.post('http://127.0.0.1:5000/send',
                                 json={"username": username, "password": password, "text": text})
        if not response.json()['ok']:
            self.Wrtext('Access denied')  # Доступ запрещен
            self.Wrtext('')
            return

        self.textEdit.clear()
        self.textEdit.repaint()

    def Wrtext(self, text):
        self.textBrowser.append(text)
        self.textBrowser.repaint()

    def getUpdates(self):
        response = requests.get('http://127.0.0.1:5000/history',
                                params={'after': self.last_message_time})
        # параметр, сюда нам нужно передавать дату последнего сообщения, которое у нас уже имеется (подгрузили)
        # чтобы нам передали только те сообщения, у которых дата больше чем наше сообщение
        data = response.json()
        for message in data['messages']:
            # float => datetime
            norm_time = datetime.fromtimestamp(message['time'])
            norm_time = norm_time.strftime('%Y/%m/%d %H:%M:%S')
            self.Wrtext(norm_time + ' ' + message['username'])
            self.Wrtext(message['text'])
            self.Wrtext('')
            self.last_message_time = message['time']


# событие (pressed) - кто-то кликнул кнопку send, обработчик self.sendMessage
# когда мы что-то делаем в мессенджере, то это событие - разные типы
# на все эти события записан обработчик, вешаем своих обработчиков)))


app = QtWidgets.QApplication([])
window = MessengerWindow()
window.show()  # при вызове данного метода он отрисовывает окошко со всеми кнопками
app.exec_()
