#-*- coding:utf-8 -*-

import XXCmd
from XXDB import YmmDB
from XXLog import logout
import re

class XXToken(object):
    def __init__(self, db, cmd_str):
        reg = r'[,.，。、]+'
        self.tokens_ = re.split(reg, cmd_str)
        self.cmd_ = None
        self.reason_ = ''
        self.db_ = db
        self.analyse()

    def command(self):
        return self.cmd_

    def reason(self):
        return self.reason_

    def analyse(self):
        if not len(self.tokens_):
            self.reason_ = "空指令"
        elif len(self.tokens_) == 1:
            self.with_parameter_1()
        elif len(self.tokens_) == 2:
            self.with_parameter_2()
        elif len(self.tokens_) == 3:
            self.with_parameter_3()
        else:
            self.with_parameter_4()

    def with_parameter_1(self):
        action = self.tokens_[0]
        if '列表' in action:
            self.cmd_ = XXCmd.ListCmd(self.db_, True)
        elif '统计' in action:
            self.cmd_ = XXCmd.ListCmd(self.db_, False)
        elif '导出' in action:
            self.cmd_ = XXCmd.ExportCmd(self.db_)
        else:
            l = self.db_.products()
            l1 = []
            for product in l:
                if re.search(action, product, re.IGNORECASE):
                    l1.append(product)
            if len(l1):
                self.cmd_ = XXCmd.ReadMultiProductsCmd(self.db_, l1)
            else:
                self.reason_ = "未找到匹配的产品！"
    
    def with_parameter_2(self):
        p1 = self.tokens_[0]
        p2 = self.tokens_[1]
        if '删除' in p1:
            self.cmd_ = XXCmd.DeleteCmd(self.db_, p2)
        elif '连接' in p1:
            self.cmd_ = XXCmd.ConnectDBCmd(self.db_, p2)
        elif '提示' in p1:
            self.cmd_ = XXCmd.HintCmd(self.db_, p2)
        else:
            try:
                sold_added = int(p2)
                self.cmd_ = XXCmd.AddSoldCmd(self.db_, p1, sold_added)
            except ValueError:
                self.reason_ = "参数不对，第二个要写数字，可以为负"

    def with_parameter_3(self):
        p1 = self.tokens_[0]
        p2 = self.tokens_[1]
        p3 = self.tokens_[2]
        try:
            sold_added = int(p2)
        except ValueError:
            self.reason_ = "参数不对，第二个要写数字，可以为负"
            return
        try:
            bought_added = int(p3)
            self.cmd_ = XXCmd.AddSoldAndBoughtCmd(self.db_, p1, sold_added, bought_added)
        except ValueError:
            logout('Skip non-numbered parameter:', p3)
            self.cmd_ = XXCmd.AddSoldCmd(self.db_, p1, sold_added)

    def with_parameter_4(self):
        p1 = self.tokens_[0]
        p2 = self.tokens_[1]
        p3 = self.tokens_[2]
        p4 = self.tokens_[3]

        if (not '修改' in p1) and (not '更新' in p1):
            self.reason_ = "你可能想【更新】或【修改】？"
        else:
            try:
                new_sold = int(p3)
            except ValueError:
                self.reason_ = "参数不对，第三个要写数字"
                return
            try:
                new_bought = int(p4)
            except ValueError:
                self.reason_ = "参数不对，第四个要写数字"
                return
            self.cmd_ = XXCmd.ResetCmd(self.db_, p2, new_sold, new_bought, '')

if __name__ == '__main__':
    t = YmmDB('root', 'ymm1030', 'xxdxx_01')
    
    s = XXToken(t, "连接 20180709")
    cmd = s.command()
    if cmd is not None:
        cmd.execute()
        logout(cmd.result())
    else:
        logout(s.reason())

    s = XXToken(t, "列表")
    cmd = s.command()
    if cmd is not None:
        cmd.execute()
        logout(cmd.result())
    else:
        logout(s.reason())

    s = XXToken(t, "统计")
    cmd = s.command()
    if cmd is not None:
        cmd.execute()
        logout(cmd.result())
    else:
        logout(s.reason())

    s = XXToken(t, "WhiteMilk 5 5")
    cmd = s.command()
    if cmd is not None:
        cmd.execute()
        logout(cmd.result())
    else:
        logout(s.reason())

    s = XXToken(t, "milk")
    cmd = s.command()
    if cmd is not None:
        cmd.execute()
        logout(cmd.result())
    else:
        logout(s.reason())
