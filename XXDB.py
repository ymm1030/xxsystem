#-*- coding:utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from XXLog import logout

class YmmDB(object):
    def __init__(self, user, passwd, table_name):
        try:
            self.conn = mysql.connector.connect(user=user, password=passwd, use_unicode=True)
            self.table_name = table_name
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logout("MySQL connection failed: Invalid user/password.")
            else:
                logout(err)
        
    def connected_database(self):
        db = getattr(self.conn, 'database', '')
        if len(db):
            db = db[3:]
        return db

    def valid(self):
        return self.connected_database() != ''

    def database_list(self):
        s = 'show databases'
        if not self.execute(s):
            return []
        l = self.cursor.fetchall()
        return [db[0] for db in l if 'xx_' in db[0]]
        
    def execute(self, cmd):
        try:
            self.cursor.execute(cmd)
            return True
        except mysql.connector.Error as err:
            logout('Failed to execute cmd:%s' % cmd)
            logout(err)
            return False

    def connect_to_db(self, db):
        l = self.database_list()
        realdb = 'xx_' + db
        if realdb in l:
            self.connect_to_db_impl(realdb)
        else:
            self.create_db(realdb)

    def connect_to_db_impl(self, db):
        logout('Conneting to database:', db)
        try:
            self.conn.connect(database=db)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                logout("Database [%s] does not exist!" % db)
            else:
                logout(err)
            logout('Failed to connect to database [%s]!' % db)
            return
        logout('Successfully connected to db:[%s]! Now check table...' % db)
        tstr = "select * from information_schema.tables where table_name='" + self.table_name + "'"
        tstr += " and TABLE_SCHEMA='" + self.conn.database + "'"
        if not self.execute(tstr):
            return
        t = self.cursor.fetchall()
        if not len(t):
            tstr = "create table " + self.table_name + "(PRODUCT varchar(512), SOLD int, BOUGHT int, CODE varchar(64), PRIMARY KEY(PRODUCT)) DEFAULT CHARSET=utf8"
            if not self.execute(tstr):
                return
            logout('Created new table %s.' % self.table_name)
        else:
            logout('Found table %s exist!' % self.table_name)

    def create_db(self, db):
        logout('Creating database:', db)
        cstr = 'create database ' + db
        if not self.execute(cstr):
            return
        logout('Create successful!')
        self.connect_to_db_impl(db)

    def add(self, product, sold = 0, bought = 0, code = ''):
        logout('Add product[%s], sold[%d], bought[%d], code[%s]' % (product, sold, bought, code))
        s = "insert into %s values('%s', %d, %d, '%s')" % (self.table_name, product, sold, bought, code)
        if not self.execute(s):
            logout('Add failed!')
            return False
        self.conn.commit()
        logout('Add sucessed!')
        return True

    def get(self, product):
        logout('Get info of product[%s]' % product)
        s = "select * from %s where PRODUCT='%s'" % (self.table_name, product)
        if not self.execute(s):
            return []
        ret = self.cursor.fetchall()
        logout('Result is:', ret)
        return ret

    def delete(self, product):
        logout('Delete product:', product)
        s = "delete from %s where product='%s'" % (self.table_name, product)
        if not self.execute(s):
            return False
        self.conn.commit()
        logout('Delete sucessed!')
        return True

    def update(self, product, sold, bought, code):
        logout('Update to: product[%s], sold[%d], bought[%d], code[%s]' % (product, sold, bought, code))
        s = "update %s set sold=%d, bought=%d, code='%s' where product='%s'" % (self.table_name, sold, bought, code, product)
        if not self.execute(s):
            return False
        self.conn.commit()
        logout('Update successed!')
        return True

    def updateRecord(self, product, sold, bought, code):
        if not len(product):
            logout('The product name must not be empty!')
            return False
        l = self.get(product)
        if not len(l):
            return self.add(product, sold, bought, code)
        else:
            return self.update(product, sold, bought, code)

    def products(self):
        s = "select * from %s" % self.table_name
        if not self.execute(s):
            return []
        l = self.cursor.fetchall()
        l = [r[0] for r in l]
        return l

    def records(self):
        s = "select * from %s" % self.table_name
        if not self.execute(s):
            return []
        l = self.cursor.fetchall()
        return l

if __name__ == '__main__':
    t = YmmDB('root', 'ymm1030', 'xxdxx_01')
    t.connect_to_db('20180709')
    t.updateRecord('YSL', 20, 10, '')
    t.updateRecord('burger', 10, 5, '')
    t.updateRecord('burger', 7, 4, '876578976')
    t.get('YSL')
    t.get('burger')
    logout(t.products())
    logout(t.records())