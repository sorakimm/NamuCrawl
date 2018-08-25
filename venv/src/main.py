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

if __name__ == '__main__':

    testlogger = MyLogger("test")
    testlogger.debug('main.py')

    crawler = Crawler()
    urlList = []
    while(1):
        selectRecentUrl = db.selectRecentUrl()
        testlogger.info("selectRecentUrl : " + selectRecentUrl)
        urlList.append(selectRecentUrl) if len(selectRecentUrl) > 0 else urlList.append(startPageUrl)

        for url in urlList:
            testlogger.info("url : " + url)
            try:
                crawlStart = time.time()
                urlList.extend(crawler.getCrawl(url))

            except:
                testlogger.error("error url : " + url)
            crawlEnd = time.time()
            sleepTime = CRAWLTERM - (crawlEnd - crawlStart)
            if sleepTime > 0 :
                time.sleep(sleepTime)






