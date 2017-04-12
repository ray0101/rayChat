#!/usr/bin/env python3
# coding: utf-8
import re
str=u""""Ray"邀请"熙依达人"加入了群聊"""
print str
new_member_name = re.compile(u'(.*?)邀请(.*?)加入了群聊').findall(str)
# print new_member_name
# DROP TABLE IF EXISTS  wechat_users;
# CREATE TABLE
#   wechat_users
# (
#   id INT NOT NULL AUTO_INCREMENT COMMENT 'ID',
#   username varchar(100) default '' COMMENT'微信用户名',
#   nick_name varchar(100) default '' COMMENT '微信昵称',
#   group_name varchar(100) default '' COMMENT'群名称',
#   create_time TIMESTAMP  COMMENT '加入时间',
#   invite_num int default 0 COMMENT '邀请人数',
#   pid int default 0 COMMENT '被邀请人ID' ,
#   master int default 0 COMMENT '管理员id',
#    PRIMARY KEY (id)
# )  ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='微信组邀请表';
