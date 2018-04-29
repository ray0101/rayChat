#encoding=utf-8
import itchat
import json

config={};
def sendmsg():
        title=config["groupname"];
        msglist=config["msglist"]

def sendmsg():

def loadconfig():
    with open("msglist/list.json", 'r') as load_f:
        config = json.load(load_f)
afterLogin();