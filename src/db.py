# -*- coding:utf-8 -*-
# db.py
from src import config
import pymysql
import mylogging
import enum
import dbConnect

dbLogger = mylogging.MyLogger("db")

class isUrlCrawled(enum.Enum):
    TRUE = 1
    FALSE = 2
    ERROR = 3

dbi = dbConnect.DBConnect()

def insertNamuwikiDB(dbTuple):
    insertDBQuery = """
        INSERT INTO namuwiki (title, url, content, image, editdate, crawltime, html, urlhash)\
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, md5(%s))
        ON DUPLICATE KEY UPDATE 
        title=%s, url=%s, content=%s, image=%s, editdate=%s, crawltime=NOW(), html=%s
        """

    dbLogger.info('insertNamuwikiDB')
    try:
        dbi.insert(insertDBQuery, dbTuple + dbTuple[:-1])
    except:
        dbLogger.error(dbTuple)
    return

def selectUrls(offset):
    selectUrlQuery = """
    SELECT url FROM namuwiki LIMIT 100 OFFSET %s
    """
    dbLogger.info("selectUrls")
    return dbi.select(selectUrlQuery, offset)

def countRows():
    dbLogger.info("countRows")
    return dbi.rows()


