#coding=utf-8

import requests
from bs4 import BeautifulSoup
# import sys
# sys.path.append(r'C:\Users\Administrator\Desktop\ganjiFang')
from sqlHelper import MongoHelper
# from getIPProxy import getIPProxyFrom
import time
import os
from config import userAgentList, proxyList
import random

mongo = MongoHelper()
# headers = {
# 	'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
#     }
linkTime = 1

def getFangUrlFrom(url, page):
	# proxies = getIPProxyFrom()
	proxies = {'http':'{}'.format(random.choice(proxyList))}
	headers = {'User-Agent':'{}'.format(random.choice(userAgentList))}
	homeUrl = 'http://gz.ganji.com'
	pageUrl = '{}o{}/'.format(url, page)
	# pageUrl = url
	try:
		# print('child process {} start'.format(os.getpid()))
		print('现在开始爬取%s' %pageUrl)
		html = requests.get(pageUrl, headers=headers, proxies=proxies, timeout=5)
		bsObj = BeautifulSoup(html.content, 'lxml')
		findFangUrl = bsObj.select('div.f-list-item dd.dd-item.title > a')
		if len(findFangUrl) == 0:
			mongo.insert('fangUrlBad',{'url':pageUrl, 'reason':'findFangUrl is None'})
			print('没有找到相关房源Url信息，爬取失败！')
		else:
			fangUrl = (homeUrl + i.get('href') for i in findFangUrl)
			fangTitle = (i.get_text() for i in findFangUrl)
			for url, title in zip(fangUrl, fangTitle):
				if url in [i['url'] for i in mongo.fangUrl.find()]:
					print('%s---------->已存在！' %url)
				else:
					fangUrl = {'url':url, 'title':title}
					mongo.insert('fangUrl', fangUrl)
			mongo.insert('fangUrlOk', {'url':pageUrl})
			print('{} ---------->已爬取完成'.format(pageUrl))
	except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
		global linkTime
		linkTime += 1
		if linkTime < 3:
		    print('链接失败，现在进行第{}次连接...'.format(linkTime+1))
		    getFangUrlFrom(url, page)
		else:
			mongo.insert('fangUrlBad', {'url':pageUrl, 'reason':'linkTimeOut'})
			print('已达连接上限，连接失败，爬取失败！')
	finally:
		# print('进程{}爬取完成'.format(os.getpid()))
		time.sleep(1)

if __name__ == '__main__':
	getFangUrlFrom('http://dg.ganji.com/fang5', 11)