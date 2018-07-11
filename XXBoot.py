import itchat
from XXDB import YmmDB
from XXTokenAnalyzer import XXToken
import os, platform

dir_path = os.path.dirname(os.path.realpath(__file__))
if platform.system() == 'Windows':
    dir_path = dir_path.replace('\\', '/')

itchat.__ymmdb__ = None

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg.text
    print("From:%s,To:%s" % (msg['FromUserName'], msg['ToUserName']))
    if msg['FromUserName'] == 'filehelper' or msg['ToUserName'] != 'filehelper':
        return
    t = XXToken(itchat.__ymmdb__, text)
    cmd = t.command()
    if cmd is not None:
        cmd.execute()
        itchat.send(cmd.result(), 'filehelper')
    else:
        itchat.send(t.reason(), 'filehelper')

@itchat.msg_register(itchat.content.SYSTEM)
def system_hooker(msg):
    if itchat.__ymmdb__ is None:
        itchat.__ymmdb__ = YmmDB('root', 'ymm', msg['User']['NickName'])

itchat.auto_login(hotReload=True)
itchat.run()