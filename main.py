# -*- coding:utf-8 -*-
from mylogging import MyLogger
from db import DB
from crawler import Crawler

START_PAGE_URL = "http://namu.wiki/w/"
db = DB()


mainLogFile = 'log/main.log'
mainLogger = MyLogger(mainLogFile)

if __name__ == '__main__':
    crawler = Crawler()
    db.makeNamuwikiTable()

    url = START_PAGE_URL
    selectRecentUrl = db.selectRecentUrl()
    mainLogger.info("selectRecentUrl : " + selectRecentUrl)

    if len(selectRecentUrl) > 0:
        url = selectRecentUrl

    while(1):
        mainLogger.debug("main url : " + url)
        try:
            crawler.getCrawl(url, 0)
        except:
            mainLogger.error("error url : " + url)

        url = crawler.getRecentChangeLink()[0]





