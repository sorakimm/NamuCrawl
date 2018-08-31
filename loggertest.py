# -*- coding:utf-8 -*-
from mylogging import MyLogger
import db
import crawler
import time
from datetime import datetime

loggertestLogFile = 'log/loggertest.log'
testlogger = MyLogger(loggertestLogFile)

startPageUrl = "http://namu.wiki/w/상하이%20콜링"
crawlTerm = 3.0
if __name__ == '__main__':
    testlogger.debug('main.py')

    urlList = [startPageUrl]
    while (len(urlList) > 0):
        selectRecentUrl = db.selectRecentUrl()
        testlogger.info("selectRecentUrl : " + selectRecentUrl)
        # urlList = [selectRecentUrl] if len(selectRecentUrl) > 0 else urlList.append(selectRecentUrl)

        for url in urlList:
            testlogger.info("url : " + url)
            try:
                crawlStart = time.time()
                urlList.extend(crawler.getCrawl(url))

            except:
                testlogger.error("error url : " + url)
            urlList.pop(0)
            crawlEnd = time.time()
            sleepTime = crawlTerm - (crawlEnd - crawlStart)
            if sleepTime > 0:
                time.sleep(sleepTime)






