# -*- coding:utf-8 -*-
import re
import requests
import os
from requests.compat import urljoin
from mylogging import MyLogger
from bs4 import BeautifulSoup
from selenium import webdriver
from db import DB

crawlLogFile = "log/crawler.log"
crawlLogger = MyLogger(crawlLogFile)
baseUrl = "https://namu.wiki/w/"

db = DB()



class Crawler():
    def __init__(self):
        self.url = ""
        self.title = ""
        self.image = ""
        self.editdate = ""
        self.content = ""
        self.html = ""
        self.bsObj = ""
        self.linkList = []
        self.dbTuple = tuple()

    def getCrawl(self, _url):
        try:
            self.url = _url
            crawlLogger.debug("getCrawl url : " + self.url)

            try:
                resp = requests.get(self.url)
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument("disable-gpu")
                options.add_argument(
                    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
                options.add_argument("lang=ko_KR")  # 한국어
                driver = webdriver.Chrome(chrome_options=options,
                                          executable_path=os.getcwd() +"\\chromedriver.exe")

                driver.get(self.url)
                self.html = driver.page_source
                self.bsObj = BeautifulSoup(self.html, 'html.parser')

                if resp.status_code == 200:
                    self.getTitle()
                    self.getImage()
                    self.getEditDate()
                    self.getContent()

                    for link in self.bsObj.findAll("a", href=re.compile("^(/w/)((?!:).)*?$")):
                        self.linkList.append(urljoin(baseUrl, link.get('href')))

                if resp.status_code == 404:
                    self.getTitle()
                    self.image = None
                    self.editdate = None
                    self.content = None

                self.linkList.append(self.getRecentChangeLink())

            except requests.exceptions.RequestException as e:
                crawlLogger.error(e + "url : " + self.url)

            self.dbTuple = (self.title, self.url, self.content, self.image, self.editdate, self.html, self.url)
            db.insertNamuwikiDB(self.dbTuple)


            return self.linkList

        except Exception as e:
            crawlLogger.error(e)


    def getTitle(self):
        try:
            self.title = self.bsObj.find("h1", {"class": "title"}).text.strip()
            crawlLogger.debug('getTitle : ' + self.title)

        except Exception as e:
            crawlLogger.error(e + "title : " + self.title)


    def getImage(self):
        try:
            imgPattern = re.compile('^(파일:)(?!나무위키).*?$')
            for imageUrl in self.bsObj.findAll("img", {"data-src": re.compile('^(//cdn.namuwikiusercontent.com)(.*?)$')}):
                if imgPattern.search(imageUrl.attrs['alt']):
                    self.imageUrl = 'https:' + imageUrl.attrs['data-src']
                    crawlLogger.debug('getImage : ' + self.imageUrl)
                    break

        except Exception as e:
            crawlLogger.error(e)


    def getEditDate(self):
        try:
            self.editdate = self.bsObj.find("p", {"class": "wiki-edit-date"}).find("time").text
            crawlLogger.debug('getEditDate : ' + self.editdate)

        except Exception as e:
            crawlLogger.error(e + "editdate : " + self.editdate)


    def getContent(self):
        try:
            self.content = self.bsObj.find("div", {"class": "wiki-inner-content"}).get_text(" ")
            self.content = re.sub(r'\s{2,}', ' ', self.content)
            crawlLogger.debug('getContent')

        except Exception as e:
            crawlLogger.error(e)


    def getRecentChangeLink(self):
        recentChangeLinkList = []
        try:
            for recentChangeLink in self.bsObj.find("div", {"id": "recentChangeTable"}).findAll("a"):
                recentChangeLinkList.append(recentChangeLink.get('href'))
            crawlLogger.debug(recentChangeLinkList)

        except Exception as e:
            crawlLogger.error(e)

        return recentChangeLinkList


