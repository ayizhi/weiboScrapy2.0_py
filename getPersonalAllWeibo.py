# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import urllib
import json
import re
import simplejson
import sqlite3 as sqlite
import getProxy
# import fs

def getPersonalAllWeibo(containerid,cookieJar):



	f = open(r'F:\py\22_weiboshiyan\data\myWeiboData.txt','w+')

	def getPage(containerid,pageNum,filename,opener):
		print pageNum

		url = 'http://m.weibo.cn/page/json?containerid='+ str(containerid) + '_-_WEIBO_SECOND_PROFILE_WEIBO&page=' + str(pageNum)
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1','Referer':'','Content-Type':'application/x-www-form-urlencoded'}
		req = urllib2.Request(url,'',headers)
		res = opener.open(req)


		info = res.read()
		dict_t = simplejson.loads(info)
		cards = dict_t["cards"][0]["card_group"]

		if len(cards)==0 : 
			print '没有了'
			return

		for i in range(0,len(cards)):
			
			date = myContent = zhuanfaContent = ifOrigin = zhuanfaOriginId = zhuanfaOriginName = "**"
			if 'mblog' in cards[i]:
				date = cards[i]['mblog']["created_at"]
				myContent = cards[i]['mblog']['text']#content
				ifOrigin = 1
				if 'retweeted_status' in cards[i]['mblog']:
					ifOrigin = 0
					zhuanfaContent = cards[i]['mblog']['retweeted_status']['text']#转发内容
					zhuanfaOriginId = cards[i]['mblog']['retweeted_status']['user']['id']#被转发者id
					zhuanfaOriginName = cards[i]['mblog']['retweeted_status']['user']['screen_name']#被转发者name

				filename.writelines([date,'======',myContent,'======',str(ifOrigin),'======',zhuanfaContent,'======',str(zhuanfaOriginId),'======',str(zhuanfaOriginName)])
				filename.writelines("+++++++++")
		
	proxyArr = getProxy.getProxy()
	cookie_support = urllib2.HTTPCookieProcessor(cookieJar)

	maxPage = 1000
	ipNum = 0
	pageNum = 0
	while pageNum < maxPage:
		ip = proxyArr[ipNum%len(proxyArr)]
		print ip
		proxy_handler = urllib2.ProxyHandler({'HTTP':ip})
		opener = urllib2.build_opener(proxy_handler,cookie_support,urllib2.HTTPHandler)
		try:
			getPage(containerid,pageNum,f,opener)
			pageNum = pageNum + 1

		except:
			print '这个代理不好用'
		ipNum = ipNum + 1




	filename.close()





