#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
#*********************************************************************
#设计思路：通过网站静态页面爬取，获得整站职位关键词，再逐个关键词爬取职位信息     *
#                             程序版本v1.3                             *
#*********************************************************************

from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json
import time
keywords = []
BaseUrl = 'https://www.lagou.com/'

def get_keywords():                         #获取全站关键词列表
    positionList = []
    url = 'https://www.lagou.com/'
    html = urlopen(url)
    bsObj = BeautifulSoup(html,'lxml')
    target = bsObj.findChildren('div',{'class':'menu_sub dn'})
    for i in range(len(target)):
        for item in target[i].find_all('a'):
            positionList.append(item.get_text())
    return positionList

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
    count = 3              #异常处理次数为3,处理连接超时次数为3次
    while count:
        try:
            html = requests.post(url = url,data = data, headers = headers)
        except Exception as e:
            print(e)
            print('网络连接异常，60秒后自动重试.')
            time.sleep(60)              #异常
            continue
        else:
            position_dic = json.loads(html.text)
            return position_dic

def get_position(keywords):      #获取某关键词爬取到的职位信息字典，输入为职位列表，考虑到使用列表，是为了在本函数中加入异常处理，针对没有获取到'content'的情况设计。
    positionInfo_dic = {}        #定义一个字典，用于存放爬取到的职位信息
    '''预留获取keyword的代码空间
    '''
    try:
        position_dic = get_json(1,['python'][0]) #'python'等测试成功就使用keyword变量替换
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
            position_dic = get_json(pageNum, ['python'][0])
            positionInfo = position_dic['content']['positionResult']['result']    #positionInfo为list类型
            '''获取信息如下
            dict_keys(['industryField', 'jobNature', 'adWord', 'score', 'subwayline', 'companySize', 'imState', 'explain', 'city', 'secondType', 'deliver', 'companyLogo', 'companyFullName', 'positionName', 'plus', 'linestaion', 'isSchoolJob', 'publisherId', 'firstType', 'positionId', 'companyLabelList', 'salary', 'appShow', 'stationname', 'positionAdvantage', 'financeStage', 'companyId', 'lastLogin', 'formatCreateTime', 'education', 'gradeDescription', 'district', 'approve', 'workYear', 'longitude', 'latitude', 'positionLables', 'businessZones', 'createTime', 'companyShortName', 'industryLables', 'pcShow', 'promotionScoreExplain'])
            dict_values(['其他', '全职', 0, 0, '1号线(下沙江滨)', '50-150人', 'sevenDays', None, '杭州', '后端开发', 0, 'i/image/M00/46/E3/Cgp3O1eN2CGAO5pJAAAXRqiHOqA949.jpg', '浙江大禹信息技术有限公司', '.NET开发工程师', None, '1号线(下沙江滨)_城站;1号线(下沙江滨)_定安路;1号线(临平)_城站;1号线(临平)_定安路', 0, 1648814, '技术', 1960764, ['带薪年假', '绩效奖金', '扁平管理', '领导好'], '10k-15k', 0, '城站', '五险一金、定期体检、弹性管理、年终奖金', '不需要融资', 67245, 1514946139000, '2018-01-02', '本科', None, None, 1, '1-3年', '120.17206999', '30.23451008', ['MySQL', 'c#', 'oracle'], None, '2018-01-02 10:05:31', '水利水电勘测设计院研发中心', [], 0, None])
            '''
            #{companyId: 148909, positionName: "Python开发工程师", workYear: "3-5年", education: "本科", jobNature: "全职"}
            for item in positionInfo:
                companyFullName = item['companyFullName']
                compayId = item['companyId']
                positionName = item['positionName']
                positionId = item['positionId']
                salary = item['salary']
                city = item['city']
                district = item['district']
                workYear = item['workYear']
                education = item['education']
                jobNature = item['jobNature']
                firstType = item['firstType']
                secondType = item['secondType']
                positionAdvantage = item['positionAdvantage']
                createTime = item['createTime']

        return positionInfo_dic

positionInfo_dic  = get_position(keywords)


