#coding=utf-8

import requests
from bs4 import BeautifulSoup
# from getIPProxy import getIPProxyFrom
from sqlHelper import MongoHelper
import time
from config import userAgentList, proxyList
import random

mongo = MongoHelper()
# headers = {
# 	'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)'
#     }
linkTime = 1

def getFangInfoFrom(url):
	# proxies = getIPProxyFrom()
	proxies = {'http':'{}'.format(random.choice(proxyList))}
	headers = {'User-Agent':'{}'.format(random.choice(userAgentList))}
	try:
		print('现在开始爬取{}'.format(url))
		html = requests.get(url, headers=headers, proxies=proxies, timeout=5)
		if html.status_code == 404:
			mongo.insert('fangInfoUrlBad', {'url':url, 'reason':404})
			print('网页状态码为404，没有找到相关信息！')
		else:
		    bsObj = BeautifulSoup(html.content, 'lxml')
		    title = bsObj.select('p.card-title > i')[0]
		    #判断该Url是否存在有效信息
		    if len(title.get_text()) == 0:
		    	mongo.insert('fangInfoUrlBad', {'url':url, 'reason':'title is None'})
		    	print('title内容为空，没有找到有效信息！')
		    else:
		    	title = title.get_text()
		    	price = bsObj.select('span.price')[0].get_text()
		    	avgPrice = bsObj.select('span.unit')[0].get_text()
		    	infoList = bsObj.select('ul.er-list.f-clear > li > span.content')
		    	infoDict = {
		    	    'title':title,
		    	    'price':price,
		    	    'avgPrice':avgPrice,
		    	    'zhuangxiu':infoList.pop().get_text(),
		    	    'chanquan':infoList.pop().get_text(),
		    	    'xingzhi':infoList.pop().get_text(),
		    	    'niandai':infoList.pop().get_text(),
		    	    'dianti':infoList.pop().get_text(),
		    	    'leixing':infoList.pop().get_text(),
		    	    'louceng':infoList.pop().get_text(),
		    	    'chaoxiang':infoList.pop().get_text(),
		    	    'mianji':infoList.pop().get_text(),
		    	    'huxing':infoList.pop().get_text()
		    	    }
		    	mongo.insert('fangInfo', infoDict)
		    	mongo.insert('fangInfoUrlOk', {'url':url})
		    	print('{} --------->已爬取完成'.format(url))
	except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout):
		global linkTime
		linkTime += 1
		if linkTime < 3:
			print('链接失败，现在进行第{}次连接...'.format(linkTime+1))
			getFangInfoFrom(url)
		else:
			mongo.insert('fangInfoUrlBad', {'url':url, 'reason':'linkTimeOut'})
			print('已达连接上限，连接失败，爬取失败！')
	finally:
		time.sleep(1)