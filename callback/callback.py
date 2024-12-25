import sqlite3
import json
import io

from telebot import types
from telebot.util import antiflood
with io.open('config/lang-ru-0.json', encoding='utf-8') as file:
    config_lang = json.load(file)

zodiak_list = []
for i in range (12):
    zodiak_list.append(config_lang[str(i)])

astrolog_list=[]
for i in range (3):
    astrolog_list.append(config_lang["astrolog"+str(i)])


#change zodiak
def callback_zodiak(call, bot):
    number = int(str(call.data).split("_")[1])
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()
        cursor.execute(f""" UPDATE Users set Zodiak = '{number}' WHERE Id = {call.from_user.id}""")
        db.commit()   
    db.close()
    bot.answer_callback_query(call.id, config_lang["message_change_zodiak"]+zodiak_list[number])
    return


#Claim goroskop card
def callback_goroskop(call, bot):
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()
        cursor.execute(f""" SELECT Claimed FROM Users WHERE Id = {call.from_user.id}""")
        claimed = cursor.fetchall()
        if claimed[0][0]=='false':
            cursor.execute(f""" UPDATE Users SET Claimed = 'true' WHERE Id = {call.from_user.id}""")
            cursor.execute(f""" SELECT CountCard FROM Users WHERE Id = {call.from_user.id}""")
            CountCard = cursor.fetchall()
            CountCard = int(CountCard[0][0])+2
            cursor.execute(f""" UPDATE Users SET CountCard = '{CountCard}' WHERE Id = {call.from_user.id}""")
            bot.answer_callback_query(call.id, config_lang["message_claimed_card"])
        else:
            bot.answer_callback_query(call.id, config_lang["message_already_claimed_card"])
    db.close()
    bot.answer_callback_query(call.id, "")
    return


#Claimed for all users = false
def callback_admin_zero_claimed(call, bot):
    with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
            cursor.execute(f""" UPDATE Users SET Claimed = 'false'""")
    db.close()
    bot.answer_callback_query(call.id, config_lang["test_sussesful"])
    return

#Groupe Message
def callback_admin_everyday(call, bot):
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()
        cursor.execute(f""" SELECT Id FROM Users""")
        i = 0
        for result in cursor:
            i+=1
            antiflood(bot.send_message, result[0], config_lang["test_message_1"])
    db.close()
    bot.answer_callback_query(call.id, "Успешно. Отправлено "+str(i)+" сообщений ", show_alert=True)
    return

def callback_change_name(call, bot):
    bot.answer_callback_query(call.id, config_lang["test_cooming_soon"])

def callback_change_tarolog(call, bot):
    try: 
        new_tarolog = int(str(call.data).split("_")[2])
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""UPDATE Users SET TypeAstrolog = '{new_tarolog}' WHERE Id = {call.from_user.id}""")
            bot.answer_callback_query(call.id, config_lang["message_your_new_tarolog"]+astrolog_list[new_tarolog])
            bot.delete_message(message_id=call.message.id, chat_id =call.message.chat.id)
    except:
        markup = types.InlineKeyboardMarkup(row_width = 1)
        markup.add(types.InlineKeyboardButton(text=astrolog_list[0], callback_data="change_tarolog_0"))
        markup.add(types.InlineKeyboardButton(text=astrolog_list[1], callback_data="change_tarolog_1"))
        markup.add(types.InlineKeyboardButton(text=astrolog_list[2], callback_data="change_tarolog_2"))
        bot.edit_message_text(message_id=call.message.id, chat_id =call.message.chat.id, text=config_lang["message_choose_tarolog"], reply_markup = markup)

def callback_change_sub(call, bot):
    with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT Subscription FROM Users WHERE Id = {call.from_user.id}""")
            is_sub = cursor.fetchall()[0][0]
            if(is_sub==0):
                cursor.execute(f"""UPDATE Users SET Subscription = '{1}' WHERE Id = {call.from_user.id}""")
                bot.answer_callback_query(call.id, config_lang["alert_now_you_sub"])
            else:
                cursor.execute(f"""UPDATE Users SET Subscription = {0} WHERE Id = {call.from_user.id}""")
                bot.answer_callback_query(call.id, config_lang["alert_now_you_dont_sub"])
