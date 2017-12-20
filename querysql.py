#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20171122
@author:wyl QQ635864540
'''
__author__ = 'wyl QQ635864540'


import MySQLdb

import readconfig

class ClsQuerySql:
	def __init__(self):
		readconfigs = readconfig.ClsReadConfigFile()
		self.dbuser = readconfigs.GetDbUser()
		self.dbpwd = readconfigs.GetDbPwd()
		self.host = readconfigs.GetDbHost()
		self.dbase = readconfigs.GetDataBase()
		self.steam_package_detail_table = 'steam_package_details'
		self.nga_user_phone_info_table = 'nga_user_phone_info'
		self.db = MySQLdb.connect(self.host, self.dbuser, self.dbpwd, self.dbase)
		self.cursor = self.db.cursor()
		
	def QueryNgaUserPhoneInfoTable(self,userinfoarray = []):
		sql = """select * from %s where user_uid=\'%s\' and user_phonetype=\'%s\' and user_phonesysversion=\'%s\'"""
		sql = sql % (self.nga_user_phone_info_table,userinfoarray[0],userinfoarray[2],userinfoarray[3])
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			if len(results) == 0:
				return False
			else:
				return True
		except Exception as e:
			print 'Exception in QueryNgaUserPhoneInfoTable:',str(e)
			return True
	
	def __del__(self):
		self.cursor.close()
		self.db.close()
			
			
if __name__=='__main__':
	qsql = ClsQuerySql()
	index = 0
	while True:
		array = []
		array.append('386509542')
		array.append('Xiaomi MI NOTE LTE')
		array.append('Android 6.0.1')
		if qsql.QueryNgaUserPhoneInfoTable(array):
			print 'Founded'
		else:
			print 'Not founded'
		index += 1
		if index == 10:
			break