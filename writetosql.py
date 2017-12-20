#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
Created on 20171122
@author:wyl QQ635864540
'''
__author__ = 'wyl QQ635864540'



import MySQLdb

import readconfig


class WriteDataToSql:
	def __init__(self):
		readconfigs = readconfig.ClsReadConfigFile()
		self.dbuser = readconfigs.GetDbUser()
		self.dbpwd = readconfigs.GetDbPwd()
		self.host = readconfigs.GetDbHost()
		self.dbase = readconfigs.GetDataBase()
		self.steam_package_detail_table = 'steam_package_details_test'
		self.nga_user_phone_info_table = 'nga_user_phone_info'
		self.nga_user_money_info_table = 'nga_user_money_info'
		self.db = MySQLdb.connect(self.host, self.dbuser, self.dbpwd, self.dbase)
		self.cursor = self.db.cursor()
	
	"""
	create table steam_package_details_test
	(
	ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
	user_account varchar(255),
	game_name varchar(255),
	item_name varchar(255),
	normal_price decimal(20,3),
	sale_price decimal(20,3),
	item_amount int(10),
	image_src varchar(255),
	update_time datetime default '0000-00-00 00:00:00',
	PRIMARY KEY(ID)
	);
	"""
	
	def WriteDataToSteamPackageDetailTable(self, user_acount,game_name, item_name, normal_price, sale_price,item_amount, image_src):
		sql = """insert into %s(user_account,
			game_name,item_name,normal_price,sale_price,item_amount,image_src,update_time)
			values(\'%s\',\'%s\',\'%s\',%s,%s,%s,\'%s\',sysdate())"""
		sql = sql % (self.steam_package_detail_table, user_acount, game_name, item_name, normal_price, sale_price, item_amount, image_src)
		#print sql			
		try:
			self.cursor.execute(sql)
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			return False
			
	def WriteDataToNgaUserPhoneInfoTable(self, userinfoarray = []):
		querysql = """select * from %s where user_uid=\'%s\' and user_phonetype=\'%s\' and user_phonesysversion=\'%s\'"""
		querysql = querysql % (self.nga_user_phone_info_table,userinfoarray[0], userinfoarray[2], userinfoarray[3])
		sql = """insert into %s(user_uid,user_phonetype,user_phonesysversion,update_time,phone_brand)
			values(\'%s\',\'%s\',\'%s\',sysdate(),\'%s\')"""
		sql = sql % (self.nga_user_phone_info_table,userinfoarray[0], userinfoarray[2], userinfoarray[3],userinfoarray[1])
		try:
			self.cursor.execute(querysql)
			results = self.cursor.fetchall()
			if len(results) == 0:
				self.cursor.execute(sql)
				self.db.commit()
				return 0
			else:
				return 1
		except Exception as e:
			self.db.rollback()
			print userinfoarray,'|',str(e)
			return -1
			
	def WriteDataToNgaUserMoneyTable(self, usermoneyarray=[]):
		querysql = """select * from %s where user_uid=\'%s\' and user_money=\'%s\'"""
		querysql = querysql % (self.nga_user_money_info_table,usermoneyarray[0], usermoneyarray[1])
		sql = """insert into %s(user_uid,user_money,update_time)
			values(\'%s\',\'%s\',sysdate())"""
		sql = sql % (self.nga_user_money_info_table,usermoneyarray[0], usermoneyarray[1])
		try:
			self.cursor.execute(querysql)
			results = self.cursor.fetchall()
			if len(results) == 0:
				self.cursor.execute(sql)
				self.db.commit()
				return 0
			else:
				return 1
		except Exception as e:
			self.db.rollback()
			print usermoneyarray,'|',str(e)
			return -1
	
	def __del__(self):
		self.cursor.close()
		print 'close db'
		self.db.close()
		
		
		
		
if __name__ == '__main__':
	wd = WriteDataToSql()
	wd.WriteDataToSteamPackageDetailTable('540310164','PUBG', 'Tracket Suit', '0.07','0.05', '6')