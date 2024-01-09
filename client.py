import time
import requests
from requests.auth import HTTPBasicAuth


def steps_generator():
    """Переключение шагов"""
    data = (('get', 'catalog', 'checkauth', '', ''),
            ('get', 'catalog', 'init', '', ''),
            ('post', 'catalog', 'file', '12345.png', '12345.png'),
            ('post', 'catalog', 'file', 'import.xml', 'import.xml'),
            ('post', 'catalog', 'file', 'offers.xml', 'offers.xml'),
            ('get', 'catalog', 'import', 'import.xml', ''),
            ('get', 'catalog', 'import', 'offers.xml', ''),
            ('get', 'catalog', 'checkauth', '', ''),
            ('get', 'catalog', 'init', '', ''),
            ('post', 'catalog', 'file', '12345.png', '12345.png'),
            ('post', 'catalog', 'file', 'import.xml', 'import.xml'),
            ('post', 'catalog', 'file', 'offers.xml', 'offers.xml'),
            ('get', 'catalog', 'import', 'import.xml', ''),
            ('get', 'catalog', 'import', 'offers.xml', ''),
            )
    for step in data:
        yield step


class ClientTilda:
    """Отправление запросов"""
    def __init__(self):
        # Пароль, логин и адрес для доступа к Tilda
        self.username = '7362272'  # integration.login
        self.password = '27c0d9b73d45b69ba80eba9243b6b248'  # integration.password

        self.url = 'https://store.tilda.cc/connectors/commerceml/'  # integration.address
        # self.url = 'https://alexeytest.wskitapp.ru/store.tilda.cc/connectors/commerceml '  # integration.address
        # self.url = 'https://alexeytest.wskitapp.ru'  # integration.address
        # self.url = 'http://127.0.0.1:5000/store.tilda.cc/connectors/commerceml'  # integration.address

        self.session = requests.Session()
        self.headers = {
            'Host': 'store.tilda.cc',
            'User-Agent': '1C+Enterprise/8.2',
            'Content-Type': 'application/xml',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2'
        }

    def request(self, step, params=''):
        """Выполнение запроса"""
        # Формируем url с параметрами GET
        url = self.url + f'?type={step[1]}&mode={step[2]}'
        if step[3]:
            # 3 параметр имя файла который читать
            # 4 параметр как назвать файл при отправке
            if step[0] == 'get':
                url += f'&filename={step[3]}'
            else:
                url += f'&filename={step[4]}'

        # Создаем параметры запроса
        string = {'url': url}
        if params:
            string |= params

        stop = 3
        while True:
            # Отправляем запрос
            if step[0] == 'get':
                res = self.session.get(**string)
                print('GET запрос', url)
            else:
                if step[2] == 'file':
                    # Передача файла
                    # with open(step[3], 'r', encoding='utf-8') as f:
                    #     data = f.read()
                    with open(step[3], 'rb') as f:
                        data = f.read()

                    headers = {
                        'Host': 'store.tilda.cc',
                        'User-Agent': '1C+Enterprise/8.2',
                        'Content-Type': 'application/octet-stream',
                        'Connection': 'close',
                        'Content-Length': str(len(data)),
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache',
                        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2'
                    }
                    # {'Host': 'store.tilda.cc', 'Connection': 'close', 'Content-Length': '764156',
                    #  'User-Agent': '1C+Enterprise/8.2',
                    #  'Authorization': 'Basic NzM2MjI3MjoyN2MwZDliNzNkNDViNjliYTgwZWJhOTI0M2I2YjI0OA==',
                    #  'Cookie': 'PHPSESSID=s471gb021840l74jrr845amttm', 'Content-Type': 'application/octet-stream',
                    #  'Cache-Control': 'no-cache', 'Pragma': 'no-cache',
                    #  'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2'}
                    res = self.session.post(**string, data=data, headers=headers)
                    print('POST запрос', url)
                    print(headers)
                    print('Передача файла', step[3], f' ({step[4]})')
                else:
                    res = self.session.post(**string)
                    print('POST запрос', url)

            # Проверка ответа
            if res.status_code !=200:
                print(f'\nОтвет {res.status_code} --------------------------------------')
                print('Повтор запроса')
                print('--------------------------------------\n')
                stop -= 1
                if stop:
                    continue
                return res

            print(f'\nОтвет {res.status_code} --------------------------------------')
            print(res.text)
            print('--------------------------------------\n')
            return res

    def connect(self, step):
        """Подключение к Tilda"""
        # Проверка доступности Tilda
        return self.request(step, params={'auth': HTTPBasicAuth(self.username, self.password)})


# Выполняем запросы
step = steps_generator()
tilda = ClientTilda()

# Авторизация
print('Авторизация')
print('--------------------------------------')
res = tilda.connect(next(step))
if res.status_code == 200:
    s = res.text.split('\n')
    if s[0] != 'success':
        print('Ошибка соединения с Tilda')
        exit()

# Инициализация обмена
print('Инициализация обмена')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка инициализации обмена')
    exit()

# Отправка файла изображения
print('Отправка файла изображения')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка отправки файла')
    exit()

# Отправка файла import
print('Отправка файла import')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка отправки файла')
    exit()

# Отправка файла offers
print('Отправка файла offers')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка отправки файла')
    exit()

# Обработка файла import
send = next(step)
while True:
    # Обработка файла import
    print('Обработка файла import')
    print('--------------------------------------')
    res = tilda.request(send)
    if res.status_code != 200:
        print('Ошибка отправки файла')
        exit()
    if res.text == 'success':
        break

# Обработка файла offers
send = next(step)
while True:
    # Обработка файла import
    print('Обработка файла offers')
    print('--------------------------------------')
    res = tilda.request(send)
    if res.status_code != 200:
        print('Ошибка отправки файла')
        exit()
    if res.text == 'success':
        break


tilda = ClientTilda()
# Авторизация
print('Авторизация')
print('--------------------------------------')
res = tilda.connect(next(step))
if res.status_code == 200:
    s = res.text.split('\n')
    if s[0] != 'success':
        print('Ошибка соединения с Tilda')
        exit()

# Инициализация обмена
print('Инициализация обмена')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка инициализации обмена')
    exit()
# time.sleep(3)
# Отправка файла изображения
print('Отправка файла изображения')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка отправки файла')
    exit()

# Отправка файла import
print('Отправка файла import')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка отправки файла')
    exit()

# Отправка файла offers
print('Отправка файла offers')
print('--------------------------------------')
res = tilda.request(next(step))
if res.status_code != 200:
    print('Ошибка отправки файла')
    exit()

# Обработка файла import
send = next(step)
while True:
    # Обработка файла import
    print('Обработка файла import')
    print('--------------------------------------')
    res = tilda.request(send)
    if res.status_code != 200:
        print('Ошибка отправки файла')
        exit()
    if res.text == 'success':
        break

# Обработка файла offers
send = next(step)
while True:
    # Обработка файла import
    print('Обработка файла offers')
    print('--------------------------------------')
    res = tilda.request(send)
    if res.status_code != 200:
        print('Ошибка отправки файла')
        exit()
    if res.text == 'success':
        break
