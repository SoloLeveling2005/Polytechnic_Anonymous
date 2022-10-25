import time
import os
import re
from random import randint
import telebot
from telebot import types  # кнопки Telegram
import datetime
import threading
import sqlite3 as sql



# Мои подключения
from connect import bot
from create_db import create_db
from check_new_request import application_threading
from scripts_assistant import insert_user_into_db_request_thread, cancel_find_thread, disconnect_chat_thread, \
    find_anonymous_thread,message_processing

print("Нажмите Ctrl+C если хотите завершить работу бота")

create_db()
application_threading()


def select_all_connections():
    with sql.connect('todo.db') as con:
        cur = con.cursor()
        cur.execute(f"""
                      SELECT * FROM connections;
                      """)
        data_users = cur.fetchall()
    return data_users


@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message)


# @bot.message_handler(commands=['help'])
# def help(message):
#     bot.send_message(message.chat.id,
#                      "Доступные команды:")
#     bot.send_message(message.chat.id,
#                      "/main_menu " + "- перейти в главное меню")
#     bot.send_message(message.chat.id,
#                      "/find " + "- поиск анонимуса")
#     bot.send_message(message.chat.id,
#                      "/cancel " + "- отмена поиска")
#     bot.send_message(message.chat.id,
#                      "/disconnect " + "- отсоединиться от чата")
#     bot.send_message(message.chat.id,
#                      "Вам не обязательно их вводить, они будут доступны в виде кнопок ниже")
#
#


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    find = types.KeyboardButton('🔎Поиск собеседника')
    markup.add(find)
    bot.send_message(message.chat.id,
                     f"🏠Главное меню",
                     parse_mode='HTML', reply_markup=markup)


def find_anonymous(message):
    insert_user_into_db_request_thread(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    find = types.KeyboardButton('❌Отмена поиска')
    markup.add(find)
    bot.send_message(message.chat.id,
                     f"🔎Начинаю поиск...",
                     parse_mode='HTML', reply_markup=markup)


def command_cancel_find(message):
    cancel_find_thread(message)

def command_disconnect(message):
    disconnect_chat_thread(message)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '🏠Главное меню':
        main_menu(message)
    elif message.text == '❌Отмена поиска':
        command_cancel_find(message)
    elif message.text == '🛑Отключиться':
        command_disconnect(message)
    elif message.text == '🔎Поиск собеседника':
        find_anonymous(message)
    else:
        message_processing(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
    while True:
        try:
            bot.polling(none_stop=True)
            time.sleep(1)
        except Exception as e:
            time.sleep(3)
            a = datetime.datetime.today()
            print(e)
            print(a)
            bot = telebot.TeleBot('5488566542:AAEGQsiDrnLjwFCQb4kmbn7EJYnZqoaIfxk')
            bot.send_message(1303257033,
                             'Сообщение системы: Произошла перезагрузка программы')
            os.system('python main.py')
