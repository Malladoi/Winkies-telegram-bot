author = 'KSugonyakin'

import telebot
import logging



logger = telebot.logger
telebot.logger.setLevel(logging.ERROR) # Outputs debug messages to console.
bot = telebot.AsyncTeleBot("403603722:AAE8-VK-Ovnl6vOMnnJKpe7ToSCXq9zokgA")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    task = bot.reply_to(message, "Welcome to Winkie's restaurant on Sunset Blvd")
    # bot.reply_to(message, res)
    result = task.wait()
    print(result)

bot.polling(none_stop=True)