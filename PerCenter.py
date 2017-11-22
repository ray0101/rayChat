#!/usr/bin/env python3
# coding: utf-8

import pymysql
from PooledDB import Mysql

mysql = Mysql()
master = {}


def reciveSelf(msg):
    if msg == "最新消息":
        result = mysql.getOne("""select * from chat_record order by id desc""");
        return "[%s]%s:%s" % (result[7], result[3], result[4])
    else:
        return msg
