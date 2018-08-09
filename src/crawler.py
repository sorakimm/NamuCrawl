# -*- coding:utf-8 -*-
import re
import requests
from requests.compat import urljoin
from mylogging import MyLogger
from bs4 import BeautifulSoup
import db


crawlLogFile = "log/crawler.log"
crawlLogger = MyLogger(crawlLogFile)
baseUrl = "https://namu.wiki/w/"


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
                self.html = resp.text
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



    # def getRecentChangeLink(url):
    #     recentChangeLinkSet = set()
    #     html = get_html(url)
    #     bsObj = BeautifulSoup(html, 'html.parser')
    #     for recentChangeLink in bsObj.find("div", {"id": "recentChangeTable"}).findAll("a"):
    #         recentChangeLinkSet.add(recentChangeLink.get('href'))
    #
    #     return recentChangeLinkSet

