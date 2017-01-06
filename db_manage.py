# -*-coding:utf-8 -*-
import ConfigParser
import os, sys, string
import cx_Oracle

class cxOracle(object):
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        cf.read("db_web.ini")
        self._user = cf.get("DB", "USER")
        self._pwd = cf.get("DB", "PASSWD")
        self._ip = cf.get("DB", "IPADDR")
        self._port = cf.get("DB", "PORT")
        self._sid = cf.get("DB", "SID")
        self._tns = cx_Oracle.makedsn(self._ip, self._port, self._sid)
        self._conn = None
        self._ReConnect()

    def _ReConnect(self):
        if not self._conn:
            self._conn = cx_Oracle.connect(self._user, self._pwd, self._tns)
        else:
            pass

    def __del__(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def _NewCursor(self):
        cur = self._conn.cursor()
        if cur:
            return cur
        else:
            print "#Error# Get New Cursor Failed."
            return None

    def _DelCursor(self, cur):
        if cur:
            cur.close()

# 检查是否允许执行的sql语句
    def _PermitUpdateSql(self, sql):
        rt = True
        lrsql = sql. lower()
        sql_elems = lrsql.strip().split()
        print sql_elems[0]
        print len(sql_elems)
        # update和delete最少有四个单词项
        if len(sql_elems) < 4:
            rt = False
        # 更新删除语句，判断首单词，不带where语句的sql不予执行
        elif sql_elems[0] in ['update', 'delete']:
            if 'where' not in sql_elems:
                rt = False

        return rt

# 查询
    def Query(self, sql, nStart = 0, nNum = -1 ):
        rt = []

        # 获取cursor
        cur = self. _NewCursor()
        if not cur:
            return rt

        # 查询到列表
        cur .execute(sql)
        if (nStart == 0) and (nNum == 1):
            rt.append(cur.fetchone())
        else:
            rs = cur.fetchall()
            if nNum == -1:
                rt.extend(rs[nStart:])
            else:
                rt.extend(rs[nStart:nStart + nNum])

        # 释放cursor
        self ._DelCursor(cur)

        return rt

    # 更新
    def Exec(self, sql):
        # 获取cursor
        rt = None
        cur = self. _NewCursor()
        if not cur:
            return rt

        # 判断sql是否允许其执行

        if not self._PermitUpdateSql(sql):
            return rt

        # 执行语句
        rt = cur. execute(sql)
        # 释放cursor
        self ._DelCursor(cur)
        return rt


