#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20171122
@author:wyl QQ635864540
python version 2.7
'''
__author__ = 'wyl QQ635864540'

import urllib
import urllib2
import re
import time


import writetosql
import getnewestarticles
import querysql

import readconfig

class ClsGetPhoneInfo:
	def __init__(self):
		self.phonecompiler = re.compile(r'<a href=\'([^\v\s]*?)\' id=\'postauthor[\d]*\' class=\'author b\'></a>[^\v]*?\'\',\'\',\'([^\v]*?)\',\'\',null,0 \)[\s]*?</script>', re.IGNORECASE)
		self.uidcompiler = re.compile(r'uid=([^\v]*?)$', re.IGNORECASE)
		self.nextpagecompiler = re.compile(r'<a href=\'([^\s]*?)\' title=\'[^\s]*?\' class=\'pager_spacer\'', re.IGNORECASE)
		self.usermoneycompiler = re.compile(r'\":\{\"uid\":([^\D\}]*?),[^\v]*?,\"money\":([-\d]*?),[^\v\}]*?\}', re.IGNORECASE)
		self.writesql = writetosql.WriteDataToSql()
		self.searchedurls = []
		self.querysql = querysql.ClsQuerySql()
		self.debug_on = True
		self.readconfig = readconfig.ClsReadConfigFile()
		#self.f = open('phonetype.txt', 'a')
		self.phonebrands=['iPhone','Xiaomi','samsung','HUAWEI','vivo','OnePlus','360','smartisan','Meizu',
			'ZUK','Gree','Sony','LENOVO','iPad','nubia','HTC','Hisense','Coolpad','GIONEE','LeMobile',
			'ZTE','Acer','HMD','OPPO','motorola','LGE','SHARP','alps','Delta','BBK','Changhong',
			'Amazon','BlackBerry','Essential','QiKU','PPTV','asus','Google','xiaolajiao','CMDC',
			'Kindle','iPod','IUNI','GO','DOOV']
		
	def __del__(self):
		#self.f.close()
		pass
				
	def GetPhoneInfoAndWriteToSQL(self, forumurl):
		if forumurl in self.searchedurls:
			return
		else:
			self.searchedurls.append(forumurl)
		userphonetyperesults=[]
		usermoneyresults = []
		normalurl = 'http://bbs.ngacn.cc'
		html = ''
		try:
			headers={
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
				'Accept-Language':'zh-CN,zh;q=0.8',
				'Cache-Control':'max-age=0',
				'Connection':'keep-alive',
				'Cookie':'%s',
				'Host':'bbs.ngacn.cc',
				'Upgrade-Insecure-Requests':'1',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
				}
			cookie = self.readconfig.GetNgaCookie()
			if cookie == '':
				print 'Please check \'config.txt\' file wether \'ngacookie\' is set or not.'
				return
			headers['Cookie'] = headers['Cookie'] % cookie
			request = urllib2.Request(url=forumurl,headers=headers)
			response = urllib2.urlopen(request)
			html = response.read()
			#f = open('html.txt', 'w')
			#f.write(html)
			#f.close()
			response.close()
			userphonetyperesults = self.phonecompiler.findall(html)
			usermoneyresults = self.usermoneycompiler.findall(html)
		except Exception as e:
			print 'Exception in GetPhoneInfoAndWriteToSQL:', str(e)
		for user_uid,user_money in usermoneyresults:
			usermoneyarray = []
			usermoneyarray.append(user_uid)
			usermoneyarray.append(user_money)
			#print usermoneyarray
			returnval = self.writesql.WriteDataToNgaUserMoneyTable(usermoneyarray)
			if  returnval== 0:
				if self.debug_on:
					print 'WriteDataToNgaUserMoneyTable success.'
			elif returnval == -1:
				if self.debug_on:
					print 'WriteDataToNgaUserMoneyTable failed......'
					print usermoneyarray
		for uidhref,phoneinfo in userphonetyperesults:
			#phoneinfo include:
			#HUAWEI DUK-AL20(Android 7.0)
			#iPhone 6(iOS 11.1.2)
			phonearray = self.ParsePhoneInfo(phoneinfo)
			uid = self.uidcompiler.findall(uidhref)[0]
			userinfoarray = []
			userinfoarray.append(uid)
			userinfoarray += phonearray
			if len(userinfoarray) != 4:
				continue
			if self.querysql.QueryNgaUserPhoneInfoTable(userinfoarray):
				continue
			else:
				retval = self.writesql.WriteDataToNgaUserPhoneInfoTable(userinfoarray)
				if retval == 0:
					if self.debug_on:
						print 'WriteDataToNgaUserPhoneInfoTable success.'
				elif retval == -1:
					if self.debug_on:
						print 'WriteDataToNgaUserPhoneInfoTable failed...........'
						print userinfoarray
		urls = self.nextpagecompiler.findall(html)
		#print 'urls:',urls
		for url in urls:
			if normalurl + url in self.searchedurls:
				continue
			#print 'normalurl+url:',normalurl+url
			self.GetPhoneInfoAndWriteToSQL(normalurl+url)
			continue
		
	def ParsePhoneInfo(self, phoneinfo):
		phonetypestartindex = phoneinfo.find(' ')
		phonesplitindex = phoneinfo.find('(')
		phonesysversionendindex = phoneinfo.find(')')
		phonearray = []
		if phonetypestartindex != -1 and phonesysversionendindex != -1 and phonesplitindex != -1:
			phonetype = phoneinfo[phonetypestartindex + 1:phoneinfo.find('(')]
			phonetype = phonetype.strip()
			phonebrand = 'unknown'
			for brand in self.phonebrands:
				if phonetype.lower().find(brand.lower()) != -1:
					if brand == 'iPad':
						phonebrand = 'iPhone'
					elif brand == 'iPod':
						phonebrand = 'iPhone'
					else:
						phonebrand = brand
					break
			phonesysversion = phoneinfo[phoneinfo.find('(')+1:phonesysversionendindex]
			phonesysversion = phonesysversion.strip()
			phonearray.append(phonebrand)
			phonearray.append(phonetype)
			phonearray.append(phonesysversion)
			#self.f.write(phonebrand + '|' + phonetype + '|' + phonesysversion + '\n')
		return phonearray
		
if __name__=='__main__':
	getarticles = getnewestarticles.GetNewestArticles()
	articles = getarticles.SearchArticals()
	cgpi = ClsGetPhoneInfo()
	for article in articles:
		headurl = 'http://bbs.ngacn.cc'
		cgpi.GetPhoneInfoAndWriteToSQL(headurl + article)
		#cgpi.GetPhoneInfoAndWriteToSQL('http://bbs.ngacn.cc/read.php?tid=12948688')
		#break
			
			
			