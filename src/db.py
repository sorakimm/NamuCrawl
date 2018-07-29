
# db.py
from src import config
import sys
import pymysql

sys.path.append('/opt/settings')

class MyDB(object):
    def __init__(self):
        self._db_connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                               user=config.DATABASE_CONFIG['user'],
                               password=config.DATABASE_CONFIG['password'],
                               db=config.DATABASE_CONFIG['dbname'])
        self._db_connection.set_charset('utf8mb4')
        self._db_cur = self._db_connection.cursor()

    def insert(self, query, params=None):
        return self._db_cur.execute(query, params)

    def query(self, query, params):
        return self._db_cur.execute(query, params)

    def __del__(self):
        self._db_connection.close()
        self._db_cur.close()