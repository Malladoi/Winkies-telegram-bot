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
    itembtn2 = types.KeyboardButton('Показать контактну информацию')
    itembtn3 = types.KeyboardButton('Связаться с менеджером')
    markup.add(itembtn1, itembtn2, itembtn3)
    # bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)
    task = bot.reply_to(message, "Привет, я бот mhelp.by!\nЧем я могу Вам помочь?", reply_markup=markup)
    result = task.wait()
    print(result)


@bot.message_handler(commands=['recreatedb'])
def send_welcome(message):
    if message.from_user.id == 403603722:
        task = bot.reply_to(message, databaseAPI.recreatedb(conn))
        # bot.reply_to(message, res)
        result = task.wait()
        print(result)


bot.polling(none_stop=True)
conn.close()
