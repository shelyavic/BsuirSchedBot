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


def make_schedule_list_by_days(schedule):
    result = []
    #week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for day in schedule.keys():
        mess = ''
        mess += day + '\n\n'
        for subj in schedule[day]:
            time = subj['lessonTime']
            name = subj['subject']
            typee = subj['lessonType']
            aud_list = subj['auditory']
            if aud_list == []:
                aud = ''
            else:
                aud = aud_list[0]
            mess += '{} | {:<5s}({}) | {:>5s}\n'.format(time, name, typee, aud)
        result.append(mess)
    return result


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id , 'Привет, хочешь узнать расписание?\nИспользую команду /group')


@bot.message_handler(commands=['group'])
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
    try:
        sch = bsuir.get_group(text)
    except Exception as e:
        bot.send_message(chat_id, e)
    schedule_by_days = make_schedule_list_by_days(sch)
    for day_sch in schedule_by_days:
        bot.send_message(chat_id, day_sch)
    session.isRunning = False


@bot.message_handler(commands=['master'])
def master_handler(message):
    msg = bot.send_message(message.chat.id , 'ФИО преподавателя?')
    bot.register_next_step_handler(msg, find_master)

def find_master(message):
    chat_id = message.chat.id
    text = message.text
    try:
        sch = bsuir.get_master(text)
    except Exception as e:
        bot.send_message(message.chat.id , e)
        return
    schedule_by_days = make_schedule_list_by_days(sch)
    for day_sch in schedule_by_days:
        bot.send_message(chat_id, day_sch)


@bot.message_handler(content_types=['text'])
def common_text_handler(message):
    chat_id = message.chat.id
    text = message.text
    bot.send_message(chat_id, 'Повторяю: '+text)


bot.polling(none_stop=True)