# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import random
import lxml.html as HTML
import cookielib
import re
import types
from PIL import Image
import cStringIO
import getWeiboPage
import getPersonalAllWeibo
import sqlite3 as sqlite

class Scrapy():
	def __init__(self,username,pwd,enableProxy=False):
		print 'Initializing WeiboLogin'

		self.username = username
		self.password = pwd
		self.enableProxy = enableProxy
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1','Referer':'','Content-Type':'application/x-www-form-urlencoded'}

	def EnableCookie(self,enableProxy):
		self.cookieJar = cookielib.LWPCookieJar()
		cookie_support = urllib2.HTTPCookieProcessor(self.cookieJar)
		if enableProxy:
			proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})
			opener = urllib2.build_opener(proxy_support,cookie_support,urllib2.HTTPHandler)
			print 'proxy enabled'
		else:
			opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)

		urllib2.install_opener(opener)
		# return cookieJar

	def get_rand(self,url):
		req = urllib2.Request(url,urllib.urlencode({}),self.headers)
		res = urllib2.urlopen(req)
		login_page = res.read()
		rand = HTML.fromstring(login_page).xpath('//form/@action')[0][16:]
		vk = HTML.fromstring(login_page).xpath('//input[@name="vk"]/@value')[0]
		passwordName = HTML.fromstring(login_page).xpath('//input[@type = "password"]/@name')[0]
		
		return rand,vk,passwordName

	def yanzhengma(self,page):
		# 因为有验证码，需要弹出让用户输入
		# 如果有验证码
		yanzhengma = ''
		for i in HTML.fromstring(page).xpath('//img'):
			if 'http://weibo.cn/interface' in i.xpath('./@src')[0]:
				yanzhengma = i.xpath('./@src')[0]
				break
		theFile = cStringIO.StringIO(urllib2.urlopen(yanzhengma).read())
		im = Image.open(theFile)
		im.show()
		theYanZhengNum = raw_input('请输入图片中的验证码: '.encode('gbk'))
		return theYanZhengNum

	def login(self,cookie_filename=None):
		self.EnableCookie(self.enableProxy)
		
		url = 'http://3g.sina.com.cn/prog/wapsite/sso/login.php?ns=1&revalid=2&backURL=http%3A%2F%2Fweibo.cn%2F&backTitle=%D0%C2%C0%CB%CE%A2%B2%A9&vt='
		rand,vk,passwordName = self.get_rand(url)
		thePostDict = {
			'mobile':self.username,
			passwordName:self.password,
			'remenber':'on',
			'backURL':'http://weibo.cn/',
			'backTitle':'新浪微博',
			'vk':vk,
			'submit':'登录',
			'encoding':'utf-8'
			}
		data = urllib.urlencode(thePostDict)
		loginUrl = 'http://login.weibo.cn/login/'+rand
		req = urllib2.Request(loginUrl,data,self.headers)
		res = urllib2.urlopen(req)
		page = res.read()
		
		#如果有验证码
		if len(HTML.fromstring(page).xpath('//img')) <= 2:
			print '有验证码'.encode('gbk')
			yanzhengma = self.yanzhengma(page)
			print '验证码是：'.encode('gbk'),yanzhengma
			#提取sessionID
			cookies = res.headers['Set-cookie']
			cookie = cookies[cookies.index('_T_WM='):]
			sessionId = cookie[6:cookie.index(';')]
			#提取capID
			capId = HTML.fromstring(page).xpath('//input[@name="capId"]/@value')[0]
			thePostDict.update({#合并两个dict
				'capId':capId,
				'PHPSESSID':sessionId,
				'code':yanzhengma,
				})
			#再次发送请求
			req = urllib2.Request(loginUrl,urllib.urlencode(thePostDict),self.headers)
			res = urllib2.urlopen(req)
			page = res.read()
			
		#url重定向	
		link = HTML.fromstring(page).xpath('//a/@href')[0]
		if type(link.find('http://'))==-1:
			link = 'http://weibo.cn'+link

		try:
			req = urllib2.Request(link,headers = self.headers)
			page2 = urllib2.urlopen(req)
		except:
			print 'Login error'
			return False

		print 'Login Success'
		# print page2.read().encode('gbk')
		return True

username = '15905209533@163.com'
pwd = 'Zhangyizhi112358'
aaa = Scrapy(username,pwd)

if aaa.login() == True:
	containerid = '1005051950964011'
	cookie = aaa.cookieJar
	getPersonalAllWeibo.getPersonalAllWeibo(containerid,cookie)

