author = 'KSugonyakin'

import psycopg2
import logging
import os
import telebot
import databaseAPI
from telebot import types
from urllib import parse

parse.uses_netloc.append("postgres")
heroku_db_url = parse.urlparse(os.environ['DATABASE_URL'])
conn = psycopg2.connect(
    database=heroku_db_url.path[1:],
    user=heroku_db_url.username,
    password=heroku_db_url.password,
    host=heroku_db_url.hostname,
    port=heroku_db_url.port
)

token = os.environ['TELEGRAM_TOKEN']
api_token = os.environ['SOME_API_TOKEN']
logger = telebot.logger
telebot.logger.setLevel(logging.CRITICAL)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Помочь с ремонтом')
    itembtn2 = types.KeyboardButton('Показать контактную информацию')
    itembtn3 = types.KeyboardButton('Связаться с менеджером')
    markup.add(itembtn1, itembtn2, itembtn3)
    # bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
    task = bot.reply_to(message, "Привет, я бот mhelp.by!\nЧем я могу Вам помочь?", reply_markup=markup)
    result = task.wait()
    print(result)


@bot.message_handler(commands=['Показать контактную информацию'])
def send_welcome(message):
    task = bot.reply_to(message, 'mhelp.by\n' +
                        'Мы работаем с 9:00 до 21:00\n' +
                        'По адресу ул. Я. Коласа 45/2\n'+
                        'Контактные телефоны:\n' +
                        '+375259002722\n' +
                        '+375297888893\n' +
                        '+375444811718\n')

    # bot.reply_to(message, res)
    result = task.wait()
    bot.send_location(message.chat.id, 53.9290485, 27.5958024)
    print(result)


@bot.message_handler(commands=['recreatedb'])
def send_welcome(message):
    if message.from_user.id == 333521:
        task = bot.reply_to(message, databaseAPI.recreatedb(conn))
        # bot.reply_to(message, res)
        result = task.wait()
        print(result)


# Handles all messages for which the lambda returns True
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain')
def handle_text_doc(message):
    task = bot.reply_to(message, 'Я такое не умею(')
    result = task.wait()
    print(result)


bot.polling(none_stop=True)
conn.close()
