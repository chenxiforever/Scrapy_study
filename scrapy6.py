#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from urllib.request import urlopen
from bs4 import BeautifulSoup
import MySQLdb
import sqlite3
import os
Article_list = []
DOMAIN = 'http://www.cdhrss.gov.cn/'
Url_List = []                                                   #文章目录列表

conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = 'chenxi1983##',db= 'test',port = 3306,charset ='utf8')
cursor = conn.cursor()

# dbPath = 'Article.sqlite'
# if os.path.exists(dbPath):
#     os.remove(dbPath)
# conn = sqlite3.connect(dbPath)
# cursor = conn.cursor()
cursor.execute('create table IF NOT EXISTS Article_Info (id integer primary key AUTO_INCREMENT not null,title char(100) not null,Public_Date DATE not NULL,Title_ID CHAR(255) not NULL,Title_URL TEXT NOT  NULL);')
conn.commit()
Target_url = 'http://www.cdhrss.gov.cn/moreGovInfoPub.action?classId=070317030302&tn=2'
html = urlopen(Target_url)
bsObj = BeautifulSoup(html,'lxml')
# print(bsObj)
#<div class="pagenum"><span class="normal">每页 20 条  共 2331 条/117 页
Tmp_str = bsObj.findChild('div',{'class':'pagenum'}).get_text()
Record_Count = Tmp_str.split('共')[1].split('条')[0]        #Record_Count为总记录条数
Page_Count = Tmp_str.split('/')[1].split(' 页')[0]          #Page_Count为总页数
# <a href="http://www.cdhrss.gov.cn/moreGovInfoPub.action?classId=070317030302&tn=2&ps=20&p=2">下一页</a>
for i in range(1,int(Page_Count)+1):                                             #生成分页地址列表Url_List
    Url_List.append('http://www.cdhrss.gov.cn/moreGovInfoPub.action?classId=070317030302&tn=2&ps=20&p='+str(i))

for url in Url_List:
    html = urlopen(url)
    bsObj = BeautifulSoup(html,'lxml')
    text = bsObj.findAll('div',{'class':'xl'})[0].findAll('li')               #text为列表页内容
    tmp = text[0].findAll('li')
    for item in text:                                                           #获取列表页文章信息：标题、ID、文章发表日期、文章地址
        tmp_a = str(item.find('a'))
        title_id = tmp_a.split('id=')[1].split('" target')[0]                   #文章对应的唯一ID
        # print(item)  #<li><span>2017-12-14</span><a href="detailAllPurpose.action?id=1338386" target="_blank">青白江区三项措施做好职称评审工作</a></li>
        title = item.find('a').get_text()
        Title_ID = title_id
        Public_Date = item.find('span').get_text().split('-')
        Public_Date = ''.join(Public_Date)                                   #将日期格式由YYYY-MM-DD转换成YYYYMMDD
        url = item.find('a', href=True)
        Title_URL = DOMAIN+url['href']
        print(title)
        print(Public_Date)
        print(Title_ID)
        print(Title_URL)
        # sql = "insert into Article_Info (title,Public_Date,Title_ID,Title_URL) VALUES (%s,%s,%s,%s)"%(title,Public_Date,Title_ID,Title_URL)
        cursor.execute("insert into Article_Info (title,Public_Date,Title_ID,Title_URL) VALUES ('%s','%s','%s','%s')"%(title,Public_Date,Title_ID,Title_URL))
        print('成功插入一条数据库记录\n')
    conn.commit()
cursor.close()
conn.close()