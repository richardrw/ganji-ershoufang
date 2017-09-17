#!/usr/bin/python3
#coding=utf-8

import requests
from bs4 import BeautifulSoup
from sqlHelper import MongoHelper

mongo = MongoHelper()

headers = {
	'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
    }

def getCateFrom(url):
    homeUrl = 'http://dg.ganji.com/fang'
    try:
        html = requests.get(url, headers=headers, timeout=5)
        bsObj = BeautifulSoup(html.content, 'lxml')
        findCate = bsObj.select('div.i-footer > ul.f-nav > li > a')
        urlList = (homeUrl + i.get('href') for i in findCate)
        titleList = (i.get_text() for i in findCate)
        for url, title in zip(urlList,titleList):
            cateUrl = {'url':url, 'title':title}
            mongo.insert('cateUrl', cateUrl)
        print('类目爬取完成，类目Url已存储到cateUrl表中')
    except requests.exceptions.ConnectTimeout:
    	print('链接超时，爬取失败！')

if __name__ == '__main__':
	url = 'http://dg.ganji.com/fang/'
	getCateFrom(url)
