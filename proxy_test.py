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

def validateIp(iPList):
    ipInfoList = []
    url = "http://ip.chinaz.com/getip.aspx"
    socket.setdefaulttimeout(3)
    for item in iPList:
        try:
            ip = item[0].strip()
            port = item[1]
            protocol = item[4]
            # if protocol == 'HTTPS':
            #     continue
            proxy_host = "http://" + ip + ":" + port
            proxy_temp = {"http": proxy_host}
            print('开始验证,当前验证的IP为：%s,端口号为:%s'%(ip,port))
            res = requests.get(url, proxies=proxy_temp).text
            print('可用IP信息为:%s,端口:%s'%(ip,port))
            info = ip+':'+port
            ipInfoList.append(info)
        except Exception as e:
            continue
    print('所有IP验证结束!')
    return ipInfoList

def main():
    IPList = get_IPList()
    ipInfoList = validateIp(IPList)
    with open('proxyIp.txt','w') as proxyip:
        proxyip.write(ipInfoList)

if __name__ == '__main__':
    main()


