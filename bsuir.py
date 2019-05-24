# -*- coding: utf-8 -*-

# %%
import requests
from pprint import pprint
import csv


def get_group(group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule'
    par = {'studentGroup': group_num}
    resp = requests.get(url, params=par)
    if resp.text == '':
        raise Exception('Не удалось найти расписание группы {}, \
                        проверьте правильность введённой информации'.format(group_num))
    resp_json = resp.json()

    cur_week = resp_json['currentWeekNumber']
    days = resp_json['schedules']

    res = {}

    for day in days:
        for subj in day['schedule']:
            if cur_week in subj['weekNumber']:
                res.setdefault(day['weekDay'], []).append(subj)
    return res


def get_masters_update():
    response = requests.get('https://journal.bsuir.by/api/v1/employees')
    masters = response.json()
    fields = ['fio', 'id']
    with open("masters.csv", 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        for master in masters:
            fio = master['fio']
            ind = fio.find('(')
            if ind != -1:
                fio = fio[:ind].rstrip(' ')
            writer.writerow({'fio': fio, 'id': master['id']})


def get_masters():
    masters = []
    with open('masters.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for master in reader:
            masters.append(master)
    return masters

def get_master(name_to_find):
    masters = get_masters()
    ID = None
    for master in masters:
        if master['fio'] == name_to_find:
            ID = master['id']
            break
    if ID is None:
        raise Exception(
                'Не получилось найти {}, проверьте правильность ввода'.format(name_to_find))
    par = {'employeeId': ID}
    response = requests.get(
            'https://journal.bsuir.by/api/v1/portal/employeeSchedule',
            params=par
            )
    resp_json = response.json()
    cur_week = resp_json['currentWeekNumber']
    days = resp_json['schedules']

    res = {}

    for day in days:
        for subj in day['schedule']:
            if cur_week in subj['weekNumber']:
                res.setdefault(day['weekDay'], []).append(subj)
    return res
    pprint(res)












