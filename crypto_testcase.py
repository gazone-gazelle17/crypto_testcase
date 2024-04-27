import os
from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
COINMARKET_TOKEN = os.getenv('COINMARKET_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(bot=bot)
dispatcher = updater.dispatcher

crypto_settings = {}


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Привет!'
        'Отправь мне /set <symbol> <min_price> <max_price>'
        'чтобы установить алерт.'
        )


def set_alert(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    try:
        symbol = context.args[0].upper()
        min_price = float(context.args[1])
        max_price = float(context.args[2])
        crypto_settings[chat_id] = (symbol, min_price, max_price)
        update.message.reply_text(
            f"""
            Алерт установлен для {symbol} при цене
            меньше ${min_price} и больше ${max_price}.
            """
            )
    except (IndexError, ValueError):
        update.message.reply_text(
            'Используйте формат: /set <symbol> <min_price> <max_price>'
            )


def get_crypto_price(symbol, api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    parameters = {'symbol': symbol, 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    price = data['data'][symbol]['quote']['USD']['price']
    return price


def monitor_prices(context: CallbackContext):
    api_key = COINMARKET_TOKEN
    for chat_id, settings in crypto_settings.items():
        symbol, min_price, max_price = settings
        current_price = get_crypto_price(symbol, api_key)
        if current_price <= min_price or current_price >= max_price:
            bot.send_message(
                chat_id=chat_id,
                text=f'Цена {symbol} достигла ${current_price}!'
                )


start_handler = CommandHandler('start', start)
set_alert_handler = CommandHandler('set', set_alert)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(set_alert_handler)

job_queue = updater.job_queue
job_queue.run_repeating(monitor_prices, interval=300, first=0)

updater.start_polling()
updater.idle()
