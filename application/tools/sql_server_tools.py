# !/usr/bin/env python
# coding:utf-8
# @Time    : 2021/10/10 23:28
# @Contact : shangyameng@datagrand.com
# @Name    : sql_server_tools.py
# @Desc    :

import pymssql
from application.initialization.logger_process import logger


class SqlServerTools(object):

    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.conn = None

    def connect_and_get_cursor(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if self.db:
            try:
                self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db,
                                            charset="utf8", tds_version="7.0")
                cur = self.conn.cursor()
                logger.info('connect success ...')
            except Exception as e:
                logger.info(e)
                cur = None
            if not cur:
                logger.info("bdo数据库连接失败")
                raise (NameError, "连接数据库失败")
            else:
                return cur
        else:
            logger.info("no db ...")

    def exec_query(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        """
        logger.info("start connect ...")
        cur = self.connect_and_get_cursor()
        cur.execute(sql.encode('cp936'))
        res_list = cur.fetchall()
        # 查询完毕后必须关闭连接
        self.conn.close()
        return res_list

    def exec_non_query(self, sql):
        """
        执行非查询语句
        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        cur = self.connect_and_get_cursor()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    s = SqlServerTools(host="dbserver01.bdo.com.cn",
                       db="myehrlx",
                       user="daguan_reader",
                       pwd="aFvX3@Dild")
    sql = 'select dept_id from cloudDept;'
    res = s.exec_query(sql)
    logger.info(len(res))