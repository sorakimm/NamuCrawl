# -*- coding:utf-8 -*-
import re
import requests
import mylogging
import db
from bs4 import BeautifulSoup
import enum


crawlLogger = mylogging.MyLogger("crawler")

dbi = db.MyDB()

class isUrlCrawled(enum.Enum):
    TRUE = 1
    FALSE = 2
    ERROR = 3


def insertUrls(urlList):
    insertUrlToUrls = """
    INSERT INTO urls (url, state, urlhash) VALUES (%s, "FALSE", md5(%s))
    """
    crawlLogger.debug("insertUrls")
    for url in urlList:
        dbi.insert(insertUrlToUrls, (url, url))
    return


def insertNamuwikiDB(dbTuple):
    insertDBQuery = """
    INSERT INTO namuwiki (title, url, content, image, editdate, crawltime, urlhash)\
    VALUES (%s, %s, %s, %s, %s, NOW(), md5(%s))
    """
    crawlLogger.debug('insertNamuwikiDB')

    dbi.insert(insertDBQuery, dbTuple)
    return



def get_html(url):
    crawlLogger.debug('get_html')
    _html = ""

    resp = requests.get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html


def getTitle(bsObj):
    crawlLogger.debug('getTitle')
    try:
        title = bsObj.find("h1", {"class": "title"}).text.strip()
        return title

    except Exception as e:
        crawlLogger.error(e)
        return None


def getImage(bsObj):
    try:
        fullImageUrl = ""
        crawlLogger.debug('getImage')
        imgPattern = re.compile('^(파일:)(?!나무위키).*?$')
        for imageUrl in bsObj.findAll("img", {"data-src": re.compile('^(//cdn.namuwikiusercontent.com)(.*?)$')}):
            if imgPattern.search(imageUrl.attrs['alt']):
                fullImageUrl = 'https:' + imageUrl.attrs['data-src']
                break

        return fullImageUrl

    except Exception as e:
        crawlLogger.error(e)
        return None


def getEditDate(bsObj):
    try:
        crawlLogger.debug('getEditDate')
        editDate = bsObj.find("p", {"class": "wiki-edit-date"}).find("time").text
        return editDate

    except Exception as e:
        crawlLogger.error(e)
        return None


def getContent(bsObj):
    try:
        crawlLogger.debug('getContent')
        content = bsObj.find("div", {"class": "wiki-inner-content"}).get_text(" ")
        content = re.sub(r'\s{2,}', ' ', content)
        return content

    except Exception as e:
        crawlLogger.error(e)
        return None


def getCrawl(pageUrl):
    try:
        crawlLogger.debug('getCrawl')
        fullPageUrl = "https://namu.wiki" + pageUrl
        html = get_html(fullPageUrl)
        bsObj = BeautifulSoup(html, 'html.parser')

        if bsObj == None:
            return None
        title = getTitle(bsObj)
        content = getContent(bsObj)
        editDate = getEditDate(bsObj)
        image = getImage(bsObj)
        dbTuple = (title, fullPageUrl, content, image, editDate, html)
        linkSet = set()
        for link in bsObj.findAll("a", href=re.compile("^(/w/)((?!:).)*?$")):
            linkSet.add(link.get('href'))
        insertNamuwikiDB(dbTuple)
        insertUrls(linkSet)

        return

    except Exception as e:
        crawlLogger.error(e)



