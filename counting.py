#coding=utf-8

from sqlHelper import MongoHelper
import time

mongo = MongoHelper()

def counting(table):
	if table is None:
		print('请指定要查询的table')
	else:
		while True:
		    count = mongo.select(table)
		    print('{} has {} items'.format(table, count['count']))
		    # for i in count['value']:
		    # 	print i
		    # print count['count']
		    time.sleep(3)

if __name__ == '__main__':
	counting('fangInfo')
	# counting(fangInfo)
