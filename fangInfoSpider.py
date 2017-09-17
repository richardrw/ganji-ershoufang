#coding=utf-8

from fangInfoParsing import getFangInfoFrom
from sqlHelper import MongoHelper
from multiprocessing import Pool

mongo = MongoHelper()
fangUrl = set(i['url'] for i in mongo.fangUrl.find())
fangInfoUrlOk = set(i['url'] for i in mongo.fangInfoUrlOk.find())
toBeCrawling = fangUrl - fangInfoUrlOk
# print(len(toBeCrawling))

if __name__ == '__main__':
	p = Pool()
	for url in toBeCrawling:
		p.apply_async(getFangInfoFrom, args=(str(url),))
	print('有{}个待爬取url'.format(len(toBeCrawling)))
	p.close()
	p.join()
	print('{}个待爬取Url已全部爬取完毕！'.format(len(toBeCrawling)))

	# for url in toBeCrawling:
	# 	getFangInfoFrom(url)
	# print('{}个待爬连接已全部爬取完毕'.format(len(toBeCrawling)))