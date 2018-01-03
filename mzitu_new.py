#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Chenxiforever
import requests
from bs4 import BeautifulSoup
import os
import re
import time

class mzitu:
    all_url = 'http://www.mzitu.com'
    same_url = 'http://www.mzitu.com/page/'
    path = '/mzitu/'  # 保存地址
    # http请求头
    Hostreferer = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Referer': 'http://www.mzitu.com'
    }
    Picreferer = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        'Referer': 'http://i.meizitu.net'
    }
    start_html = requests.get(all_url,headers = Hostreferer)

    def removePunctuation(self,text):                             #去除标点符号的函数
        punctuation = '!,;:?"\''                            # 用于去除文件名中含有标点符号
        text = re.sub(r'[{}]+'.format(punctuation), '', text)
        return text.strip().replace(' ','')


    #找寻最大页数
    def get_max_page(self):
        soup = BeautifulSoup(self.start_html.text,"html.parser")
        page = soup.find_all('a',class_='page-numbers')
        max_page = page[-2].text
        return max_page


    def get_pic(self):
        max_page = int(self.get_max_page())
        for n in range(1, max_page + 1):
            ul = self.same_url + str(n)
            start_html = requests.get(ul, headers=self.Hostreferer)
            soup = BeautifulSoup(start_html.text, "html.parser")
            all_a = soup.find('div', class_='postlist').find_all('a', target='_blank')
            for a in all_a:
                # n = 1
                title = a.get_text()  # 提取文本
                if (title != ''):
                    print("准备爬取：" + title)

                    # win不能创建带？的目录
                    file = self.removePunctuation(title)
                    if (os.path.exists(self.path + file)):
                        # print('目录已存在')
                        flag = 1
                    else:
                        os.makedirs(self.path + file)
                        flag = 0
                    os.chdir(self.path + file)
                    href = a['href']
                    html = requests.get(href, headers=self.Hostreferer)
                    mess = BeautifulSoup(html.text, "html.parser")
                    pic_max = mess.find_all('span')
                    pic_max = pic_max[10].text  # 最大页数
                    if (flag == 1 and len(os.listdir(self.path + file)) >= int(pic_max)):
                        print('已经保存完毕，跳过')
                        continue
                    for num in range(1, int(pic_max) + 1):
                        pic = href + '/' + str(num)
                        html = requests.get(pic, headers=self.Hostreferer)
                        mess = BeautifulSoup(html.text, "html.parser")
                        pic_url = mess.find('img', alt=title)
                        print(pic_url['src'])
                        # exit(0)
                        html = requests.get(pic_url['src'], headers=self.Picreferer)
                        file_name = pic_url['src'].split(r'/')[-1]
                        f = open(file_name, 'wb')
                        f.write(html.content)
                        f.close()
                    print('完成')
                    time.sleep(15)
            print('第', n, '页完成')

def main():
    pic = mzitu()
    pic.get_pic()

if __name__ == '__main__':
    main()

