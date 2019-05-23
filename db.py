
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import getpass
import os

class DataBase :

    def __init__ (self) :
        user = getpass.getuser()
        self.dbAddress = os.getcwd() + '/'

        self.table = 'lists'

        if self.connect() == False:
            self.connStat = False
        else :
            self.connStat = True
            self.chkTable()

    def __del__ (self) :
        if self.connStat == True :
            self.disConn()

    def connect (self) :
        try:
            if not os.path.exists(self.dbAddress) :
                os.makedirs(self.dbAddress)
            self.dbAddress += 'db.sqlite3'
            self.conn = sqlite3.connect(self.dbAddress)
            self.cur = self.conn.cursor()
            return True
        except Exception, e:
            return False

    def create (self) :
        if self.connStat == False : return False

        sql = 'create table ' + self.table + ' (id integer PRIMARY KEY autoincrement, title text, quality text, url text, enable integer, online integer, delay integer, update text)'
        self.cur.execute(sql)

    def query (self, sql) :
        if self.connStat == False : return False

        self.cur.execute(sql)
        values = self.cur.fetchall()

        return values

    def insert (self, data):
        if self.connStat == False : return False

        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')

        keyList = []
        valList = []
        for k, v in data.iteritems():
            keyList.append(k)
            valList.append(str(v).replace('"','\"').replace("'","''"))

        sql = "insert into " + self.table + " (`" + '`, `'.join(keyList) + "`) values ('" + "', '".join(valList) + "')"
        self.cur.execute(sql)
        self.conn.commit()

    def disConn (self) :
        if self.connStat == False : return False

        self.cur.close()
        self.conn.close()

    def chkTable (self) :
        if self.connStat == False : return False

        sql = "SELECT tbl_name FROM sqlite_master WHERE type='table'"
        tableStat = False

        self.cur.execute(sql)
        values = self.cur.fetchall()

        for x in values:
            if self.table in x :
                tableStat = True

        if tableStat == False :
            self.create()

