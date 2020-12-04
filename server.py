import os
from dotenv import load_dotenv
from flask import Flask
from pymemcache.client.base import Client

load_dotenv()

app = Flask(__name__)

cache_host = os.getenv('MEMCACHED_HOST')
client = Client(cache_host)


def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@app.route('/', methods=['GET'])
def index():
    return 'Добавьте в GET запрос номер k-го числа Фиббоначи, которое хотите вычислить.'


@app.route('/<int:n>', methods=['GET'])
def get_fib(n):
    result = client.get(f'{n}')
    if not result:
        result = fibonacci(n)
        client.set(f'{n}', result)
        return 'Вычислено при помощи функции: ' + f' {result} '
    return 'Взято из кэша: ' + f' {result} '


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8081)
