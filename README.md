# Телеграм-бот для отслеживания курса валют.
## Предварительные требования:
#### Python 3 должен быть установлен на сервере.
#### Pip должен быть установлен на сервере.
## Установка:
#### Клонирование репозитория.
`git clone https://github.com/gazone-gazelle17/crypto_testcase`

`cd crypto_testcase`
#### Активация виртуального окружения.
`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`
#### Настройка переменных окружения.
В файле .env введите переменные TELEGRAM_TOKEN, CHAT_ID и COINMARKET_TOKEN.
#### Запуск скрипта.
`python crypto_testcase.py`
## Работа бота:
#### Начало работы.
Отправьте боту команду `/start`.
#### Установка алертов.
Используйте команду вида `/set <symbol> <min_price> <max_price>`, например: `/set EUR 5 100`
#### Мониторинг.
Работает атоматически.

