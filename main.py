import sqlite3
import logging
import telebot
from telebot import types
from telebot.types import LabeledPrice

from config.config import TOKEN
from db.db import *
from commands.commands import *
from callback.callback import *

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

bot = telebot.TeleBot(TOKEN)

commands_list = ["Настройки профиля", "Гороскоп на сегодня", "", ""]
zodiak_list = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева", "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
markup_zodiak = types.InlineKeyboardMarkup(row_width = 3)
button_array = []
for zodiak in zodiak_list:
    button_array.append(types.InlineKeyboardButton( text=zodiak, callback_data="zodiak_"+str(zodiak_list.index(zodiak))))
markup_zodiak.add(*button_array)

#first checkup
try: 
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()
        cursor.execute(f"""CREATE TABLE "Users" (`Id` INTEGER NOT NULL, `Username` TEXT NOT NULL, `CountCard` INTEGER NOT NULL, `Subscription` BOOLEAN, `TypeAstrolog` TEXT NOT NULL, Zodiak TEXT, Rolename TEXT)""")
        db.commit()
    db.close()
    logging.warning("New DB created!")
    print("New DB created!")
except: 
    print("DB created yet!")
    logging.info("DB created yet!")


#In commands/commands.py
@bot.message_handler(commands=['ping'])
def ping_message(message):
    bot.send_message(message.chat.id,"Pong🏓")

@bot.message_handler(commands=['start'])
def start_message(message):
    send_start_message(message, bot)

@bot.message_handler(commands=['admin'])
def admin_message(message):
    send_admin_message(message, bot)

@bot.message_handler(func=lambda message : message.text =="Гороскоп на сегодня")
def goroskop_message(message):
    send_today_goroskop(message, bot)

@bot.message_handler(func=lambda message : message.text =="Настройки профиля")
def profile_generate(message):
        send_profile(message, bot)


#@bot.message_handler(content_types=['text'])
#def ai_generate(message):
#  if (not message.text in commands_list) and (message.chat.id > 0):
#    bot.send_message(message.chat.id, "Ожидайте ответ свыше...")

#in callback factory
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    if str(call.data).startswith("zodiak_"):
        callback_zodiak(call, bot)  

    if str(call.data).startswith("goroskop"):
        callback_goroskop(call, bot)

    if str(call.data).startswith("admin_zero_claimed"):
       callback_admin_zero_claimed(call, bot)

    if str(call.data).startswith("admin_everyday"):
        callback_admin_everyday(call, bot)

    if str(call.data).startswith("change_tarolog"):
        callback_change_tarolog(call, bot)
    
    if str(call.data).startswith("change_name"):
        callback_change_name(call, bot)



if __name__ == '__main__':
    logging.warning("Bot started")
    bot.infinity_polling()