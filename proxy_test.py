#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
}
def get_IPList():
    IPList =[]
    for num in range(1,11):
        url = 'http://www.xicidaili.com/nn/'+str(num)
        html = requests.get(url=url, headers=header).text
        bsObj = BeautifulSoup(html,'lxml')
        tmp = bsObj.find_all('tr',{'class':'odd'})
        for item in tmp:
            tmp = item.get_text().replace('\n\n\n','')
            tmp = tmp.strip('\n\n').replace('\n\n','|')
            tmp = tmp.replace('\n','|')
            result = tmp.split('|')
            IPList.append(result)
    return IPList

IPList = get_IPList()
for item in IPList:
    print(item)

