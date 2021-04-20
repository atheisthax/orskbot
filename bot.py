#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import random
import re
from datetime import time

import config
import pytz
import requests
import telebot
import xmltodict
from pytz import timezone

try:
    if config.useproxy:
        telebot.apihelper.proxy = {config.proxytype: config.proxy}
except:
    print('no proxy in config')
bot = telebot.TeleBot(config.token)

f = open('./etc/cucbka.dat')
links = f.read().split('\n')
f.close()

@bot.message_handler(commands=['w', 'п'])
@bot.message_handler(regexp="^.п$")
# @bot.message_handler(regexp="^п$")
def send_weather(message):
    r = requests.get('http://pc.ornpz.ru/meteo/temperature1day.png')
    if r.status_code == 200:
        f = open('out.jpg', 'wb')
        f.write(r.content)
        f.close()

        bot.send_chat_action(message.chat.id, 'upload_photo')
        img = open('out.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        img.close()
    else:
        bot.send_message(message.chat.id,
                         "Произошла какая-то хуйня (URL: http://pc.ornpz.ru/meteo/temperature1day.png)...")

        # get temperature
    r = requests.get('http://pc.ornpz.ru/meteo/meteo.xml')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)

        for section in doc['points']['point']:
            key = section.get('@name', None)
            # направление ветра
            # if key == 'PointName01':
            #    value = section.get('@value', None)
            #    print 'P:'+value

            # температура
            if key == 'PointName05':
                value = section.get('@value', None)
                print('T:' + value)
                bot.send_message(message.chat.id, 'T: ' + value)
    else:
        bot.send_message(message.chat.id,
                         u"cannot get content of ( URL: http://pc.ornpz.ru/meteo/meteo.xml)... ERROR:" + str(r.status))


@bot.message_handler(commands=['wm', 'пм'])
@bot.message_handler(regexp="^.пм$")
# @bot.message_handler(regexp="^пм$")
def send_weather(message):
    # get temperature MSK
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=524901&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('MSK T:' + value)
        bot.send_message(message.chat.id, 'MSK T: ' + value)
    else:
        bot.send_message(message.chat.id,
                         u"cannot get content of ( URL: http://api.openweathermap.org/data/2.5/weather?id=524901&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8)... ERROR:" + str(
                             r.status))


@bot.message_handler(commands=['wy', 'пя'])
@bot.message_handler(regexp="^.пя$")
@bot.message_handler(regexp="^пя$")
def send_weather(message):
    # get temperature MSK
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=468902&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('YAR T:' + value)
        bot.send_message(message.chat.id, 'YAR T: ' + value)
    else:
        bot.send_message(message.chat.id,
                         u"cannot get content of ( URL: http://api.openweathermap.org/data/2.5/weather?id=468902&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8)... ERROR:" + str(
                             r.status))


@bot.message_handler(commands=['wh', 'пр'])
@bot.message_handler(regexp="^.пр$")
@bot.message_handler(regexp="^пр$")
def send_weather(message):
    # get temperature Riga
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=456173&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('YAR T:' + value)
        bot.send_message(message.chat.id, 'RIGA T: ' + value)
    else:
        bot.send_message(message.chat.id,
                         u"cannot get content of ( URL: http://api.openweathermap.org/data/2.5/weather?id=456173&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8)... ERROR:" + str(
                             r.status))


@bot.message_handler(commands=['wp', 'пп'])
@bot.message_handler(regexp="^.пп$")
@bot.message_handler(regexp="^пп$")
def send_weather(message):
    # get temperature MSK
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=498817&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8')
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('SPB T:' + value)
        bot.send_message(message.chat.id, 'SPB T: ' + value)
    else:
        bot.send_message(message.chat.id,
                         u"cannot get content of ( URL: http://api.openweathermap.org/data/2.5/weather?id=498817&units=metric&mode=xml&appid=7cad4e5a16fc989137d9dcaa7d726ff8)... ERROR:" + str(
                             r.status))


@bot.message_handler(commands=['ku', 'ку'])
@bot.message_handler(regexp="^(ку|\.ку|ku|\.ku|re|\.re)$")
def send_ku(message):
    tz = 'Asia/Yekaterinburg'
    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    bot.send_message(message.chat.id, time_str)


@bot.message_handler(regexp="^(ку|\.ку|ku|\.ku|re|\.re) ([А-Яa-я]*)")
def send_ku_town(message):
    tz = 'Asia/Yekaterinburg'

    if re.search(r'Орск|Orsk', message.text):
        tz = 'Asia/Yekaterinburg'

    if re.search(r'Москва|Moscow|Питер|Piter|СПб', message.text):
        tz = 'Europe/Moscow'

    fmt = '%Y-%m-%d %H:%M:%S'
    utc = datetime.datetime.utcnow()
    time_str = timezone(tz).fromutc(utc).strftime(fmt)
    bot.send_message(message.chat.id, time_str)


@bot.message_handler(commands=['сиськи'])
@bot.message_handler(regexp="^(сиськи|\.сиськи)$")
def send_cucki(message):
    error = True
    if message.chat.id != -242669552:
        while error:
            i = random.randint(0, len(links) - 1)
            url = "https://blog.stanis.ru/imgs/" + links[i]
            try:
                bot.send_photo(message.chat.id, requests.get(url).content)
                error = False
            except:
                error = True
    else:
        tz = 'Europe/Moscow'
        fmt = '%Y-%m-%d %H:%M:%S'
        utc = datetime.datetime.utcnow()
        now = timezone(tz).fromutc(utc)
        time_str = timezone(tz).fromutc(utc).strftime(fmt)
        now_time = now.time()
        if now_time <= time(7, 00) or now_time >= time(18, 30):
            while error:
                i = random.randint(0, len(links) - 1)
                url = "https://blog.stanis.ru/imgs/" + links[i]
                try:
                    bot.send_photo(message.chat.id, requests.get(url).content)
                    error = False
                except:
                    error = True
        else:
            print(time_str + 'с 7:00 по 18:30 MSK сиськи не показываю. Пишите в приват. @OPCKBot ')
            bot.send_message(message.chat.id, 'с 7:00 по 18:30 MSK сиськи не показываю. Пишите в приват @OPCKBot')


bot.polling(none_stop=True)
