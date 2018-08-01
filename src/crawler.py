# -*- coding:utf-8 -*-
import re
import requests
import mylogging
import db
from bs4 import BeautifulSoup
import enum
import db

crawlLogger = mylogging.MyLogger("crawler")



def get_html(url):
    crawlLogger.info('get_html')
    _html = ""
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            _html = resp.text

    except requests.exceptions.RequestException as e:
        crawlLogger.error(e)
    return _html


def getTitle(bsObj):
    crawlLogger.info('getTitle')
    try:
        title = bsObj.find("h1", {"class": "title"}).text.strip()
        return title

    except Exception as e:
        crawlLogger.error(e)
        return None


def getImage(bsObj):
    try:
        fullImageUrl = ""
        crawlLogger.info('getImage')
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
        crawlLogger.info('getEditDate')
        editDate = bsObj.find("p", {"class": "wiki-edit-date"}).find("time").text
        return editDate

    except Exception as e:
        crawlLogger.error(e)
        return None


def getContent(bsObj):
    try:
        crawlLogger.info('getContent')
        content = bsObj.find("div", {"class": "wiki-inner-content"}).get_text(" ")
        content = re.sub(r'\s{2,}', ' ', content)
        return content

    except Exception as e:
        crawlLogger.error(e)
        return None


def getCrawl(pageUrl):
    try:
        crawlLogger.info('getCrawl')
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
        db.insertNamuwikiDB(dbTuple)


        linkSet = set()
        crawlLogger.debug(linkSet)
        for link in bsObj.findAll("a", href=re.compile("^(/w/)((?!:).)*?$")):
            linkSet.add(link.get('href'))
        # db.insertUrls(linkSet)

        return linkSet

    except Exception as e:
        crawlLogger.error(e)
        crawlLogger.debug(dbTuple)


