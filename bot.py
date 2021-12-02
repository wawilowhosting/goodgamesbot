import os
from flask import Flask, request

#I deleted an irrelevant code here for the question ...
server = Flask(__name__)


# pip3 install pytelegrambotapi --upgrade
#

# token
from config import telegram_token
# bot answers


# button 1
from config import start_button_name, start_message, reset_button_name
# button 2
from config import support_button_name, support_message
# button 3
from config import write_admin_button_name, write_admin_message
# button 4
from config import work_in_progress_button_name, work_in_progress_message
# button 5
from config import market_button_name, market_message
# button 6
from config import choose_tournament_time_button_name, choose_tournament_time_message
# button 7
from config import choose_tournament_slot_button_name, choose_tournament_slot_message
# button 8
from config import set_discord_nick_button_name, set_discord_nick_message
# button 9
from config import confirm_discord_button_name, confirm_discord_message,\
    confirm_discord_message_button_one, confirm_discord_message_button_two
# button 10
from config import payment_button_name, payment_message

from datetime import datetime as dt
import time

import telebot
from telebot import types


import flask
app = flask.Flask(__name__)


import os
PORT = int(os.environ.get('PORT', 5000))


bot = telebot.TeleBot(telegram_token, threaded=False)
slots_time = ["13:00", "15:00"]
free_slot = ['1', '2', '23', '24']

# -
# main commands


@bot.message_handler(commands=['go', f'{start_button_name}'])
@bot.message_handler(func=lambda msg: msg.text == 'start')
def start(message):
    print(f"""start message from '{message.from_user.username}' -- {str(dt.now())[:-7]}""")

    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(f"support")
    item2 = types.KeyboardButton(f"buy slots")
    item3 = types.KeyboardButton(f"feedback")

    markup.row(item1, item2)
    markup.row(item3)

    bot.send_message(message.chat.id, f'{start_message}', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'support')
def support(message):
    print(f"""support message from '{message.from_user.username}' -- {str(dt.now())[:-7]}""")

    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(f'{"Регламент"}', callback_data='regulation')
    button2 = types.InlineKeyboardButton(f'{"Как попасть на практические игры"}',
                                         callback_data='how to get to the practical tournament')

    markup.row(button1)
    markup.row(button2)

    bot.send_message(message.chat.id, f'{support_message}', reply_markup=markup)


@bot.message_handler(commands=[f'feedback'])
@bot.message_handler(func=lambda msg: msg.text == 'feedback')
def feedback(message):
    print(f"""feedback message from '{message.from_user.username}' -- {str(dt.now())[:-7]}""")

    bot.send_message(message.chat.id, 'Вы обратились в поддержку...')
    bot.send_message(message.chat.id, """Написать разработчикам\nЗдесь вы можете написать сообщение создателям бота, задать свой вопрос, предложить идею или сообщить об ошибке.""")
    bot.register_next_step_handler(message, save_feedback)


@bot.message_handler(commands=[f'buy_slot'])
@bot.message_handler(func=lambda msg: msg.text == 'buy slots')
def buy_slot(message):
    print(f"""buy slot message from '{message.from_user.username}' -- {str(dt.now())[:-7]}""")

    markup = types.InlineKeyboardMarkup()

    for i in slots_time:
        button1 = types.InlineKeyboardButton(f'{i}', callback_data=f'slot_buy@{i}')
        markup.row(button1)

    bot.send_message(message.chat.id, f'{support_message}', reply_markup=markup)

    # bot.send_message(message.chat.id, 'функция пока что не готова и находится в процессе разработки')


# -
# here will be message buttons function

@bot.callback_query_handler(func=lambda call: call.data == "regulation")
def regulation_query(call):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(f'Назад', callback_data='back_to_support')
    markup.add(button1)

    bot.answer_callback_query(call.id, "loading")

    bot.edit_message_text(f'Тут будет регламент, возможно ветка будет расширятся далее',
                          chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "how to get to the practical tournament")
def how_to_get_to_the_practical_tournament_query(call):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(f'Назад', callback_data='back_to_support')
    markup.add(button1)

    bot.answer_callback_query(call.id, "loading")

    bot.edit_message_text(f'Разказ о том как попасть на практические игры, тут можно даже прикрепить красивую картинку',
                          chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split('@')[0] == 'slot_buy')
def save_tournament_time(call):
    print(f"""Покупают слот на {call.data.split('@')[-1]}""")
    bot.answer_callback_query(call.id, "loading")

    markup = types.InlineKeyboardMarkup()
    for i in free_slot:
        button1 = types.InlineKeyboardButton(f'Слот номер {i}', callback_data=f'choose_slot@{i}')
        markup.add(button1)

    bot.edit_message_text(f'Выбери свободный слот',
                          chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.split('@')[0] == 'choose_slot')
def save_tournament_slot(call):
    print(f"""Покупают слот номер {call.data.split('@')[-1]}""")
    bot.answer_callback_query(call.id, "loading")



    bot.edit_message_text(f'Пришли ссылку на свой дискорд аккаунт',
                          chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.register_next_step_handler(call.message, set_discord_account)


# -
# here will be next step function
def save_feedback(message):
    print(f"""Там в поддержку обратились\n\n{message.text}""")
    bot.send_message(message.chat.id, 'Сообщение будет отправлено администрации, мы вам перезвоним!')


def set_discord_account(message):
    print(f"""дискорд аккаунт {message.text}""")

    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(f'Оплата киви', url='https://qna.habr.com/q/746129')
    button2 = types.InlineKeyboardButton(f'Оплата тинькофф', url='https://www.tinkoff.ru/business/open-api/')
    markup.add(button1, button2)


    bot.send_message(message.chat.id, f'Оплата сбербанком или киви', reply_markup=markup)

    bot.send_message(message.chat.id, '\nОплату пока что не допелил')


# -
# here will be function to come back


@bot.callback_query_handler(func=lambda call: call.data == "back_to_support")
def back_to_support_query(call):
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(f'{"Регламент"}', callback_data='regulation')
    button2 = types.InlineKeyboardButton(f'{"Как попасть на практические игры"}',
                                         callback_data='how to get to the practical tournament')

    markup.row(button1)
    markup.row(button2)

    bot.edit_message_text(f'{support_message}',
                          chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



# app
@server.route("/")
def webhook():

    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))

    bot.process_new_updates([update])
    return "ok", 200, update


def main():
    bot.remove_webhook()

    bot.set_webhook(url='https://goodgamesbot.herokuapp.com/' + telegram_token)


if __name__ == "__main__":
    while True:
        try:
            server.run()
        except ConnectionError as e:
            print('Ошибка соединения: ', e)
        except Exception as r:
            print("Непридвиденная ошибка: ", r)
        finally:
            print("Здесь всё закончилось")
