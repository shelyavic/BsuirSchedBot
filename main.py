# -*- coding: utf-8 -*-
#%%
import telebot
import bsuir
from Session import Session

file = open('./config.txt',mode='r')
TOKEN = file.read()
file.close()

bot = telebot.TeleBot(TOKEN)
session = Session()

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id , 'Привет, хочешь узнать расписание?\nИспользую команду /group')

@bot.message_handler(commands='group')
def group_handler(message):
    msg = bot.send_message(message.chat.id , 'Какой номер группы?')
    bot.register_next_step_handler(msg, find_group)
    session.isRunning = True

def find_group(message):
    chat_id = message.chat.id
    text = message.text
    if not (len(text) == 6 or text.isdigit() == True):
        msg = bot.send_message(chat_id, 'Номер группы должен состоять из 6 цифр, введи ещё раз.')
        bot.register_next_step_handler(msg, find_group)
        return
    sch = bsuir.get_group(text)
    week = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']
    for day in week:
        mess = ''
        mess += day + '\n\n'
        for subj in sch[day]:
            time = subj['lessonTime']
            name = subj['subject']
            typee = subj['lessonType']
            aud_list = subj['auditory']
            if aud_list == []:
                aud = ''
            else:
                aud = aud_list[0]
            mess += '{} | {:<5s}({}) | {:>5s}\n'.format(time,name,typee,aud)

        bot.send_message(chat_id,mess)
    session.isRunning = False

@bot.message_handler(commands='master')
def master_handler(message):
    msg = bot.send_message(message.chat.id , 'ФИО преподавателя?')
    bot.register_next_step_handler(msg, find_master)

def find_master(message):
    chat_id = message.chat.id
    text = message.text

    bot.send_message(chat_id,'Здесь будет расписание препода '+text)

bot.polling(none_stop=True)