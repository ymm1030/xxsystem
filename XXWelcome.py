#-*- coding:utf-8 -*-

import os

class XXInit(object):
    def __init__(self, db, path):
        self.db_ = db
        self.dbfile_ = path + "/lastdb"
        self.lastdbname_ = ''
        self.welcome_contents_ = "欢迎使用xxsystem！\n"

        if not os.path.exists(path):
            os.mkdir(path)

        if os.path.isfile(self.dbfile_):
            with open(self.dbfile_, 'r') as f:
                self.lastdbname_ = f.readline()
                db.connect_to_db(self.lastdbname_)
                self.welcome_contents_ += "最后使用的数据库是[%s]，已经自动连接！\n" % self.lastdbname_
        else:
            self.welcome_contents_ += "未检测到最后使用数据库，请手动连接！\n"
        self.welcome_contents_ += "例：指令[连接，20180709]将连接数据库20180709，建议使用日期命名！"

    def welcome_contents(self):
        return self.welcome_contents_

    def refresh_database(self, dbname):
        with open(self.dbfile_, 'w') as f:
            f.write(dbname)