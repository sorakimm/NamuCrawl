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

def get_html(url):
    crawlLogger.debug('get_html : ' + url)
    _html = ""
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            _html = resp.text

    except requests.exceptions.RequestException as e:
        crawlLogger.error(e + "url : " + url)
    return _html


def getTitle(bsObj):
    try:
        title = bsObj.find("h1", {"class": "title"}).text.strip()
        crawlLogger.debug('getTitle : ' + title)
        return title

    except Exception as e:
        crawlLogger.error(e + "title : " + title)


def getImage(bsObj):
    try:
        fullImageUrl = ""
        imgPattern = re.compile('^(파일:)(?!나무위키).*?$')
        for imageUrl in bsObj.findAll("img", {"data-src": re.compile('^(//cdn.namuwikiusercontent.com)(.*?)$')}):
            if imgPattern.search(imageUrl.attrs['alt']):
                fullImageUrl = 'https:' + imageUrl.attrs['data-src']
                crawlLogger.debug('getImage : ' + fullImageUrl)
                break

        return fullImageUrl

    except Exception as e:
        crawlLogger.error(e)
        return None


def getEditDate(bsObj):
    try:
        editDate = bsObj.find("p", {"class": "wiki-edit-date"}).find("time").text
        crawlLogger.debug('getEditDate : ' + editDate)
        return editDate

    except Exception as e:
        crawlLogger.error(e + "editdate : " + editDate)
        return None


def getContent(bsObj):
    try:
        content = bsObj.find("div", {"class": "wiki-inner-content"}).get_text(" ")
        content = re.sub(r'\s{2,}', ' ', content)
        crawlLogger.debug('getContent')
        return content

    except Exception as e:
        crawlLogger.error(e)
        return None


def getCrawl(pageUrl):
    try:
        crawlLogger.debug('getCrawl')
        fullPageUrl = urljoin(baseUrl, pageUrl)
        html = get_html(fullPageUrl)
        bsObj = BeautifulSoup(html, 'html.parser')

        if bsObj == None:
            return None
        title = getTitle(bsObj)
        content = getContent(bsObj)
        editDate = getEditDate(bsObj)
        image = getImage(bsObj)
        dbTuple = (title, fullPageUrl, content, image, editDate, html, fullPageUrl)
        db.insertNamuwikiDB(dbTuple)

        linkList = []
        crawlLogger.debug(linkList)
        for link in bsObj.findAll("a", href=re.compile("^(/w/)((?!:).)*?$")):
            linkList.append(urljoin(baseUrl, link.get('href')))

        return linkList

    except Exception as e:
        crawlLogger.error(dbTuple)


def getRecentChangeLink(url):
    recentChangeLinkSet = set()
    html = get_html(url)
    bsObj = BeautifulSoup(html, 'html.parser')
    for recentChangeLink in bsObj.find("div", {"id": "recentChangeTable"}).findAll("a"):
        recentChangeLinkSet.add(recentChangeLink.get('href'))

    return recentChangeLinkSet

