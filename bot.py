from decouple import config
from telebot import types

import telebot

from database import Database


db = Database('db.db')
bot = telebot.TeleBot(config('API_KEY'))
search_for_interlocutor_text = 'Adam axtar 🔎'



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(search_for_interlocutor_text)
    markup.add(item1)
    
    # Adding user's id to db
    db.add_user_id_to_db(message.chat.id)
    
    bot.send_message(message.chat.id, f'Salam, {message.from_user.first_name}. Adam axtarmaq üçün { search_for_interlocutor_text }   düyməsinə bas.', reply_markup=markup)
    
@bot.message_handler(commands=['special_mailing'])
def mailing(message):
    if message.chat.id == config('ADMIN_ID', cast=int):
        user_ids = db.get_all_user_ids()
        for user_id in user_ids:
            bot.send_message(user_id, ' '.join(message.text.split(' ')[1:]))
    else:
        bot.send_message(message.chat.id, 'You are not allowed here!!')
        

@bot.message_handler(commands=['count'])
def counting(message):
    if message.chat.id == config('ADMIN_ID', cast=int):
        num_of_users = db.count_users()
        bot.send_message(message.chat.id, num_of_users)
    else:
        bot.send_message(message.chat.id, 'You are not allowed here!!')
    
    
@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if chat_info != False:
        db.delete_chat(chat_info[0])
        item1 = types.KeyboardButton(search_for_interlocutor_text)
        markup.add(item1)

        bot.send_message(chat_info[1], 'User çatdan ayrıldı 😔', reply_markup=markup)
        bot.send_message(message.chat.id, 'Sən çatdan ayrıldın!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Aktiv user yoxdur, gözlə', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == search_for_interlocutor_text:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Axtarışı diyandır')
            markup.add(item1)
            
            chat_two = db.get_chat(message.chat.id)  # getting interlocutor's id if exists in queue, excluding current user

            # If there's no active user in queue just add in queue
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id, 'Adam axtarılır...', reply_markup=markup)
            else:                
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('/stop')
                markup.add(item1)
                bot.send_message(message.chat.id, 'User tapıldı! Nəsə yaz. Ayrılmaq üçün /stop bas', reply_markup=markup)
                bot.send_message(chat_two, 'User tapıldı! Nəsə yaz. Ayrılmaq üçün /stop bas', reply_markup=markup)
            
        elif message.text == 'Axtarışı diyandır':
            # Adding markup
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton(search_for_interlocutor_text)
            markup.add(item1)
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, 'Axtarış diyandırıldı', reply_markup=markup)

        
        else:
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)

        
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
