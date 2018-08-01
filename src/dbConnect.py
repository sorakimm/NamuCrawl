from src import config
import pymysql
import mylogging

# sys.path.append('/opt/settings')
dbLogger = mylogging.MyLogger("db")

class DBConnect(object):
    def __init__(self):
        dbLogger.info(("DBConnect init"))
        self._db_connection = pymysql.connect(host=config.DATABASE_CONFIG['host'],
                               user=config.DATABASE_CONFIG['user'],
                               password=config.DATABASE_CONFIG['password'],
                               db=config.DATABASE_CONFIG['dbname'])
        self._db_connection.set_charset('utf8mb4')
        self._db_cur = self._db_connection.cursor()

    def insert(self, query, params=None):
        dbLogger.info("db insert")
        self._db_cur.execute(query, params)
        return self._db_connection.commit()

    def select(self, query, params):
        self._db_cur.execute(query, params)
        return self._db_cur.fetchall()

    def rows(self):
        return self._db_cur.rowcount

    def __del__(self):
        self._db_connection.close()
        self._db_cur.close()