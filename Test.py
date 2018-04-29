#!/usr/bin/env python3
# coding: utf-8
# import re
# str=u""""Ray"邀请"熙依达人"加入了群聊"""
# print str
from snownlp import SnowNLP
text = u"觉得我无理取闹。"
s = SnowNLP(text)
# s.sentiments
print s.sentiments
# new_member_name = re.compile(u'(.*?)邀请(.*?)加入了群聊').findall(str)
# name=1
# if name:
#     print name
# else:
#     print "11"
# # print new_member_name


