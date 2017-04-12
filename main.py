#!/usr/bin/env python3
# coding: utf-8
import re
import time
import pymysql
import itchat
import settings

master={}
@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)
def text_reply(msg):
    print msg
    returnmsg = ""
    try:
        new_member_name = re.compile(u'"(.*?)"邀请"(.*?)"加入了群聊').findall(msg['Content'])
        if len(new_member_name) > 0:
            invertuser = new_member_name[0]
            itchat.send(u'@Ray %s\u2005邀请了 @%s\u2005' % (invertuser[0], invertuser[1]), msg['FromUserName'])
            itchat.send(u'欢迎新成员 @%s\u2005' % invertuser[1], msg['FromUserName'])
            memberList = itchat.update_chatroom(msg['FromUserName'], detailedMember=True)
            ml=memberList["MemberList"]
            if len(ml)>0:
                for user in ml:
                    if user["NickName"]==invertuser[1]:
                        print u"新用户%s"%user["UserName"]
                    else:
                        print u"已存在%s" % user["UserName"]
        else:
            new_member_name = re.compile(u'"(.*?)"通过扫描"(.*?)"分享的二维码加入群聊').findall(msg['Content'])
            if len(new_member_name) > 0:
                invertuser = new_member_name[0]
                itchat.send(u'@Ray %s\u2005邀请了 @%s\u2005' % (invertuser[1], invertuser[0]), msg['FromUserName'])
                itchat.send(u'欢迎新成员 @%s\u2005' % invertuser[0], msg['FromUserName'])
                memberList = itchat.update_chatroom(msg['FromUserName'], detailedMember=True)
                print memberList
    except AttributeError:
        print "error"
        return
        # print "asdfs"
        # return new_member_name
@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    fromuser=msg["FromUserName"]
    print msg["FromUserName"]
    print msg["ToUserName"]
    # if master.has_key(msg["FromUserName"]):
    #     print fromuser
    # else:
    #     master[msg["FromUserName"]]=getMaster(msg["FromUserName"])

def dateFormat(strtime):
    x = time.localtime(strtime)
    return time.strftime('%Y-%m-%d %H:%M:%S', x)
def saveUser(userName,NickName,InviteUser,groupName):
    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8',
        use_unicode=True)
    cursor = connect.cursor()
    cursor.execute("""select * from wechat_users where  group_name=%s and username=%s""", (groupName,InviteUser))
    ret = cursor.fetchone()
    if ret:
        cursor.execute(
            """INSERT INTO wechat_users (username, nick_name, group_name, create_time, invite_num, pid, master) VALUES ( %s,  %s, %s,now(), 0, %s, 0)""",
                (userName,NickName,groupName,ret["id"]))
        connect.commit()
    else:
        print""
    connect.commit()
    cursor.close()
    connect.close()

def getMaster(groupname):
    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8',
        use_unicode=True)
    cursor = connect.cursor()
    cursor.execute("""select * from wechat_users where  master=1 and group_name=%s""",groupname)
    ret = cursor.fetchone()
    cursor.close()
    # conn.commit()
    connect.close()
    return ret["username"]
def afterLogin():
    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8',
        use_unicode=True)
    cursor =  connect.cursor()
    cursor.execute("""select * from wp_postmeta """)
    ret = cursor.fetchone()
    cursor.close()
    # conn.commit()
    connect.close()
    print ret

itchat.auto_login(loginCallback=afterLogin)
itchat.run()
