#!/usr/bin/env python3
# coding: utf-8
import re
import time
import pymysql
import itchat
import settings
import logging
from PooledDB import Mysql
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
mysql = Mysql()
master = {}


@itchat.msg_register(itchat.content.NOTE, isGroupChat=True)
def text_reply(msg):
    logging.debug(msg["Content"])
    groupInfo = mysql.getOne("""select * from wechat_group where group_ids=%s""", msg['FromUserName'])
    try:
        new_member_name = re.compile(u'"(.*?)"邀请"(.*?)"加入了群聊').findall(msg['Content'])
        if len(new_member_name) > 0:
            logging.debug("邀请方式")
            invertuser = new_member_name[0]
            if getUser("",invertuser[1],groupInfo[1]):
                print "已经邀请过该用户"
            else:
                welcomNewMember(invertuser[1], invertuser[0], groupInfo[1],  msg['FromUserName'])
        elif msg["Content"].find(u"你邀请")>=0:
            new_member_name = re.compile(u'你邀请"(.*?)"加入了群聊').findall(msg['Content'])
            if len(new_member_name) > 0:
                invertuser = new_member_name[0]
                if getUser("",invertuser, groupInfo[1]):
                    print "已经邀请过该用户"
                else:
                    log
                    welcomNewMember(invertuser, "", groupInfo[1], msg['FromUserName'])
        else:
            new_member_name = re.compile(u'"(.*?)"通过扫描"(.*?)"分享的二维码加入群聊').findall(msg['Content'])
            if len(new_member_name) > 0:
                invertuser = new_member_name[0]
                welcomNewMember(invertuser[1], invertuser[0], groupInfo[1], msg['FromUserName'])
            else:
                print msg["Content"]
    except AttributeError:
                print "error"
                return
    print "done"


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    fromuser = msg["FromUserName"]
    print msg["FromUserName"]
    print msg["ToUserName"]
    # if master.has_key(msg["FromUserName"]):
    #     print fromuser
    # else:
    #     master[msg["FromUserName"]]=getMaster(msg["FromUserName"])


def dateFormat(strtime):
    x = time.localtime(strtime)
    return time.strftime('%Y-%m-%d %H:%M:%S', x)
def getUser(wechatId,remarkName,groupName):
    if wechatId=="":
        result = mysql.getOne("""select * from wechat_users where  group_name=%s and back_name=%s""",
                              (groupName, remarkName))
        return result
    else:
        result = mysql.getOne("""select * from wechat_users where  group_name=%s and wechat_id=%s""",
                              (groupName, wechatId))
        return result

def saveUser(userName, NickName, wxId, InviteUser, groupName,back_name):
    inviteId = 0;
    if InviteUser != "":
        result = mysql.getOne("""select * from wechat_users where  group_name=%s and back_name=%s""",
                              (groupName, InviteUser))
        if result:
            inviteId = result[0]
        else:
            inviteId = 0
    result = mysql.getOne("""select * from wechat_users where  group_name=%s and wechat_id=%s""",
                          (groupName, wxId))
    if result:
        mysql.update("""update wechat_users set username=%s,nick_name=%s where wechat_id=%s """,
                     (userName, NickName, wxId));
    else:
        mysql.update("""update wechat_users set invite_num=invite_num+1 where id=%s """, inviteId);
        newid=mysql.insertOne(
            """INSERT INTO wechat_users (username, nick_name, group_name, create_time, invite_num, pid, master,wechat_id,back_name) VALUES ( %s,  %s, %s,now(), %s, %s, 0,%s,%s)""",
            (userName, NickName, groupName, 0, inviteId, wxId,back_name))
        if back_name=="":
            mysql.update("""UPDATE wechat_users set back_name=%s where id=%s""",('%s%s'%(groupName,newid),newid))
            myback=u"%s%s"% (groupName, newid)
            itchat.set_alias(userName, myback)
        return newid

def welcomNewMember(NickName,invteName,GroupName,FromId):
    logging.debug("欢迎新成员:%s %s %s"%(NickName,GroupName))
    if getUser("", NickName, GroupName):
        print "已经邀请过该用户"
    else:
        #获取邀请人信息
        result = getUser("",invteName, GroupName)
        inviteNickName=""
        inviteNum=0
        if result:
            inviteNickName=result[2]
            inviteNum=int(result[7])+1
            #获取群成员列表
        chatRoom = itchat.update_chatroom(FromId, detailedMember=True)
        ml = chatRoom["MemberList"]
        for user in ml:
            if user["NickName"] == NickName:
                logging.debug("找到新用户%s" % (NickName, GroupName))
                if NickName.find(chatRoom["NickName"])>=0:
                    print "has exists" + user["NickName"] + "" + user["Alias"]
                else:
                    itchat.send(u'欢迎新成员 @%s\u2005' % NickName, FromId)
                    if inviteNum>0:
                        itchat.send(u'%s\u2005邀请了 @%s\u2005' % (result[2], NickName), FromId)


                    id = saveUser(user["UserName"], user["NickName"], user["Alias"], invteName,
                                          GroupName,"")
                    User = getUser("", invteName, GroupName)
                    if User:
                        itchat.send(u'@%s\u2005已经邀请了%s个成员' % (result[2], result[7]), FromId)
                    if id:
                        itchat.set_alias(user["UserName"], "%s%s" % (chatRoom["NickName"], id))
                        print "设置备注%s%s" % (chatRoom["NickName"], id)
            else:
                print u"已存在%s" % user["UserName"]


@itchat.msg_register(itchat.content.SYSTEM)
def get_uin(msg):
    if msg['SystemInfo'] != 'uins': return
    ins = itchat.instanceList[0]
    fullContact = ins.memberList + ins.chatroomList + ins.mpList
    for chatroom in ins.chatroomList:
        if chatroom["IsOwner"]:
            mygroup = mysql.getOne("""select * from wechat_group where group_name=%s""", chatroom["NickName"])
            for user in chatroom["MemberList"]:
                saveUser(user["UserName"], user["NickName"], user["Alias"], "", chatroom["NickName"],"")
            if mygroup:
                mysql.update("""update wechat_group set group_ids=%s where group_name=%s""",
                             (chatroom["UserName"], chatroom["NickName"]))
            else:
                mysql.insertOne(
                    "INSERT INTO wechat_group (group_name, group_ids, owner, manager_id, remark) VALUES ( %s, %s, 0, 0, %s)",
                    (chatroom["NickName"], chatroom["UserName"], " "))
    print('** Uin Updated **')
    for username in msg['Text']:
        member = itchat.utils.search_dict_list(
            fullContact, 'UserName', username)
        print(('%s: %s' % (
            member.get('NickName', ''), member['Uin'])))

def afterLogin():
    chatrooms = itchat.get_chatrooms()
    for chatroom in chatrooms:
        memberList = itchat.update_chatroom(chatroom['UserName'], detailedMember=True)


        # print chatroom


def saveGroup(groupNames, groupIds):
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
