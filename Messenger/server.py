import time
from datetime import datetime

from flask import Flask, request

app = Flask(__name__)  # создаем приложение, в который мы будем добавлять наш метод

messages = [

    {'username': 'alex', 'text': 'Hi team !!!', 'time': time.time()},

    {'username': 'nikola', 'text': 'Hello, alex :)))', 'time': time.time()},

    {'username': 'mary', 'text': 'Hi my friends !:)', 'time': time.time()},

    {'username': 'olga', 'text': 'Hi.', 'time': time.time()},

    {'username': 'petr', 'text': 'Hello all!', 'time': time.time()}

]

# глобальная переменная, в которую мы будем складывать все сообщения которые нам приходят, лист словарей
# или еще можно назвать лист диктов, каждый дикт содержит три ключа.

# БД пользователей - username: password

users = {
    'alex': '5885',
    'nikola': '4332',
    'mary': '46780',
    'olga': '123421',
    'petr': '000'

}

@app.route("/")  # главный локатор
def hello():  # вызываем функцию и возвращаем ее
    return "Hi, welcome to my messenger. I hope you are wondering here! :)"


@app.route("/status")  # обрабатывает функцию status как адрес(ссылку) на функцию представления нашего приложения.
def status():  # вызываем функцию и возвращаем ее
    return {'Status': True,
            'time': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'messages_quantity': len(messages),  # количество сообщений
            'users_quantity': len(users)  # количество пользователей
            }
    # либо можем использовать 'time': time.ctime()} #получаем актуальное время на сервере.
    # если использовать просто time, то время будет показываться в виде - float (секунды).
    # также можно использовать strftime ('') - для вольного написания формата времени и даты.


@app.route("/history")  # этот метод берет и отправляет наши сообщения наружу, так чтобы ими мог кто-то воспользоваться
def history():
    """
    request: ?after=12376867.88 #делаем фильтрацию истории, добавляем аргумент и будем передавать после этой отметки времени
    response: {"messages": [{"username": "str", "text:" "str", "time": float}, ...]}
    """
    after = float(request.args['after'])  # ImmutableMultiDict

    # filtered_messages = [] объявляем массив
    # for message in messages: цикл
    # if after < message['time']:
    # filtered_messages.append(message)
    # общий вывод, мы вместо того чтобы отправлять все сообщения, отправляем только часть,
    # мы в фильтр messages  кладем те сообщения, которые удовлетворяют нашему условию
    # т.е. мы берем очередное сообщение, мы смотрим время, сравниваем с after
    # таким образом в filtered_messages попадают только те сообщения, которые позже чем переданное нам время.

    # напишем тот же фильтр, только покороче
    filtered_messages = [message for message in messages if after < message['time']]
    return {'messages': filtered_messages}
    # таким образом у нас есть метод с помощью которого можно получить историю.


@app.route("/send", methods=['POST'])
# метод по отправке сообщений, мы указали фласк что это он обрабатывает пост запросы
# сделали это, указав специальный ключ, если бы этого не сделали получали бы 405 ошибку.
def send():
    """
        request: {"username": "str", "password": "str" "text:" "str"}
        response: {"ok": true}
    """
    data = request.json  # хранится словарь ({"username": "str", "text:" "str"})
    username = data['username']
    password = data['password']
    text = data['text']
    # если такой пользователь существует -> проверим пароль
    # иначе мы зарегистрируем его
    if username in users:  # есть ли такой юзер в нашем словарике
        real_password = users[username]
        if real_password != password:  # если реальный пароль равен правильному то код продолжится
            return {"ok": False}  # отказано в доступе
    else:
        users[username] = password
    new_message = {'username': username, 'text': text, 'time': time.time()}
    messages.append(new_message)
    return {"ok": True}


# затем в коде данного метода мы взяли, получили JSON который мы прислали в POST запросе -> dict (словарь)
# и из этого словаря мы достаем переменные, с этими данными мы сформировали новый словарь и добавляем его в наш массив
# в наш лист со всеми сообщениями, и потом он хранится со всеми сообщениями в листе (словаре) messages

if __name__ == '__main__':
    app.run()  # запуск

# То есть чтобы при запуске нашего приложения увидеть "Hello, World!", нам нужно обратится к функции hello,
# которая вернет нам эту строку, А функция вызывается с помощью указания ее имени как пути к странице приложения.

