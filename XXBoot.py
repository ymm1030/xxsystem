#-*- coding:utf-8 -*-

import itchat
from XXDB import YmmDB
from XXTokenAnalyzer import XXToken
from XXWelcome import XXInit
import os, platform, time

dir_path = os.path.dirname(os.path.realpath(__file__))
if platform.system() == 'Windows':
    dir_path = dir_path.replace('\\', '/')

db = None
welcome = None

def sendmsg(msg):
    itchat.send(msg, 'filehelper')

def sendlist(l):
    sendmsg('-----------')
    for item in l:
        sendmsg(item)
        time.sleep(0.5)
    sendmsg('+++++++++++')

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg.text
    #print("From:%s,To:%s" % (msg['FromUserName'], msg['ToUserName']))
    if msg['FromUserName'] == 'filehelper' or msg['ToUserName'] != 'filehelper':
        return
    t = XXToken(db, text)
    cmd = t.command()
    if cmd is not None:
        cmd.execute()
        if hasattr(cmd, 'connected_database'):
            welcome.refresh_database(cmd.connected_database)
        res = cmd.result()
        if isinstance(res, list):
            sendlist(res)
        elif hasattr(cmd, 'path'):
            itchat.send_file(cmd.path, 'filehelper')
        else:
            sendmsg(res)
    else:
        sendmsg(t.reason())

itchat.auto_login(hotReload=True)
nickName = itchat.originInstance.storageClass.nickName
db = YmmDB('root', 'ymm1030', nickName)
XXInit.nickName = nickName
XXInit.private_path = dir_path + '/' + nickName
welcome = XXInit(db, XXInit.private_path)
sendmsg(welcome.welcome_contents())
itchat.run()