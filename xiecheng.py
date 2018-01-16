#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from bs4 import BeautifulSoup
import requests
import json
import re
import MySQLdb
from warnings import filterwarnings
filterwarnings('ignore', category = MySQLdb.Warning)            #过滤数据库警告

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='chenxi1983##', port=3306, charset='utf8')
cursor = conn.cursor()
BaseUrl = 'http://hotels.ctrip.com'
url = 'http://hotels.ctrip.com/domestic-city-hotel.html'
jsonUrl = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
cityIdList = []
hotelSummaryList = []
headers = {
    'Connection':'keep-alive',
    'Cookie':'_abtest_userid=a5b7a4e0-7efb-4b98-b286-cc2b11d57c83; HotelDomestic_CitySight=7544=3938914; traceExt=campaign=CHNbaidu81&adid=index; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1516325470915; _abtest_=1b41edb6-552e-4627-8b99-068bb473f553; HotelDomesticVisitedHotels1=1943326=0,0,4.4,179,/fd/hotel/g4/M05/0C/F1/CggYHFX2EkmAXcAeAAW1tIayAbo845.jpg,&435383=0,0,4.7,21538,/hotel/20000/19308/acf707bec06941b78c7ef74b78cdc471.jpg,&1504212=0,0,4.6,578,/20020e00000072la8F897.jpg,&6598066=0,0,4.8,1215,/200w0d0000006svieCFA4.jpg,&1228738=0,0,3.8,189,/fd/hotel/g3/M09/AF/EB/CggYGlXsUGKAKd3qAAKlSUCRJEw488.jpg,; appFloatCnt=8; adscityen=Neijiang; CtripUserIdEx=FC1FBDA1C0A9039F665A80B37FFFE6473EA2AD1467CD3B3FC43654F7CEF66BE0; CtripUserId=FC1FBDA1C0A9039F600DA901008A89D0; corpid=; corpname=; LoginStatus=1%7c; cticket=27ED44925AA0F58BD8E456C365E0311970EDD773595A736F345FF0B58957A2C6; DUID=u=EC746E1C64A025766D8A57DBA259A9F6&v=0; IsNonUser=F; ticket_ctrip=uoeOwviAJ6VQEgTNwLuTqSV9j/bS+aOP3Riia1P+kyQbgkQZsD2giTCVzGDGSJj7LFvOZ0fxpo6B1jONAkVC5by+17HXEeRLSJUFS680j/gYERoBR0qSPf1j0QlJ4OffJLcd2TsvXZDJ6iAjWv7/YFdJRX6yEogbMpEGMhOi/bi7oM9Od5decSCyrsMQ4nuXitPgdJ8U9Xwr/wBLqO6qlQ/golrisFXKAId8ah/uVOQrHGuWcrsZQAyGvJ9QDuysAv1b1leEKHRtBmAdrGIJ4NxVUGu+4mRtZ7/Ezga9WTzaZDgYU1vUAA==; login_type=0; login_uid=CD9910A2F6F630D9CB468C1E8628D2D1; ASP.NET_SessionId=x4pefafqorjcfvvtwdsxl2mb; CtripUserInfo=VipGrade=0&UserName=&NoReadMessageCount=1&U=5DE98EFD8E58066DAAFCF22010882151; AHeadUserInfo=VipGrade=0&UserName=&NoReadMessageCount=1&U=5DE98EFD8E58066DAAFCF22010882151; OID_ForOnlineHotel=149621992687744nmpb1516064178475102003; _RF1=119.5.201.237; _RSG=C6aRr.Nu6j5yVuoR52jhR9; _RDG=28340654aa41ab2ba906975496422c49db; _RGUID=5b46e17f-b56e-418c-96eb-b4215bcb87fc; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1516066168021%7D%5D; _ga=GA1.2.56298346.1496219931; _gid=GA1.2.2140388480.1515992407; __zpspc=9.15.1516064182.1516066168.5%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C1515992407785%7C1.2037470421.1515463233195.1516065037639.1516066168065.1516065037639.1516066168065.undefined.0.0.47.47; MKT_Pagesource=PC; _bfa=1.1496219926877.44nmpb.1.1515992403426.1516064178367.13.82; _bfs=1.6; _bfi=p1%3D102002%26p2%3D102002%26v1%3D82%26v2%3D80',
    'Origin':'http://hotels.ctrip.com',
    'Referer':'http://hotels.ctrip.com/domestic-city-hotel.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}

def getCityId():
    head = {
        'Cookie':'Cookie:AHeadUserInfo=VipGrade=0&UserName=&NoReadMessageCount=0&U=F0B6A150C5D71C369827855DA7DDAD85; _abtest_userid=43139b9b-aa71-4ae6-a075-16f688b5c913; __guid=208231307.3690029046937470000.1510971618992.3616; HotelCityID=95split%E4%B8%8A%E6%B5%B7splitEmeishansplit2018-01-11split2018-01-12split0; Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||; Session=SmartLinkCode=U155952&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; adscityen=Neijiang; traceExt=campaign=CHNbaidu81&adid=index; appFloatCnt=4; manualclose=1; HotelDomesticVisitedHotels1=4374378=0,0,4.6,403,/200g0g00000086ena9ACA.jpg,&2298680=0,0,4.6,2803,/200p0k000000b1zndCF28.jpg,&916432=0,0,4.7,281,/200k0j000000afyk849B1.jpg,; ASP.NET_SessionId=rvh2iiyqx1iljypelbnnourg; OID_ForOnlineHotel=15109708813313wom8k1516104541638102002; _bfa=1.1510970881331.3wom8k.1.1516104534939.1516107596975.7.45; _bfs=1.14; _RF1=110.190.174.223; _RSG=5EaCReE6XAB.Swux0Yip78; _RDG=28dde1ad3feff729a0118f529722046919; _RGUID=b2a118ea-1b32-4385-81f3-b2203be3a73e; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1516108607548%7D%5D; _ga=GA1.2.806793281.1510971657; _gid=GA1.2.1985413515.1516026245; __zpspc=9.5.1516107599.1516108607.5%231%7Cbaidu%7Ccpc%7Cbaidu81%7C%25E6%2590%25BA%25E7%25A8%258B%7C%23; _jzqco=%7C%7C%7C%7C1516026244725%7C1.227931446.1510971656550.1516108587332.1516108607605.1516108587332.1516108607605.undefined.0.0.25.25; _bfi=p1%3D102086%26p2%3D102086%26v1%3D45%26v2%3D43; MKT_Pagesource=PC',
        'Referer':'http://hotels.ctrip.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }
    html = requests.get(url,head).text
    bsObj = BeautifulSoup(html,'lxml')
    hotelList = bsObj.findAll('dl',{'class':'pinyin_filter_detail layoutfix'})
    areaList = hotelList[0].findAll('a')
    for item in areaList:
        id = re.sub('\D',"",item['href'])
        cityIdList.append(item.text+'|'+id)
    return cityIdList

def getPageNum(cityId):
    FormData = {
        'cityId':cityId,
        'page':1,
    }
    html = requests.post(jsonUrl,FormData,headers).text
    dataJson = json.loads(html)
    hotelCount = dataJson['hotelAmount']                            #hotelCount为酒店数量
    pageSize = divmod(int(hotelCount),25)
    if pageSize[1]:
        pageNum = pageSize[0] + 1
    else:
        pageNum = pageSize[0]
    return pageNum                                                  #pageNum为列表页数


def getSummaryInfo(pageNum,cityId):
    cursor.execute('Create database if not EXISTS hotelInfo')
    cursor.execute('use hotelInfo')
    cursor.execute(
        'Create table if NOT EXISTS hotelSummary(id int primary key not null,name char(255) not null,score char(10) not null,dpcount char(10) not null,dpscore char(10) not null,stardesc char(255) not null,address char(255) not null,url char(255) not null);')
    conn.commit()
    for page in range(1, pageNum+1):
        FormData = {
            'cityId': cityId,
            'page': page,
        }
        print('第%d页' % page)
        try:
            html = requests.post(jsonUrl, FormData, headers).text
            dataJson = json.loads(html)
            hotelList = dataJson['hotelPositionJSON']
            for hotelInfo in hotelList:
                url = BaseUrl + hotelInfo['url']
                cursor.execute(
                    "insert into hotelSummary(id,name,score,dpcount,dpscore,stardesc,address,url) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (hotelInfo['id'], hotelInfo['name'], hotelInfo['score'], hotelInfo['dpcount'],hotelInfo['dpscore'], hotelInfo['stardesc'], hotelInfo['address'], url))
                print('酒店名称:', hotelInfo['name'])  # 酒店名称
                print('酒店评分:', hotelInfo['score'])  # 酒店评分
                print('点评数:', hotelInfo['dpcount'])  # 点评数
                print('推荐率:', hotelInfo['dpscore'])  # 推荐率
                print('评价描述:', hotelInfo['stardesc'])  # 评价描述
                print('地址:', hotelInfo['address'])  # 地址
                print('酒店id:', hotelInfo['id'])  # 酒店id
                print('详细页地址:', BaseUrl + hotelInfo['url'])  # 详细页地址
                print('插入一条数据成功!')
                conn.commit()
                print('\n')
        except Exception as e:
            print(e)
            continue

def main():
    idList = getCityId()
    for item in idList:
        print(item)
        id = item.split('|')[1]
        try:
            pageNum = getPageNum(id)
            # print(id,pageNum)
            getSummaryInfo(pageNum, id)
        except Exception as e:
            continue
    cursor.close()
    conn.close()
if __name__ =='__main__':
    main()
