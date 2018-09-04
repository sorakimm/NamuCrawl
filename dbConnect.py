# -*- coding:utf-8 -*-
import config
import pymysql
from mylogging import MyLogger

dbConnectLogFile = 'log/dbConnect.log'
dbConnectLogger = MyLogger(dbConnectLogFile)

class DBConnect(object):
    def __init__(self):
        dbConnectLogger.debug(("DBConnect init"))
        self._db_connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                               user=config.DATABASE_CONFIG['user'],
                               password=config.DATABASE_CONFIG['password'],
                               db=config.DATABASE_CONFIG['dbname'])
        self._db_connection.set_charset('utf8mb4')
        self._db_cur = self._db_connection.cursor()

    def query(self, query, params=None):
        dbConnectLogger.debug("db query execute")
        self._db_cur.execute(query)
        return self._db_cur.fetchone()


    def insert(self, query, params=None):
        dbConnectLogger.debug("db insert")
        self._db_cur.execute(query, params)
        return self._db_connection.commit()


    def select(self, query, params=None):
        try:
            self._db_cur.execute(query, params)
            result = self._db_cur.fetchone()
            if result:
                return result[0]
            else:
                return None

        except Exception as e:
            dbConnectLogger.error(e)


    def __del__(self):
        self._db_connection.close()
        self._db_cur.close()