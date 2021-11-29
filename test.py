import telebot
from telebot import types

from config import telegram_token


import time



bot = telebot.TeleBot(telegram_token)

sp = ['пизда', 'залупа']


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(f'{sp[0]}', callback_data='cb_yes')
    markup.add(button1)
    bot.send_message(message.chat.id, f"{sp[0]}", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(f'{sp[1]}', callback_data='cb_no')
        markup.add(button1)

        bot.answer_callback_query(call.id, "Answer is Yes")

        bot.edit_message_text(f'{sp[1]}', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)


if __name__ == '__main__':
    print('strt')
    bot.infinity_polling()
#    pass
