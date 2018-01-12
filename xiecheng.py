#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
from bs4 import BeautifulSoup
import requests

provinceDic = {}                                #存储省份信息,key为省份名称，values为省份对应链接
BaseUrl = 'http://hotels.ctrip.com'
url = 'http://hotels.ctrip.com/jiudian/'
def getProvinceInfo():
    html = requests.get(url).text
    bsObj = BeautifulSoup(html,'lxml')
    tmp = bsObj.find('div',{'class':'index_item sec_province'})
    provinceList = tmp.findAll('dt')[1:]
    for provinceInfo in provinceList:                   #provinceInfo包括省份名称与地址链接
        name = provinceInfo.text
        provinceUrl = provinceInfo.find('a')['href']
        provinceDic[name]=BaseUrl + provinceUrl
    return provinceDic

def getCityInfo(city):
    provinceDic = getProvinceInfo()
    cityInfoDIC = {}                # 存储城市酒店信息，元素为各城市酒店信息字典
    tmpDic = {}                      #用于存放具体城市链接与酒店数量的字典
    cityUrl = provinceDic[city + '酒店']
    html = requests.get(cityUrl).text
    bsObj = BeautifulSoup(html,'lxml')
    tagList = bsObj.find('ul',{'class':'p_n_list grid_8'}).findAll('li')
    for tag in tagList:
        cityName = tag.find('a').get_text()
        areaUrl = BaseUrl + tag.find('a')['href']
        hotelNum = tag.find('span').text
        tmpDic['名称'] = cityName
        tmpDic['链接'] = areaUrl
        tmpDic['酒店数量'] = hotelNum
        cityInfoDIC[cityName] = {'链接':areaUrl,'酒店数量':hotelNum}
    return cityInfoDIC


#http://hotels.ctrip.com/Domestic/Tool/AjaxGetGroupProductList.aspx
'''
Form Data={
cityName:九寨沟
checkIn:2018-01-12
checkOut:2018-01-13
page:1
}
'''
def getHotelInfo(areaUrl):
    areaUrl = 'http://hotels.ctrip.com/hotel/jiuzhaigou91'
    html = requests.get(areaUrl).text
    bsObj = BeautifulSoup(html,'lxml')
    countNum = bsObj.find('div',{'class':'total_htl_amount'}).find('b').text

getHotelInfo('http://hotels.ctrip.com/hotel/jiuzhaigou91')