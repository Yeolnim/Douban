# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import pymongo
import re
from lxml import etree
import time,random

# 建立数据库
client = pymongo.MongoClient('localhost',27017)
douban = client['filmtest']
# 建表
url_list = douban['url_list']
item_detail = douban['item_detail']

# 用户代理
user_agent = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
# 头文件
headers = {
        'Host': 'movie.douban.com',
        'User-Agent': random.choice(user_agent)# 随机取
    }

# 爬取网页的通用框架
def getHTMLText(url):
    try:
        r=requests.request("get",url,headers=headers,timeout=10)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "exception"

# 获取全部地址
def getAllUrls():

    urls=[]
    url="https://movie.douban.com/top250?start="
    for i in range(0,249,25):
        urls.append(url+str(i))
    return urls

# 获取全部链接
def getAllLinks(urls):

    for url in urls:
        html=getHTMLText(url)# 获取网页的内容
        soup=BeautifulSoup(html,"lxml")# 对获取的网页内容按照特定的解析器解析
        links = soup.select("div > div.info > div.hd > a")

        for link in links:
            allLinks=link.get("href")
            url_list.insert({'url': allLinks}) # 链接插入链接表
            print(allLinks)

            # xpath用
            data = requests.get(allLinks,headers=headers).text
            s = etree.HTML(data)

            time.sleep(random.random() * 3)# 随机延时

            # re用
            html = requests.get(allLinks,headers=headers)

            allFilm = s.xpath('//*[@id="content"]/h1/span[1]/text()')[0] # 电影名
            allYear = re.findall('<span class="year">\((.*?)\)</span>', html.text, re.S)[0]# 括号里的年份
            allScore = s.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0] # 评分
            allDirector = s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0] # 导演
            allCountry = re.findall('制片国家/地区:</span>\ (.*?)<br/>', html.text, re.S)[0].split(" ")[0]# 空格后的国家

            # 信息插入信息表
            item_detail.insert_one({
                'film': allFilm,
                'year': allYear,
                'score': allScore,
                'director': allDirector,
                'country': allCountry,
            })

urls=getAllUrls()
getAllLinks(urls)