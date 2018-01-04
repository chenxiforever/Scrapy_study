#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from urllib.parse import quote
import json
import requests
import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)

conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = 'chenxi1983##',port = 3306,charset ='utf8')
cursor = conn.cursor()
cursor.execute('Create database if not EXISTS lagou')
cursor.execute('use lagou')
cursor.execute('Create table if NOT EXISTS positionList(id int primary key AUTO_INCREMENT not null, 公司全称 char(255) not null,公司简称 char(255) not null,工作地点 char(255) not null,公司ID int not null,职位名称 char(255) not null,职位Id int not null,工作年限 char(30) not null,薪资 char(20) not null,详细页面地址 char(255) not null,职位关键词 char(255) not null);')

pagesize = 1
pageCount = 0
KEYWORD = ''
url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false&isSchoolJob=0'
data = {
    'first':True,
    'pn':pagesize,
    'kd':KEYWORD
}
headers = {
    'Cookie':'user_trace_token=20171231003229-1a4fa3c7-3748-4e3d-ac7a-79672505b26b; __guid=237742470.1615529817819117600.1514651550359.597; LGUID=20171231003230-07960980-ed7f-11e7-b908-525400f775ce; JSESSIONID=ABAAABAAAIAACBICAF8D2F1015DD6E499E455E72EBD864F; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=829c78f8b205c0b552fb2f05c0dd4607; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514651551,1514796223; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514797701; LGSID=20180101164340-ddea570d-eecf-11e7-9fc4-5254005c3644; LGRID=20180101170819-4f66baac-eed3-11e7-9fc4-5254005c3644; _ga=GA1.2.137387786.1514651551; _gid=GA1.2.541396088.1514796223; _putrc=FDE651ACDC2518B5; login=true; unick=%E4%BD%99%E5%9C%A3%E6%9B%A6; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; SEARCH_ID=eb62d31bc43f4329acbc8fda80fcc956; index_location_city=%E5%8C%97%E4%BA%AC; monitor_count=4',
    'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
page  = requests.post(url=url,data=data,headers = headers)
page.encoding ='utf-8'
position_dic = page.json()
totalCount = position_dic['content']['positionResult']['totalCount']
PerCount = position_dic['content']['positionResult']['resultSize']
print('总共%s条记录'%totalCount)
print('每页共%s条记录'%PerCount)
tmp = divmod(totalCount,PerCount)
if tmp[1]:
    pageCount = str(int(tmp[0]) + 1)
else:
    pageCount = tmp[0]
print('总共%s页\n'%pageCount)
for i in range(1,int(pageCount)+1):
    data = {
        'first': True,
        'pn': i,
        'kd': KEYWORD
    }
    page = requests.post(url=url, data=data, headers=headers)
    page.encoding = 'utf-8'
    position_dic = page.json()
    position_list = position_dic['content']['positionResult']['result']
    for item in position_list:
        print('公司全称:%s'%item['companyFullName'])
        print('公司名称:%s'%item['companyShortName'])
        print('工作地点:%s'%item['city'])
        print('公司ID:%s'%item['companyId'])
        print('职位名称:%s'%item['positionName'])
        print('职位ID:%s'%item['positionId'])
        print('工作年限:%s'%item['workYear'])
        print('薪资:%s'%item['salary'])
        detail_url = 'https://www.lagou.com/jobs/'+str(item['positionId'])+'.html'
        print('详细页面地址:%s'%detail_url)
        print('\n')
        cursor.execute("insert into positionList(公司全称,公司简称,工作地点,公司Id,职位名称,职位Id,工作年限,薪资,详细页面地址,职位关键词) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(item['companyFullName'],item['companyShortName'],item['city'],item['companyId'],item['positionName'],item['positionId'],item['workYear'],item['salary'],detail_url,KEYWORD))
        print('插入一条数据成功')
    conn.commit()
cursor.close()
conn.close()