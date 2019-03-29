# -*- coding: utf-8 -*-

import telebot

file = open('./config.txt',mode='r')
TOKEN = file.read()
file.close()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id , 'Привет, хочешь узнать расписание?')

@bot.message_handler(commands='group')
def group_handler(message):
    msg = bot.send_message(message.chat.id , 'Какой номер группы?')
    bot.register_next_step_handler(msg, find_sch_group)

def find_sch_group(message):
    chat_id = message.chat.id
    text = message.text
    if not (len(text) == 6 or text.isdigit() == True):
        msg = bot.send_message(chat_id, 'Номер группы должен состоять из 6 цифр, введи ещё раз.')
        bot.register_next_step_handler(msg, find_sch_group)
        return
    bot.send_message(chat_id,'Здесь будет расписание группы '+text)

@bot.message_handler(commands='master')
def master_handler(message):
    msg = bot.send_message(message.chat.id , 'ФИО преподавателя?')
    bot.register_next_step_handler(msg, find_sch_master)

def find_sch_master(message):
    chat_id = message.chat.id
    text = message.text
    if not (len(text) == 6 or text.isdigit() == True):
        msg = bot.send_message(chat_id, 'Номер группы должен состоять из 6 цифр, введи ещё раз.')
        bot.register_next_step_handler(msg, find_sch_group)
        return
    bot.send_message(chat_id,'Здесь будет расписание препода '+text)

bot.polling(none_stop=True)