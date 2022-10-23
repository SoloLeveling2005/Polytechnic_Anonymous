import time
import os
import re
from random import randint
import telebot
from telebot import types  # кнопки Telegram
import datetime
import threading
import sqlite3 as sql
from connect import bot





def main_menu_assistant(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    find = types.KeyboardButton('🔎Поиск собеседника')
    markup.add(find)
    bot.send_message(message,
                     f"🏠Главное меню",
                     parse_mode='HTML', reply_markup=markup)


def insert_user_into_db_request_thread(message):
    applications_thread = threading.Thread(target=insert_user_into_db_request, args=(message,))
    applications_thread.daemon = True
    applications_thread.start()


def insert_user_into_db_request(message):
    print("запустился скрипт с добавлением пользователей")
    user_id = message.chat.id
    with sql.connect('todo.db') as con:
        cur = con.cursor()
        cur.execute(f"""
                      SELECT * FROM requests WHERE id_user = {user_id};
                      """)
        request_user = cur.fetchall()
        if request_user is None or request_user == []:
            cur.execute(f"""
                                  SELECT * FROM connections WHERE first = {user_id};
                                  """)
            connections_user = cur.fetchall()
            if connections_user is None or request_user == []:
                cur.execute(f"""
                                INSERT INTO requests (id_user) VALUES({user_id})
                            """)
                print("данные добавлены")
                find_anonymous_thread(message)
                return

            else:
                bot.send_message(message.chat.id,
                                 f"Поиск уже начался, пожалуйста подождите",
                                 parse_mode='HTML')
                return
        else:
            bot.send_message(message.chat.id,
                             f"Поиск уже начался, пожалуйста подождите",
                             parse_mode='HTML')
            return


def find_anonymous_thread(message):
    applications_thread = threading.Thread(target=find_anonymous, args=(message,))
    applications_thread.daemon = True
    applications_thread.start()


def find_anonymous(message):
    while True:

        user_id = message.chat.id
        with sql.connect('todo.db') as con:
            cur = con.cursor()
            cur.execute(f"""
                              SELECT * FROM connections WHERE first = {user_id};
                              """)
            request_user1 = cur.fetchall()
            cur.execute(f"""
                                          SELECT * FROM connections WHERE second = {user_id};
                                          """)
            request_user2 = cur.fetchall()
            if request_user1 is None or request_user1 == []:
                time.sleep(2)
            else:
                you = user_id
                # you = request_user1[0][1]
                # your_partner = request_user[0][2]
                try:
                    if you == request_user1[0][1]:
                        your_partner = request_user1[0][2]
                    else:
                        your_partner = request_user1[0][1]
                except:
                    if you == request_user2[0][1]:
                        your_partner = request_user2[0][2]
                    else:
                        your_partner = request_user2[0][1]

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                find = types.KeyboardButton('🛑Отключиться')
                markup.add(find)
                bot.send_message(you,
                                 f"Нашел, ваш собеседник онлайн.",
                                 parse_mode='HTML', reply_markup=markup)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                find = types.KeyboardButton('🛑Отключиться')
                markup.add(find)
                bot.send_message(your_partner,
                                 f"Нашел, ваш собеседник онлайн.",
                                 parse_mode='HTML', reply_markup=markup)

                return


def cancel_find_thread(message):
    applications_thread = threading.Thread(target=cancel_find, args=(message,))
    applications_thread.daemon = True
    applications_thread.start()


def cancel_find(message):
    user_id = message.chat.id
    with sql.connect('todo.db') as con:
        cur = con.cursor()
        cur.execute(f"""
                          SELECT * FROM requests WHERE id_user = {user_id};
                          """)
        request_user = cur.fetchall()
        if request_user is None or request_user == []:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            find = types.KeyboardButton('🔎Поиск собеседника')
            markup.add(find)
            bot.send_message(message.chat.id,
                             f"Вы не заускали поиск собеседника",
                             parse_mode='HTML', reply_markup=markup)
        else:
            with sql.connect('todo.db') as con:
                cur = con.cursor()
                cur.execute(f"""
                              DELETE FROM requests WHERE id_user = {user_id};
                              """)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            find = types.KeyboardButton('🔎Поиск собеседника')
            markup.add(find)
            bot.send_message(message.chat.id,
                             f"Поиск отменен",
                             parse_mode='HTML', reply_markup=markup)
            main_menu_assistant(message)


def disconnect_chat_thread(message):
    applications_thread = threading.Thread(target=disconnect_chat, args=(message,))
    applications_thread.daemon = True
    applications_thread.start()




def disconnect_chat(message):
    user_id = message.chat.id
    with sql.connect('todo.db') as con:
        cur = con.cursor()


        cur.execute(f"""
                                      SELECT * FROM connections WHERE first = {user_id};
                                      """)
        request_user1 = cur.fetchall()
        cur.execute(f"""
                                                  SELECT * FROM connections WHERE second = {user_id};
                                                  """)
        request_user2 = cur.fetchall()

        if (request_user1 is None or request_user1 == []) and (request_user2 is None or request_user2 == []):
            pass
        else:
            you = user_id
            # you = request_user1[0][1]
            # your_partner = request_user[0][2]
            try:
                if you == request_user1[0][1]:
                    your_partner = request_user1[0][2]
                else:
                    your_partner = request_user1[0][1]
            except:
                if you == request_user2[0][1]:
                    your_partner = request_user2[0][2]
                else:
                    your_partner = request_user2[0][1]

            def dell(user_id_, you_, your_partner_):
                first = you_
                second = your_partner_
                try:
                    cur.execute(f"""
                                DELETE FROM connections WHERE first = {user_id_};
                             """)
                    cur.execute(f"""
                                    DELETE FROM connections WHERE second = {user_id_};
                                """)
                except:
                    cur.execute(f"""
                                 DELETE FROM connections WHERE second = {user_id_};
                             """)
                    cur.execute(f"""
                                DELETE FROM connections WHERE first = {user_id_};
                            """)
                bot.send_message(first,
                                 "Вы отключились от чата")
                main_menu_assistant(first)
                bot.send_message(second,
                                 "Ваш собеседник вышел из чата")
                main_menu_assistant(second)

            cur = con.cursor()
            cur.execute(f"""
                               SELECT * FROM connections WHERE first = {user_id};
                            """)
            request_user = cur.fetchall()
            if request_user1 is None or request_user1 == []:
                if request_user2 is None or request_user2 == []:
                    bot.send_message(message.chat.id,
                                     "Вы не заускали поиск собеседника")
                else:
                    dell(user_id, you, your_partner)
            else:
                dell(user_id, you, your_partner)
