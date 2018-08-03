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

def insertUrls(urlList):
    insertUrlToUrls = """
    INSERT INTO urls (url, state, urlhash) VALUES (%s, "FALSE", md5(%s))
    """
    dbLogger.debug("insertUrls")
    for url in urlList:
        dbi.insert(insertUrlToUrls, (url, url))
    return

    # db.beginTransction();
    #     try {
    #         while(...){
    #             insert();
    #         }
    #         db.setTransctionSuccessful();
    #     } catch (Exception e){
    #         ...
    #     } finally {
    #         db.endTransction();
    #     }


def insertNamuwikiDB(dbTuple):

    insertDBQuery = """
        INSERT INTO namuwiki (title, url, content, image, editdate, crawltime, html, urlhash)\
        VALUES (%s, %s, %s, %s, %s, NOW(), %s, md5(%s))
        ON DUPLICATE KEY UPDATE 
        title=%s, url=%s, content=%s, image=%s, editdate=%s, crawltime=NOW(), html=%s
        """

    dbLogger.info('insertNamuwikiDB')
    dbi.insert(insertDBQuery, dbTuple + dbTuple[:-1])

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


