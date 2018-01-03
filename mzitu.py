#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
import requests
from bs4 import BeautifulSoup
import os
import re
import time

all_url = 'http://www.mzitu.com'

punctuation = '!,;:?"\''                             #用于去除文件名中含有标点符号
def removePunctuation(text):                          #去除标点符号的函数
    text = re.sub(r'[{}]+'.format(punctuation), '', text)
    return text.strip().replace(' ','')

#http请求头
Hostreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://www.mzitu.com'
               }
Picreferer = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer':'http://i.meizitu.net'
}
#此请求头破解盗链

start_html = requests.get(all_url,headers = Hostreferer)

#保存地址
path = '/mzitu/'

#找寻最大页数
soup = BeautifulSoup(start_html.text,"html.parser")
page = soup.find_all('a',class_='page-numbers')
max_page = page[-2].text


same_url = 'http://www.mzitu.com/page/'
for n in range(1,int(max_page)+1):
    ul = same_url+str(n)
    start_html = requests.get(ul, headers = Hostreferer)
    soup = BeautifulSoup(start_html.text,"html.parser")
    all_a = soup.find('div',class_='postlist').find_all('a',target='_blank')
    for a in all_a:
        # n = 1
        title = a.get_text() #提取文本
        if(title != ''):
            print("准备爬取："+title)

            #win不能创建带？的目录
            file = removePunctuation(title)
            if(os.path.exists(path+ file)):
                    #print('目录已存在')
                    flag=1
            else:
                os.makedirs(path+file)
                flag=0
            os.chdir(path+file)
            href = a['href']
            html = requests.get(href,headers = Hostreferer)
            mess = BeautifulSoup(html.text,"html.parser")
            pic_max = mess.find_all('span')
            pic_max = pic_max[10].text #最大页数
            if(flag == 1 and len(os.listdir(path+file)) >= int(pic_max)):
                print('已经保存完毕，跳过')
                continue
            for num in range(1,int(pic_max)+1):
                pic = href+'/'+str(num)
                html = requests.get(pic,headers = Hostreferer)
                mess = BeautifulSoup(html.text,"html.parser")
                pic_url = mess.find('img',alt = title)
                print(pic_url['src'])
                #exit(0)
                html = requests.get(pic_url['src'],headers = Picreferer)
                file_name = pic_url['src'].split(r'/')[-1]
                f = open(file_name,'wb')
                f.write(html.content)
                f.close()
            print('完成')
            time.sleep(15)
    print('第',n,'页完成')