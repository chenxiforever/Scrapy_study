#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

BaseUrl = 'https://www.kuaidaili.com/free/inha/1/'
url = BaseUrl
html = requests.get(url).text
bsObj = BeautifulSoup(html,'lxml')
tmp = bsObj.find('tbody')
li = tmp.findAll('tr')
for single in li:
    # print(single.get_text())
    element = single.get_text().split('\n')
    print(element[1],':',element[2])

proxie = {
    'http' : 'http://122.114.31.177:808'}
url = 'https://www.facebook.com'
header = {
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36',
    }
s = requests.session()
response = s.get(url,headers = header,proxies = proxie)
print(response)
