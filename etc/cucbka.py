#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Scripts parse links for cuckI pictures =) 
 and write to file cucbka.dat
"""
import time
from io import StringIO
import requests
from lxml import html, etree

r = requests.get('https://blog.stanis.ru/?action=sch&searchby=category&what=4',
                 proxies={'https': 'http://127.0.0.1:8118'})
if r.status_code == 200:
    index = r.text.rfind('<a href="?action=sch&amp;searchby=category&amp;what=4&amp;page=')
    if index != -1:
        tmp = r.text[index + 65:index + 75]
        index1 = tmp.find('>')
        index2 = tmp.find('<')
        tmp1 = tmp[index1 + 1:index2]
MIN_PAGE = 1
MAX_PAGE = int(tmp1)
print("Max page for processing: " + str(MAX_PAGE))
f = open('./cucbka.dat', 'a')
tmp = list()
for page in range(MIN_PAGE, MAX_PAGE):
    print("Proccess page: " + str(page))
    hlink = 'https://blog.stanis.ru/?action=sch&searchby=category&what=4&page=' + str(page)
    r = requests.get(hlink, proxies={'https': 'http://127.0.0.1:8118'})
    if r.status_code == 200:
        tree = html.fromstring(r.text)
        links = tree.xpath('//div[@class="pic"]/img/@src')
        print(links[0])
        for link in links:
            tmp.append(link[5:])
        # time.sleep(0.5)

f.write("\n".join(tmp))
f.close()
