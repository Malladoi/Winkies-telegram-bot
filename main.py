author = 'KSugonyakin'

import logging
import os
from urllib import parse

import psycopg2
import telebot

token = os.environ['TELEGRAM_TOKEN']
api_token = os.environ['SOME_API_TOKEN']

parse.uses_netloc.append("postgres")
heroku_db_url = parse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect(
    database=heroku_db_url.path[1:],
    user=heroku_db_url.username,
    password=heroku_db_url.password,
    host=heroku_db_url.hostname,
    port=heroku_db_url.port
)

cur = conn.cursor()
logger = telebot.logger
telebot.logger.setLevel(logging.CRITICAL)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        cur.execute("""select version()""")
        test = cur.fetchall()[1]
    except:
        test = "I can't SELECT from bar"
    # task = bot.reply_to(message, "Welcome to Winkie's restaurant on Sunset Blvd")
    task = bot.reply_to(message, test)
    # bot.reply_to(message, res)
    result = task.wait()
    print(result)

bot.polling(none_stop=True)