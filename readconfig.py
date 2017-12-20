#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20171220
@author:wyl QQ635864540
'''
__author__ = 'wyl QQ635864540'

class ClsReadConfigFile:
	def __init__(self):
		self.cookiefile = 'config.txt'
		self.mysqlconfigfile = 'mysqlconfig.txt'
		
	def GetNgaCookie(self):
		with open(self.cookiefile, 'r') as f:
			cookie = f.read()
			f.close()
			cookie = cookie.replace('\r','')
			results = cookie.split('\n')
			return results[1].strip()
		return ''
		
	def GetBaseUrl(self):
		with open(self.cookiefile, 'r') as f:
			cookie = f.read()
			f.close()
			cookie = cookie.replace('\r','')
			results = cookie.split('\n')
			return results[3].strip()
		return ''
		
	def GetDbUser(self):
		with open(self.mysqlconfigfile, 'r') as f:
			configures = f.read()
			configures = configures.replace('\r','')
			results = configures.split('\n')
			return results[1].strip()
		return ''
		
	def GetDbPwd(self):
		with open(self.mysqlconfigfile, 'r') as f:
			configures = f.read()
			configures = configures.replace('\r','')
			results = configures.split('\n')
			return results[3].strip()
		return ''
		
	def GetDbHost(self):
		with open(self.mysqlconfigfile, 'r') as f:
			configures = f.read()
			configures = configures.replace('\r','')
			results = configures.split('\n')
			return results[5].strip()
		return ''
		
	def GetDataBase(self):
		with open(self.mysqlconfigfile, 'r') as f:
			configures = f.read()
			configures = configures.replace('\r','')
			results = configures.split('\n')
			return results[7].strip()
		return ''
		
if __name__=='__main__':
	cls = ClsReadConfigFile()
	cookie = cls.GetNgaCookie()
	print cookie
	url = cls.GetBaseUrl()
	print url