# -*- coding:utf-8 -*-
import config
import pymysql
from mylogging import MyLogger

dbConnectLogFile = 'log/dbConnect.log'
dbConnectLogger = MyLogger(dbConnectLogFile)

class DBConnect(object):
    def __init__(self):
        dbConnectLogger.info(("DBConnect init"))
        self._db_connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                               user=config.DATABASE_CONFIG['user'],
                               password=config.DATABASE_CONFIG['password'],
                               db=config.DATABASE_CONFIG['dbname'])
        self._db_connection.set_charset('utf8mb4')
        self._db_cur = self._db_connection.cursor()

    def insert(self, query, params=None):
        dbConnectLogger.info("db insert")
        self._db_cur.execute(query, params)
        return self._db_connection.commit()


    def select(self, query):
        try:
            self._db_cur.execute(query)
        except:
            dbConnectLogger.error("select Error : "+ query)
        return self._db_cur.fetchone()[0]

    def rows(self):
        try:
            return self._db_cur.rowcount
        except:
            dbConnectLogger.error("rows Error : ")
            return None

    def __del__(self):
        self._db_connection.close()
        self._db_cur.close()