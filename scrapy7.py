#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from urllib.request import urlopen
from bs4 import BeautifulSoup
import MySQLdb

TitleUrlList = []                          #具体文章地址列表
conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = 'chenxi1983##',db= 'test',port = 3306,charset ='utf8')
cursor = conn.cursor()

count = cursor.execute("select Title_URL from article_info")    #获取记录条数
results_tuple = cursor.fetchall()                               #获取对应的所有记录数据,元组格式
tmp_tuple = list(results_tuple)                                 #由于是((),(),())格式元组，所以需要转换两次

for tmp in tmp_tuple:
    url = list(tmp)[0]
    TitleUrlList.append(url)
cursor.execute("create table if not exists Article(id int primary key AUTO_INCREMENT not null,Title char(100) not null,TitleID CHAR(255) not NULL,PublicDate date not null,Content text not null);")
conn.commit()
for url in TitleUrlList:
    html = urlopen(url)
    bsObj = BeautifulSoup(html,'lxml')
    Title_ID = url.split('id=')[1]                                        #文章ID
    content = bsObj.findChild('td', {'id': 'myFont'}).get_text().strip()  #文章正文
    title = bsObj.findChild('h1').get_text()                              #文章标题
    tmp_str = bsObj.find('div',{'id':'part07'}).findChild('h3').get_text()
    tmp_str = tmp_str.split('填报时间：')[1]
    tmp_str = tmp_str.split('   责任')[0]
    tmp_list = tmp_str.split('-')
    Public_date = "".join(tmp_list)                                       #填报时间
    print(title)
    print(Title_ID)
    print(Public_date)
    print(content)
    cursor.execute("insert into Article(Title,TitleId,PublicDate,Content) VALUES ('%s','%s','%s','%s')"%(title,Title_ID,Public_date,content))
    print('成功插入一条记录\n')
    conn.commit()
cursor.close()
conn.close()