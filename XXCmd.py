#-*- coding:utf-8 -*-

from XXDB import YmmDB

PRODUCT = 0
SOLD = 1
BOUGHT = 2
CODE = 3

class CmdBase(object):
    def __init__(self, db):
        self.db = db
        self.result_ = "未初始化的命令"
        self.sucessed_ = False

    def result(self):
        return self.result_

    def sucessed(self):
        return self.sucessed_

class ReadProductCmd(CmdBase):
    def __init__(self, db, product):
        super(ReadProductCmd, self).__init__(db)
        self.product_ = product

    def execute(self):
        l = self.db.get(self.product_)
        if len(l):
            s = "产品：[%s] 已卖出：[%d] 已购得：[%d]" % (l[0][PRODUCT], l[0][SOLD], l[0][BOUGHT])
            if len(l[0][3]):
                s += " 条码：[%s]" % l[0][CODE]
            self.result_ = s
            self.sucessed_ = True
        else:
            self.result_ = "未找到产品：[%s]" % self.product_

class ReadMultiProductsCmd(CmdBase):
    def __init__(self, db, product_list):
        super(ReadMultiProductsCmd, self).__init__(db)
        self.product_list_ = product_list

    def execute(self):
        if not isinstance(self.product_list_, list):
            cmd = ReadProductCmd(self.db, self.product_list_)
            cmd.execute()
            self.result_ = cmd.result()
        else:
            self.result_ = ''
            for product in self.product_list_:
                cmd = ReadProductCmd(self.db, product)
                cmd.execute()
                if cmd.sucessed():
                    self.result_ += cmd.result()
                    self.result_ += '\n'
            if len(self.result_):
                self.sucessed_ = True
            else:
                self.result_ = "查询失败！"

class AddSoldCmd(CmdBase):
    def __init__(self, db, product, sold_added):
        super(AddSoldCmd, self).__init__(db)
        self.product_ = product
        self.sold_added_ = sold_added

    def execute(self):
        l = self.db.get(self.product_)
        if len(l):
            new_sold = l[0][SOLD] + self.sold_added_
            if self.db.update(l[0][PRODUCT], new_sold, l[0][BOUGHT], l[0][CODE]):
                self.result_ = "成功为产品[%s]添加了卖出数[%d],卖出数[%d->%d]" % (self.product_, self.sold_added_, l[0][SOLD], new_sold)
                self.sucessed_ = True
            else:
                self.result_ = "为产品[%s]添加卖出数[%d]失败！" % (self.product_, self.sold_added_)
        else:
            if self.sold_added_ < 0:
                self.sold_added_ = 0
            if self.db.add(self.product_, self.sold_added_, 0, ''):
                self.result_ = "成功添加产品[%s]，卖出数[%d]" % (self.product_, self.sold_added_)
                self.sucessed_ = True
            else:
                self.result_ = "添加产品[%s]失败！" % (self.product_)

class AddSoldAndBoughtCmd(CmdBase):
    def __init__(self, db, product, sold_added, bought_added):
        super(AddSoldAndBoughtCmd, self).__init__(db)
        self.product_ = product
        self.sold_added_ = sold_added
        self.bought_added_ = bought_added

    def execute(self):
        l = self.db.get(self.product_)
        if len(l):
            new_sold = l[0][SOLD] + self.sold_added_
            new_bought = l[0][BOUGHT] + self.bought_added_
            if self.db.update(l[0][PRODUCT], new_sold, new_bought, l[0][CODE]):
                self.result_ = "成功为产品[%s]添加了" % self.product_
                if self.sold_added_:
                    self.result_ += "卖出数[%d],卖出数[%d->%d]和" % (self.sold_added_, l[0][SOLD], new_sold)
                self.result_ += "买入数[%d],买入数[%d->%d]" % (self.bought_added_, l[0][BOUGHT], new_bought)
                self.sucessed_ = True
            else:
                self.result_ = "为产品[%s]添加卖出数[%d]和买入数[%d]失败！" % (self.product_, self.sold_added_, self.bought_added_)
        else:
            if self.sold_added_ < 0:
                self.sold_added_ = 0
            if self.bought_added_ < 0:
                self.bought_added_ = 0
            if self.db.add(self.product_, self.sold_added_, self.bought_added_, ''):
                self.result_ = "成功添加产品[%s]，卖出数[%d]，买入数[%d]" % (self.product_, self.sold_added_, self.bought_added_)
                self.sucessed_ = True
            else:
                self.result_ = "添加产品[%s]失败！" % (self.product_)

class ListCmd(CmdBase):
    def __init__(self, db, product_only):
        super(ListCmd, self).__init__(db)
        self.product_only_ = product_only

    def execute(self):
        l = []
        if self.product_only_:
            l = self.db.products()
        else:
            l = self.db.records()
        self.result_ = ''
        for one in l:
            if self.product_only_:
                self.result_ += one + '\n'
            else:
                self.result_ += "产品：[%s] 卖出[%d] 买入[%d]" % (one[PRODUCT], one[SOLD], one[BOUGHT])
                if len(one[CODE]):
                    self.result_ += " 条码[%s]" % one[CODE]
                self.result_ += '\n'
        if not len(self.result_):
            self.result_ = "还没有任何条目！"
        self.sucessed_ = True

class ResetCmd(CmdBase):
    def __init__(self, db, product, sold, bought, code):
        super(ResetCmd, self).__init__(db)
        self.product_ = product
        self.sold_ = sold
        self.bought_ = bought
        self.code_ = code

    def execute(self):
        l = self.db.get(self.product_)
        if len(l):
            if self.db.update(self.product_, self.sold_, self.bought_, self.code_):
                self.result_ = "更新产品[%s]成功,卖出[%d],买入[%d]" % (self.product_, self.sold_, self.bought_)
                if len(self.code_):
                    self.result_ += ",条码[%s]" % self.code_
                self.sucessed_ = True
            else:
                self.result_ = "更新产品[%s]失败！" % self.product_
        else:
            if self.db.add(self.product_, self.sold_, self.bought_, self.code_):
                self.result_ = "成功添加产品[%s],卖出[%d],买入[%d]" % (self.product_, self.sold_, self.bought_)
                if len(self.code_):
                    self.result_ += ",条码[%s]" % self.code_
                self.sucessed_ = True
            else:
                self.result_ = "添加产品[%s]失败！" % (self.product_)

class DeleteCmd(CmdBase):
    def __init__(self, db, product):
        super(DeleteCmd, self).__init__(db)
        self.product_ = product
    
    def execute(self):
        if self.db.delete(self.product_):
            self.result_ = "成功删除产品[%s]" % self.product_
            self.sucessed_ = True
        else:
            self.result_ = "删除产品[%s]失败！" % self.product_

class ExportCmd(CmdBase):
    pass

class ImportCmd(CmdBase):
    pass

class ConnectDBCmd(CmdBase):
    def __init__(self, db, db_name):
        super(ConnectDBCmd, self).__init__(db)
        self.db_name_ = db_name

    def execute(self):
        self.db.connect_to_db(self.db_name_)
        if len(self.db.connected_database()):
            self.result_ = "已经连接数据库[%s]" % self.db_name_
            self.sucessed_ = True
        else:
            self.result_ = "连接数据库[%s]失败！" % self.db_name_

if __name__ == '__main__':
    t = YmmDB('root', 'ymm1030', 'xxdxx_01')
    t.connect_to_db('20180709')

    readCmd1 = ReadProductCmd(t, 'YSL')
    readCmd1.execute()
    print(readCmd1.result())

    readCmd2 = ReadProductCmd(t, 'NotExist')
    readCmd2.execute()
    print(readCmd2.result())

    addSoldCmd1 = AddSoldCmd(t, 'YSL', 2)
    addSoldCmd1.execute()
    print(addSoldCmd1.result())

    addSoldCmd2 = AddSoldCmd(t, 'NotExist', 1)
    addSoldCmd2.execute()
    print(addSoldCmd2.result())

    addSoldCmd3 = AddSoldCmd(t, 'YSL', -2)
    addSoldCmd3.execute()
    print(addSoldCmd3.result())

    addSoldCmd4 = AddSoldCmd(t, 'PP water', -2)
    addSoldCmd4.execute()
    print(addSoldCmd4.result())

    addSoldAndBoughtCmd1 = AddSoldAndBoughtCmd(t, 'YSL', 0, 1)
    addSoldAndBoughtCmd1.execute()
    print(addSoldAndBoughtCmd1.result())

    addSoldAndBoughtCmd2 = AddSoldAndBoughtCmd(t, 'YSL', 0, -1)
    addSoldAndBoughtCmd2.execute()
    print(addSoldAndBoughtCmd2.result())

    addSoldAndBoughtCmd3 = AddSoldAndBoughtCmd(t, 'YSL', -1, 1)
    addSoldAndBoughtCmd3.execute()
    print(addSoldAndBoughtCmd3.result())

    addSoldAndBoughtCmd4 = AddSoldAndBoughtCmd(t, 'CleanMilk', -1, 1)
    addSoldAndBoughtCmd4.execute()
    print(addSoldAndBoughtCmd4.result())

    listCmd1 = ListCmd(t, True)
    print(listCmd1.result())

    listCmd2 = ListCmd(t, False)
    print(listCmd2.result())

    resetCmd1 = ResetCmd(t, 'CleanMilk', 8, 8, '7878797970')
    resetCmd1.execute()
    print(resetCmd1.result())

    resetCmd2 = ResetCmd(t, 'DirtyMilk', 9, 9, '7675665765')
    resetCmd2.execute()
    print(resetCmd2.result())

    delCmd1 = DeleteCmd(t, 'NotExist')
    delCmd1.execute()
    print(delCmd1.result())

    delCmd2 = DeleteCmd(t, 'DirtyMilk')
    delCmd2.execute()
    print(delCmd2.result())