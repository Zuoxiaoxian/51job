#-*-coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

import MySQLdb
import xlwt

db = MySQLdb.connect(host='localhost', passwd='123456', user='root',db='51job', charset='utf8', use_unicode=True)
cursor = db.cursor()
print "连接 数据库 OK, 正在读取数据..."


sql = "select many_min, many_max from jobs where many_min >= 6000 "
cursor.execute(sql)
result = cursor.fetchall()
le = len(result)
print le
work_book = xlwt.Workbook('utf-8')
work_sheet = work_book.add_sheet(u"51job")
style = xlwt.XFStyle()

font = xlwt.Font()
font.bold = True
style.font = font
work_sheet.write(0,0,u"最低工资", style)
work_sheet.write(0,1,u"最高工资", style)


for i,re in enumerate(result):
    print i
    work_sheet.write(i+1,0,re[0])
    work_sheet.write(i+1,1,re[1])

work_book.save("1.xls")
cursor.close()
db.close()