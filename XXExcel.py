#-*- coding:utf-8 -*-

import xlwt, time
from XXWelcome import XXInit
from XXLog import logout

class Exporter(object):
    def __init__(self, data):
        filename =  getattr(XXInit, 'nickName', '') + '-' + time.strftime('%Y-%m-%d-%H-%M', time.localtime(time.time())) + ".xls"
        logout('Export file name:', filename)
        wk = xlwt.Workbook()
        st = wk.add_sheet('统计表', cell_overwrite_ok=True)
        titles = ['产品', '卖出', '买入', '条码']
        st.write(2, 2, titles[0])
        st.write(2, 3, titles[1])
        st.write(2, 4, titles[2])
        st.write(2, 5, titles[3])
        for row in range(3, 3+len(data)):
            d = data[row-5]
            st.write(row, 2, d[0])
            st.write(row, 3, d[1])
            st.write(row, 4, d[2])
            st.write(row, 5, d[3])
        self.path = getattr(XXInit, 'private_path', '') + '/' + filename
        wk.save(self.path)
