#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
#*********************************************************************
#设计思路：通过网站静态页面爬取，获得整站职位关键词，再逐个关键词爬取职位信息     *
#                             程序版本v2.0                             *
#*********************************************************************

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import MySQLdb
import json
import time
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)            #过滤数据库警告


keywords = []
BaseUrl = 'https://www.lagou.com/'

#获取全站所有关键词函数
def get_keywords():                         #获取全站关键词列表
    positionList = []
    url = BaseUrl
    html = urlopen(url)
    bsObj = BeautifulSoup(html,'lxml')
    target = bsObj.findChildren('div',{'class':'menu_sub dn'})
    for i in range(len(target)):
        for item in target[i].find_all('a'):
            positionList.append(item.get_text())
    return positionList

#获取指定页码指定职位的json数据函数
def get_json(pageNum,keyword):                               #通过url获取反馈的json数据,pageNum为当前页码，keyword为职位名称
    data = {
        'first': 'true',
        'pn': pageNum,
        'kd': keyword,
    }
    headers = {
        'Cookie': 'user_trace_token=20170308154044-89cac203-03d2-11e7-9229-5254005c3644; LGUID=20170308154044-89cacb03-03d2-11e7-9229-5254005c3644; login=true; unick=%E4%BD%99%E5%9C%A3%E6%9B%A6; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=15e201bb686649952131d0862e6b97327a3502da410e8692; index_location_city=%E5%8C%97%E4%BA%AC; TG-TRACK-CODE=search_code; JSESSIONID=ABAAABAAAIAACBI1801706615ED62D359563D2D405704C1; SEARCH_ID=b5bedcf11cbb4f4ab8f92f1eeb59149b; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1514974054,1515059160,1515126789,1515371244; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515377765; _gid=GA1.2.862982167.1515371243; _gat=1; _ga=GA1.2.320672603.1488958844; LGSID=20180108101559-ddd6dcd7-f419-11e7-a01e-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; LGRID=20180108101559-ddd6de88-f419-11e7-a01e-5254005c3644; _putrc=FDE651ACDC2518B5',
        'Host': 'www.lagou.com',
        'Referer':'https://www.lagou.com/jobs/list_java?px=default&city=%E5%85%A8%E5%9B%BD',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    }
    url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'
    count = 3              #异常处理次数为3,远程服务器强制关闭连接后尝试3次
    while count:
        try:
            html = requests.post(url = url,data = data, headers = headers)
        except Exception as e:
            print(e)
            print('网络连接异常，60秒后自动重试.')
            time.sleep(60)              #异常
            continue
            count -= 1
        else:
            count = 3
            position_dic = json.loads(html.text)
            return position_dic

#获取职位信息函数
def get_position(keyword):      #获取某关键词爬取到的职位信息字典
    positionInfo_dic = {}        #定义一个字典，用于存放爬取到的职位信息
    positionIdList = []           #定义一个职位ID列表，作为后面查找的索引
    InfoList = []
    try:
        position_dic = get_json(1,keyword)
    except Exception as e:
        print(e)
    else:
        #以下为获取keyword对应职位的总记录条数与记录总页数
        totalCount = position_dic['content']['positionResult']['totalCount']
        if totalCount>=450:
            pageSize = 30
        else:
            tmp = divmod(int(totalCount),15)
            if tmp[1]:
                pageSize = tmp[0] + 1                      #pageSize为整数类型数据
            else:
                pageSize = tmp[0]
        #获取总记录数与总页数代码结束
        for pageNum in range(1,pageSize+1):
            position_dic = get_json(pageNum, keyword)
            positionInfoList = position_dic['content']['positionResult']['result']    #positionInfoList为list类型
            #{companyId: 148909, positionName: "Python开发工程师", workYear: "3-5年", education: "本科", jobNature: "全职"}
            print(positionInfoList)
            for positions in positionInfoList:
                SinglePositionInfo = {}
                companyFullName = positions['companyFullName']
                companyId = positions['companyId']
                positionName = positions['positionName']
                positionId = positions['positionId']
                salary = positions['salary']
                city = positions['city']
                district = positions['district']
                workYear = positions['workYear']
                education = positions['education']
                jobNature = positions['jobNature']
                firstType = positions['firstType']
                secondType = positions['secondType']
                positionAdvantage = positions['positionAdvantage']
                createTime = positions['createTime']

                SinglePositionInfo['companyFullName'] = companyFullName
                SinglePositionInfo['companyId'] = companyId
                SinglePositionInfo['positionName'] = positionName
                SinglePositionInfo['positionId'] = positionId
                SinglePositionInfo['salary'] = salary
                SinglePositionInfo['city'] = city
                SinglePositionInfo['district'] = district
                SinglePositionInfo['workYear'] = workYear
                SinglePositionInfo['education'] = education
                SinglePositionInfo['jobNature'] = jobNature
                SinglePositionInfo['firstType'] = firstType
                SinglePositionInfo['secondType'] = secondType
                SinglePositionInfo['positionAdvantage'] = positionAdvantage
                SinglePositionInfo['createTime'] = createTime
                InfoList.append(SinglePositionInfo)
        return InfoList

# infolist = get_position(keywords)
# print('\n')
# print(len(infolist))
# for i in infolist:
#     print(i)

#创建数据库函数
def Createtable():
    conn = MySQLdb.connect(host='127.0.0.1',user = 'root',passwd = 'chenxi1983##',port = 3306,charset ='utf8')
    cursor = conn.cursor()
    cursor.execute('Create database if NOT EXISTS lagou')
    cursor.execute('use lagou')
    sql = '''Create table if NOT EXISTS positionInfo(
          Id int primary key AUTO_INCREMENT not null,
          companyFullName char(255) not NULL ,
          companyId char(255) not NULL ,
          positionName char(100) NOT null,
          positionId char(100) not null,
          salary char(100) not NULL ,
          city char(100) not null,
          district char(200) not null,
          workYear char(100) NOT NULL ,
          education char(80) NOT NULL ,
          jobNature char(60) not null,
          firstType char(100) not null,
          secondType char(100) not null,
          positionAdvantage char(255) not null,
          createTime char(100) NOT NULL);
    '''
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    print('数据库及数据表创建完成。')

#将数据写入数据库函数
def saveData(InfoList):
    try:
        Createtable()
    except Exception as e:
        print('数据库/表创建失败，错误代码%s'%e)
    #连接数据库
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='chenxi1983##', port=3306, charset='utf8')
    cursor = conn.cursor()
    cursor.execute('use lagou')
    for dic in (InfoList):
        companyFullName = dic['companyFullName']
        companyId = dic['companyId']
        positionName = dic['positionName']
        positionId = dic['positionId']
        salary = dic['salary']
        city = dic['city']
        district = dic['district']
        workYear = dic['workYear']
        education = dic['education']
        jobNature = dic['jobNature']
        firstType = dic['firstType']
        secondType = dic['secondType']
        positionAdvantage = dic['positionAdvantage']
        createTime = dic['createTime']
        try:
            cursor.execute("insert ignore into positionInfo(companyFullName,companyId,positionName,positionId,salary,city,district,workYear,education,jobNature,firstType,secondType,positionAdvantage,createTime) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(companyFullName,companyId,positionName,positionId,salary,city,district,workYear,education,jobNature,firstType,secondType,positionAdvantage,createTime))
        except Exception as e:
            print('插入数据库失败，错误代码%s'%e)
        else:
            print('成功写入一条数据。职位ID为:%s'%positionId)
        conn.commit()
    cursor.close()
    conn.close()

def main():
    keywords = get_keywords()                  #获取职位名称列表
    for keyword in keywords:                   #循环获取职位名称
        print(keyword)
        InfoList = get_position(keyword)       #获取职位名称对应的职位数据列表
        print(InfoList)
        saveData(InfoList)                     #将职位数据写入数据库
        print('职位:%s采集结束，广告60秒后，精彩继续~~~~'%keyword)
        time.sleep(60)

if __name__ == '__main__':
    main()




