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

import requests
from bs4 import BeautifulSoup

def getmeteo(city):
    if city =='orsk':
        myUrl = "https://rp5.ru/Погода_в_Орске,_Оренбургская_область"
    elif city == 'msk':
        myUrl = "https://rp5.ru/Погода_в_Москве_(центр,_Балчуг)"
    elif city == 'spb':
        myUrl = "https://rp5.ru/Погода_в_Санкт-Петербурге"
    elif city == 'yar':
        myUrl = "https://rp5.ru/Погода_в_Ярославле,_Ярославская_область"
    elif city == 'riga':
        myUrl = "https://rp5.ru/Погода_в_Риге,_Латвия"
    else:
        print("not correct city")
        output = ["", ""]
        return output
    #
    # Используем более распространенный User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(myUrl, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Парсим HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим <div> с id 'ArchTemp'
        arch_temp_div = soup.find('div', id='ArchTemp')
        if arch_temp_div:
            # Находим <span> с классом 't_0' для температуры в Цельсиях
            temp_celsius = arch_temp_div.find('span', class_='t_0')
            if temp_celsius:
                outtemp = temp_celsius.text.strip()
                #print(f"Температура: {temp_celsius.text.strip()}")  # Печатаем температуру
            else:
                print("Не удалось найти температуру в Цельсиях.")
        else:
            print("Не удалось найти элемент с id='ArchTemp'.")

        meta_description = soup.find('meta', attrs={'name': 'description'})
        if meta_description and 'content' in meta_description.attrs:
            # Извлекаем содержимое атрибута content
            description_content = meta_description['content']
            outmetar = description_content
            #print(description_content)
        else:
            print("Тег <meta name='description'> не найден.")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка: {e}")
    output = [outtemp,outmetar,myUrl]
    return output



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
# @bot.message_handler(regexp="^пм$")
def send_weather(message):
    # get temperature ORSK
    meteo = getmeteo("orsk")
    if meteo[0] != "":
        text = '<b>ORSK T:' + meteo[0] + '</b>\n' + meteo[1] + '\n' + meteo[2]
        print(text)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,"не получилось получить погоду")

@bot.message_handler(commands=['wm', 'пм'])
@bot.message_handler(regexp="^.пм$")
# @bot.message_handler(regexp="^пм$")
def send_weather(message):
    # get temperature MSK
    meteo = getmeteo("msk")
    if meteo[0] != "":
        text = '<b>MSK T:' + meteo[0] + '</b>\n' + meteo[1] + '\n' + meteo[2]
        print(text)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,"не получилось получить погоду")

@bot.message_handler(commands=['wy', 'пя'])
@bot.message_handler(regexp="^.пя$")
@bot.message_handler(regexp="^пя$")
def send_weather(message):
    # get temperature YAR
    meteo = getmeteo("yar")
    if meteo[0] != "":
        text = '<b>YAR T:' + meteo[0] + '</b>\n' + meteo[1] + '\n' + meteo[2]
        print(text)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,"не получилось получить погоду")

@bot.message_handler(commands=['wh', 'пр'])
@bot.message_handler(regexp="^.пр$")
@bot.message_handler(regexp="^пр$")
def send_weather(message):
    # get temperature Riga
    meteo = getmeteo("riga")
    if meteo[0] != "":
        text = '<b>RIGA T:' + meteo[0] + '</b>\n' + meteo[1] + '\n' + meteo[2]
        print(text)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,"не получилось получить погоду")

@bot.message_handler(commands=['wp', 'пп'])
@bot.message_handler(regexp="^.пп$")
@bot.message_handler(regexp="^пп$")
def send_weather(message):
    # get temperature SPB
    meteo = getmeteo("spb")
    if meteo[0] != "":
        text = '<b>SPB T:' + meteo[0] + '</b>\n' + meteo[1] + '\n' + meteo[2]
        print(text)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id,"не получилось получить погоду")

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
                bot.send_photo(message.chat.id, requests.get(url).content, has_spoiler=True)
                error = False
            except:
                bot.send_message(message.chat.id, "Произошла какая то хуйня")
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
                    bot.send_photo(message.chat.id, requests.get(url).content, has_spoiler=True)
                    error = False
                except:
                    bot.send_message(message.chat.id, "Произошла какая то хуйня")
                    error = True
        else:
            print(time_str + 'с 7:00 по 18:30 MSK сиськи не показываю. Пишите в приват. @OPCKBot ')
            bot.send_message(message.chat.id, 'с 7:00 по 18:30 MSK сиськи не показываю. Пишите в приват @OPCKBot')


bot.polling(none_stop=True)
