#coding=utf-8

from fangUrlParsing import getFangUrlFrom
from multiprocessing import Pool
import os
import time
from sqlHelper import MongoHelper

if __name__ == '__main__':
	url = 'http://gz.ganji.com/fang5/'
	print('Parent process {} start'.format(os.getpid()))
	p = Pool()
	for page in range(1, 300):
		p.apply_async(getFangUrlFrom, args=(url, page))
	p.close()
	p.join()
	print('类目{}下所有页面已爬取完毕!'.format(url))

    #从‘fangUrlBad'表中提取url，重新爬取之前爬取失败的url
    # mongo = MongoHelper()
    # badUrlList = set(str(i['url']) for i in mongo.fangUrlBad.find())
    # p = Pool()
    # for url in badUrlList:
    # 	p.apply_async(getFangUrlFrom, args=(url, None))
    # p.close()
    # p.join()
    # print('badUrl爬取完成')