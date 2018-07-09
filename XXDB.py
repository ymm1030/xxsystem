import mysql.connector
from mysql.connector import errorcode

class YmmDB(object):
    def __init__(self, user, passwd, table_name):
        try:
            self.conn = mysql.connector.connect(user=user, password=passwd, use_unicode=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("MySQL connection failed: Invalid user/password.")
            else:
                print(err)
        self.table_name = table_name
        self.cursor = self.conn.cursor()

    def connected_database(self):
        return getattr(self.conn, 'database', '')

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
            print('Failed to execute cmd:%s' % cmd)
            print(err)
            return False

    def connect_to_db(self, db):
        l = self.database_list()
        realdb = 'xx_' + db
        if realdb in l:
            self.connect_to_db_impl(realdb)
        else:
            self.create_db(realdb)

    def connect_to_db_impl(self, db):
        print('Conneting to database:', db)
        try:
            self.conn.connect(database=db)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database [%s] does not exist!" % db)
            else:
                print(err)
            print('Failed to connect to database [%s]!' % db)
            return
        print('Successfully connected to db:[%s]! Now check table...' % db)
        tstr = "select * from information_schema.tables where table_name='" + self.table_name + "'"
        if not self.execute(tstr):
            return
        t = self.cursor.fetchall()
        if (len(t) == 0):
            tstr = "create table " + self.table_name + "(PRODUCT varchar(512), SOLD int, BOUGHT int, CODE varchar(64), PRIMARY KEY(PRODUCT))"
            if not self.execute(tstr):
                return
            print('Created new table %s.' % self.table_name)
        else:
            print('Found table %s exist!' % self.table_name)

    def create_db(self, db):
        print('Creating database:', db)
        cstr = 'create database ' + db
        if not self.execute(cstr):
            return
        print('Create successful!')
        self.connect_to_db_impl(db)

    def add(self, product, sold = 0, bought = 0, code = ''):
        print('Add product[%s], sold[%d], bought[%d], code[%s]' % (product, sold, bought, code))
        s = "insert into %s values('%s', %d, %d, '%s')" % (self.table_name, product, sold, bought, code)
        if not self.execute(s):
            print('Add failed!')
            return False
        self.conn.commit()
        print('Add sucessed!')
        return True

    def get(self, product):
        print('Get info of product[%s]' % product)
        s = "select * from %s where PRODUCT='%s'" % (self.table_name, product)
        if not self.execute(s):
            return []
        ret = self.cursor.fetchall()
        print('Result is:', ret)
        return ret

    def delete(self, product):
        print('Delete product:', product)
        s = "delete from %s where product=%s" % (self.table_name, product)
        if not self.execute(s):
            return False
        self.conn.commit()
        print('Delete sucessed!')
        return True

    def update(self, product, sold, bought, code):
        print('Update to: product[%s], sold[%d], bought[%d], code[%s]' % (product, sold, bought, code))
        s = "update %s set sold=%d, bought=%d, code='%s' where product='%s'" % (self.table_name, sold, bought, code, product)
        if not self.execute(s):
            return False
        self.conn.commit()
        print('Update successed!')
        return True

    def updateRecord(self, product, sold, bought, code):
        if not len(product):
            print('The product name must not be empty!')
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

if __name__ == '__main__':
    t = YmmDB('root', 'ymm', 'xxdxx_01')
    t.connect_to_db('20180709')
    t.updateRecord('YSL', 20, 10, '')
    t.updateRecord('burger', 10, 5, '')
    t.updateRecord('burger', 7, 4, '876578976')
    t.get('YSL')
    t.get('burger')
    print(t.products())