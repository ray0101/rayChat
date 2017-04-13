#!/usr/bin/env python3
# coding: utf-8
import re
import time
import pymysql
import itchat
import settings
from PooledDB import Mysql

mysql = Mysql()
master={}
@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)
def text_reply(msg):
    print msg
    groupInfo=mysql.getOne("""select * from wechat_group where group_ids=%s""", msg['FromUserName'])
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
                        # saveUser(user["UserName"],user["NickName"],,groupInfo["NickName"])
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
    inviteId=0;
    if InviteUser!="":
        result= mysql.getOne("""select * from wechat_users where  group_name=%s and username=%s""", (groupName,InviteUser))
        if result:
            inviteId=mysql.insertOne(
                """INSERT INTO wechat_users (username, nick_name, group_name, create_time, invite_num, pid, master) VALUES ( %s,  %s, %s,now(), 0, %s, 0)""",
                    (userName,NickName,groupName,0))
        else:
            inviteId=result["id"]

    mysql.insertOne(
            """INSERT INTO wechat_users (username, nick_name, group_name, create_time, invite_num, pid, master) VALUES ( %s,  %s, %s,now(), %s, %s, 0)""",
            (userName, NickName, groupName,0,inviteId))
    mysql.update("""update wechat_users set invite_num=invite_num+1 where id=%s """,inviteId);

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
    chatrooms=itchat.get_chatrooms()
    for chatroom in chatrooms:
        if chatroom["IsOwner"]:
            mygroup=mysql.getOne("""select * from wechat_group where group_name=%s""",chatroom["NickName"])
            memberList = itchat.update_chatroom(chatroom['UserName'], detailedMember=True)
            for member in memberList["MemberList"]:
                result = mysql.getOne("select * from wechat_users where username=%s", member["UserName"])
                if result:
                    print "已存在用户" + member["NickName"]
                else:
                    saveUser(member["UserName"], member["NickName"], "", chatroom["NickName"])
            if mygroup:
                mysql.update("update wechat_group set group_ids=%s where group_name=%s",(chatroom["UserName"],chatroom["NickName"]))
            else:
                mysql.insertOne("INSERT INTO wechat_group (group_name, group_ids, owner, manager_id, remark) VALUES ( %s, %s, 0, 0, %s)",(chatroom["NickName"],chatroom["UserName"]," "))

    # print chatroom
def saveGroup(groupNames,groupIds):
    connect = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8',
        use_unicode=True)
    cursor = connect.cursor()

itchat.auto_login(loginCallback=afterLogin)
itchat.run()
