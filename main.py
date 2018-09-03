# -*- coding:utf-8 -*-
from mylogging import MyLogger
from db import DB
import db
from crawler import Crawler
import time
from datetime import datetime

startPageUrl = "http://namu.wiki/w/"
CRAWLTERM = 3.0
db = DB()


mainLogFile = 'log/main.log'
mainLogger = MyLogger(mainLogFile)

if __name__ == '__main__':
    crawler = Crawler()
    db.makeNamuwikiTable()

    url = startPageUrl
    selectRecentUrl = db.selectRecentUrl()
    mainLogger.info("selectRecentUrl : " + selectRecentUrl)

    if len(selectRecentUrl) > 0:
        url = selectRecentUrl

    while(1):
        mainLogger.info("url : " + url)
        try:
            crawler.getCrawl(url, 0)
        except:
            mainLogger.error("error url : " + url)

        url = crawler.getRecentChangeLink()[0]





