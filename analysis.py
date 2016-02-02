# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import sqlite3 as sqlite
import time
import datetime
import clusters
from PIL import Image,ImageDraw

con = sqlite.connect('./data/myWeibo.db')

allData = con.execute('select * from myWeibodata').fetchall()

# time1 = datetime.datetime.strptime(allData[0][0],'%Y-%m-%d %H:%M')
# print time1#得到的字符串
# print time.mktime(time1.timetuple())#转化为时间戳


def makeDate(allData):
	allInfo = {}
	words = {}
	wordneed = []
	times = []
	for i in range(0,len(allData)):
		date = datetime.datetime.strptime(allData[i][0],'%Y-%m-%d %H:%M')
		dateTuple = time.mktime(date.timetuple())
		times.append(dateTuple)
		content = ''
		if allData[i][2] == 0:#转发
			content = allData[i][3]
		else:
			content = allData[i][1]
		jiebaContent = jieba.lcut(content,cut_all = False)#分词
		obj = {}
		# print jiebaContent
		for r in range(0,len(jiebaContent)):
			words[jiebaContent[r]] = 0
			obj.setdefault(jiebaContent[r],0)
			obj[jiebaContent[r]] = 1 if obj[jiebaContent[r]] == 0 else obj[jiebaContent[r]] + 1

		allInfo[dateTuple] = obj

	dataList = []

	for i in words:
		wordneed.append(i)

	for r in allInfo:
		print r
		clone = words
		theList = []
		for i in allInfo[r]:
			if i in words:
				clone[i] = allInfo[r][i]
		for n in clone:
			theList.append(clone[n])
		dataList.append(theList)

	return dataList,times,wordneed






data,time,word = makeDate(allData)
print 'done'
# print len(data)
clust = clusters.hcluster(data)
print 'done'
clusters.drawdendrogram(clust,time,jpeg = './myWeibo.jpg')