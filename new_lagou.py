#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever

from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import MySQLdb
import json
import requests
from lxml import etree
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)            #过滤数据库警告

conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = 'chenxi1983##',port = 3306,charset ='utf8')
cursor = conn.cursor()
cursor.execute('Create database if not EXISTS lagou')
cursor.execute('use lagou')
cursor.execute('Create table if NOT EXISTS position_info(id int primary key AUTO_INCREMENT not null,companyFullName char(255) not null,positionName char(255) not null,firstType char(100) not null,salary char(100) not null,positionAdvantage char(255) not null,city char(255) not null,district char(100) not null,jobNature char(50) not null,workYear char(50) not null,education char(100) not null,createTime char(100) not null,skillTag char(255) not null,industryField char(100) not NULL );')
conn.commit()

def get_keywords():
    positionList = []
    url = 'https://www.lagou.com/'
    html = urlopen(url)
    bsObj = BeautifulSoup(html,'lxml')
    target = bsObj.findChildren('div',{'class':'menu_sub dn'})
    for i in range(len(target)):
        for item in target[i].find_all('a'):
            positionList.append(item.get_text())
    return positionList

cookie = {
    'Cookie':'JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
             'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644; '
             'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
             'index_location_city=%E6%B7%B1%E5%9C%B3; '
             'TG-TRACK-CODE=index_navigation; _gat=1; '
             '_gid=GA1.2.807135798.1504227456; _ga=GA1.2.1721572155.1504227456; '
             'LGSID=20170901085741-8ea70793-8eb0-11e7-902f-5254005c3644; '
             'LGRID=20170901095027-ed9ebf87-8eb7-11e7-902f-5254005c3644; '
             'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
             'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504230623;'
             'SEARCH_ID=a274b85f40b54d4da62d5e5740427a0a'
}

headers = {
    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/60.0.3112.90 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_java?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
}
cookies = {
    'Cookie': 'user_trace_token=20170901085741-8ea70518-8eb0-11e7-902f-5254005c3644;'
              'LGUID=20170901085741-8ea7093b-8eb0-11e7-902f-5254005c3644; '
              'index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=7277bc08d137413dac2590cea0465e39; '
              'TG-TRACK-CODE=search_code; JSESSIONID=ABAAABAAAGGABCBF0273ED764F089FC46DF6B525A6828FC; '
              'PRE_UTM=; PRE_HOST=; '
              'PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; '
              'PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3413383.html; _gat=1; _'
              'gid=GA1.2.807135798.1504227456; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504227456; '
              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1504252636; _ga=GA1.2.1721572155.1504227456; '
              'LGSID=20170901153335-dd437749-8ee7-11e7-903c-5254005c3644; '
              'LGRID=20170901155728-336ca29d-8eeb-11e7-9043-5254005c3644',
}
data = {
    'first': False,
    'pn':1,
}

def get_job(data):
    countNum = 0
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'
    page = requests.post(url=url, cookies=cookie, headers=headers, data=data)
    page.encoding = 'utf-8'
    result = page.json()
    jobs = result['content']['positionResult']['result']
    for job in jobs:
        countNum += 1
        companyShortName = job['companyShortName']
        positionId = job['positionId']  # 主页ID
        companyFullName = job['companyFullName']  # 公司全名
        companyLabelList = job['companyLabelList']  # 福利待遇
        companySize = job['companySize']  # 公司规模
        industryField = job['industryField']
        createTime = job['createTime']  # 发布时间
        city = job['city']#岗位所在城市
        district = job['district']  # 地区
        education = job['education']  # 学历要求
        financeStage = job['financeStage']  # 上市否
        firstType = job['firstType']  # 类型
        secondType = job['secondType']  # 类型
        formatCreateTime = job['formatCreateTime']  # 发布时间
        publisherId = job['publisherId']  # 发布人ID
        salary = job['salary']  # 薪资
        workYear = job['workYear']  # 工作年限
        positionName = job['positionName']  #
        jobNature = job['jobNature']  # 全职
        positionAdvantage = job['positionAdvantage']  # 工作福利
        positionLables = job['positionLables']  # 工种

        detail_url = 'https://www.lagou.com/jobs/{}.html'.format(positionId)
        response = requests.get(url=detail_url, headers=headers, cookies=cookies)
        response.encoding = 'utf-8'
        tree = etree.HTML(response.text)
        desc = tree.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')

        # print(companyFullName)
        # print('拉勾网链接:-> %s' % detail_url)
        # print('职位：%s' % positionName)
        # print('职位类型：%s' % firstType)
        # print('薪资待遇：%s' % salary)
        # print('职位诱惑：%s' % positionAdvantage)
        # print('城市：%s' % city)
        # print('地区：%s' % district)
        # print('类型：%s' % jobNature)
        # print('工作经验：%s' % workYear)
        # print('学历要求：%s' % education)
        # print('发布时间：%s' % createTime)
        skillTag = ''
        for label in positionLables:
            skillTag += label + ','
        # print('技能标签：%s' % skillTag)
        # print('公司类型：%s' % industryField)
        cursor.execute("insert into position_info(companyFullName,positionName,firstType,salary,positionAdvantage,city,district,jobNature,workYear,education,createTime,skillTag,industryField) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (companyFullName, positionName, firstType, salary, positionAdvantage, city, district, jobNature, workYear,education, createTime, skillTag, industryField))
        print('插入一条数据成功!%d'%countNum)
        conn.commit()

def url(data):
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'
    page = requests.post(url=url, cookies=cookie, headers=headers, data=data)
    page.encoding = 'utf-8'
    result = page.json()
    totalCount = result['content']['positionResult']['totalCount']                   #总记录数
    perCount = result['content']['positionResult']['resultSize']                     #每页记录条数
    ret = divmod(int(totalCount),int(perCount))                                          #总页数
    if ret[1]:
        pageCount = ret[0] + 1
    else:
        pageCount = ret[0]
    for keyword in get_keywords():
        data['keyword'] = keyword
        for x in range(1,pageCount+1):
            data['pn'] = x
            get_job(data)

if __name__ == '__main__':
    url(data)
    cursor.close()
    conn.close()

