import json
import io

from modules.ai import *
from db.db import *
from telebot import types

with io.open('config/lang-ru-0.json', encoding='utf-8') as file:
    config_lang = json.load(file)

zodiak_list = []
for i in range (12):
    zodiak_list.append(config_lang[str(i)])

markup_zodiak = types.InlineKeyboardMarkup(row_width = 3)
button_array = []
for zodiak in zodiak_list:
    button_array.append(types.InlineKeyboardButton( text=zodiak, callback_data="zodiak_"+str(zodiak_list.index(zodiak))))
markup_zodiak.add(*button_array)


#ADMIN COMMAND LIST
def send_admin_message(message, bot):
    user = get_user_from_db(message.from_user.id)
    if(user[0][6] == "admin"):
        markup = types.InlineKeyboardMarkup(row_width = 1)
        markup.add(types.InlineKeyboardButton(text="Ежедневная рассылка", callback_data="admin_everyday"))
        markup.add(types.InlineKeyboardButton(text="Обнуление Claimed", callback_data="admin_zero_claimed"))
        bot.send_message(message.chat.id, "Hello! "+str(user), reply_markup=markup)
    else:
        bot.send_message(message.chat.id, config_lang["error_no_admin"])


#TODAY GOROSKOP
def send_today_goroskop(message, bot):
        bot.send_message(message.chat.id, config_lang["message_waiting1"])
        user = get_user_from_db(message.from_user.id)[0]
        answer = generate_goroskope(astrolog_type=user[4], zodiak=user[5])
        markup = types.InlineKeyboardMarkup(row_width = 1)
        markup.add(types.InlineKeyboardButton(text=config_lang["button_claim_card"], callback_data="goroskop"))
        bot.edit_message_text(message_id=message.id+1, chat_id =message.chat.id, text=config_lang["message_your_goroskop"]+answer, reply_markup = markup)


#SEND PROFILE
def send_profile(message, bot):
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
            cursor.execute(f""" SELECT * FROM Users WHERE Id = {message.from_user.id}""")
            user = cursor.fetchall()
        db.close()
        markup = types.InlineKeyboardMarkup(row_width = 1)
        markup.add(types.InlineKeyboardButton(text=config_lang["button_change_name"], callback_data="change_name"))
        markup.add(types.InlineKeyboardButton(text=config_lang["button_change_tarolog"], callback_data="change_tarolog"))
        markup.add(types.InlineKeyboardButton(text=config_lang["button_change_sub"], callback_data="change_sub"))
        markup.add(types.InlineKeyboardButton(text=config_lang["button_change_zodiak"], callback_data="change_zodiak"))
        #bot.delete_message(message_id=message.id, chat_id =message.chat.id)
        bot.send_message(message.chat.id, 
                         f"Ваш профиль: \n Имя: {user[0][1]} \n Количество каточек: {user[0][2]} \n Знак зодиака: {config_lang[str(user[0][5])]} \n Персональный астролог: {config_lang["astrolog"+str(user[0][4])]}",
                         reply_markup = markup)


#START MESSAGE
def send_start_message(message, bot):
    insert_user_into_db(message)
    bot.send_message(message.chat.id, config_lang["start_message_1"], reply_markup=markup_zodiak)
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton(config_lang["button_today_goroskop"])
    item2=types.KeyboardButton(config_lang["button_profile_settings"])
    markup.add(item1, item2)
    bot.send_message(message.chat.id, config_lang["start_message_2"], reply_markup=markup)


#CHANGE