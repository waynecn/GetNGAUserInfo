create table nga_user_phone_info
(
ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
user_uid varchar(20),
user_phonetype varchar(40),
user_phonesysversion varchar(30),
article_url varchar(255),
phone_brand varchar(30) default 'unknown',
update_time datetime default '0000-00-00 00:00:00',
PRIMARY KEY(ID)
);

drop table nga_user_phone_info;
commit;

#向表中插入手机品牌对应列
alter table nga_user_phone_info add column phone_brand varchar(30);

#更新用户手机品牌
update nga_user_phone_info set phone_brand='iPhone' where user_phonetype like 'iPhone%';
update nga_user_phone_info set phone_brand='Xiaomi' where user_phonetype like 'Xiaomi%';
update nga_user_phone_info set phone_brand='samsung' where user_phonetype like 'samsung%';
update nga_user_phone_info set phone_brand='HUAWEI' where user_phonetype like 'HUAWEI%';
update nga_user_phone_info set phone_brand='vivo' where user_phonetype like 'vivo%';
update nga_user_phone_info set phone_brand='OnePlus' where user_phonetype like 'OnePlus%';
update nga_user_phone_info set phone_brand='360' where user_phonetype like '360%';
update nga_user_phone_info set phone_brand='smartisan' where user_phonetype like 'smartisan%';
update nga_user_phone_info set phone_brand='Meizu' where user_phonetype like 'Meizu%';
update nga_user_phone_info set phone_brand='ZUK' where user_phonetype like 'ZUK%';
update nga_user_phone_info set phone_brand='Gree' where user_phonetype like 'Gree%';
update nga_user_phone_info set phone_brand='Sony' where user_phonetype like 'Sony%';
update nga_user_phone_info set phone_brand='LENOVO' where user_phonetype like 'LENOVO%';
update nga_user_phone_info set phone_brand='iPhone' where user_phonetype like 'iPad%';
update nga_user_phone_info set phone_brand='nubia' where user_phonetype like 'nubia%';
update nga_user_phone_info set phone_brand='HTC' where user_phonetype like 'HTC%';
update nga_user_phone_info set phone_brand='Hisense' where user_phonetype like 'Hisense%';
update nga_user_phone_info set phone_brand='Coolpad' where user_phonetype like '%Coolpad%';
update nga_user_phone_info set phone_brand='GIONEE' where user_phonetype like 'GIONEE%';
update nga_user_phone_info set phone_brand='LeMobile' where user_phonetype like 'LeMobile%';
update nga_user_phone_info set phone_brand='ZTE' where user_phonetype like 'ZTE%';
update nga_user_phone_info set phone_brand='Acer' where user_phonetype like 'Acer%';
update nga_user_phone_info set phone_brand='HMD' where user_phonetype like 'HMD%';
update nga_user_phone_info set phone_brand='OPPO' where user_phonetype like 'OPPO%';
update nga_user_phone_info set phone_brand='motorola' where user_phonetype like 'motorola%';
update nga_user_phone_info set phone_brand='LGE' where user_phonetype like 'LGE%';
update nga_user_phone_info set phone_brand='Letv' where user_phonetype like 'Letv%';

update nga_user_phone_info set phone_brand='SHARP' where user_phonetype like 'SHARP%';
update nga_user_phone_info set phone_brand='alps' where user_phonetype like 'alps%';
update nga_user_phone_info set phone_brand='Delta' where user_phonetype like 'Delta%';
update nga_user_phone_info set phone_brand='vivo' where user_phonetype like '%vivo%';
update nga_user_phone_info set phone_brand='Changhong' where user_phonetype like 'Changhong%';
update nga_user_phone_info set phone_brand='Amazon' where user_phonetype like 'Amazon%';
update nga_user_phone_info set phone_brand='BlackBerry' where user_phonetype like 'BlackBerry%';
update nga_user_phone_info set phone_brand='Essential' where user_phonetype like 'Essential%';
update nga_user_phone_info set phone_brand='QiKU' where user_phonetype like 'QiKU%';
update nga_user_phone_info set phone_brand='PPTV' where user_phonetype like 'PPTV%';
update nga_user_phone_info set phone_brand='asus' where user_phonetype like 'asus%';
update nga_user_phone_info set phone_brand='Google' where user_phonetype like 'Google%';
update nga_user_phone_info set phone_brand='xiaolajiao' where user_phonetype like 'xiaolajiao%';
update nga_user_phone_info set phone_brand='CMDC' where user_phonetype like 'CMDC%';
update nga_user_phone_info set phone_brand='Kindle' where user_phonetype like '%Kindle%';
update nga_user_phone_info set phone_brand='iPhone' where user_phonetype like 'iPod%';
update nga_user_phone_info set phone_brand='IUNI' where user_phonetype like 'IUNI%';
update nga_user_phone_info set phone_brand='GO' where user_phonetype like 'GO%';
update nga_user_phone_info set phone_brand='DOOV' where user_phonetype like '%DOOV%';
update nga_user_phone_info set phone_brand='Amazon' where user_phonetype like 'amzn%';
update nga_user_phone_info set phone_brand='unknown' where user_phonetype like 'unknown%';


#列出每个用户对应的手机型号或者系统有几个
select user_uid,count(user_uid) user_uid_count from nga_user_phone_info group by user_uid order by user_uid_count;

#列出特定用户的所有信息
select * from nga_user_phone_info where user_uid='38318523';


#列出手机型号排行
select user_phonetype 手机型号,count(user_phonetype) 数量 from nga_user_phone_info group by 手机型号 order by 数量 desc;

#列出以手机系统版本为主的手机型号排行榜
select user_phonetype,user_phonesysversion,count(user_phonesysversion) user_phonesysversion_count from nga_user_phone_info group by user_phonetype order by user_phonesysversion_count desc;

#列出手机品牌排行
select phone_brand 手机品牌,count(phone_brand) 品牌数量 from nga_user_phone_info group by 手机品牌 order by 品牌数量 desc;




create table nga_user_money_info
(
ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
user_uid varchar(20),
user_money varchar(20),
update_time datetime default '0000-00-00 00:00:00',
PRIMARY KEY(ID)
);

drop table nga_user_money_info;
commit;


select * from nga_user_money_info;

#查询用户金钱是否有多个值，有多个值表示有变动，匿名发帖或者匿名回复会扣钱。
select user_uid,count(user_uid) user_uid_count from nga_user_money_info group by user_uid having count(user_uid)>1 order by user_uid_count;


select * from nga_user_money_info where user_uid='40056370' order by update_time;


select user_uid,count(user_uid) user_uid_count from nga_user_money_info group by user_uid having count(user_uid)>1;


drop table temp_table;
commit;
create table temp_table(
ID bigint(20) unsigned NOT NULL AUTO_INCREMENT,
user_uid varchar(20),
user_uid_count int(20),
PRIMARY KEY(ID)
);





#将查询用户金钱变动的结果保存到临时表temp_table中。
insert into temp_table(user_uid,user_uid_count) 
select user_uid,count(user_uid) user_uid_count from nga_user_money_info group by user_uid having count(user_uid)>1;

#联合查出用户金钱变动的详细信息
select * from nga_user_money_info numi inner join temp_table tt on numi.user_uid=tt.user_uid order by numi.user_uid,numi.update_time;
select numi.user_uid,convert(numi.user_money,signed) cmoney,numi.update_time from nga_user_money_info numi inner join temp_table tt on numi.user_uid=tt.user_uid order by numi.user_uid,numi.update_time;



