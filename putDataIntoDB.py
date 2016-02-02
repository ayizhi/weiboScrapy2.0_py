# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sqlite3 as sqlite
import re

con = sqlite.connect('./data/myWeibo.db')

con.execute('create table if not exists myWeibodata(date,myContent,ifOrigin,zhuanFaContent,zhuanFaOrigin,ZhuanFaId)')

f = open('./data/myWeiboData.txt')

strs = f.readlines()

f.close()

arr = strs[0].split("+++++++++")
wrongArr = []

a1 = re.compile(r'\<.*\>')

wrongFile = open('./data/wrongWeibo.txt','w+')

for i in range(0,len(arr)):
	theData = arr[i].split('======')
	if len(theData)<6:
		continue
	date = theData[0]
	if len(date) == 11:
		date = '2016-' + date
	myContent = a1.sub('',theData[1])
	ifOrigin = theData[2]
	zhuanFaContent = a1.sub('',theData[3])
	zhuanFaId = theData[4]
	zhuanFaOrigin = theData[5]
	
	try:
		# print (str(date),str(myContent),str(ifOrigin),str(zhuanFaContent),str(zhuanFaOrigin),str(zhuanFaId))
		con.execute("insert into myWeibodata values ('%s','%s','%s','%s','%s','%s')" % (str(date),str(myContent),str(ifOrigin),str(zhuanFaContent),str(zhuanFaOrigin),str(zhuanFaId)))
	except:
		wrongArr.append(i)
		wrongFile.writelines(str(i))
		wrongFile.writelines('')
		print i,'有错'
		print arr[i].split('======')
		con.execute('''insert into myWeibodata values ("%s","%s","%s","%s","%s","%s")''' % (str(date),str(myContent),str(ifOrigin),str(zhuanFaContent),str(zhuanFaOrigin),str(zhuanFaId)))

con.commit()
