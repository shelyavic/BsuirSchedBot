# -*- coding: utf-8 -*-
#%%
import requests

def get_group(group_num):
    url = 'https://journal.bsuir.by/api/v1/studentGroup/schedule'
    par = {'studentGroup': group_num}
    resp = requests.get(url, params=par)
    resp_json = resp.json()
    cur_week = resp_json['currentWeekNumber']
    days = resp_json['schedules']

    res = {}

    for day in days:
        for subj in day['schedule']:
            if cur_week in subj['weekNumber']:
                res.setdefault(day['weekDay'], []).append(subj)
    return res

