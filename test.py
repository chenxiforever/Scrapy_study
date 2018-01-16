#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from bs4 import BeautifulSoup
import requests
import json

BaseUrl = 'http://hotels.ctrip.com'
url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
headers = {
    'Connection':'keep-alive',
    'Cookie':'_abtest_userid=a5b7a4e0-7efb-4b98-b286-cc2b11d57c83; HotelDomestic_CitySight=7544=3938914; traceExt=campaign=CHNbaidu81&adid=index; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1516325470915; _abtest_=1b41edb6-552e-4627-8b99-068bb473f553; HotelDomesticVisitedHotels1=1943326=0,0,4.4,179,/fd/hotel/g4/M05/0C/F1/CggYHFX2EkmAXcAeAAW1tIayAbo845.jpg,&435383=0,0,4.7,21538,/hotel/20000/19308/acf707bec06941b78c7ef74b78cdc471.jpg,&1504212=0,0,4.6,578,/20020e00000072la8F897.jpg,&6598066=0,0,4.8,1215,/200w0d0000006svieCFA4.jpg,&1228738=0,0,3.8,189,/fd/hotel/g3/M09/AF/EB/CggYGlXsUGKAKd3qAAKlSUCRJEw488.jpg,; appFloatCnt=8; adscityen=Neijiang; CtripUserIdEx=FC1FBDA1C0A9039F665A80B37FFFE6473EA2AD1467CD3B3FC43654F7CEF66BE0; CtripUserId=FC1FBDA1C0A9039F600DA901008A89D0; corpid=; corpname=; LoginStatus=1%7c; cticket=27ED44925AA0F58BD8E456C365E0311970EDD773595A736F345FF0B58957A2C6; DUID=u=EC746E1C64A025766D8A57DBA259A9F6&v=0; IsNonUser=F; ticket_ctrip=uoeOwviAJ6VQEgTNwLuTqSV9j/bS+aOP3Riia1P+kyQbgkQZsD2giTCVzGDGSJj7LFvOZ0fxpo6B1jONAkVC5by+17HXEeRLSJUFS680j/gYERoBR0qSPf1j0QlJ4OffJLcd2TsvXZDJ6iAjWv7/YFdJRX6yEogbMpEGMhOi/bi7oM9Od5decSCyrsMQ4nuXitPgdJ8U9Xwr/wBLqO6qlQ/golrisFXKAId8ah/uVOQrHGuWcrsZQAyGvJ9QDuysAv1b1leEKHRtBmAdrGIJ4NxVUGu+4mRtZ7/Ezga9WTzaZDgYU1vUAA==; login_type=0; login_uid=CD9910A2F6F630D9CB468C1E8628D2D1; ASP.NET_SessionId=x4pefafqorjcfvvtwdsxl2mb; CtripUserInfo=VipGrade=0&UserName=&NoReadMessageCount=1&U=5DE98EFD8E58066DAAFCF22010882151; AHeadUserInfo=VipGrade=0&UserName=&NoReadMessageCount=1&U=5DE98EFD8E58066DAAFCF22010882151; OID_ForOnlineHotel=149621992687744nmpb1516064178475102003; _RF1=119.5.201.237; _RSG=C6aRr.Nu6j5yVuoR52jhR9; _RDG=28340654aa41ab2ba906975496422c49db; _RGUID=5b46e17f-b56e-418c-96eb-b4215bcb87fc; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1516066168021%7D%5D; _ga=GA1.2.56298346.1496219931; _gid=GA1.2.2140388480.1515992407; __zpspc=9.15.1516064182.1516066168.5%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C1515992407785%7C1.2037470421.1515463233195.1516065037639.1516066168065.1516065037639.1516066168065.undefined.0.0.47.47; MKT_Pagesource=PC; _bfa=1.1496219926877.44nmpb.1.1515992403426.1516064178367.13.82; _bfs=1.6; _bfi=p1%3D102002%26p2%3D102002%26v1%3D82%26v2%3D80',
    'Origin':'http://hotels.ctrip.com',
    'Referer':'http://hotels.ctrip.com/domestic-city-hotel.html',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
}

FormData = {
    'cityId':'28',
    'page':1,
}
html = requests.post(url,FormData,headers).text
dataJson = json.loads(html)
hotelCount = dataJson['totalMsg'].split('>')[1].split('<')[0]         #hotelCount为酒店数量
# print(hotelCount)
pageSize = divmod(int(hotelCount),25)
if pageSize[1]:
    pageNum = pageSize[0] + 1
else:
    pageNum = pageSize
# print(pageNum)                                                        #pageNum为列表页数
for page in range(1,pageNum+1):
    FormData = {
        'cityId': '28',
        'page': page,
    }
    print('第%d页'%page)
    try:
        html = requests.post(url, FormData, headers).text
        print(html)
        dataJson = json.loads(html)
        hotelList = dataJson['hotelPositionJSON']
        for hotelInfo in hotelList:
            print(hotelInfo)
            print('酒店名称:',hotelInfo['name'])                  #酒店名称
            print('酒店评分:',hotelInfo['score'])                 #酒店评分
            print('点评数:',hotelInfo['dpcount'])               #点评数
            print('推荐率:',hotelInfo['dpscore'])               #推荐率
            print('评价描述:',hotelInfo['stardesc'])              #评价描述
            print('地址:',hotelInfo['address'])               #地址
            print('酒店id:',hotelInfo['id'])                    #酒店id
            print('详细页地址:',BaseUrl + hotelInfo['url'])         #详细页地址
            print('\n')
    except Exception as e:
        print(e)
        continue
