# -*- coding:utf-8 -*-
# db.py
from mylogging import MyLogger
import dbConnect

dbLogFile = 'log/db.log'
dbLogger = MyLogger(dbLogFile)

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

def countRows():
    dbLogger.info("countRows")
    return dbi.rows()

def selectRecentUrl():
    selectRecentUrl = """
    SELECT url FROM namuwiki ORDER BY id DESC
    """
    dbLogger.info("selectRecentUrl")
    return dbi.select(selectRecentUrl)

