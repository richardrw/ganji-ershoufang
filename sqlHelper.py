#!/usr/bin/python3
#coding=utf-8

#定义mongodb相关操作
import pymongo

class MongoHelper(object):
	def __init__(self):
		self.client = pymongo.MongoClient('localhost', 27017)
		self.ganjiCrawler = self.client['ganjiCrawler']
		self.cateUrl = self.ganjiCrawler['cateUrl']      #爬取类目信息，如：租房／二手房／新房等
		self.fangUrl = self.ganjiCrawler['fangUrl']      #爬取某类目下所有页的房源Url
		self.fangUrlOk = self.ganjiCrawler['fangUrlOk']     #存储某类目下第N页爬取成功的该页Url
		self.fangUrlBad = self.ganjiCrawler['fangUrlBad']   #存储某类目下第N页爬取失败的该页Url
		self.fangInfo = self.ganjiCrawler['fangInfo']    #爬取房源Url下的详细信息，如：面积／价格等
		self.fangInfoUrlOk = self.ganjiCrawler['fangInfoUrlOk']     #存储已成功爬取详细信息的房源Url
		self.fangInfoUrlBad = self.ganjiCrawler['fangInfoUrlBad']   #存储爬取详细信息失败的房源Url

		#建立字典，用于判断对哪个表进行操作
		self.tableDict = {
		    'cateUrl':self.cateUrl,
		    'fangUrl':self.fangUrl,
		    'fangUrlOk':self.fangUrlOk,
		    'fangUrlBad':self.fangUrlBad,
		    'fangInfo':self.fangInfo,
		    'fangInfoUrlOk':self.fangInfoUrlOk,
		    'fangInfoUrlBad':self.fangInfoUrlBad
		    }

	def insert(self, table=None, value=None):
		'''
		table ---> str
		value ---> dict
		'''
		if table is not None:
			if value is not None:
			    self.tableDict[table].insert(value)
			else:
				print('value is None. Insert Failed')
		else:
			print('tabel is None. Insert Failed')

	def delete(self, table=None, condition=None):
		'''
		table ---> str
		condition ---> dict  such as: {'url':'http://www.baidu.com'}
		'''
		if table is not None:
			self.tableDict[table].remove(condition)
		else:
			print('table is None. Delete Failed')

	def select(self, table=None, condition=None):
		'''
		table --->str
		condition --->dict such as: {'url':'http://www.baidu.com'}
		rerurn ---> result(is a dict)
		'''
		selectResult = self.tableDict[table].find(condition)
		count = selectResult.count()
		iterableResult = (i['url'] for i in self.tableDict[table].find(condition))
		result = {'count':count, 'value':iterableResult}
		return result

if __name__ == '__main__':
	mongo = MongoHelper()
	mongo.delete('fangInfoUrlBad')