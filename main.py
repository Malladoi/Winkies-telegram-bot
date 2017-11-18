author = 'KSugonyakin'

import logging
import os

import telebot

token = os.environ['TELEGRAM_TOKEN']
api_token = os.environ['SOME_API_TOKEN']

logger = telebot.logger
telebot.logger.setLevel(logging.CRITICAL)  # Outputs debug messages to console.
bot = telebot.AsyncTeleBot(token + ":" + api_token)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    task = bot.reply_to(message, "Welcome to Winkie's restaurant on Sunset Blvd")
    # bot.reply_to(message, res)
    result = task.wait()
    print(result)

bot.polling(none_stop=True)