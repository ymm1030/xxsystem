import mysql.connector

class YmmDB(object):
    def __init__(self, table):
        self.conn = mysql.connector.connect(user='root', password='ymm', database='ymm1030', use_unicode=True)
        self.cursor = self.conn.cursor()
        tstr = "select * from information_schema.tables where table_name='"
        tstr += table
        tstr += "'"
        self.execute(tstr)
        t = self.cursor.fetchall()
        if (len(t) == 0):
            tstr = "create table " + table + "(PRODUCT varchar(512), COUNT int, CODE varchar(64), PRIMARY KEY(PRODUCT, COUNT))"
            self.execute(tstr)
        else:
            print('Found table %s exist:' % table)
            print(t)
        
    def execute(self, cmd):
        result = False
        count = 0
        while not result:
            try:
                self.cursor.execute(cmd)
                result = True
            except Exception as e:
                if count >= 10:
                    print('Failed tried 10 times for reconnect, abort!')
                    print(e)
                    raise
                print('Try to reconnect to database...')
                self.conn.reconnect(attempts=10, delay=10000)
                self.cursor = self.conn.cursor()
                count += 1

if __name__ == '__main__':
    t = YmmDB('test_table1')