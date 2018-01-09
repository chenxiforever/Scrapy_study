#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import socket


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

def validateIp(proxy):
    url = "http://ip.chinaz.com/getip.aspx"
    f = open("E:\ip.txt", "w")
    socket.setdefaulttimeout(3)
    for i in range(0, len(proxy)):
        try:
            ip = proxy[i].strip().split("\t")
            proxy_host = "http://" + ip[0] + ":" + ip[1]
            proxy_temp = {"http": proxy_host}
            res = urllib.urlopen(url, proxies=proxy_temp).read()
            f.write(proxy[i] + '\n')
            print
            proxy[i]
        except Exception as e:
            continue
    f.close()


