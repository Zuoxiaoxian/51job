#-*-coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import MySQLdb

class MysqlPipeline(object):
    '''
        保存数据库前,确保数据库已存在
    '''
    def __init__(self):
        '''
            连接数据库, host, passwd, db, charset, user, use_unicode,
            创建 数据表:
        '''
        # self.db = MySQLdb.connect()
        self.db = MySQLdb.connect(host='localhost', passwd='123456', user='root', charset='utf8', use_unicode=True, db='51job')
        self.cursor = self.db.cursor()
        print '数据库已连接,正在储存数据...'
        sql = "drop table if exists jobs"
        self.cursor.execute(sql)
        sql = "create table if not exists jobs(id INTEGER PRIMARY KEY auto_increment NOT NULL, zhi_wei VARCHAR (100), gong_si VARCHAR (100), di_dian VARCHAR (100), ri_qi VARCHAR (50), many_min VARCHAR (50) , many_max VARCHAR (50))"
        self.cursor.execute(sql)
        # self.db.commit()

    def save(self, *args):
        sql = "insert into jobs(zhi_wei, gong_si, di_dian, ri_qi, many_min, many_max) values(%s, %s, %s, %s, %s, %s)"
        args = args[0]
        self.cursor.execute(sql, args)
        self.db.commit()
        print "已存储完毕!"
    def __del__(self):
        '''
            关闭数据库
        '''
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':

    b = ['1','2','3','4','5','6']
    a = MysqlPipeline()
    a.save(b)
