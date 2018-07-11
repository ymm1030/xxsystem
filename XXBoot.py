import itchat
from XXDB import YmmDB
from XXTokenAnalyzer import XXToken

db = YmmDB('root', 'ymm1030', 'xxdxx_01')

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    text = msg.text
    print("From:%s,To:%s" % (msg['FromUserName'], msg['ToUserName']))
    if msg['FromUserName'] == 'filehelper' or msg['ToUserName'] != 'filehelper':
        return
    t = XXToken(db, text)
    cmd = t.command()
    if cmd is not None:
        cmd.execute()
        itchat.send(cmd.result(), 'filehelper')
    else:
        itchat.send(t.reason(), 'filehelper')

itchat.auto_login(hotReload=True)
itchat.run()