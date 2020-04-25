# он будет бесконечно запрашивать историю  и выводить ее в консоль
from datetime import datetime
from time import sleep

import requests

# {
#     "messages": [
#         {"username": "str", "text": "str", "time": float},
#         ...
#     ]
# }

# У нас должна быть переменная, которая будет хранить дату последнего полученного сообщения
last_message_time = 0
while True:
    response = requests.get('http://127.0.0.1:5000/history?after=12376867.88')
    params = {'after': last_message_time}
    # параметр, сюда нам нужно передавать дату последнего мообщения, которое у нас уже имеется (подгрузили)
    # чтобы нам передали только те сообщения, у которых дата больше чем наше сообщение
    data = response.json()
    for message in data['messages']:
        # float => datetime
        norm_time = datetime.fromtimestamp(message['time'])
        norm_time = norm_time.strftime('%Y/%m/%d %H:%M:%S')
        print(norm_time, message['username'])
        print(message['text'])
        print()
        last_message_time = message['time']

    sleep(1)
