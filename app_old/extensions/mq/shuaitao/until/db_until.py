#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/6/9 11:26
# @Author  : WangLei
# @FileName: sqltools.py
# @Software: PyCharm
import pymysql
# from config.config import configs
from flask import current_app



class SQLManager:

    # 初始化实例方法
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    # 连接数据库
    @classmethod
    def connect(cls):
        cls.conn = current_app.config.get('POOL').connection()
        cls.cursor = cls.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return cls.cursor, cls.conn

    @classmethod
    def get_list(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        cls.close()
        return result

    # 查询单条数据
    @classmethod
    def get_one(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        if result == None:
            return False
        cls.close()
        return result

    # 执行单条SQL语句
    # 支持执行报错事务回滚操作
    @classmethod
    def moddify(cls, sql, args=None):
        cursor, coon = cls.connect()
        flag = 0  # 标识数据执行成功的状态信息
        try:
            cursor.execute(sql, args)
            flag = 1
        except Exception as e:
            print(e)
            coon.rollback()
            flag = 0
        coon.commit()
        cls.close()
        return flag

    # 执行多条SQL语句
    @classmethod
    def multi_modify(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.executemany(sql, args)
        coon.commit()
        cls.close()
        return True

    # 创建单条记录的语句
    @classmethod
    def create(cls, sql, args=None):
        cursor, coon = cls.connect()
        cursor.execute(sql, args)
        coon.commit()
        last_id = cursor.lastrowid
        cls.close()
        return last_id

    # 创建或更新
    @classmethod
    def create_or_update(cls, table, params, condition, other=None):
        """
        :param table: 表名称
        :param params: [[key1,key2],[value1,value2]]
        :param condition: {"key":"value"}
        :param other: other_sql
        :return:
        """
        sql = "select * from %s where 1=1" % (table)
        if condition:
            condition_sql = ''
            for key in condition.keys():
                condition_sql = condition_sql + " and " + key + "=" + "\'" + str(condition.get(key)) + "\'"
            sql += condition_sql
        try:
            cursor, coon = cls.connect()
            cursor.execute(sql)
            if cursor.fetchall():
                params_str = ''
                for i, v in enumerate(params[0]):
                    if i < len(params[0]) - 1:
                        params_str += "%s='%s'," % (v, params[1][i])
                    else:
                        params_str += "%s='%s'" % (v, params[1][i])
                sql = "update %s set %s where 1=1 %s" % (table, params_str, condition_sql)
                cursor.execute(sql)
            else:
                newkey = str(params[0]).replace('[', '(').replace(']', ')').replace("'", '')
                newvalue = str(params[1]).replace('[', '(').replace(']', ')')
                sql = "insert into %s %s values%s" % (table, newkey, newvalue)
                cursor.execute(sql)
            coon.commit()
            cursor.close()
            coon.close()
            return True
        except Exception as e:
            return False

    # 从单个表数据中查询数据
    @classmethod
    def one(cls, table, condition):
        sql = f'select * from {table} where 1=1 '
        for key in condition.keys():
            sql = sql + " and " + key + "=" + "\'" + str(condition.get(key)) + "\'"
        obj = cls.get_list(sql)
        return obj

    # 关闭数据库cursor和连接
    @classmethod
    def close(cls):
        cursor, coon = cls.connect()
        cursor.close()
        coon.close()

    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
