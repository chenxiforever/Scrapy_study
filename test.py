#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
import requests

headers = {
    'Referer':'http://hotels.ctrip.com/hotel/jiuzhaigou91',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    'cookie':'_abtest_userid=a5b7a4e0-7efb-4b98-b286-cc2b11d57c83; HotelDomestic_CitySight=7544=3938914; traceExt=campaign=CHNbaidu81&adid=index; adscityen=Neijiang; Session=smartlinkcode=U130026&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4897&SID=130026&OUID=&Expires=1516325470915; HotelDomesticVisitedHotels1=1504212=0,0,4.6,578,/20020e00000072la8F897.jpg,&6598066=0,0,4.8,1215,/200w0d0000006svieCFA4.jpg,&1228738=0,0,3.8,189,/fd/hotel/g3/M09/AF/EB/CggYGlXsUGKAKd3qAAKlSUCRJEw488.jpg,; ASP.NET_SessionId=lcckvhpawgwtf1uo35wx4nf5; OID_ForOnlineHotel=149621992687744nmpb1515738123138102002; manualclose=1; appFloatCnt=7; _abtest_=1b41edb6-552e-4627-8b99-068bb473f553; _bfa=1.1496219926877.44nmpb.1.1515745431364.1515748324420.10.64; _bfs=1.1; _RF1=119.5.201.237; _RSG=C6aRr.Nu6j5yVuoR52jhR9; _RDG=28340654aa41ab2ba906975496422c49db; _RGUID=5b46e17f-b56e-418c-96eb-b4215bcb87fc; Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp%22%3A1515748327200%7D%5D; __zpspc=9.12.1515748327.1515748327.1%232%7Cwww.baidu.com%7C%7C%7C%7C%23; _ga=GA1.2.56298346.1496219931; _gid=GA1.2.1160883161.1515720677; _gat=1; _jzqco=%7C%7C%7C%7C1515720677254%7C1.2037470421.1515463233195.1515745440969.1515748327226.1515745440969.1515748327226.undefined.0.0.35.35; MKT_Pagesource=PC; _bfi=p1%3D102002%26p2%3D102002%26v1%3D64%26v2%3D63'
}
FormData={
    '__VIEWSTATEGENERATOR':'DB1FBB6D',
    'cityName':'%E4%B9%9D%E5%AF%A8%E6%B2%9F',
    'checkIn':'2018-01-12',
    'checkOut':'2018-01-13',
    'page':1
}
url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxGetGroupProductList.aspx'
page = requests.post(url,data=FormData,headers=headers).text
print(page)