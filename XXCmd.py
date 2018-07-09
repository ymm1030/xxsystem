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

    def result(self):
        return self.result_

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
        else:
            self.result_ = "未找到产品：[%s]" % self.product_

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
            else:
                self.result_ = "为产品[%s]添加卖出数[%d]失败！" % (self.product_, self.sold_added_)
        else:
            if self.sold_added_ < 0:
                self.sold_added_ = 0
            if self.db.add(self.product_, self.sold_added_, 0, ''):
                self.result_ = "成功添加产品[%s]，卖出数[%d]" % (self.product_, self.sold_added_)
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
            else:
                self.result_ = "为产品[%s]添加卖出数[%d]和买入数[%d]失败！" % (self.product_, self.sold_added_, self.bought_added_)
        else:
            if self.sold_added_ < 0:
                self.sold_added_ = 0
            if self.bought_added_ < 0:
                self.bought_added_ = 0
            if self.db.add(self.product_, self.sold_added_, self.bought_added_, ''):
                self.result_ = "成功添加产品[%s]，卖出数[%d]，买入数[%d]" % (self.product_, self.sold_added_, self.bought_added_)
            else:
                self.result_ = "添加产品[%s]失败！" % (self.product_)

class ListCmd(CmdBase):
    pass

class ResetCmd(CmdBase):
    pass

class DeleteCmd(CmdBase):
    pass

if __name__ == '__main__':
    t = YmmDB('root', 'ymm', 'xxdxx_01')
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