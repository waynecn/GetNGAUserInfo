#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20171122
@author:wyl QQ635864540
'''
__author__ = 'wyl QQ635864540'

import urllib
import urllib2
import re
import time

import readconfig


ignorelist = []	


class GetNewestArticles:
	def __init__(self):
		self.compiler = re.compile(r'href=\'([^\s]*?)\'[\s]*id=', re.IGNORECASE)
		self.commentcompiler = re.compile(r'class=\'forumbox postbox\'', re.IGNORECASE)
		self.multipagecompiler = re.compile(r'(name=\'pageball\' id=\'pagebtop\'[^\\\\]*?</div>)', re.IGNORECASE)
		self.titlecompiler = re.compile(r'id=\'postsubject0\'>([^\t\n\r\f\v]*?)</h3>',re.IGNORECASE)
		self.contentcompiler = re.compile(r'id=\'postcontent0\' class=\'postcontent ubbcode\'>([^\t\n\r\f\v]*?)</p>', re.IGNORECASE)
		self.readconfig = readconfig.ClsReadConfigFile()
		
	def SearchArticals(self):
		result = []
		url = self.readconfig.GetBaseUrl()
		if url == '':
			print 'Please check \'config.txt\' file wether \'baseurl\' is set or not.'
			return
		cookie = self.readconfig.GetNgaCookie()
		if cookie == '':
			print 'Please check \'config.txt\' file wether \'ngacookie\' is set or not.'
			return
		headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Language':'zh-CN,zh;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Cookie':'%s',#你的cookie
			'Host':'bbs.ngacn.cc',
			'Referer':'http://bbs.ngacn.cc/thread.php?fid=-7',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
			}
		headers['Cookie'] = headers['Cookie'] % cookie
		try:
			request = urllib2.Request(url=url, headers=headers)
			response = urllib2.urlopen(request)
			html = response.read()
			#print html
			response.close()
			result = self.compiler.findall(html)
		except Exception as e:
			print 'Exception in SearchArticals:',str(e)
		return result
		
	def GetZeroCommentAr(self, results=None):
		headurl = 'http://bbs.ngacn.cc'
		commentcount = 0
		for res in results:
			normalurl = headurl + res
			if normalurl in ignorelist:
					continue
			else:
				try:
					request = urllib2.Request(url=normalurl, headers = self.headers)
					response = urllib2.urlopen(request)
					html = response.read()
					response.close()
					comments = self.commentcompiler.findall(html)
					commentcount=len(comments)-1
					if commentcount != 0:
						continue
					pages = self.multipagecompiler.findall(html)
					titles = self.titlecompiler.findall(html)
					print 'url:',normalurl
					print ''
					print u'    标题:    '
					print titles[0]
					contents = self.contentcompiler.findall(html)
					contentresult = contents[0].replace('<br/>','\n')
					print ''
					print u'    内容:    '
					print contentresult
					print '**********************************'
					print '*                                *'
					print '*                                *'
					print '*                                *'
					print '**********************************'
					print u'输入0忽略该帖，查找下一个帖子。输入其他表示准备回复该贴。'
					select = raw_input()
					if select == '0':
						ignorelist.append(normalurl)
						break
					if normalurl.find('tid=') == -1:
						print 'no tid found in:',normalurl
						return
					tid = normalurl[normalurl.find('tid=') + 4:]
					pm = postcomment.NGAPost(normalurl, tid)
					pm.Post()
				except Exception as e:
					print 'Exception in GetZeroCommentAr:',str(e)
		
		
				
			
if __name__=='__main__':
	gna=GetNewestArticles()
	while True:
		results = gna.SearchArticals()
		gna.GetZeroCommentAr(results)